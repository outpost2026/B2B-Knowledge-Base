# GROUND TRUTH: Aktuální stav autora, projektu Moodpasta & portfolia

**Verze:** 2.0 | **Datum:** 2026-08-06 | **Autor:** Ondřej Soušek (SYSTEQ)
**Účel:** Deterministický snapshot současného stavu — profil, vývoj, skills, Moodpasta kontext, portfolio, komunikace, zadání. Reality first.
**Klasifikace:** Interní, zdroj pravdy pro LLM agenty i autora
**Provenance:** Aktualizováno z live GitHub API auditu (2026-08-06) + původní v1.0 (2026-06-25)

---

## ČÁST 1: Autorův profil

### 1.1 Identita

| Atribut | Hodnota |
| - | - |
| **Jméno** | Ondřej Soušek |
| **Věk / zkušenost** | 14 let v průmyslové výrobě a CNC (2010–2024), 2 roky development (2025–2026) |
| **Právní forma** | OSVČ, IČO |
| **Doména** | systeq.cz |
| **GitHub** | github.com/outpost2026 |
| **Email** | sousek@systeq.cz |
| **Telefon** | +420 735 045 256 |
| **Lokalita** | Praha 8 – Dolní Chabry |
| **Bydlení** | Off-grid (FVE 1,9 kWp, LiFePO4 630 Ah) |
| **Životní náklady** | ~15 000 Kč/měsíc |


### 1.2 Positioning

**Není:** Programátor, software engineer, web developer, IT specialista.

**Je:** Systémový integrátor — formalizace tacitních znalostí, reverzní inženýrství proprietárních formátů, převod implicitních procesů na explicitní datové modely.

Programování je nástroj, ne cíl.

### 1.3 CV — klíčová narativní linie

```
CNC dílna (2010–2024) → 14 let praxe ve výrobě
    ↓
Python autodidakt (2025) → samostudium, první skripty
    ↓
VCF parser (03-06/2026) → 22 iterací, >99.98% přesnost, GCP Cloud Run
    ↓
B2B pivot (06/2026) → SYSTEQ, Moodpasta, první reference
    ↓
MCP ekosystém (07-08/2026) → 3 veřejné servery, agentic workflow, CI/CD
```

### 1.4 Vývojová trajektorie (03-08/2026)

První GitHub commit: **03/2026**. Během 5 měsíců:

| Měsíc | Milník |
| - | - |
| **03/2026** | První GitHub commit. Začátek Python autodidakt. |
| **04/2026** | Reverzní inženýrství VCF formátu. První verze parseru. |
| **05/2026** | Stínování v Moodpastě (12.-22.5.). VCF parser v10+. NDA jednání. |
| **06/2026** | VCF parser v23. Streamlit dashboard. DXF engine v2.3. B2B jednání s Františkem. Cenová nabídka. |
| **07/2026** | MCP servery (linkedin, lichess, jobs). CI/CD implementace. Vcf-compiler. |
| **08/2026** | Portfolio audit: 14+ veřejných repů, ~600+ commitů, 3 MCP servery. |


**Tempo:** 0 → 14+ veřejných repů + 3 MCP servery za ~5 měsíců. ~600+ commitů.


## ČÁST 2: Skills set / Stack

### 2.1 Doloženo GitHubem (produkční úroveň)

