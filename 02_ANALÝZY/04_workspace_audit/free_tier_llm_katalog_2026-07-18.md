---
typ: analýza / referenční katalog
účel: Kompletní katalog free-tier / zero-setup LLM API napojitelných na opencode workflow
autor: AI (Session 19)
datum: 2026-07-18
EROI: vysoký (fallback + redundance pro DeepSeek paid setup)
zdroj: opencode.ai/docs/providers, /docs/zen (ověřeno 2026-07-18)
stav: DRAFT (markdown → DOCX po schválení)
---

# Free-tier & zero-setup LLM API pro opencode — referenční katalog

## 1. Účel a kontext

Aktuální produkční setup používá **placené DeepSeek API** (má kredity). Tento dokument je
**kompletní referenční katalog** všech free-tier a zero-setup providerů, které lze napojit
na opencode workflow — bez ohledu na aktuální volbu. Slouží jako:

- **Fallback plán** — když dojdou kredity nebo je DeepSeek API nedostupné.
- **Redundance** — sekundární cesta pro nekritické tasky (title generation, drafty).
- **Rozhodovací báze** — jestli má smysl routovat levné tasky mimo placené API.

opencode staví na **AI SDK + Models.dev** a podporuje 75+ providerů. Připojení je vždy
přes `/connect` (uloží klíč do `~/.local/share/opencode/auth.json`) nebo přes `provider`
sekci v `opencode.json` / `opencode.jsonc`.

---

## 2. Kategorizace zdrojů

Providery dělím do 4 tříd podle způsobu získání a nákladů:

| Třída | Popis | Náklady | Setup |
|-------|-------|---------|-------|
| **A. Zero-setup subscription** | Použije existující předplatné, které už možná máš | fixní měsíční | OAuth, žádný API klíč |
| **B. Free-tier cloud API** | Provider nabízí free kvótu / free modely | zdarma do limitu | API klíč přes `/connect` |
| **C. Local (self-hosted)** | Modely běží na tvém HW | zdarma (HW + energie) | lokální server + config |
| **D. Free gateway** | Agregátor s free modely (např. Zen `-free`) | zdarma (omezené) | API klíč |

---

## 3. Třída A — Zero-setup subscription

opencode explicitně podporuje tato předplatná „bez setupu" (jen OAuth):

| Provider | Modely | Předplatné | Poznámka |
|----------|--------|-----------|----------|
| **GitHub Copilot** | GPT / Claude / Gemini rodiny | Copilot (příp. Pro+) | `/connect` → github.com/login/device |
| **ChatGPT Plus/Pro** | OpenAI modely | ChatGPT Plus/Pro | `/connect` → OpenAI → OAuth v prohlížeči |
| **GitLab Duo** | duo-chat-haiku/sonnet/opus-4-5 | Premium/Ultimate | experimentální, native tool calling |

> **Anthropic Claude Pro/Max**: opencode **NEpodporuje** (Anthropic to explicitně zakazuje;
> pluginy byly odstraněny od v1.3.0). Neuvádět jako cestu.

### Konfigurace (žádná — jen /connect)
```
/connect   → vyber providera → OAuth
/models    → vyber model
```

---

## 4. Třída B — Free-tier cloud API

Providery s free kvótou nebo přímo free modely, napojitelné přes `/connect`:

| Provider | Charakteristika | Tool calling | Vhodné pro opencode |
|----------|-----------------|-------------|---------------------|
| **NVIDIA** (build.nvidia.com) | Nemotron + řada open modelů **zdarma** | ano | ★★★ nejsilnější free-tier |
| **Groq** | Extrémně rychlá inference, free tier | ano | ★★★ rychlost, code tasky |
| **Cerebras** | Qwen 3 Coder 480B, free tier | ano | ★★★ velký coder model |
| **Hugging Face** | Inference Providers (17+), Kimi-K2, GLM-4.6 | ano | ★★ dostupnost modelů |
| **Fireworks AI** | Kimi K2 Instruct ap., free kredity | ano | ★★ |
| **Together AI** | open modely, free kredity | ano | ★★ |
| **Cortecs** | Kimi K2 Instruct, free | ano | ★ |
| **Nebius Token Factory** | Kimi K2 Instruct | ano | ★ |

### Připojení (identické pro všechny třídy B)
```
/connect   → vyhledej providera → vlož API klíč
/models    → vyber model
```

### Poznámka k tool callingu
opencode agent workflow **vyžaduje spolehlivý tool calling** (edit/read/bash/grep).
Pro free modely volit varianty se silným tool-callingem (Qwen-Coder, DeepSeek-Coder,
Kimi K2). Slabší modely selhávají na multi-step agentních taskách.

---

## 5. Třída C — Local (self-hosted)

Plná kontrola, zero cost za inference, žádné odesílání dat ven. Vše přes
`@ai-sdk/openai-compatible` a `baseURL` na lokální server.

