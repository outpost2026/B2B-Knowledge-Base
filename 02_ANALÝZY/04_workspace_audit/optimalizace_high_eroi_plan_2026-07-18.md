---
typ: analýza / plán
účel: Návrh high-EROI optimalizací pro _github workspace, včetně root AGENTS.md
autor: AI (Session 20)
datum: 2026-07-18
EROI: 9/10
stav: NÁVRH (čeká na schválení)
---

# High-EROI optimalizace _github workspace — návrh

## Kontext

Session 19 dokončila workspace cleanup (P0/P1/P3): root .gitignore, orphans delete,
CI→.ci/, session→.session/, scripts→.scripts/, GCP→_archive.zip.
Session 20 přidala: NVIDIA + Cerebras API provider config, free-tier LLM referenční katalog,
korekce Cerebras model nabídky (Gemma 4, GPT OSS, Z-AI GLM).

Zbývající bottlenecky (z B4/B6) + nové příležitosti z tohoto vlákna:

| ID | Stav | Popis |
|----|------|-------|
| B4 | ⏳ open | Custom commands v opencode |
| B6 | ⏳ open | AGENTS.md pro root _github |
| — | 🆕 | Provider routing (DeepSeek→NVIDIA→Cerebras) není konfigurován |
| — | 🆕 | `small_model` není nastaven → DeepSeek kredity se spalují na titulky |
| — | 🆕 | Security patterns (*.key, credentials*) chybí v root .gitignore |
| — | 🆕 | CONTEXT_REPOS.md + index.md neodrážejí Session 20 |

---

## Navrhované optimalizace (řazeno podle EROI)

### P0 — implementovat ihned (EROI 10/10)

#### 1. Vytvořit AGENTS.md v root _github/

**Proč:** Současný AGENTS.md v B2B-Knowledge-Base řídí jen KB agenty.
Root _github potřebuje master agentní pravidla pro:
- Bezpečnostní guardrails (ALLOWED ROOTS, zakázané cesty)
- Pravidla pro čtení/zápis napříč všemi repy (git checkpoint, read-after-write)
- Encoding pravidla (cp1250→UTF-8, -X utf8, zákaz emoji)
- MCP server konfiguraci (cnc-tools, linkedin-analyzer, mcp-jobs)
- Provider config (DeepSeek paid primární, NVIDIA/Cerebras fallback)
- B2B stav a prioritizaci

**Obsah:**
- Sekce 1: Účel a scope (master pro všechny LLM agenty v _github)
- Sekce 2: Bezpečnostní guardrails (převzít z `.ai_guardrails.json` + CONTEXT_REPOS.md)
- Sekce 3: Encoding pravidla (převzít z `.ai_guardrails.json`)
- Sekce 4: Provider config (primární DeepSeek, fallback NVIDIA, Cerebras)
- Sekce 5: Před/po úkolu (git checkpoint, read-after-write, commit format)
- Sekce 6: Povolené adresáře a zakázané operace
- Sekce 7: Rychlý lookup — mapa všech rep s účely
- Sekce 8: Odkaz na podrobnější doc (CONTEXT_REPOS.md, index.md, B2B-KB/AGENTS.md)

**EROI:** Eliminuje opakované dotazy na guardrails, zrychluje agent startup ~5 min/session.

---

#### 2. Nastavit `small_model` v opencode.jsonc

**Proč:** opencode používá `gpt-5-nano` (přes Zen) pro title generation a podobné
triviality. To spaluje DeepSeek paid kredity na věci, které zvládne i malý model.

**Config:**
```json
{
  "small_model": "cerebras/gemma-4",
  "share": "disabled"
}
```
Nebo pro absolutní offline režim (Ollama):
```json
{
  "small_model": "ollama/qwen3-coder",
  "share": "disabled"
}
```

**EROI:** Ušetří ~20-30% tokenů na DeepSeek účtu, protože titulky a malé úkoly
jdou přes free tier. Doslova ~$5-15/měsíc úspora, ~5 min implementace.

---

### P1 — implementovat v této session (EROI 8/10)

#### 3. Security patterns do root .gitignore

