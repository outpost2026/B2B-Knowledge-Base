# MCP GROUND TRUTH — Agregovaná pitevní kniha

**Datum:** 2026-08-26 | **Verze:** 20 (souborová generace v2; interní řada pokračuje z v1/v19)
**Účel:** Jediný zdroj pravdivých ponaučení z vývoje všech MCP serverů v portfoliu. Nahrazuje: linkedin_mcp_pitevni_kniha_v1.md, mcp_jobs_pitevni_kniha_v1.md, sdilena_pitevni_kniha_mcp.md, MCP_komplexni_analyza_a_strategie_v1.md (pouze postmortem části), pitevni_kniha_mcp_v1.md (cnc-tools).
**Rozsah:** linkedin-mcp-custom, MCP-Jobs, mcp-local-server (cnc-tools), lichess-analyzer-mcp, GCP infrastructure (pitevni_kniha_v8)
**Určení:** Výukový materiál pro deva, instrukce pro LLM, ground truth pro rozhodování
**Provenance trimu:** v2 = trim iterace A nad v1/v19 (sémantická analýza 2026-08-26): dedup `Pravidlo:` textů entrií → ukazatele (kanonický text v §4), kanonizace P80–P83 a P90–P96 do §4, odstranění duplicitního changelogu a statistického narrativu, komprese sekundárních pasáží. Zachováno: všech 108 GT záznamů, 48 Provenance polí, file:line reference. Historie verzí = git log repa.
**Skill:** Před editací loadni `skill({name: "kb-workflow"})` → sekce Postmortem Workflow obsahuje pravidla pro konzistentní zápis GT/P a prevenci konfabulace.

---

## 1. Mapa superseded artefaktů

| Původní soubor | Co se přebírá | Co se zahazuje |
|----------------|---------------|----------------|
| `linkedin_mcp_pitevni_kniha_v1.md` | Entry 007-024 (plné znění) | Duplicitní statistiky, Session 3→4 timeline (historický) |
| `mcp_jobs_pitevni_kniha_v1.md` | Entry 022-035 (plné znění) | Cross-LLM audit metoda 032 (meta-poznatek, ne bug) |
| `sdilena_pitevni_kniha_mcp.md` | Průřezová pravidla P1-P23, Entry 001-028 (stručné) | Duplicitní popisy (odkazovaly na originály) |
| `pitevni_kniha_mcp_v1.md` (cnc-tools) | Entry 001-014, Diagnostický filtr, P24-P28 | Cross-referenční mapa (nyní redundantní) |
| `MCP_komplexni_analyza_a_strategie_v1.md` | §9 Secret exposure, EROI framework, §10-11 akční plány | §1 Fenomén MCP, §4 Rešerše, §6 Use case, §7 Predikce |
| `MCP_practical_workflow_guide_v1.md` | §7 Falsifikace, §8 Rozhodovací framework | §2 Filosofie, §3 Scénáře (není postmortem) |
| `GCP/pitevni_kniha_v8.md` | GT-GCP-001..005 (5 entries, GCP infra: 5vrstvá auth, cron context, immutable infra, statelessness, Hard Reset) | Zbytek (~30 záznamů): inferovatelné z obecných SE principů nebo příliš specifické |

---

## 2. Nálezy agregace (komprimováno ve v2)

Vyřešené rozpory statusů při agregaci: Entry 016 (Fixed), Entry 020 (Fixed), input validation (Implementováno, Session 16); jednotné číslování GT#ID se zdrojovým ID v závorce. Eliminované duplicity: encoding/shell/quoting (6 zápisů → GT-031), MCP transport timeout (3 výskyty → GT-013), EROI matice a secret exposure sloučeny. Odstraněn nepostmortem obsah (tržní analýza, predikce 2027, filosofické pasáže, tabulky veřejných serverů). Zachovány unikátní části: Diagnostický filtr, WF simulace v3, 6-layer encoding stack (GT-041), L2 Resources architektura (GT-040).

---

## 3. Katalog chyb

108 záznamů: GT-001..GT-105 + GT-GCP-001..005. V závorce původní ID ze zdrojového artefaktu.

**Číslování a rezervace:** GT-082 a GT-084 nebyly přiděleny (mezera vznikla ve v10); P78/P79 neexistují; P84–P89 jsou rezervovány epistemické řadě (Gate protokol destruktivních operací). Sekce katalogu čísluje 3.1–3.3 a 3.5–3.7 (mezera 3.4 historická, zachována kvůli externím referencím).

**Formát záznamu:** Symptom → Root cause → Fix → Pravidlo (ukazatel; kanonický text pravidla viz §4) → Provenance.