| Skill | Důkaz | Level |
| - | - | - |
| **Python 3.11/3.12** | 14+ repozitářů, 2 produkční parsery, 3 MCP servery | Expert |
| **Reverzní inženýrství** | VCF binární formát, 29 dní, 22 iterací, IEEE 754 | Expert |
| **GCP Cloud** | Cloud Run, Firestore, Scheduler, Artifact Registry, 6 služeb | Produkční |
| **Docker** | python:3.11-slim → GCP Cloud Run | Produkční |
| **Streamlit** | VCF parser dashboard (GCP Cloud Run) | Produkční |
| **Golden Master Testing** | 10+ testů, baseline JSON diff, determinism testy | Expert |
| **LLM multi-model orchestrace** | 5 modelů, handoff JSON, OpenCode CLI | Expert |
| **IoT/ESP32** | Outpost-security-perimeter, van-peugeot-offgrid, PIR, Doppler, low-power | Produkční |
| **ELT/Data Pipeline** | Meteo miner, scraping, RAG pipeline | Produkční |
| **Google Apps Script** | VCF → Google Sheets pipeline | Produkční |
| **MCP server development** | 3 veřejné servery (linkedin, lichess, jobs), FastMCP framework | Produkční |
| **CI/CD (GitHub Actions)** | README: "Actions, CodeQL, Dependabot" — deklarováno, přítomno v repozitářích | Deklarovaný |
| **DevSecOps** | README: "CI/CD & DevSecOps" — CodeQL security scanning | Deklarovaný |
| **CNC→ML pipeline** | CNC_2_LLM: DXF→ERP, 8 open issues, ML feature vektory (55+ featů) | Produkční |
| **B2B product packaging** | Vcf-compiler: 13 topics, MIT license, proper README | Produkční |
| **Web development** | Systeq.cz_dev (Hugo/HTML), van-peugeot-offgrid | Základní |


### 2.2 Doloženo CV, nedoloženo GitHubem (ale deklarováno)

| Skill | Stav |
| - | - |
| **Playwright** | Známý, používaný pro scraping — není v public repu |
| **Flask REST API** | Deklarováno pro ERP integraci — private repo |
| **BeautifulSoup** | Meteo miner — pravděpodobně používá |


### 2.3 Gapy (potvrzeno chybí)

| Skill | Důležitost | Čas na zacelení |
| - | - | - |
| TypeScript / JavaScript | Vysoká (2× výskyt v nabídkách) | 15-25 h |
| Kubernetes | Střední (3× výskyt) | 40+ h |
| PLC (Siemens/Rockwell) | Střední (3× výskyt) | 40-60 h |
| Azure (AZ-900) | Střední (4× výskyt) | 10-15 h |

### 2.4 Nové dovednosti (zjištěné z GitHub auditu 2026-08-06)

| Kompetence | Důkaz | Level |
|-----------|-------|:-----:|
| **MCP server development** | 3 veřejné servery (linkedin, lichess, jobs) — FastMCP | Produkční |
| **CI/CD (GitHub Actions)** | README: "Actions, CodeQL, Dependabot" | Deklarovaný |
| **DevSecOps** | CodeQL security scanning v README | Deklarovaný |
| **CNC→ML pipeline** | CNC_2_LLM: DXF→ERP, 8 open issues | Produkční |
| **B2B product packaging** | Vcf-compiler: topics, license, discussions | Produkční |
| **Web development** | Systeq.cz_dev, van-peugeot-offgrid | Základní |


### 2.5 Doménová znalost (nedigitální, ale reálná)

- CNC obrábění (vodní paprsek, oscilační nůž, frézování)

- CAM software (VCutWorks, LightBurn, NCstudio 10)

- G-code, DXF pipeline, CAM palety (barevná divergence)

- Materiály: PET felt, dřevo, kov, akrylát

- Off-grid energetika: FVE, LiFePO4 BMS


## ČÁST 3: Kontext Moodpasta

### 3.1 Klient

| Atribut | Hodnota |
| - | - |
| **Firma** | Moodpasta s.r.o. (Wwynwood s.r.o.) |
| **Produkt** | Akustické a designové panely z PET feltu |
| **Obrat 2026** | ~50 000 000 Kč |
| **Cíl 2027** | ~100 000 000 Kč |
| **Lokalita** | Praha 9 – Na Harfě, výroba za Prahou |
| **Zaměstnanci** | ~20 |
| **CNC stroj** | Plotr s Ruida/VCutWorks controllerem |


### 3.2 Zástupci

