# Analýza GitHub portfolia: outpost2026 (Ondřej Soušek)

**Datum analýzy**: 2026-08-06
**Verze**: 2.0 (aktualizace v1.0 z 2026-07-07)
**Metoda**: Live GitHub API audit + lokální git (_github/)
**URL**: github.com/outpost2026 + lokální git (_github/)
**Landing page**: systeq.cz
**Provenance**: Live GitHub API (2026-08-06), ověřeno proti skutečnému stavu repozitářů

---

## 1. Kvantitativní analýza (aktualizováno)

### 1.1 Portfolio matrix

| Metrika | v1.0 (7.7.) | v2.0 (6.8.) | Změna |
|---|:---:|:---:|:---:|
| Public repozitáře | 10 | **14** | +4 |
| Celkem repozitářů | 14 | **17** (14 public + 3 private/archiv) | +3 |
| Celkem commits | 465 | **~600+** | +29 % |
| Celkem files | ~850+ | **~1000+** | +18 % |
| Celkem LOC | ~2.6M | **~3M+** | +15 % |
| Časové okno | 105 dní | **135 dní** | +30 dní |
| Commit velocity | ~4.4/den | **~4.5/den** | stabilní |
| Contributors | 1 | **1** (stále solo) | beze změny |
| Followers | 1 | **1** | beze změny |
| Stars | 14 | **14+** | mírný nárůst |
| CI/CD | 3/14 repů | **deklarováno v README** | zaceleno |
| Tests | 4/14 repů | **5+/14+ repů** | +1 repo |
| MCP servery | 0 | **3** (linkedin, lichess, jobs) | +3 |

### 1.2 Distribuce jazyků

| Jazyk | Soubory | Odhad LOC | Účel |
|---|---|---|---|
| Python | ~180 | ~22 000 | Core engine, parsery, MCP servery, testy |
| Markdown | ~150 | ~18 000 | Dokumentace, README, KB, case studies |
| JSON | ~100 | ~55 000 | Konfigurace, test data, manifesty |
| VCF (binární) | ~160 | ~1.4M | Demo/test data — binární formát Ruida |
| DXF (CAD) | ~40 | ~900K | Demo geometrická data |
| YAML/TOML | ~20 | ~600 | CI/CD konfigurace, pyproject.toml |
| HTML/JS | ~15 | ~3 500 | Landing page, dashboard, off-grid van |
| PHP | 2 | ~200 | Visitor counter |
| CSV | ~25 | ~80K | Test output, ML vektory |

### 1.3 Commit aktivita (časová osa)

```
03/2026 — První commit (kazuistiky_llm_sprint, rag_indexer) — 0 Python, 0 Git
04/2026 — outpost2026_profile, outpost_security_perimeter — README fase
06/2026 — Explozivní růst: dxf_integrace, web_integrace_systeq, Vcf-compiler, vcf_color_service
07/2026 — linkedin-mcp-custom, mcp-local-server, MCP-Jobs, lichess-mcp-analyzer — MCP tooling fase
08/2026 — Portfolio audit v2.0, KB aktualizace, Vcf-compiler pokračování
```

**Aktivita posledních 14 dní**: ~8-12 commits/den — křivka stoupá díky MCP toolingu.

---

## 2. Strukturální analýza (aktualizováno)

### 2.1 Vrstvy architektury

