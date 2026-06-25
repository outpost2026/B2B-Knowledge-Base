# OpenRouter Model Analysis v2 — Verifikovaná data z API

**Autor:** Ondřej Soušek  
**Datum:** 24. června 2026  
**Budget:** $20–25/měsíc  
**Stack:** Open Code GUI + OpenRouter API  
**Doména:** Python (VCF parser, Streamlit UI), kognitivní vědy, filosofie

---

## Metodologie

Všechny modely, ceny a parametry byly ověřeny přímo z OpenRouter API katalogu k 24. 6. 2026:

| Zdroj | URL | Účel |
|-------|-----|-------|
| DeepSeek katalog | `openrouter.ai/models/deepseek` | Layer 1 + 2 |
| Anthropic katalog | `openrouter.ai/models/anthropic` | Layer 1 + 2 premium |
| Google katalog | `openrouter.ai/models/google` | Layer 1 |
| Meta katalog | `openrouter.ai/models/meta-llama` | Layer 1 + 2 budget |
| Qwen katalog | `openrouter.ai/models/qwen` | Layer 2 |

Hodnocení vychází z:
- Oficiálních benchmarků (SWE-bench, HumanEval, LMArena)
- OpenRouter rankingu podle objemu tokenů (reálné usage)
- Parametrů modelu (context window, reasoning support, tool calling)

---

## Klíčový insight: DeepSeek V4 Flash jako univerzální řešení

DeepSeek V4 Flash (284B total, 13B active, 1M context) podporuje `reasoning effort: high` a `xhigh`. To znamená, že **jeden model může sloužit oběma vrstvám** — běžné kódování bez reasoning effort, kognitivní diskuze s `xhigh` reasoning effort.

Cena $0.09/$0.18/M tok. je nejlepší poměr cena/výkon na trhu.

---

## Layer 1: Reasoning — kognitivní vědy, IT, filosofie

### Výběrová kritéria
- Kvalita chain-of-thought (otevřené reasoning tokeny)
- Hloubka epistemické analýzy
- Podpora extended thinking / reasoning effort
- Cost per reasoning session

### Pořadí (1 = nejvhodnější)

| # | Model (OpenRouter slug) | Cena I/O / 1M | Context | Reasoning support | Měsíční kapacita* | Silné stránky | Slabiny |
|---|------------------------|---------------|---------|-------------------|--------------------|---------------|---------|
| 1 | `deepseek/deepseek-v4-flash` | $0.09 / $0.18 | 1M | `high` / `xhigh` | ~100M tok. | Nejlepší poměr cena/kvalita; 1M kontext; reasoning effort škálovatelný | Méně hluboký než R1 v max režimu |
| 2 | `deepseek/deepseek-v4-pro` | $0.435 / $0.87 | 1M | `high` / `xhigh` | ~20M tok. | 49B aktivních parametrů; reasoning pro komplexní doménové analýzy | 4–5× dražší než Flash |
| 3 | `google/gemini-2.5-flash` | $0.30 / $2.50 | 1M | Built-in thinking | ~8M tok. (output) | Vestavěné thinking; multimodální; 1M kontext | Výstup 14× dražší než V4 Flash |
| 4 | `deepseek/deepseek-r1` | $0.70 / $2.50 | 164K | Nativní CoT | ~2.5M tok. (output) | Plně otevřené reasoning tokeny; ověřená kvalita | 8× dražší než V4 Flash; kratší kontext; pomalý |
| 5 | `deepseek/deepseek-r1-0528` | $0.50 / $2.15 | 164K | Nativní CoT | ~3M tok. (output) | Vylepšený R1; o3-level reasoning | Stále drahý; kratší kontext |
| 6 | `meta-llama/llama-4-maverick` | $0.15 / $0.60 | 1M | Instruction-tuned | ~30M tok. | Otevřené váhy; 1M kontext; dobrý reasoning | Slabší na hlubokou epistemickou analýzu |
| 7 | `google/gemini-2.5-pro` | $1.25 / $10 | 1M | Built-in thinking | ~2M tok. (output) | #1 na LMArena; nejlepší reasoning kvalita | Extrémně drahý ($10/M output) |
| 8 | `meta-llama/llama-3.3-70b-instruct` | $0.10 / $0.32 | 131K | Standard | ~50M tok. | Solidní všeobecný reasoning | Kratší kontext; žádné extended thinking |
| 9 | `deepseek/deepseek-v3.2` | $0.2288 / $0.3432 | 131K | Reasoning enabled | ~30M tok. | GPT-5 class performance; reasoning enable/disable | Nový model, méně prověřený |
| 10 | `qwen/qwen-3.6-flash` | $0.1875 / $1.125 | 1M | Built-in thinking | ~15M tok. (output) | 1M kontext; agentní reasoning | Výstup 6× dražší než V4 Flash |