| Runtime | Default baseURL | Poznámka |
|---------|-----------------|----------|
| **Ollama** | `http://localhost:11434/v1` | auto-config pro opencode; zvýšit `num_ctx` (16k–32k) pro tool calls |
| **LM Studio** | `http://127.0.0.1:1234/v1` | GUI, snadná správa modelů |
| **llama.cpp** (llama-server) | `http://127.0.0.1:8080/v1` | max kontrola, ruční limit context/output |
| **Atomic Chat** | `http://127.0.0.1:1337/v1` | desktop appka, OpenAI-compatible |
| **Ollama Cloud** | (cloud) | hybrid; nutno `ollama pull model:cloud` |

### Konfigurace — příklad Ollama
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": { "qwen3-coder": { "name": "Qwen3 Coder (local)" } }
    }
  }
}
```

### Konfigurace — příklad llama.cpp (s limity)
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "llama.cpp": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "llama-server (local)",
      "options": { "baseURL": "http://127.0.0.1:8080/v1" },
      "models": {
        "qwen3-coder:a3b": {
          "name": "Qwen3-Coder a3b-30b (local)",
          "limit": { "context": 128000, "output": 65536 }
        }
      }
    }
  }
}
```

> **Kritické pro local:** doporučené coder modely s tool-callingem — Qwen3-Coder,
> DeepSeek-Coder. Malé modely (<7B) nezvládají opencode agentní smyčku.

---

## 6. Třída D — Free gateway (Zen -free)

opencode Zen nabízí modely se suffixem `-free`. Vlastnosti (z migrační analýzy v1.18):

| Atribut | Hodnota | Dopad na workflow |
|---------|---------|-------------------|
| Context cap | ~200K (gateway limit) | omezuje velké repo kontexty |
| Cache TTL | ~5 min | opětovné načítání kontextu |
| `supportsStore` | false | bez server-side persistence |
| `thinkingLevelMap` | null (minimal/low/medium) | žádné reasoning úrovně |
| Data | možné využití pro trénink | **nevhodné pro citlivý kód** |

> **Doporučení:** Zen `-free` jen pro triviální / veřejné tasky. Ne pro B2B repo s IP.

---

## 7. Souhrnná srovnávací matice

| Kritérium | A. Subscription | B. Free cloud | C. Local | D. Zen-free |
|-----------|-----------------|---------------|----------|-------------|
| Náklad na inference | fixní/měs. | 0 (do limitu) | 0 (HW) | 0 |
| Rate limit / kvóty | dle plánu | ano | žádné | přísné |
| Context window | vysoký | dle modelu | dle HW/config | ~200K cap |
| Tool calling | výborný | dobrý (výběr) | dle modelu | základní |
| Data privacy | provider | provider | **plná** | slabá |
| Offline | ne | ne | **ano** | ne |
| Setup složitost | nízká (OAuth) | nízká | střední | nízká |
| Vhodnost pro B2B IP | střední | střední | **vysoká** | nízká |

---

## 8. Doporučená fallback strategie (vůči DeepSeek paid)

1. **Primární:** DeepSeek paid API (stávající, kredity).
2. **Fallback #1 (výkon):** NVIDIA build.nvidia.com — free, silné modely, tool calling.
3. **Fallback #2 (rychlost):** Groq / Cerebras — rychlá inference free tier.
4. **Fallback #3 (privacy/offline):** Ollama + Qwen3-Coder lokálně — nezávislé na síti.
5. **Malé tasky (title gen):** `small_model` lze nastavit zvlášť, ať nespotřebovává
   drahé API na triviality.

### `small_model` odklonění (šetří kredity)
```json
{
  "$schema": "https://opencode.ai/config.json",
  "small_model": "ollama/qwen3-coder"
}
```

---

## 9. Bezpečnostní poznámky

- **Nikdy** neposílat B2B repo (VCF/DXF/CNC IP) přes free gateway s tréninkem dat.
- Lokální (Třída C) je jediná varianta s garantovanou plnou data privacy.
- Klíče v `~/.local/share/opencode/auth.json` — nezahrnovat do gitu.
- Zen malý model (gpt-5-nano) běží defaultně i u některých úkolů — u citlivých
  self-hosted setupů zvážit `small_model` override + `"share": "disabled"`.

---

## 10. Otevřené otázky pro validaci

- [ ] Ověřit aktuální free kvóty (NVIDIA/Groq/Cerebras) — mění se; verifikovat na účtu.
- [ ] Změřit reálný tool-calling success rate free modelů na opencode taskách.
- [ ] Rozhodnout: má smysl `small_model` → local, nebo nechat DeepSeek celé?

---

*Zdroj dat: opencode.ai/docs/providers (ověřeno 2026-07-18). Kapacity a limity se
u free-tier providerů mění — před nasazením verifikovat přímo na účtu providera.*