| Osoba | Role | Vztah k projektu |
| - | - | - |
| **Tomáš Kučva** | CEO / jednatel | Právní rámec, exkluzivita, kompenzace. Kontakt iniciován autorem 25.5. |
| **František Sehnal** | Technický manažer | Technické zadání, specifikace modulů, cenová nabídka. Hlavní protějšek od 4.6. |
| **Jakub** | (Grafik, Projektový manažer) | Účast na první schůzce 4.6. |
| **Karel Pruška** | Hlavní technolog | Gatekeeper tacitních znalostí, obsluha CNC. Autor u něj stínoval 12.-22.5. |


### 3.3 Historie kontaktu

| Datum | Událost |
| - | - |
| **Duben 2026** | Autor nastupuje do Moodpasty jako CNC operátor |
| **12.-22.5.2026** | Stínování u Karla. Autor získává přístup k VCF souborům se souhlasem Karla. Začíná RE. |
| **25.5.2026** | Autor posílá CEO první email: VCF parser + dokumentace. |
| **26.5.2026** | CEO reaguje pozitivně, zajímá se. Autor posílá prototyp GSheets integrace. |
| **2.6.2026** | Autor posílá znalostní korpus + oznamuje DXF pre-processor. CEO propojuje na Františka. |
| **4.6.2026** | První schůzka s Františkem + Jakubem (2 h). Domluva: technická specifikace do 19.6. |
| **5.6.2026** | Autor posílá shrnutí schůzky. |
| **8.6.2026** | CEO posílá NDA draft s výhradní licencí + nabídka 10 000 Kč kompenzace. |
| **9.6.2026** | Autor posílá counter-proposal: standardní NDA, nevýhradní licence, reference. |
| **12.6.2026** | Autor posílá Jakubovi demo v23 URL (bez reakce). |
| **16.6.2026** | Autor posílá CEO + Františkovi: VCF QC demo + DXF pre-processor stav (bez reakce). |
| **19.6.2026** | CEO píše: nesouhlas s využitím dat, požaduje exkluzivitu. Autor: "dejme si týden." |
| **19.6.2026** (90 min později) | František: "mohli bychom si v pondělí zavolat?" — technický call. |
| **22.6.2026** | Call František + autor (30 min). František specifikuje 3 moduly. |
| **22.6.2026** (večer) | František posílá Technicke_zadani_Parser_Ondra_Sousek.docx.pdf (6 stran). |
| **23.6.2026** | Autor posílá RAG chatbot prototyp (NotebookLM). |
| **25.6.2026** | Čeká na cenovou nabídku. |
| **28.6.2026** | Executive summary v2.1 odeslána Františkovi. |
| **7.7.2026** | Follow-up plán. |


### 3.4 Sémantické shrnutí komunikace

**CEO (Tomáš) linie:**
- Počáteční: nadšený, "parádní struktura nabídky", chce pokračovat
- Právní: požaduje NDA + výhradní licenci + 10 000 Kč kompenzaci
- Eskalace: "využití dat nebylo košer", "bez exkluzivity nemohu mít zájem"
- Aktuální: ultimátum — exkluzivita nebo konec

**František linie:**
- Technická: specifikuje požadavky, posílá zadání, chce cenovou nabídku
- Pragmatická: odděluje techniku od práv (22.6.)
- Aktuální: čeká na cenovou nabídku, poté další kolo

**Autorova linie:**
- Iniciativní: nečeká na zadání, sám vyvíjí (VCF, DXF, GSheets, chatbot)
- Obranná (právní): "data použita se souhlasem", "IP je moje", nabízí kompromis
- Pragmatická: odděluje technický development od právního jednání

**Klíčový nedořešený bod: Exkluzivita**
- CEO: "jakýkoli nástroj pracující s VCF soubory a CNC cutterem našeho typu musí být předmětem exkluzivity"
- Autor: ochoten akceptovat pro VCF a daný stroj, ne pro DXF obecně