> *Měsíční kapacita = reálný odhad při budgetu $8 na Layer 1, počítáno pro input:output poměr 3:1

### Doporučený workflow pro Layer 1

```yaml
Výchozí: deepseek/deepseek-v4-flash (s --reasoning_effort high)
  → kognitivní diskuze, filosofie, analýza konceptů
  
Hluboká analýza: deepseek/deepseek-v4-pro (s --reasoning_effort xhigh)
  → komplexní doménové modelování, epistemická kalibrace
  
Premium: google/gemini-2.5-flash
  → multi-perspektivní analýza, vyžaduje-li úkol multimodální vstup
  
Free fallback: meta-llama/llama-3.3-70b-instruct:free
  → jednoduché rešerše, definice pojmů
```

---

## Layer 2: Software development — Python, testy, refactoring

### Výběrová kritéria
- Přesnost generování kódu (Python, pytest, Streamlit)
- Schopnost práce s existujícím kódem (repo-level)
- Generování testů a dokumentace
- Cost per coding session

### Pořadí (1 = nejvhodnější)

| # | Model (OpenRouter slug) | Cena I/O / 1M | Context | Coding benchmarks | Měsíční kapacita* | Silné stránky | Slabiny |
|---|------------------------|---------------|---------|-------------------|--------------------|---------------|---------|
| 1 | `deepseek/deepseek-v4-flash` | $0.09 / $0.18 | 1M | HumanEval ~89% | ~200M tok. | Nejlepší poměr cena/výkon na trhu; 1M kontext; rychlý | Občasné chyby v komplexní architektuře |
| 2 | `qwen/qwen-3.5-9b` | $0.10 / $0.15 | 262K | Solidní | ~150M tok. | Extrémně levný výstup; rychlý | Menší kontext; slabší na rozsáhlé refactoringy |
| 3 | `deepseek/deepseek-v4-pro` | $0.435 / $0.87 | 1M | SWE-bench ~78% | ~40M tok. | 49B aktivních; architektonické rozhodování | 4–5× dražší než Flash |
| 4 | `google/gemma-4-31b-it` | $0.12 / $0.35 | 256K | Reasoning + coding | ~100M tok. | Otevřené váhy; thinking mode | Menší kódová specializace |
| 5 | `qwen/qwen-3.6-27b` | $0.2885 / $3.17 | 262K | Repo-level kód | ~12M tok. (output) | Silný v repo-level komprehenzi | Výstup 18× dražší než V4 Flash |
| 6 | `deepseek/deepseek-v3.2` | $0.2288 / $0.3432 | 131K | GPT-5 class | ~50M tok. | Reasoning pro komplexní debugování | Kratší kontext; nový model |
| 7 | `meta-llama/llama-4-scout` | $0.10 / $0.30 | 10M | Standardní | ~120M tok. | **10M kontext** — celý repozitář najednou | Nižší kvalita kódu než DeepSeek |
| 8 | `anthropic/claude-sonnet-4` | $3 / $15 | 1M | SWE-bench 72.7% | ~2.5M tok. (output) | Špičková architektura; autonomní codebase navigace | Extrémně drahý — jen na kritické úkoly |
| 9 | `meta-llama/codellama-70b-instruct` | kontakt | 2K | Code-specialized | — | Specializovaný na kód; legacy podpora | Zastaralý; 2K kontext; nedostupné ceny |
| 10 | `google/gemini-2.5-flash-lite` | $0.10 / $0.40 | 1M | Thinking enabled | ~90M tok. | Levný; 1M kontext; thinking | Pomalejší než V4 Flash |