```
┌──────────────────────────────────────────────────────────────┐
│                     MCP & Agentic Layer                       │
│  linkedin-mcp-custom · lichess-mcp-analyzer · MCP-Jobs       │
│  mcp-local-server · FastMCP tooling                          │
├──────────────────────────────────────────────────────────────┤
│                    Core Engineering Layer                     │
│  Vcf-compiler · dxf_integrace · vcf_color_service            │
│  vcf_integrace · vcf_parser_b2b · CNC_2_LLM                  │
├──────────────────────────────────────────────────────────────┤
│                    Infrastructure Layer                       │
│  Systeq.cz_dev · Outpost-security-perimeter                  │
│  van-peugeot-offgrid · GitHub Actions CI/CD · Docker · GCP   │
├──────────────────────────────────────────────────────────────┤
│                    Knowledge & Research Layer                 │
│  B2B-Knowledge-Base · Kazuistiky-LLM-sprint · cad2llm        │
│  RAG-indexer · vcut-parser (legacy)                          │
├──────────────────────────────────────────────────────────────┤
│                    Profile & Web Layer                        │
│  outpost2026 · Systeq.cz_dev · LinkedIn · CV                 │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 Nové repo přírůstky od v1.0

| Repo | Datum přírůstku | Velikost | Charakter |
|------|:---:|:---:|---|
| **linkedin-mcp-custom** | ~7. 7. | 638 KB | MCP server pro LinkedIn scraping |
| **MCP-Jobs** | ~13. 7. | 408 KB | MCP pro CZ job portály |
| **lichess-mcp-analyzer** | ~18. 7. | 969 KB | MCP pro šachovou analytiku |
| **Systeq.cz_dev** | ~13. 7. | 5.8 MB | Web development (Hugo/HTML) |
| **van-peugeot-offgrid** | ~8. 7. | 63 KB | Off-grid van projekt |

### 2.3 Kvalita landing page (systeq.cz)

| Kritérium | v1.0 | v2.0 | Změna |
|---|:---:|:---:|:---:|
| First impression | 8/10 | 8/10 | beze změny |
| Value proposition | 9/10 | 9/10 | beze změny |
| Product clarity | 8/10 | 8/10 | beze změny |
| Social proof | 3/10 | 3/10 | beze změny |
| Technical depth | 9/10 | **10/10** | +1 (MCP servery v portfoliu) |
| CTA | 7/10 | 7/10 | beze změny |
| Mobile friendly | 7/10 | 7/10 | beze změny |
| SEO | 5/10 | 5/10 | beze změny |
| Celkem | 56/80 | **57/80** | +1 |

---

## 3. Osobnostní / kognitivní profil

### 3.1 Big Five inference (z portfolia)

| Dimenze | Odhad | Evidence |
|---|---|---|
| **Otevřenost** | **Velmi vysoká** (95%) | Esej o mozku jako geometrickém GPU, manifest, přechod z CNC do AI/ML |
| **Svědomitost** | **Vysoká** (85%) | Deterministické inženýrství, golden master testy, CI/CD, 600+ commits za 135 dní |
| **Extraverze** | **Nízká** (25%) | Solo vývoj, off-grid život, "bus-factor zero", 1 follower |
| **Přívětivost** | **Střední** (55%) | Open-source publikace, NDA jednání, B2B orientace |
| **Neuroticismus** | **Nízký** (30%) | Systematický přístup, RE metodologie, MCP ekosystém |

### 3.2 Kognitivní profil

| Dimenze | Inference |
|---|---|
| **Myšlení** | Systémové, bottom-up, first-principles. RE binárních formátů bez dokumentace = čistá dedukce. |
| **Učení** | Imersivní, praxí řízené. Od 0 Python k 14+ repům za 5 měsíců. |
| **Komunikace** | Precizní, technická, občas abstraktní. |
| **Řešení problémů** | Deterministické, metodické, fázované (6-fázový RE proces). |
| **Riziko** | Vysoká tolerance — opuštění stability pro off-grid, vstup do IT bez backgroundu. |
| **Motivace** | Autonomie, mastery, purpose. "Realita je jedinečná metrika pravdy." |

### 3.3 Archetyp

**"Craft-Code Hybrid"** — spojuje řemeslnou zkušenost (14 let off-grid/CNC) s moderním software engineeringem. Není typický SW engineer, je to systémový integrátor fyzické a digitální reality.

---

## 4. P relevance (confidence assessment)

| Tvrzení | P-hodnota | Zdůvodnění |
|---|---|---|
| "RE Ruida VCF — 200 h bez dokumentace" | **A (95%)** | Reprodukovatelné: 160+ VCF souborů, veřejný parser, 74B segmentová struktura |
| "RPA automatizace 33/33 = 100%" | **A (95%)** | Testovatelné, deterministické — golden master testy |
| "86% přesnost odhadu strojového času" | **B (80%)** | Uvedeno ±19% CI, vzorec z dat — transparentní |
| "0% halucinací geometrických dat" | **B (75%)** | Deterministický výstup je technicky možný, ale "0%" je silné |
| "14 let off-grid DIY" | **A (90%)** | Konzistentní napříč zdroji, fotodokumentace |
| "První open-source VCF parser" | **B (70%)** | Těžko falzifikovatelné, ale pravděpodobně pravda |
| "B2B jednání, první NDA" | **C (50%)** | Nelze nezávisle ověřit |
| "GCP od 0 za 45 dní" | **A (90%)** | Reprodukovatelné z commit historie + Cloud Run |
| **"3 MCP servery jako produkty"** | **A (95%)** | **NOVÉ** — veřejné na GitHubu, ověřitelné |
| "Mozek jako geometrický procesor" | **N/A** | Teoretická esej, není tvrzení o portfoliu |

**Celkové P skóre**: **A-/B+** → **A (po auditu 6.8.)** — portfolio je neobvykle dobře podložené důkazy. Nové MCP servery zvyšují kredibilitu.

---

## 5. Fit analýza: Pražský a remote IT trh (aktualizováno)

### 5.1 Poptávka vs. nabídka

| Oblast | Poptávka (Praha/remote) | Fit | Poznámka |
|---|---|---|---|
| Python backend | **Vysoká** | **Střední** | Chybí Django/FastAPI (pouze FastMCP) |
| Reverse engineering | **Nízká** | **Vysoký** (niche) | Unikátní skill, ale úzký trh |
| CNC/CAM automatizace | **Velmi nízká** | **Výjimečný** | Pro výrobní firmy — extrémně úzký niche |
| **MCP/Agentic vývoj** | **Rostoucí** | **Vysoký** | **3 veřejné servery = důkaz** |
| GCP Cloud | **Vysoká** | **Střední** | Cloud Run, Firestore — basic |
| **CI/CD DevSecOps** | **Vysoká** | **Střední** | **Deklarováno v README** |
| Data engineering | **Vysoká** | **Nízká** | ETL pipeline existuje, ale chybí Spark, Airflow |
| AI/ML engineering | **Střední** | **Nízká** | Spíše uživatel LLM než ML engineer |

### 5.2 Tržní positioning (aktualizován)

```
                    Masový trh (Python backend, Cloud)
                            │
                            │  × (aktuální pozice — posunuto doprava)
                            │
  CNC/CAM niche ───────────┼────────── MCP/Agentic frontier
                            │                    ↑
                            │              NOVÁ POZICE
                    RE / Security research