## ČÁST 4: Současné portfolio — co je hotovo a co se vyvíjí

### 4.1 VCF Parser (v23) — ✅ PRODUKČNÍ MVP

| Atribut | Hodnota |
| - | - |
| **Verze** | v23 |
| **Stav** | Stabilní, 8/8 testů OK, 2/2 determinism testy OK |
| **Přesnost** | >99.98 % extrakce délky dráhy |
| **Deployment** | GCP Cloud Run (Docker, Artifact Registry) |
| **Demo URL** | vcf-parser-demo-537446704644.europe-west1.run.app |
| **Frontend** | Streamlit dashboard (2 role: Obchodní + Dílna/CNC) |
| **Engine** | Deterministický, izolovaný od UI |

**Funkce:**
- Extrakce: geometrie, vrstvy, nástroje, rychlosti, hloubky H1/H2
- QC modul: detekce 20+ typů defektů (Třída A/B/C, priorita P0-P4)
- 2D vizualizace s overlay defektů
- Kalkulátor marží + Odoo CSV export
- Layer Card (nástroje per vrstva)
- Risk score (sémantický, 0-15)

### 4.2 DXF Engine (v2.3 beta) — ⚠️ ROZPRACOVÁNO

| Atribut | Hodnota |
| - | - |
| **Verze** | v2.3 beta |
| **Stav** | Deterministický parser hotový, topologická sanace chybí |
| **Hotovo** | ACI barevný mapping, V-slot double-pass model, ML feature vektor (55+ featů) |
| **Chybí** | Topologická sanace, modularizace pro cloud, kalibrace na datech |

### 4.3 Vcf-compiler — ✅ R&D (READ-ONLY + WRITE)

| Atribut | Hodnota |
| - | - |
| **Stav** | Produkční read + write (DXF→VCF kompilace) |
| **Commits** | 414 (nejaktivnější repo v portfoliu) |
| **Topics** | 13 (včetně "cnc-controller", "dxf", "cam", "vcf") |
| **License** | MIT |
| **RE nástroje** | 5 vlastních (decode_subtype_bits, dissect_footers, atd.) |

### 4.4 MCP Ecosystem — ✅ PRODUKČNÍ (3 servery)

| Server | Repo | Tools | Stack | Stav |
|--------|------|-------|-------|------|
| **linkedin-analyzer** | linkedin-mcp-custom | 8 nástrojů | FastMCP, Playwright | ✅ Produkční |
| **lichess-analyzer** | lichess-analyzer-mcp | 8 nástrojů | FastMCP, Stockfish | ✅ Produkční |
| **mcp-jobs** | MCP-Jobs | 5 nástrojů | FastMCP, 4 portály | ✅ Produkční |

### 4.5 GitHub repozitáře (14 veřejných + 1 private)

| # | Repo | Jazyk | Velikost | Push | Stav |
|:-:|------|:-----:|:--------:|:----:|:----:|
| 1 | **Vcf-compiler** | Python | 8.7 MB | 2.8 | ✅ Aktivní, pinned |
| 2 | **Kazuistiky-LLM-sprint** | Python | 15 MB | 2.8 | ✅ Aktivní, pinned |
| 3 | **outpost2026** (profile) | — | 100 KB | 2.8 | ✅ Aktivní, pinned |
| 4 | **CNC_2_LLM** | Python | 2.7 MB | 2.8 | ✅ Aktivní, 8 open issues |
| 5 | **linkedin-mcp-analyzer** | Python | 638 KB | 2.8 | ✅ Featured project |
| 6 | **lichess-mcp-analyzer** | Python | 969 KB | 3.8 | ✅ Aktivní |
| 7 | **MCP-Jobs** | Python | 408 KB | 1.8 | ✅ Aktivní |
| 8 | **B2B-Knowledge-Base** | — | 1 MB | 3.8 | ✅ Aktivní |
| 9 | **Systeq.cz_dev** | HTML | 5.8 MB | 1.8 | ✅ Aktivní |
| 10 | **vcf_color_service** | Python | 35 KB | 30.7 | ✅ Aktivní |
| 11 | **Outpost-security-perimeter** | — | 214 KB | 5.8 | ✅ Aktivní, Apache 2.0 |
| 12 | **van-peugeot-offgrid** | HTML | 63 KB | 8.7 | ✅ Aktivní |
| 13 | **cad2llm** | — | — | — | ⚠️ POC/archiv |
| 14 | **RAG-indexer** | — | — | — | ⚠️ POC/archiv |
| — | **mcp-local-server** | — | — | — | 🔒 Private |
| — | **vcut-parser** | — | — | — | ⚠️ POC/archiv |
| — | **Vcutworks-vcf-parser** | — | — | — | ❌ **404 (smazán/private)** |

