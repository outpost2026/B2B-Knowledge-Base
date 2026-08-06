# GROUND TRUTH: Aktuální stav autora, projektu Moodpasta & portfolia

**Verze:** 1.0 | **Datum:** 2026-06-25 | **Autor:** Ondřej Soušek (SYSTEQ) **Účel:** Deterministický snapshot současného stavu — profil, vývoj, skills, Moodpasta kontext, portfolio, komunikace, zadání. Reality first. **Klasifikace:** Interní, zdroj pravdy pro LLM agenty i autora


## ČÁST 1: Autorův profil

### 1.1 Identita

| Atribut | Hodnota |
| - | - |
| **Jméno** | Ondřej Soušek |
| **Věk / zkušenost** | 14 let v průmyslové výrobě a CNC (2010–2024), 2 roky development (2025–2026) |
| **Právní forma** | OSVČ, IČO |
| **Doména** | systeq.cz |
| **GitHub** | github.com/outpost2026 |
| **Email** | [sousek@systeq.cz](mailto:sousek@systeq.cz) |
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
VCF parser (03-06/2026) → 22 iterací, \>99.98% přesnost, GCP Cloud Run  
    ↓  
B2B pivot (06/2026) → SYSTEQ, Moodpasta, první reference
```

### 1.4 Vývojová trajektorie (03-06/2026)

První GitHub commit: **03/2026**. Během 4 měsíců:

| Měsíc | Milník |
| - | - |
| **03/2026** | První GitHub commit. Začátek Python autodidakt. |
| **04/2026** | Reverzní inženýrství VCF formátu. První verze parseru. |
| **05/2026** | Stínování v Moodpastě (12.-22.5.). VCF parser v10+. NDA jednání. |
| **06/2026** | VCF parser v23. Streamlit dashboard. DXF engine v2.3. B2B jednání s Františkem. Cenová nabídka. |


**Tempo:** 0 → produkční MVP (VCF parser v23) za ~4 měsíce. 6 repozitářů, 93+ commitů.


## ČÁST 2: Skills set / Stack

### 2.1 Doloženo GitHubem (produkční úroveň)

| Skill | Důkaz | Level |
| - | - | - |
| **Python 3.11/3.12** | 7 repozitářů, 2 produkční parsery | Expert |
| **Reverzní inženýrství** | VCF binární formát, 29 dní, 22 iterací, IEEE 754 | Expert |
| **GCP Cloud** | Cloud Run, Firestore, Scheduler, Artifact Registry, 6 služeb | Produkční |
| **Docker** | python:3.11-slim → GCP Cloud Run | Produkční |
| **Streamlit** | VCF parser dashboard (GCP Cloud Run) | Produkční |
| **Golden Master Testing** | 10 testů, baseline JSON diff, determinism testy | Expert |
| **LLM multi-model orchestrace** | 5 modelů, handoff JSON, OpenCode CLI | Expert |
| **IoT/ESP32** | Security perimeter, PIR, Doppler, low-power | Produkční |
| **ELT/Data Pipeline** | Meteo miner, scraping, RAG pipeline | Produkční |
| **Google Apps Script** | VCF → Google Sheets pipeline | Produkční |


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
| GitHub Actions CI/CD | Střední (chybí v repu) | 10-12 h |
| Kubernetes | Střední (3× výskyt) | 40+ h |
| PLC (Siemens/Rockwell) | Střední (3× výskyt) | 40-60 h |
| Azure (AZ-900) | Střední (4× výskyt) | 10-15 h |


### 2.4 Doménová znalost (nedigitální, ale reálná)

- CNC obrábění (vodní paprsek, oscilační nůž, frézování)

- CAM software (VCutWorks, LightBurn, NCstudio 10)

- G-code, DXF pipeline, CAM palety (barevná divergence)

- Materiály: PET felt, dřevo, kov, akrylát

- Off-grid energetika: FVE, LiFePO4 BMS


## ČÁST 3: Kontext Moodpasta

### 3.1 Klient

| Atribut | Hodnota |
| - | - |
| **Firma** | Moodpasta s.r.o. (Wynwood s.r.o.) |
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
| **Karel Pruška** | Hlavní technolog | Gatekeeper tacitních znalostí, obsluha CNC. Autor u něj stínoval 12.-22.5., ukončena spolupráce s Moodpasta na pozici CNC technolog = autor vyhozen 22.5.2026 = K.Pruška inicioval |


### 3.3 Historie kontaktu

| Datum | Událost |
| - | - |
| **Duben 2026** | Autor nastupuje do Moodpasty jako CNC operátor |
| **12.-22.5.2026** | Stínování u Karla. Autor získává přístup k VCF souborům se souhlasem Karla. Začíná RE. K.Pruška nespokojen, napětí s technologem graduje vyhazovem, CEO: „Karel je důležitý, Autor je příliš chytrý, potřebujeme někoho hloupějšího k plotru a ke Karlovi = implicitně ohrožení statusu hlavního technologa. Autor během posledního rozhovoru s CEO prezentuje výstupy = knowledge korpus tacitních znalostí & VCF parser = CEO zcela překvapen, diskuze 15+ minut. Dohoda o zaslání podrobností |
| **25.5.2026** | Autor posílá CEO první email: VCF parser + dokumentace. |
| **26.5.2026** | CEO reaguje pozitivně, zajímá se. Autor posílá prototyp GSheets integrace. |
| **2.6.2026** | Autor posílá znalostní korpus + oznamuje DXF pre-processor. CEO propojuje na Františka. |
| **4.6.2026** | První schůzka s Františkem + Jakubem (2 h). Domluva: technická specifikace do 19.6. |
| **5.6.2026** | Autor posílá shrnutí schůzky. |
| **8.6.2026** | CEO posílá NDA draft s výhradní licencí + nabídka 10 000 Kč kompenzace. |
| **9.6.2026** | Autor posílá counter-proposal: standardní NDA, nevýhradní licence, reference. |
| **12.6.2026** | Autor posílá Jakubovi demo v23 URL (bez reakce). |
| **16.6.2026** | Autor posílá CEO + Františkovi: VCF QC demo + DXF pre-processor stav (bez reakce). |
| **19.6.2026** | CEO píše: nesouhlas s využitím dat, požaduje exkluzivitu. Autor: "dejme si týden, připravím varianty." CEO: "exkluzivita je podmínka, bez ní nelze pokračovat." |
| **19.6.2026** (90 min později) | František: "mohli bychom si v pondělí zavolat?" — technický call. |
| **22.6.2026** | Call František + autor (30 min). František specifikuje 3 moduly. |
| **22.6.2026** (večer) | František posílá `Technicke\_zadani\_Parser\_Ondra\_Sousek.docx.pdf` (6 stran). |
| **23.6.2026** | Autor posílá RAG chatbot prototyp (NotebookLM). |
| **25.6.2026** | Aktuální stav: Čeká na cenovou nabídku. |


### 3.4 Sémantické shrnutí komunikace

**CEO (Tomáš) linie:**

- Počáteční: nadšený, "parádní struktura nabídky", chce pokračovat

- Právní: požaduje NDA + výhradní licenci + 10 000 Kč kompenzaci

- Eskalace: "využití dat nebylo košer", "bez exkluzivity nemohu mít zájem"

- Aktuální: ultimátum — exkluzivita nebo konec. Tvrdá linie. Žádný prostor pro kompromis.

**František linie:**

- Technická: specifikuje požadavky, posílá zadání, chce cenovou nabídku

- Pragmatická: odděluje techniku od práv (22.6.): "navrhuji obsah hovoru zúžit na technickou rovinu"

- Aktuální: čeká na cenovou nabídku, poté další kolo

**Autorova linie:**

- Iniciativní: nečeká na zadání, sám vyvíjí (VCF, DXF, GSheets, chatbot)

- Obranná (právní): "data použita se souhlasem", "IP je moje", nabízí kompromis

- Pragmatická: odděluje technický development od právního jednání

- Aktuální: připravuje cenovou nabídku, čeká na signál od CEO ohledně exkluzivity

**Klíčový nedořešený bod: Exkluzivita**

- CEO: "jakýkoli nástroj pracující s VCF soubory a CNC cutterem našeho typu musí být předmětem exkluzivity"

- Autor: ochoten akceptovat pro VCF a daný stroj, ne pro DXF obecně

- Stav: visí ve vzduchu. František tlačí techniku, CEO drží právní linii.


## ČÁST 4: Současné portfolio — co je hotovo a co se vyvíjí

### 4.1 VCF Parser (v23) — ✅ PRODUKČNÍ MVP

| Atribut | Hodnota |
| - | - |
| **Verze** | v23 |
| **Stav** | Stabilní, 8/8 testů OK, 2/2 determinism testy OK |
| **Přesnost** | \>99.98 % extrakce délky dráhy |
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


### 4.3 GitHub repozitáře (veřejné i private)

| Repo | Stav | Vizuální |
| - | - | - |
| **vcut-parser** | Private | VCF parser engine (v23) |
| **CNC\_2\_LLM** | Private | DXF engine (v2.3) |
| **cad2llm** | Public | CAD → LLM konvertor |
| **RAG-indexer** | Public | RAG pipeline s deduplikací |
| **web\_integrace\_systeq** | Public | SYSTEQ landing page + Three.js demo |
| **B2B-Knowledge-Base** | Private | Znalostní báze B2B pivotu |


### 4.4 SYSTEQ web (systeq.cz)

| Komponenta | Stav |
| - | - |
| Landing page (`src/index.html`) | Produkční — B2B landing s API docs |
| Three.js demo (`systeq\_v3.html`) | Produkční — 4-fázový entropy-to-order narativ |
| Music page (`music.html`) | Produkční — Ateliér múz |
| Streamlit dashboard (GCP) | Produkční — VCF parser demo |
| Live API endpoint | ❌ **Chybí** — data jsou embedovaná |
| Sekce Reference | ❌ **Chybí** — po Moodpastě bude |



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

### 5.4 Co není v zadání (ale klient si to možná představuje)

- ✅ Není: ML model, umělá inteligence, chatbot

- ✅ Není: Odoo integrace (pouze CSV export)

- ✅ Není: Hosting na straně dodavatele

- ⚠️ Možná: "Aplikace která sama vyřeší naše problémy" — klient si může myslet, že parser vyřeší vše. Realita: parser je nástroj, ne řešení procesních problémů.

### 5.5 Technická rizika

| Riziko | Pravděpodobnost | Dopad |
| - | - | - |
| C1 (DXF inference) je výzkumná úloha, ne parser | 100 % | Vysoký — klient může podcenit náročnost |
| Kalibrace vyžaduje 100-200 párů dat | Střední | Vysoký — bez dat nelze dodat |
| .exe kompilace (PyInstaller) selže | Nízká | Střední |
| CEO zablokuje deal kvůli exkluzivitě | Střední | Kritický |
| Karel odmítne používat .exe | Nízká | Střední |



## ČÁST 6: Finanční realita

### 6.1 Autorova ekonomika

| Položka | Kč/měsíc |
| - | - |
| Životní náklady | ~15 000 |
| Cloud náklady (GCP) | ~500-1 000 |
| Vývojová investice (03-06/2026) | ~480 000 Kč (vlastní čas) |
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

- Aplikovat na follow leade (Desoutter \#003, Siemens \#007)

- Freelance B2B projekty (Toloka \#024)

- Pokračovat v LinkedIn optimalizaci


## Metadata dokumentu

| Atribut | Hodnota |
| - | - |
| **Verze** | 1.0 |
| **Datum** | 2026-06-25 |
| **Autor** | Ondřej Soušek (SYSTEQ) |
| **Klasifikace** | Interní, zdroj pravdy |
| **Umístění** | B2B-Knowledge-Base/00\_STRATEGIE/00\_manifesty/ |
| **Zdroje** | Korekce\_vektoru\_rozvoje\_OS.json, CV redesign, portfolio audit, emaily, technické zadání, 3 preview analýzy, cenová metodika |



*Tento dokument je deterministický snapshot k 25.6.2026. Při každé změně stavu (podpis smlouvy, změna zadání, nový kontakt) vytvořit novou verzi.*