> *Měsíční kapacita = reálný odhad při budgetu $15 na Layer 2, počítáno pro input:output poměr 3:1

### Doporučený workflow pro Layer 2

```yaml
Výchozí (90% úkolů): deepseek/deepseek-v4-flash
  → vývoj Python/VCF parser, pytest testy, Streamlit UI, refactoring
  
Komplexní kód: deepseek/deepseek-v4-pro
  → architektonická rozhodnutí, optimalizace, multi-file změny
  
Velký refactoring: meta-llama/llama-4-scout (10M kontext)
  → celý repozitář v kontextu, hledání duplicit, rozsáhlé změny

Premium: anthropic/claude-sonnet-4
  → kritická architektura, komplexní bug hunting (max 1–2× týdně)

Free jednoduché: qwen/qwen-3.5-9b

  → dokumentace, formátování, jednoduché unit testy
```

---

## Budget model — reálná kalkulace

### Základní scénář: $20/měsíc

| Vrstva | Model | Podíl | Input tok. | Output tok. | Cena |
|--------|-------|-------|------------|-------------|------|
| Coding 85% | V4 Flash | 80% | 72M | 24M | $10.80 |
| Coding 85% | V4 Pro | 5% | 4.5M | 1.5M | $3.26 |
| Reasoning 12% | V4 Flash (xhigh) | 10% | 9M | 3M | $1.35 |
| Reasoning 12% | R1/R1-0528 | 2% | 0.6M | 0.2M | $0.85 |
| Premium 3% | Claude Sonnet 4 | 3% | 0.3M | 0.1M | $2.40 |
| **Free** | Llama 3.3 70B free | — | 5M | 2M | $0 |
| **Rezerva** | | | | | **$1.34** |
| **Celkem** | | **100%** | | | **$20.00** |

### Ekonomický scénář: $15/měsíc

| Vrstva | Model | Podíl | Input tok. | Output tok. | Cena |
|--------|-------|-------|------------|-------------|------|
| Coding 90% | V4 Flash | 88% | 72M | 24M | $10.80 |
| Reasoning 10% | V4 Flash (xhigh) | 10% | 9M | 3M | $1.35 |
| Premium 2% | Odebrat Sonnet | 0% | — | — | $0 |
| Free tier | Llama 3.3 70B free | — | 10M | 3M | $0 |
| **Rezerva** | Gemma 4 31B free | — | 5M | 2M | $0 |
| **Celkem** | | **100%** | | | **~$13** |

---

## OpenRouter routing strategie

OpenRouter podporuje routing modifikátory, které lze využít pro optimalizaci ceny:

| Modifikátor | Funkce | Použití |
|-------------|--------|---------|
| `:floor` | Nejlevnější provider pro daný model | `deepseek/deepseek-v4-flash:floor` |
| `:free` | Free model (rate limited) | `meta-llama/llama-3.3-70b-instruct:free` |
| `max_price` | Hard budget cap | V programovém volání |