**Chybí:** `*.key`, `*.pem`, `credentials*`, `secrets*` — tyto patterny jsou
blokovány jen na úrovni MCP serveru (FORBIDDEN_PATTERNS), ne v .gitignore.
Riziko: náhodný commit API klíče nebo credentials souboru.

**Přidat do .gitignore:**
```gitignore
# Security — keys, credentials, secrets
*.key
*.pem
credentials*
secrets*
```

**EROI:** Prevence incidentu. Incident = hodiny reverzace + rotace klíčů.

---

#### 4. Uložit Session 20 stav + update kontextových souborů

**Proč:** `.ai_state.json` neobsahuje Session 20. CONTEXT_REPOS.md + index.md
neodrážejí:
- NVIDIA + Cerebras provider config
- Free-tier LLM katalog
- Korekce Cerebras modelů (Gemma 4, ne Qwen 3 Coder)

**EROI:** Kontinuita agentního stavu. Bez update ztrácí agent přehled.

---

### P2 — implementovat po schválení (EROI 6/10)

#### 5. Automatický provider fallback (DeepSeek → NVIDIA → Cerebras)

**Proč:** opencode podporuje pouze jeden model najednou. Při rate limitu
nebo výpadku DeepSeek padá celý workflow. Ruční přepínání trvá ~2 min.

**Řešení:** Není nativní v opencode — ale lze docílit:
- OpenRouter jako gateway (agreguje více providerů s fallbackem)
- Nebo script pro quick-switch mezi providery v configu

**EROI:** Zvýšení availability z 95% → ~99.9%. Kritické při B2B deadlinech.

---

#### 6. Custom commands (B4)

**Proč:** B4 zůstává otevřený. Custom commands v opencode.jsonc
mohou urychlit opakované úkoly.

**Příklady:**
```json
{
  "custom_commands": [
    { "name": "commit-session", "command": "git add -A && git commit -m \"[SESSION] update\"" },
    { "name": "pipeline-mcp", "command": "python -X utf8 -m mcp_local_server.server" }
  ]
}
```

**EROI:** Ušetří ~30s na každém commitu. Nízký individuální dopad, ale
3+ commity/den = ~30 min/měsíc.

---

### P3 — dlouhodobé (EROI 4/10)

#### 7. Vcf-compiler reconnect na dxf_integrace.DxfIndexer

**Proč:** Po OOP refactoru dxf_integrace volá Vcf-compiler staré API.
V CONTEXT_REPOS.md označeno jako pending.
**Čas:** ~2-4 hodiny (testování + adapter).

#### 8. CI/CD Tier 2 — cross-repo dispatch PAT

**Proč:** Blokováno chybějícím PAT tokenem. Po zprovoznění:
automatická CI cascade při změně dxf_integrace → Vcf-compiler.

#### 9. linkedin-mcp-custom merge → main

**Proč:** Branch `test/verify-main-baseline` není mergnutá do main.
Riziko divergence a konfliktů. Po schválení testů merge.

---

## Souhrnná tabulka

| # | Optimalizace | EROI | Čas | Priorita |
|---|-------------|------|-----|----------|
| 1 | Root AGENTS.md | 10/10 | ~20 min | **P0** |
| 2 | small_model config | 10/10 | ~2 min | **P0** |
| 3 | .gitignore security | 8/10 | ~1 min | P1 |
| 4 | Session state + kontext update | 8/10 | ~10 min | P1 |
| 5 | Provider fallback routing | 6/10 | ~30 min | P2 |
| 6 | Custom commands (B4) | 6/10 | ~10 min | P2 |
| 7 | Vcf-compiler reconnect | 4/10 | ~2-4 h | P3 |
| 8 | CI/CD Tier 2 PAT | 4/10 | ~1 h | P3 |
| 9 | linkedin-mcp merge main | 4/10 | ~30 min | P3 |

---

## Další krok

Schválit priority a spustit implementaci:
- P0: AGENTS.md + small_model (teď)
- P1: .gitignore + session update
- P2/P3: dle potřeby

*Návrh vytvořen 2026-07-18 na základě kompletního auditu Session 19-20.*
