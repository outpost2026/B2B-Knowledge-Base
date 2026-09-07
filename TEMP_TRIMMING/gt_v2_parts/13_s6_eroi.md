## 6. EROI rozhodovací framework

### 6.1 Kdy MCP NEPOUZÍT

| Situace | Proc MCP nefunguje | Co místo toho |
|---------|-------------------|---------------|
| Sub-100ms operace (ctení 1 souboru) | JSON-RPC overhead > samotná operace | CLI nebo skript |
| Hromadné operace (git status na 13 repo) | Sériové volání 13x tool je pomalejší | Dávkový skript |
| Jednorázové ad-hoc príkazy | Tool musíš definovat, otestovat, dokumentovat | CLI |
| Credentials / secrets | Riziko úniku do LLM kontextu | OS env var + gh CLI |
| 100% determinismus | LLM se muze rozhodnout tool nepouzít | Skript/Makefile |
| Rychle se menící API | Kazdá zmena toolu = restart serveru | Jupyter / skript |

### 6.2 EROI matice

| | Jednoduché rešení | Slozité rešení |
|--|------------------|----------------|
| **Vysoká potřeba MCP** | MCP dává smysl (doménové nástroje, multi-client) | MCP dává smysl |
| **Nízká potřeba MCP** | Nepouzívat (prímý príkaz stací) | Zatím nepouzívat |

### 6.3 Rozhodovací flowchart

```
Potrebuju provést operaci?
├─ Jednorázová? → CLI / rucne
├─ >3×?
│  ├─ Cistě lokální, bez doménového kontextu? → Python skript
│  └─ Potrebuji to zpřístupnit LLM / více klientům?
│     ├─ Read-only a bezpečnostne citlivé? → MCP tool (povolené cesty, audit)
│     ├─ Vyžaduje doménové know-how? → MCP tool (tool description = dokumentace)
│     └─ Write operace? → MCP tool (jen se zárukou bezpecnosti)
└─ >50×? → Zvaž samostatný balícek / pip modul
```

### 6.4 Template pro nový tool

| Otázka | Váha |
|--------|------|
| Frekvence pouzití (>5×/mesíc?) | tool pokud ano |
| Počet klientů (>1?) | tool pokud ano |
| Doménová znalost (střední+?) | tool pokud ano |
| Bezpecnostní riziko (střední+?) | tool (s audit) |
| Write operace? | tool (s validací) |

