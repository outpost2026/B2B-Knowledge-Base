## 8. Statistiky

| Metrika | Hodnota |
|---------|---------|
| Celkem GT | **108** (GT-001..GT-105, mezery GT-082/GT-084 + GT-GCP-001..GT-GCP-005) |
| Fixed (vč. „Fixed / Mitigated", „Fixed (policy)") | 74 |
| Implemented | 6 |
| Mitigated | 6 |
| Documented | 18 |
| Workaround | 3 |
| Pending | 1 |
| **Kontrolní součet** | **108** |

Rozpad: environment/CI 11 · application logic 63 · cross-repo 17 · cross-LLM audit 5 (GT-061..065) · DBCL Phase 2 7 (GT-071..077) · data-correctness batch 1 (GT-079) · ASCII-NOM 1 (GT-080) · GCP infra 5 (GT-GCP-001..005).

---

*MCP_GROUND_TRUTH_postmortem_agregovany_v2.md — 2026-08-26 — v20 (souborová generace v2) — trim iterace A nad v1/v19 dle sémantické analýzy 2026-08-26: (1) dedup `Pravidlo:` textů entrií → ukazatele, kanonický text výhradně §4; (2) kanonizace P80–P83 a P90–P96 do §4 (ve v1 definovány pouze inline); (3) odstranění duplicitního footer changelogu, per-version poznámek ve statistikách a sebekorekčního narrativu (plná historie verzí = git log repa; komprese −30 % při zachování 108 GT záznamů, 48 Provenance polí a všech file:line referencí); (4) integritní opravy: titulek §4 (P1–P96), titulek §5 (82 checkpointů), reference GT-083 P71→P70, dokumentace mezer GT-082/GT-084 a P78/P79, stale rozsah v úvodu §3.7. Originál v1 zachován do validace v2 (rozhodnutí autora 2026-08-26); po validaci přesunout do `_ARCHIVE/`. Header/footer verze 20 konzistentní.*