### 4.6 SYSTEQ web (systeq.cz)

| Komponenta | Stav |
| - | - |
| Landing page (`src/index.html`) | Produkční — B2B landing s API docs |
| Three.js demo (`systeq_v3.html`) | Produkční — 4-fázový entropy-to-order narativ |
| Music page (`music.html`) | Produkční — Ateliér múz |
| Streamlit dashboard (GCP) | Produkční — VCF parser demo |
| Live API endpoint | ❌ **Chybí** — data jsou embedovaná |
| Sekce Reference | ❌ **Chybí** — po Moodpastě bude |

### 4.7 Autorův GitHub README

Autorův profilový README obsahuje:
- **Pinned repos:** Vcf-compiler, Kazuistiky-LLM-sprint, outpost2026
- **Featured project:** linkedin-mcp-analyzer (s EROI scoring modelem)
- **Skills sekce:** 8 kategorií (RE, CNC/CAM, Python, Deterministic, RPA, CI/CD, MCP, Cloud)
- **Trajektorie:** 2020→2026 s milníky
- **Manifest:** "Osel, geometrie a konsolidace" (PDF)
- **R&D sekce:** Brain essay + audio
- **RE metodologie:** 6-fázový proces

**Verdikt:** Profil není junior profil. Je to profil systémového integrátora s hotovými produkty, metodologií a diferenciací.



## ČÁST 5: Zadání projektu — realistický souhrn

### 5.1 Co klient skutečně potřebuje

Klient (Moodpasta) má jeden konkrétní problém: **bus factor = 1** (Karel). Když Karel není, výroba stojí nebo dělá chyby.

Klient nepotřebuje "AI platformu" nebo "digitální transformaci". Potřebuje:

1. Vědět, jak dlouho bude zakázka trvat (pro nacenění a plánování)

2. Automaticky archivovat data z výroby (bez ručního přepisu)

3. Snížit závislost na Karlovi

### 5.2 Co klient požaduje (technické zadání — 5 modulů)

| ID | Název | Popis | Cena (doporučeno) | Stav u autora |
| - | - | - | - | - |
| **A** | VCF Engine API | Python balíček pro extrakci dat z .VCF | 10 000 Kč | **85 % hotovo** |
| **B-A** | ETL lokální (.exe) | File watcher → parser → Google Sheets na Karlově PC | 15 000 Kč | 30 % hotovo |
| **B-B** | ETL cloud (GCP) | Totéž jako B-A, ale v Moodpasta GCP | 18 000 Kč | 20 % hotovo |
| **C1** | DXF Inference Engine | Expertní systém odhadu času z DXF geometrie | 55 000 Kč | 15 % hotovo |
| **C2** | DXF Web UI | Streamlit dashboard pro obchodníky | 18 000 Kč | 40 % hotovo |


### 5.3 Co je reálné dodat

**Fáze 1 (43 000 Kč, dodání do 3 týdnů):**
- Modul A: 1 týden
- Modul B-A: 2 týdny (paralelně s A)
- Modul C2: 2-3 týdny (paralelně s A+B)

