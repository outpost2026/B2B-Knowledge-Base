# Ondřej Soušek

## Automation & Integration Engineer

**Python · Data/ETL · SQL/PostgreSQL · MCP/LLM Integration · Reverse Engineering · Industrial Systems**

Prague, Czech Republic · +420 735 045 256 · [sousek@systeq.cz](mailto:sousek@systeq.cz)  
[github.com/outpost2026](https://github.com/outpost2026) · [systeq.cz](https://www.systeq.cz/) · [LinkedIn](https://www.linkedin.com/in/ondrejsousek)

## Profile

Automation & Integration Engineer with a manufacturing and CNC background. I build Python-based automation and data systems for environments where processes are informal, data is incomplete, or software is proprietary. I combine data ingestion and transformation, SQL/PostgreSQL, deterministic validation, and an MCP/LLM integration layer with a practical understanding of manufacturing constraints.

I specialise in turning tacit rules and fragmented sources into explicit, testable, and operationally useful tools. I add the most value at the intersection of industrial digitalisation, technical B2B integration, data/ETL workflows, and applied AI.

## Core Capabilities

| Area | Skills and practical scope |
| - | - |
| **Software and data** | Python, CLI tools, data models, YAML configuration, ETL pipelines, HTTP/API integration, normalisation, deduplication, and reporting. |
| **Databases** | SQL/PostgreSQL: relational schemas, querying, upsert/persistence, local operation, and test databases in CI. |
| **MCP and applied AI** | FastMCP tools, resources, and prompts; transparent workflows in which an LLM/MCP layer operates over deterministic rules and data. |
| **Quality and delivery** | pytest, regression and determinism tests, Ruff, CI workflows, structured logging, technical documentation, and reproducible outputs. |
| **Reverse engineering** | Proprietary binary-format analysis, hex/pair-diff diagnostics, IEEE 754, serialisation, and verification against reference data. |
| **Industrial domain** | CNC/CAM, CAD/DXF, G-code, NCstudio 10, VCutWorks, LightBurn, work from 2D drawings, and manufacturing-workflow digitalisation. |
| **Infrastructure** | Git, Docker; project experience with GCP Cloud Run, Artifact Registry, Cloud Build, Cloud Scheduler, and Firestore. |


## Selected Technical Projects

### [MCP-Jobs](https://github.com/outpost2026/MCP-Jobs) — Multi-provider market-intelligence ETL | 2026

A Python MCP server for working with Czech job portals. The system combines six providers, HTTP scraping, Boolean-AST matching, URL and fuzzy deduplication, structured outputs, PostgreSQL persistence, asynchronous jobs, and MCP tools/resources/prompts.

The project demonstrates the practical ability to design a data pipeline from ingestion through transformation to persistence and an AI-facing interface. It includes a CLI, CI, linting, telemetry/logging, and 189 publicly visible test functions.

### [VCF/DXF Parser Engine](https://github.com/outpost2026/Vcf-compiler) — Reverse engineering and manufacturing automation | 2026

Reverse-engineering tooling for the undocumented `.VCF` binary format in the Ruida/VCutWorks ecosystem, together with parallel DXF processing. Without a public specification or SDK, I developed a deterministic parser across 22 iterations; the original validation case reports path-extraction accuracy above 99.98% through cross-validation against LightBurn.

The solution includes golden-master regressions, determinism tests, 2D visualisation, machine-time estimation, ERP-ready exports, and Docker/GCP Cloud Run deployment. It was developed in the context of an NDA-bound manufacturing B2B use case; client details and commercial metrics are not disclosed.

### [LinkedIn MCP Analyzer](https://github.com/outpost2026/linkedin-mcp-analyzer) — Career intelligence and decision support | 2026

A configurable MCP workflow that converts saved job postings into structured assessments of fit, gaps, and priorities. It combines a deterministic EROI model, reporting, automated knowledge-base write-back, tests, pre-commit, and a locked development stack.

The project demonstrates an applied-AI approach in which an LLM/MCP layer is not merely a text generator, but an integration layer over transparent rules and measurable decision criteria.

## Professional Experience

### SYSTEQ / Self-employed — Automation & Integration Projects

**Prague · 2026–present**

Development of tools for manufacturing digitalisation, data workflows, and technical B2B integrations. My work covers process formalisation, prototyping, and implementation of tooling for CAD/CAM data, the structuring of informal information, automated scoring, and decision support.

Outputs include VCF/DXF tooling, Python CLI and pipeline tools, PostgreSQL persistence, MCP interfaces, test automation, documentation, and project work with Docker and GCP.

### CNC

**Prague · 2025–2026**

Operation of a waterjet CNC machine, Plotter Cutting knives machines, G-code editing in NCstudio 10, and preparation of manufacturing data from 2D drawings. In parallel, mapping practical manufacturing decision rules around cutting parameters, quality control, and material flow.

This role created direct domain grounding for designing software that respects physical constraints, input-data quality, and operational dependencies.

## Professional Development

### Self-directed Software Engineering

**2025–2026**

Practical development in Python, software architecture, data/ETL pipelines, SQL/PostgreSQL, Docker, CI, MCP/LLM integrations, and reverse engineering. Evidence is available in public repositories and their testing, documentation, and release artefacts.

## Languages

| Language | Proficiency |
| - | - |
| Czech | Native |
| English | C1 — technical documentation and professional communication |
| French | Conversational |


## Target Roles and Engagements

Automation Engineer · Integration Engineer · Industrial Digitalisation Engineer · Data/AI Automation Developer · Technical Solutions Engineer. Open to full-time employment, long-term B2B engagement, or independent projects in Prague, hybrid, or remote.

