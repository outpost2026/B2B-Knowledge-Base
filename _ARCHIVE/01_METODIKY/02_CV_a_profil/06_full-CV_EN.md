# ONDŘEJ SOUŠEK (Ondrej Sousek)

**Systems Integrator — Formalization, Reverse Engineering & Automation for CAM/CNC and Manufacturing Operations**

Prague, Czech Republic | +420 735 045 256 | [sousek@systeq.cz](mailto:sousek@systeq.cz) | github.com/outpost2026 | systeq.cz


## PROFILE

I specialize in converting unformalized, tacit, and proprietary systems into explicit, transferable models — deterministic parsers, automation pipelines, documentation, and data structures. In 2026 I demonstrated this mechanism by reverse-engineering an undocumented binary format, .VCF (Ruida/VCutWorks CAM software): with no public specification or SDK, across 22 iterations I built a deterministic parser with \>99.98% toolpath extraction accuracy and deployed it on GCP Cloud Run for a real manufacturing B2B client (200+ orders/month).

The same mechanism underlies 14 years of experience in industrial manufacturing and CNC machining — which gives me the ability to recognize where information asymmetries and single-person dependencies form in operations — as well as my development of off-grid energy infrastructure and data/knowledge pipelines of my own. I use Python, GCP, Docker, and CAD/CAM tools as instruments of this transformation, not as ends in themselves.


## WHAT I BRING

**Core: extracting and formalizing complex systems**

- Reverse engineering of undocumented binary formats and proprietary data structures (hex analysis, IEEE 754, pair-diff diagnostics) with no specification or SDK.

- Systematic mapping and documentation of tacit operational know-how — typically tied to departing key employees — into structured knowledge corpora.

- Identifying information asymmetries, gatekeepers, and single points of failure in operational processes, and designing their formalization or elimination.

- Designing deterministic data models from heuristic or expert estimates — e.g., machine-time prediction and order-complexity classification from CAM data.

**Implementation — the tools through which I realize the mechanism**

- Python 3.11/3.12 (struct, math — deterministic binary parsers), pytest, golden master regression, determinism tests, type hints, structured logging.

- GCP: Cloud Run, Artifact Registry, Cloud Build, Cloud Scheduler, Firestore; Docker (python:3.11-slim); Streamlit; Flask REST API.

- CAM/CNC: G-code, NCstudio 10, VCutWorks, LightBurn, DXF pipeline processing, resolving CAM color-palette divergence.

- ETL and data engineering: web scraping (Playwright, BeautifulSoup, Requests), API integration (JSON/XML), RAG pipelines with deduplication and classification taxonomy.


## FLAGSHIP PROJECT — Demonstrating the Mechanism: VCF/DXF Parser Engine (2026)

**Starting state (high information entropy)**

A manufacturing B2B client (CNC processing, 500+ orders/month) was dependent on a proprietary binary format, .VCF (Ruida/VCutWorks), with no public specification or SDK, and on the tacit know-how of a departing key technician.

**Process (extraction and formalization)**

In parallel, I systematically documented operational know-how (materials, calibration, workflow) and reverse-engineered the .VCF binary structure — 22 parser iterations (V1–V22), cross-validated against the reference CAM software.

**Result (explicit model)**

A deterministic parser with \>99.98% toolpath-length extraction accuracy (cross-validated against LightBurn, \<0.02% deviation), with computed fields for machine-time estimation and order-complexity classification. A parallel DXF indexer resolving CAM palette color divergence (Euclidean RGB interpolation, block explosion for INSERT entities). Deployment: GCP Cloud Run (Docker, Artifact Registry) + Streamlit dashboard + Flask REST API for ERP integration. Golden master regression 10/10 PASS, determinism tests 2/2 PASS.

**Value delivered to the client**

Independence from any single individual and their departure, transferable documentation and code as a new company asset, automated data input for production planning and ERP.

🔗 Live demo: vcf-parser-demo-537446704644.europe-west1.run.app


## WORK EXPERIENCE

**SYSTEQ / Freelance Technical Implementer (Self-Employed) — Outpost, Prague** | 2023 – Present

- VCF/DXF Parser Engine — see flagship project above.

- Development and operation of an off-grid technical node (35 m²) — converting 14 years of hands-on energy and construction experience into a documented, functioning infrastructure system: 1.9 kWp solar array, LiFePO4 8S2P 630 Ah, BMS with active balancing. The same mechanism of formalizing implicit experience into an explicit system, applied to physical infrastructure.

- Data and knowledge pipelines on GCP: ETL for meteorological and sensor data, RAG pipeline for document migration with deduplication and classification taxonomy — formalizing unstructured data into structured, queryable systems.

**CNC Operator (Waterjet) — Prague** | 2025 – 2026

- Entry into a high-information-entropy manufacturing environment: operating CNC waterjet machinery, G-code editing in NCstudio 10, production data preparation from 2D drawings.

- Beyond the formal job scope, mapped implicit operational decision-making — cutting parameter choices, quality-control criteria, material flow optimization — and converted it into explicit rules. This role served as an entry point to later formalization work, not as an end goal in itself.

**Technical and Manual Trades — Manufacturing, Construction** | 2010 – 2023

- 14 years of experience in manufacturing and construction operations: technical drawing interpretation, material handling, root-cause analysis of production issues.

- Repeated exposure to high-information-entropy systems built the domain base from which my ability to recognize and formalize information asymmetries in other contexts derives.


## EDUCATION & PROFESSIONAL DEVELOPMENT

- 14 years of hands-on qualification in industrial manufacturing and CNC machining (waterjet, milling) — the domain base for identifying and formalizing information asymmetries.

- Self-directed study focused on transformation tools: Python, GCP, binary format reverse engineering, LLM-assisted development (2025–2026).


## LANGUAGES

Czech — native | English — C1 (technical documentation, communication) | French — conversational


## SEEKING

B2B collaboration and projects focused on formalizing and digitizing manufacturing and operational processes — particularly situations involving proprietary formats, individual-dependent tacit know-how, or unformalized workflows, where there is room to convert an implicit system into an explicit, transferable asset. Open to long-term B2B collaboration (consulting, IP licensing), self-employed contract projects, and full-time roles in industrial automation, CAM/CNC software, or ERP integration. Prague area / remote.