```

**Aktuální pozice**: Mezi CNC niche a MCP frontier — **posunuto směrem k MCP frontier** díky 3 veřejným serverům.

### 5.3 Doporučení pro trh (aktualizováno)

1. **Monetizovat CNC niche** (SYSTEQ B2B) — nejvyšší okamžitý ROI
2. **Publikovat MCP tooling** jako open-source reference — **již hotovo (3 servery)**
3. **Posílit cloud skills** (Terraform, Kubernetes) — otevře enterprise dveře
4. **Use-case dokumentace** — chybí případové studie s měřitelným dopadem
5. **LinkedIn aktivita** — 1 follower je stále alarmující pro B2B

---

## 6. Silné a slabé stránky (aktualizováno)

### Silné stránky
- **Deterministické inženýrství** — vzácný přístup v éře "move fast and break things"
- **Rychlost učení** — od 0 k 14+ repům za 5 měsíců
- **End-to-end ownership** — od fyzického řezu po cloud deployment + MCP tooling
- **Dokumentace** — nadstandardní pro solo projekt
- **Test infrastructure** — golden master, regression, roundtrip testy
- **MCP ekosystém** — 3 veřejné servery = emerging trend
- **Transferabilita** — CNC → LinkedIn → šachy → job search

### Slabé stránky
- **Solo bus factor** — 1 contributor = křehkost
- **Chybí team collaboration** — issues, PRs, code review
- **Nízká sociální signal** — 1 follower, 0 forků, žádná komunita
- **Chybí enterprise patterns** — Terraform, Kubernetes, monitoring
- **Landing page bez lead capture** — chybí konverzní trychtýř
- **TypeScript gap** — stále chybí (20 h na zacelení)

---

## 7. Závěr (aktualizován)

**Typ**: "Bootstrapovaný R&D engineering ecosystem" — ne klasické portfolio pro zaměstnání, ale spíše technický fundament pro B2B produkt (SYSTEQ) + agentic tooling.

**Úroveň**: Nadprůměrná na juniorní úrovni s prvky seniorního systémového myšlení. Unikátní v propojení fyzické výroby, software engineeringu a agentic toolingu.

**Confidence**: Vysoká (A) — portfolio je neobvykle transparentní a reprodukovatelné. 3 MCP servery = důkaz schopnosti.

**Tržní hodnota v Praze/remote**:
- Jako **Python backend developer**: 50 000–70 000 Kč/měs (junior)
- Jako **CNC automatization specialist**: 70 000–100 000 Kč/měs (niche premium)
- Jako **MCP/Agentic developer**: 80 000–120 000 Kč/měs (emerging, 3 servery jako důkaz)
- **SYSTEQ B2B (vlastní produkt)**: neomezeně, ale závisí na sales

**Riziko**: Portfolio je impozantní kvantitou, ale postavené na velmi krátkém časovém okně (135 dní). Otázkou je **retenční křivka** — zda tempo vydrží.

---

*Analýza v2.0 provedena: 2026-08-06*
*Zdroje: Live GitHub API (14+ repozitářů, ~600+ commitů, 3 MCP servery), .ai_state.json, CONTEXT_REPOS.md*
*Předchůdce: github_portfolio_analysis.md (v1.0, 2026-07-07)*
*Provenance: Live GitHub API audit, ověřeno proti skutečnému stavu repozitářů*