### Konkrétní nastavení pro Open Code GUI

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openrouter": {
      "models": {
        "deepseek/deepseek-v4-flash:floor": {},
        "deepseek/deepseek-v4-pro:floor": {},
        "deepseek/deepseek-r1:floor": {},
        "deepseek/deepseek-r1-0528:floor": {},
        "deepseek/deepseek-v3.2:floor": {},
        "meta-llama/llama-4-maverick:floor": {},
        "meta-llama/llama-4-scout:floor": {},
        "meta-llama/llama-3.3-70b-instruct:free": {},
        "qwen/qwen-3.5-9b:floor": {},
        "google/gemini-2.5-flash:floor": {},
        "google/gemma-4-31b-it:free": {},
        "anthropic/claude-sonnet-4:floor": {}
      }
    }
  }
}
```

---

## Model switching v praxi

| Úkol | Příkaz v Open Code | Model |
|------|--------------------|-------|
| Python vývoj (default) | `/model deepseek/deepseek-v4-flash` | V4 Flash |
| Reasoning diskuze | `/model deepseek/deepseek-v4-flash` + `--reasoning_effort xhigh` | V4 Flash (xhigh) |
| Hluboká CoT analýza | `/model deepseek/deepseek-r1` | R1 |
| Architektura | `/model deepseek/deepseek-v4-pro` | V4 Pro |
| Celý repozitář | `/model meta-llama/llama-4-scout` | Scout (10M ctx) |
| Free jednoduché | `/model meta-llama/llama-3.3-70b-instruct:free` | Llama free |
| Premium kód | `/model anthropic/claude-sonnet-4` | Sonnet 4 |

---

## Odstraněné modely z v1

Následující modely z v1 dokumentu **neexistují** na OpenRouter, nebo mají jiný slug:

| Model ve v1 | Skutečnost |
|------------|-----------|
| `qwen/qwen-3-coder` | **NEEXISTUJE** — nejbližší alternativa: `qwen/qwen-3.6-27b` |
| `code-llama-70b` | **JINÝ SLUG** — správně: `meta-llama/codellama-70b-instruct` (2K ctx, nedostupné ceny) |
| `starcoder2-30b` | **NEEXISTUJE** — OpenRouter nenabízí |
| `wizardcoder-34b` | **NEEXISTUJE** — OpenRouter nenabízí |
| `phind-code-34b` | **NEEXISTUJE** — OpenRouter nenabízí |
| `magicoder-2` | **NEEXISTUJE** — OpenRouter nenabízí |
| `xwincoder` | **NEEXISTUJE** — OpenRouter nenabízí |
| `nexusraven-2` | **NEEXISTUJE** — OpenRouter nenabízí |
| `mixtral-12x22b` | **NEEXISTUJE** — OpenRouter nenabízí |
| `nemotron-4` | **NEEXISTUJE** — OpenRouter nenabízí |
| `command-r++` | **NEEXISTUJE** — OpenRouter nenabízí |
| `yi-1.5-34b` | **NEEXISTUJE** — OpenRouter nenabízí |
| `openchat-4.5` | **NEEXISTUJE** — OpenRouter nenabízí |
| `meta-llama/llama-3.3-70b` | **JINÝ SLUG** — správně: `meta-llama/llama-3.3-70b-instruct` |

Všechny ceny a benchmark skóre ve v1 byly nahrazeny ověřenými daty z OpenRouter API.

---

## Kalibrační protokol (budoucí iterace)

Po 2–4 týdnech reálného používání:

1. **Export usage statistik** z OpenRouter dashboardu
2. **Srovnání** plánovaného budgetu se skutečnou spotřebou
3. **Adjustace poměrů** mezi vrstvami dle reálné potřeby
4. **Vytvoření v3 dokumentu** s korigovanými daty

Měřitelné metriky:
- Tokens per session (Layer 1 vs Layer 2)
- Skutečný poměr input:output tokenů
- Počet session na model
- Celková cena za model
- Satisfaction rate (subjektivní škála 1–5)

---

## Závěr

1. **Default pro obě vrstvy:** `deepseek/deepseek-v4-flash` — s `reasoning_effort high` pro Layer 1, bez pro Layer 2
2. **Premium rezerva:** `anthropic/claude-sonnet-4` — pouze na kritické úkoly
3. **Free tier:** `meta-llama/llama-3.3-70b-instruct:free` — dokumentace, rešerše
4. **Reálný budget:** ~$15–20/měsíc — včetně rezervy na experimenty
5. **Routing:** Vždy používat `:floor` pro nejlevnějšího providera