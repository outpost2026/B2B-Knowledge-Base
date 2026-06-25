# OpenRouter Model Analysis v3 — Verifikovaná data z API

**Autor:** Ondřej Soušek  
**Datum:** 24. června 2026  
**Budget:** $20–25/měsíc  
**Stack:** Open Code GUI + OpenRouter API  
**Doména:** Python (VCF parser, Streamlit UI), kognitivní vědy, filosofie

---

## Metodologie

Všechny modely, ceny a parametry byly ověřeny přímo z OpenRouter API katalogu k 24. 6. 2026. 

---

## 🚀 Klíčové modely a jejich role

### Layer 1: Reasoning — Kognitivní vědy, filosofie, komplexní architektura
Cíl: Hluboký chain-of-thought, epistemická kalibrace, 1M+ kontext.

| Rank | Model (OpenRouter slug) | Cena I/O / 1M | Context | Vlastnosti | Doporučení |
|---|------------------------|---------------|---------|---|---|
| 1 | `openai/gpt-oss-120b` | $0.039 / $0.18 | 131K | High-reasoning, agentic, extrémně levný vstup | **Default pro Layer 1** |
| 2 | `deepseek/deepseek-v4-flash` | $0.09 / $0.18 | 1M | Reasoning effort: high/xhigh, 1M kontext | **Pro dlouhé kontexty** |
| 3 | `xiaomi/mimo-v2.5` | $0.105 / $0.28 | 1M | Omnimodal, Pro-level agentic performance | **Multimodální analýza** |
| 4 | `minimax/minimax-m3` | $0.30 / $1.20 | 1M | Long-horizon agentic work, MSA (low cost at 1M) | **Komplexní agentní úlohy** |
| 5 | `deepseek/deepseek-r1` | $0.70 / $2.50 | 164K | Nativní CoT, zlatý standard reasoningu | **Kritické reasoning úlohy** |
| 6 | `google/gemini-2.5-pro` | $1.25 / $10 | 1M | #1 LMArena, špičkový reasoning | **Absolutní maximum kvality** |

---

### Layer 2: Coding — Python, pytest, Streamlit, Refactoring
Cíl: Přesnost kódu, repo-level komprehenze, nízká cena za token.

| Rank | Model (OpenRouter slug) | Cena I/O / 1M | Context | Vlastnosti | Doporučení |
|---|------------------------|---------------|---------|---|---|
| 1 | `deepseek/deepseek-v4-flash` | $0.09 / $0.18 | 1M | Nejlepší poměr cena/výkon; 1M kontext | **Default pro kódování** |
| 2 | `openai/gpt-oss-120b` | $0.039 / $0.18 | 131K | Extrémně levný; MoE architektura | **Jednoduché úkoly / Boilerplate** |
| 3 | `deepseek/deepseek-v4-pro` | $0.435 / $0.87 | 1M | 49B active params; architektonické rozhodnutí | **Komplexní refactoring** |
| 4 | `xiaomi/mimo-v2.5-pro` | $0.435 / $0.87 | 1M | Top rankings SWE-bench Pro | **Agentní vývoj** |
| 5 | `google/gemma-4-31b-it` | $0.12 / $0.35 | 256K | Thinking mode, open-weight | **Analytický kód** |
| 6 | `meta-llama/llama-4-scout` | $0.10 / $0.30 | 10M | **10M kontext** — celý repo v kontextu | **Repo-wide analýza** |
| 7 | `anthropic/claude-sonnet-4` | $3 / $15 | 1M | SWE-bench 72.7%; špičková kvalita | **Kritické bugy / Architektura** |

---

## 💰 Budget model — Reálný rozpis ($20/měsíc)

| Kategorie | Model | Podíl | Est. Cena |
|---|---|---|---|
| **Coding (Standard)** | `deepseek/deepseek-v4-flash` | 80% | ~$11 |
| **Reasoning (Standard)** | `openai/gpt-oss-120b` | 15% | ~$3 |
| **Premium/Complex** | `deepseek/deepseek-v4-pro` / `sonnet-4` | 5% | ~$4 |
| **Free Tier** | `meta-llama/llama-3.3-70b-instruct:free` | — | $0 |
| **Celkem** | | **100%** | **~$18 / měsíc** |

---

## 🛠 Open Code GUI Workflow

### 1. Konfigurace `opencode.json`
```json
{
  "provider": {
    "openrouter": {
      "models": {
        "deepseek/deepseek-v4-flash:floor": {},
        "openai/gpt-oss-120b:floor": {},
        "deepseek/deepseek-v4-pro:floor": {},
        "minimax/minimax-m3:floor": {},
        "xiaomi/mimo-v2.5:floor": {},
        "meta-llama/llama-4-scout:floor": {},
        "meta-llama/llama-3.3-70b-instruct:free": {},
        "google/gemma-4-31b-it:free": {},
        "anthropic/claude-sonnet-4:floor": {}
      }
    }
  }
}
```

### 2. Model switching v praxi

| Úkol | Model | Příkaz |
|---|---|---|
| **Standardní Python vývoj** | `deepseek/deepseek-v4-flash` | `/model deepseek/deepseek-v4-flash` |
| **Kognitivní/Filosofická diskuze** | `openai/gpt-oss-120b` | `/model openai/gpt-oss-120b` |
| **Hluboký Reasoning / CoT** | `deepseek/deepseek-v4-flash` | `/model deepseek/deepseek-v4-flash` + `--reasoning_effort xhigh` |
| **Analýza celého repozitáře** | `meta-llama/llama-4-scout` | `/model meta-llama/llama-4-scout` |
| **Kritická architektura** | `anthropic/claude-sonnet-4` | `/model anthropic/claude-sonnet-4` |
| **Rychlá rešerše / Dokumentace** | `meta-llama/llama-3.3-70b-instruct:free` | `/model meta-llama/llama-3.3-70b-instruct:free` |

---

## 📊 Kalibrační protokol (Iterace v3 $\to$ v4)
Po 30 dnech provést:
1. Export usage z OpenRouter dashboardu.
2. Výpočet reálného poměru Input:Output tokenů.
3. Srovnání: `Kvalita výsledku` vs `Cena tokenu`.
4. Pokud `DeepSeek V4 Flash (xhigh)` nahrazuje `R1` s 90% úspěšností $\to$ odstranit drahé modely.
