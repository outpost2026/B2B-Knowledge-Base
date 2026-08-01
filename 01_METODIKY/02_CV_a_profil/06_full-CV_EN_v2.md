# ONDREJ SOUSEK

**Systems Integrator — Formalization, Reverse Engineering & Automation for CAM/CNC, Manufacturing Operations and Agentic Infrastructure**

Prague, Czech Republic | +420 735 045 256 | [sousek@systeq.cz](mailto:sousek@systeq.cz) | github.com/outpost2026 | systeq.cz | linkedin.com/in/ondrejsousek

## PROFILE

I specialize in converting unformalized, tacit, and proprietary systems into explicit, transferable models — deterministic parsers, automation pipelines, documentation, and data structures. In 2026 I demonstrated this mechanism by reverse-engineering an undocumented binary format, .VCF (Ruida/VCutWorks CAM software): with no public specification or SDK, across 22 iterations I built a deterministic parser with \>99.98% toolpath extraction accuracy and deployed it on GCP Cloud Run for a real manufacturing B2B client (200+ orders/month).

In the same year I built a complete agentic infrastructure: 4 custom MCP servers (40+ tools), 7 test suites with 446 tests, CI/CD pipelines, and a knowledge base governed by my own EROI scoring model. Portfolio: 19 repositories, 845 commits (avg ~6.5/day), ~23,000 production lines of Python in 19 weeks.

The same mechanism underlies 14 years of experience in industrial manufacturing and CNC machining — which gives me the ability to recognize where information asymmetries and single-person dependencies form in operations. I use Python, GCP, Docker, MCP, and CAD/CAM tools as instruments of this transformation, not as ends in themselves.

## WHAT I BRING

**Core: extracting and formalizing complex systems**

- Reverse engineering of undocumented binary formats and proprietary data structures (hex analysis, IEEE 754, pair-diff diagnostics) with no specification or SDK.

- Systematic mapping and documentation of tacit operational know-how — typically tied to departing key employees — into structured knowledge corpora.

- Identifying information asymmetries, gatekeepers, and single points of failure in operational processes, and designing their formalization or elimination.

- Designing deterministic data models from heuristic or expert estimates — e.g., machine-time prediction (±2–5%) and order-complexity classification from CAM data.

**Agentic Engineering (2026)**

- 4 production MCP servers built in 17 days: cnc-tools (21 tools), linkedin-analyzer (EROI pipeline), mcp-jobs (job scraping), lichess-analyzer (17 tools, Stockfish 18 integration).

- Proprietary EROI scoring model (6 dimensions, weighted: domain 35%, tech 25%, role 20%, growth 10%, formal 5%, location 5%) for automated job-offer selection.

- LLM output quality control: narrative validator (anti-hallucination guard, 5 categories), compression validation of patterns, deterministic data-first architecture.

- Knowledge base with governance rules P1–P5 (clone prohibition, archive policy, drift check) — trim 86 → 56 files (−35%), 0 duplicates.

**Implementation — the tools through which I realize the mechanism**

- Python 3.11/3.12/3.14 (struct, math — deterministic binary parsers), pytest (446 tests across 7 repos), golden master regression, determinism tests, CI/CD (GitHub Actions, 3-version Python matrix, CodeQL, Dependabot).

- MCP: FastMCP, MCP stdio protocol, Streamlit, Playwright/Patchright, Python SDK.

- GCP: Cloud Run, Cloud Functions, Cloud Scheduler (6 cron jobs), GCS, Firestore, BigQuery; Docker (python:3.12-slim).

- CAM/CNC: G-code, NCstudio 10, VCutWorks, LightBurn, DXF pipeline processing, resolving CAM color-palette divergence (ACI→RGB→Euclidean resolver).

- ETL and data engineering: web scraping (Playwright, BeautifulSoup, Requests), API integration, RAG pipelines with deduplication and classification taxonomy.

## FLAGSHIP PROJECTS

**1. VCF/DXF Parser Engine (2026) — reverse engineering, B2B**