**Fáze 2 (55 000 Kč, odhad 4-6 týdnů po kalibraci):**
- Modul C1: závisí na přístupu k datům (100-200 párů DXF/VCF)

### 5.4 Technická rizika

| Riziko | Pravděpodobnost | Dopad |
| - | - | - |
| C1 (DXF inference) je výzkumná úloha, ne parser | 100 % | Vysoký |
| Kalibrace vyžaduje 100-200 párů dat | Střední | Vysoký |
| .exe kompilace (PyInstaller) selže | Nízká | Střední |
| CEO zablokuje deal kvůli exkluzivitě | Střední | Kritický |



## ČÁST 6: Finanční realita

### 6.1 Autorova ekonomika

| Položka | Kč/měsíc |
| - | - |
| Životní náklady | ~15 000 |
| Cloud náklady (GCP) | ~500-1 000 |
| Vývojová investice (03-08/2026) | ~540 000+ Kč (vlastní čas) |
| Příjem z developmentu | **0 Kč** |
| Doba do vyčerpání rezerv | ~6-12 měsíců |


### 6.2 Doporučená cenová nabídka

**43 000 Kč fixně za Fázi 1 (A + B-A + C2)**

- Ekvivalent ~60 h × 700 Kč/h

- Referenční hodnota první B2B zakázky: ~200 000 - 500 000 Kč

- Návratnost pro klienta: 1-2 měsíce (při roční úspoře 1-2.2M Kč)

### 6.3 Co se stane, když Moodpasta nevyjde

| Scénář | Pravděpodobnost | Dopad |
| - | - | - |
| CEO zablokuje (exkluzivita) | 40 % | Střední — ztráta času na jednání, ale engine zůstává |
| Klient akceptuje nabídku | 40 % | První reference + cashflow |
| Klient oddaluje rozhodnutí | 20 % | Pasivní čekání, nutnost diverzifikovat |

**BATNA (Best Alternative To Negotiated Agreement):**
- Publikovat RE metodiku jako open-source (LinkedIn článek + GitHub)
- Aplikovat na follow leade (Desoutter #003, Siemens #007)
- Freelance B2B projekty (MCP tooling jako diferenciace)
- Pokračovat v LinkedIn optimalizaci


## ČÁST 7: Revidované EROI nových dovedností (z GitHub auditu 2026-08-06)

| Nová dovednost | EROI | Čas | Dopad |
|---------------|:----:|:---:|:-----:|
| MCP jako B2B produkt | ⭐⭐⭐⭐⭐ | 0 h (hotový) | Diferenciace |
| CI/CD (GitHub Actions) | ⭐⭐⭐⭐ | 5–8 h (dopsat YAML) | Profesionalizace |
| TypeScript | ⭐⭐⭐⭐ | 15–20 h | Odemčení rolí |
| AZ-900 | ⭐⭐⭐⭐ | 10–15 h | Gatekeeper |
| PLC | ⭐⭐⭐ | 40–60 h | Industrial fit |
| CV/YOLO11 | ⭐ | 25 h | 0% tržní dopad |


## Metadata dokumentu

| Atribut | Hodnota |
| - | - |
| **Verze** | 2.0 |
| **Datum** | 2026-08-06 |
| **Autor** | Ondřej Soušek (SYSTEQ) |
| **Klasifikace** | Interní, zdroj pravdy |
| **Umístění** | B2B-Knowledge-Base/00_STRATEGIE/00_manifesty/ |
| **Zdroje** | Live GitHub API audit (2026-08-06), Korekce_vektoru_rozvoje_OS.json, CV redesign, portfolio audit, emaily, technické zadání |
| **Předchůdce** | GROUND_TRUTH_aktualni_stav_2026-06-25.md (v1.0) |
| **Provenance** | Live GitHub API audit, ověřeno proti skutečnému stavu repozitářů |



*Tento dokument je deterministický snapshot k 6.8.2026. Při každé změně stavu vytvořit novou verzi.*
