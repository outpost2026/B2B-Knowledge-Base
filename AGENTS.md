# AGENTS.md — Metodická kostra pro agentní přístup ke KB

**Verze:** 1.0 | **Datum:** 2026-06-25 | **Účel:** Definice pravidel pro LLM agenty pracující s touto znalostní bází

---

## 1. Účel tohoto souboru

Tento soubor je **povinný kontext** pro každého LLM agenta (opencode, Gemini CLI, Claude Code, DeepSeek agent), který pracuje s tímto repozitářem. Bez načtení tohoto souboru agent nesmí provádět žádné zápisové operace.

---

## 2. Povolené adresáře

Agent smí číst a zapisovat **výhradně** v:
```
C:\Users\PC\Documents\Repozitar_Dev\_github\B2B-Knowledge-Base\
```

**Zakázané cesty** (nikdy, za žádných okolností):
```
C:\Program Files\
C:\Windows\
C:\Users\PC\AppData\
C:\
```

---

## 3. Před úkolem (povinný checkpoint)

```powershell
# 1. Ověř, že jsi ve správném adresáři
Get-Location
# musí být: C:\...\B2B-Knowledge-Base

# 2. Zkontroluj aktuální stav
git status

# 3. Pokud je něco necommitnutého → commitni
git add -A
git commit -m "[checkpoint] pred: popis úkolu"

# 4. Ověř že je vše čisté
git status  # must be clean
```

---

## 4. Během úkolu

### 4.1 Čtení (vždy povoleno bez omezení)

Agent smí číst libovolný soubor v repozitáři. Povinně načíst:

1. **README.md** — struktura a pravidla
2. **AGENTS.md** — tento soubor (aktuální kontext)
3. **INDEX.md** — registr artefaktů pro orientaci
4. Relevantní modulové soubory dle zadání

### 4.2 Zápis (povoleno jen do určeného modulu)

Agent smí vytvářet a modifikovat soubory **pouze v modulu, který odpovídá zadání**:

| Pokud úkol zní | Piš do modulu |
|----------------|---------------|
| strategie, plán, EROI | `00_STRATEGIE/` |
| metodika, návod | `01_METODIKY/` |
| analýza, report | `02_ANALÝZY/` |
| provozní dokument | `03_PROVOZ/` |
| doménová znalost | `04_KNOWLEDGE_BASE/` |
| epistemika, kognitivní | `05_EPISTEMIKA/` |
| cokoliv superseded | `_ARCHIVE/` |

### 4.3 Formát zápisu

Každý nový soubor musí mít hlavičku:
```markdown
# Název souboru
**Datum:** YYYY-MM-DD | **Autor:** outpost2026
**Účel:** Jedna věta co tento soubor dělá
```

Commit message template:
```
[MODUL] akce: popis (EROI důvod)
```
Příklady:
- `[STRATEGIE] add: Q3 pivot plan (EROI 8/10)`
- `[METODIKY] update: LinkedIn headline template`
- `[ANALÝZY] add: market signal batch #4`

### 4.4 Zakázané operace

- **Mazání souborů** — pouze přesun do `_ARCHIVE/`
- **Přepisování historie** — žádné `git rebase`, `git reset --hard`, `git amend` bez potvrzení
- **Editace README.md** bez explicitního požadavku
- **Editace AGENTS.md** bez explicitního požadavku

---

## 5. Po úkolu (povinný review)

```powershell
# 1. Zjisti co se změnilo
git status
git diff --stat

# 2. Ověř že změny dávají smysl
#    - nezmizely soubory?
#    - nezměnily se soubory mimo povolený modul?
#    - neobsahují commity API klíče?

# 3. Commitni
git add -A
git commit -m "[MODUL] akce: popis (EROI)"

# 4. Push (jen pokud je to vyžádáno)
git push
```

---

## 6. RAG-ready konvence

Pro maximální SNR při sémantickém vyhledávání:

| Konvence | Pravidlo |
|----------|----------|
| **Názvy souborů** | `VELLKA_PISMENA.md` pro hlavní, `male_pismena.json` pro data |
| **Hlavička** | Povinná (viz 4.3) |
| **Tagy** | V INDEX.md, ne v každém souboru |
| **Obrázky** | Nepoužívat (snižují SNR v RAG) |
| **Odkazy** | Relativní cesty, ne absolutní |
| **Jazyk** | Dle obsahu (CS i EN smíšeně) |

---

## 7. Sebe-obrana agenta

Pokud agent narazí na:

| Situace | Reakce |
|---------|--------|
| Nejasné zadání | Zeptej se autora na upřesnění |
| Příliš velký soubor (>200 lines) | Požádej o čtení po sekcích |
| Chybějící hlavička | Přidej hlavičku (první úprava) |
| Konfliktní informace | Referencuj oba zdroje a zeptej se |
| API klíč v commitu | OKAMŽITĚ zastav a nahlas |

---

## 8. Příklad session

```powershell
# === START ===
cd C:\Users\PC\Documents\Repozitar_Dev\_github\B2B-Knowledge-Base
git status  # clean
# === READ ===
# README.md + AGENTS.md + relevantní modul
# === WORK ===
# vytvořím / upravím soubor
# === VERIFY ===
git status
git diff --stat
# === COMMIT ===
git add -A
git commit -m "[METODIKY] update: LinkedIn skills list (EROI 9/10)"
# === END ===
```

---

## 9. Zdroje pro inicializaci agenta

Při prvním kontaktu agent načte v tomto pořadí:
1. `README.md` — struktura a účel
2. `AGENTS.md` — tento soubor
3. `INDEX.md` — registr artefaktů
4. Relevantní soubory z modulu dle zadání

---

*Tento soubor je živý. Aktualizace pouze s explicitním souhlasem autora.*