A manufacturing B2B client (CNC processing, 200+ orders/month) was dependent on a proprietary binary format, .VCF, with no public specification or SDK, and on the tacit know-how of a departing key technician. In parallel I documented operational know-how and reverse-engineered the .VCF binary structure — 22 parser iterations, cross-validated against reference CAM software.

Result: deterministic parser with \>99.98% toolpath-length extraction accuracy (\<0.02% deviation vs LightBurn), machine-time prediction ±2–5%, order-complexity classification. A DXF indexer with Euclidean RGB color-divergence resolution and block explosion for INSERT entities. Deployment: GCP Cloud Run + Streamlit dashboard + Flask REST API for ERP. Golden master regression 10/10 PASS.

**2. MCP-Jobs v0.4.0 — job scraping pipeline**

MCP server for scraping Czech job portals (3 active portals). Custom boolean AST parser with AND/OR/NOT syntax and LRU cache (8000 → 8 re-parses per query), rate limiting 1.0s, exclude/location/salary filters. 125/125 tests PASS (66% coverage), pipeline 4.5× faster than legacy (46s vs 210s), 9 hardening iterations including a de novo audit (20 findings) and cross-LLM audit.

**3. LinkedIn EROI Analyzer — market intelligence**

Automated pipeline: scrape saved jobs → EROI scoring (6 dimensions) → report → KB write-back. Anti-bot engineering (adaptive delay 3–7s, fingerprint mix, session heartbeat). 71 tracked offers, 6% relevant (EROI ≥ 65) — quantified follow-up justification. 92 tests, weekly CI cron.

**4. lichess-analyzer-mcp — LLM pattern engineering**

MCP server (17 tools) with Stockfish 18 integration, pattern library of 18 patterns (A–Q1), dual cache (Stockfish + LLM). ACPL MAE 3.9 vs Lichess reference, 0% silent fail, 88 analyzed games. Empirical LLM cascade evaluation (DeepSeek V4 Flash SNR 93%). 93 tests.

## WORK EXPERIENCE

**SYSTEQ / Freelance Technical Implementer (Self-Employed) — Outpost, Prague** | 2025 – Present

- VCF/DXF Parser Engine — see flagship project above.

- Agentic infrastructure: 4 MCP servers, EROI pipeline, knowledge base (197 commits, governance P1–P5).

- Development and operation of an off-grid technical node — converting 14 years of hands-on energy and construction experience into a documented infrastructure system: 2.5 kWp solar array, LiFePO4 8S2P 630 Ah, BMS with active balancing.

- Data and knowledge pipelines on GCP: ETL for meteorological and sensor data, RAG pipeline for document migration, reverse engineering of ČHMÚ internal API (42 endpoints).

**CNC Operator (Waterjet) — Prague** | 2025 – 2026

- Operating CNC waterjet machinery, G-code editing in NCstudio 10, production data preparation from 2D drawings.

- Mapped implicit operational decision-making — cutting parameter choices, quality-control criteria — and converted it into explicit rules.

**Technical and Manual Trades — Manufacturing, Construction** | 2010 – 2023

- 14 years of experience in manufacturing and construction operations: technical drawing interpretation, material handling, root-cause analysis of production issues.

## EDUCATION & PROFESSIONAL DEVELOPMENT

- 14 years of hands-on qualification in industrial manufacturing and CNC machining (waterjet, milling).

- Self-directed study focused on transformation tools: Python, GCP, binary format reverse engineering, LLM-assisted development, MCP (2025–2026).

## LANGUAGES

Czech — native | English — C1 (technical documentation, communication) | French — conversational

## SEEKING

B2B collaboration and projects focused on formalizing and digitizing manufacturing and operational processes — particularly situations involving proprietary formats, individual-dependent tacit know-how, or unformalized workflows. Additionally, implementation of agentic infrastructure (MCP servers, EROI pipelines, automation) for SMEs and startups. Open to long-term B2B collaboration (consulting, IP licensing), self-employed contract projects, and full-time roles in industrial automation, CAM/CNC software, ERP integration, or AI tooling. Prague area / remote.

