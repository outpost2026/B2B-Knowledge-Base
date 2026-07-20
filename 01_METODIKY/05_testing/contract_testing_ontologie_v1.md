# Contract Testing — metodika

> *Verze: 1.0 | Datum: 2026-07-20 | Doména: SWE testing ontologie — Integration testing*

---

## 1. Místo v testovací ontologii

```
Unit Tests          ← testují jednu funkci/třídu izolovaně
  ↓
Contract Tests      ← ← ← testují rozhraní mezi dvěma moduly ← ZDE
  ↓
Integration Tests   ← testují více modulů dohromady (s reálnými závislostmi)
  ↓
E2E Tests           ← testují celý systém od UI/API po databázi
```

**Contract Testing** je podmnožina **Integration Testing**. Řeší jednu konkrétní otázku: *"Dodržuje producer smlouvu, kterou od něj consumer očekává?"*

---

## 2. Problém, který řeší

V modulární architektuře (MCP pipeline, microservices, ETL) si moduly předávají data přes definované rozhraní — nejčastěji JSON.

**Typický scénář selhání:**

1. Producer (např. Stockfish analyzer) změní klíč v JSON z `ply` na `move_number`
2. Consumer (např. LLM prompt builder) čte `ply` → dostává `None`
3. Nikdo nekřičí — žádná type error, žádný runtime exception
4. LLM dostane `move ?` místo `move 27`
5. Uživatel vidí low-SNR výstup bez zjevné příčiny

**Tento bug není odhalitelný unit testy** — oba moduly prochází své testy v izolaci. Problém je v *rozhraní mezi nimi*.

---

## 3. Consumer-Driven Contract (CDC)

Nejběžnější forma contract testingu:

```
  Consumer (prompt builder)          Producer (stockfish analyzer)
       │                                      │
       │   definuje: potřebuji klíče          │
       │   {ply, move_san, centipawn_loss}    │
       │   → test verifikuje, že              │
       │     producer JSON obsahuje           │
       │     tyto klíče                       │
       │                                      │
       └──────────  contract  ────────────────┘
```

**Pravidlo:** Consumer definuje kontrakt. Producer se mu přizpůsobí. Test žije u consumeru.

---

## 4. Implementační vzory

### 4.1 Schema testy (použito v GT-059)

```python
def test_blunder_subkeys():
    data = load_stockfish_cache()
    blunder = data["blunders"][0]
    for key in {"ply", "move_san", "centipawn_loss", "phase"}:
        assert key in blunder, f"Chybí klíč '{key}'"
```

Test:
- Načte reálný producer výstup (JSON)
- Zkontroluje, že obsahuje všechny klíče, které consumer čte
- Pokud ne → test selže → bug je zachycen v CI, ne v produkci

### 4.2 Placeholder detection

```python
def test_prompt_no_unknowns():
    prompt = build_prompt(data)
    assert "?" not in prompt, "Prompt obsahuje neznámé hodnoty"
```

Detekuje bugy, které schema test neodhalí (např. klíč existuje, ale je null).

### 4.3 Noise-floor detection (pro LLM vrstvu)

```python
def test_accuracy_not_zero():
    data = load_cache()
    assert data["accuracy"] > 0, "Accuracy nemůže být 0 u reálné hry"
```

Kontroluje sémantickou konzistenci dat — nejen strukturu, ale i přípustné hodnoty.

---

## 5. Kdy a kde nasadit

| Scénář | Contract test? |
|---|---|
| Dva moduly si předávají JSON | ✅ Povinný |
| ETL pipeline (source → transform → load) | ✅ Na každém rozhraní |
| Microservices (REST API) | ✅ Smlouva = API spec (OAS) |
| Jedna funkce volá druhou v témže modulu | ❌ Unit test stačí |
| LLM prompt čte data z předchozí vrstvy | ✅ Dvojitá kontrola: klíče + placeholder |

---

## 6. Profesionální nástroje vs lightweight varianta

### Nástroje (pro větší projekty)

| Nástroj | Doména |
|---|---|
| **Pact** (pact.io) | Mikroslužby, HTTP API. Consumer definuje očekávání, producer se verifikuje. |
| **OpenAPI/Swagger** | REST API. Specifikace je kontrakt. |
| **JSON Schema** | Validační schema. `jsonschema` knihovna validuje producer JSON. |
| **Avro / Protobuf** | Binary serializace. Schema je kontrakt kompilovaný do kódu. |

### Lightweight varianta (použito v lichess-analyzer)

```python
# tests/test_prompt_contract.py
PROMPT_KEYS = {"ply", "move_san", "centipawn_loss", "phase"}

def test_contract():
    data = json.load(open("cache.json"))
    for key in PROMPT_KEYS:
        assert key in data["blunders"][0]
```

Nepotřebuje Pact server, CI infra, nebo schema registry. Vhodné pro MCP servery, monorepa, malé týmy. Dostačující, protože:
- Data jsou JSON na disku (ne HTTP)
- Producer a consumer jsou v jednom repu
- Počet rozhraní je malý (~3-5)

---

## 7. Pravidla pro lichess-analyzer (P44)

1. **Každý modul** v pipeline musí mít contract test
2. **Consumer definuje kontrakt** — test píše ten, kdo data čte
3. **Test se jmenuje `test_<modul>_contract`** — pro snadné vyhledání
4. **Runuje se s `python -m pytest tests/`** — součástí běžné testovací sady
5. **Pokud se změní klíče v modelu** — contract test selže dřív, než se bug dostane do LLM

---

## 8. Související artefakty

- `tests/test_prompt_contract.py` — implementace pro Stockfish → LLM rozhraní
- `MCP_GROUND_TRUTH_postmortem_agregovany_v1.md` — GT-059, P44
- `src/models/game.py` — GameAnalysis.to_dict() (producer)
- `src/services/game_llm_cache.py` — _build_game_prompt() (consumer)
