# Market Research — Konvertovatelnost současného stacku

**Verze:** 1.0 | **Datum:** 2026-06-28
**Účel:** Identifikace reálných českých výrobních SME firem, kde lze aplikovat existující stack autora (VCF parser, KB engine, Streamlit, GCP, golden master testy)
**Klasifikace:** INTERNÍ

---

## 1. Autorův stack — co lze konvertovat

| Vrstva | Technologie | Kam konvertovat |
|--------|-------------|-----------------|
| **Binární parser** | VCF parser v20 (Ruida VCutWorks) | Jakýkoliv CNC formát (G-code, DXF, HPGL, ENG, PLT) |
| **Knowledge Base engine** | Pravidla + ontologie + confidence scoring | Libovolná výrobní doména (waterjet, laser, frézování) |
| **Golden Master testy** | pytest, determinism, regression | Jakýkoliv parser — ověření konzistence |
| **Dashboard** | Streamlit + matplotlib + HUD/MFD architektura | Reporting pro libovolnou technologii |
| **Deploy** | Docker + GCP Cloud Run | Univerzální |
| **ERP export** | Odoo CSV/JSON | Univerzální |

---

## 2. Segment A — Vodní paprsek (WIL primary target)

**Technologie:** NCStudio V10 / G-code / proprietary control systems
**Stack fit:** ✅ NC parser + KB engine + time/cost prediction
**Velikost trhu v ČR:** ~30+ firem s waterjet technologií

### 2.1 Katalog firem

| Firma | Lokalita | Strojů | Zam. | Specifika | Stack fit | Kontakt |
|-------|----------|--------|------|-----------|-----------|---------|
| **AWAC** | Praha, Brno, Plzeň | 10+ | 50+ | 35 let, 3 provozy, 2D+3D, do 250mm | ✅ Vysoký — 1500+ zakázek/měsíc, CRP | rezarna.praha@awac.cz |
| **Stellis** | Středočeský | 2-3 | 3 spol. | 30+ let, do 45° úhel, vlastní CNC řídící systém | ⚠️ Mají vlastní vývoj řídícího systému — spíše partnerství | petr.kretik@stellis.cz |
| **Hydroproduct** | Poděbrady | 2 | 60+ | 1994, 2500 m², 4 budovy, CNC + waterjet + svařování | ✅ Velký, různorodý provoz | info@hydroproduct.cz |
| **PTV** | ČR | výrobce | — | Český výrobce waterjet strojů, vlastní software PTV CNC886 | ✅ Partnerství — dodávat jako add-on k jejich strojům | info@ptv.cz |
| **Pharmix** | Kroměříž | 2 | — | 2000-2024, 2 stroje, do 180mm, ±0.2mm | ✅ Střední, vhodné pro PoC | pharmix@pharmix.cz |
| **JAPS Elements** | Horoměřice | 4 | 10-20 | **BÝVALÝ ZAMĚSTNAVATEL**, 1500+ zakázek/rok, 20+ let | ✅✅ Ideální — insider knowledge | pistulka@japselements.cz |
| **GUMEX** | ČR | — | — | Hadice + těsnění + waterjet + plotr | ✅ Hybrid — waterjet + plotr = dva stacky najednou | info@gumex.cz |
| **Feropol** | ČR | — | — | Metalurgie, neželezné kovy, CNC obrábění | ✅ | info@feropol.cz |
| **3S Design** | ČR | — | — | Waterjet do 280mm | ✅ | info@3sdesign.cz |
| **JAMA Kovo** | ČR | — | — | Waterjet + laser + ohraňování + svařování | ✅ Multitechnologie | info@jamakovo.cz |
| **Kamenictví Oškrdal** | ČR | FLOW | — | Kámen, náhrobky, FLOW waterjet | ⚠️ Malý, kamenná dílna | info@oskrdal.cz |

### 2.2 Odhad tržního potenciálu (waterjet)

| Metrika | Hodnota |
|---------|---------|
| Počet waterjet firem v ČR | ~23-30 (Firmy.cz + rešerše) |
| Průměrná velikost | 5-20 zaměstnanců |
| Roční obrat typické firmy | 5-30 mil. Kč |
| Cena modulu WIL | 30-50 000 Kč (jako Modul B) |
| Celkový adresný trh (TAM) | 10-15 firem (reálně ochotných koupit) |
| **Potenciál TAM** | **300-750 000 Kč** (bez opakovaných příjmů) |

---

## 3. Segment B — Oscilační nůž / Ruida VCutWorks (primary VCF target)

**Technologie:** Ruida RDD6584G / VCutWorks / VCF formát
**Stack fit:** ✅✅ Přímý — kompletní VCF parser stack
**Velikost trhu v ČR:** ~20+ firem

### 3.1 Katalog firem

| Firma | Lokalita | Specializace | Stack fit | Poznámka |
|-------|----------|-------------|-----------|----------|
| **Moodpasta** (Wynwood) | Praha | PET felt, reklamní předměty | ✅✅✅ **AKTUÁLNÍ B2B** | ~50M obrat, 3 lasery + oscilační nůž |
| **Kimla Czech** | ČR (výrobce) | Univerzální CNC plotry + frézy | ✅ Partner | Výrobce strojů, 2 kontakty (Bergmann, Suchánek) |
| **Raptor Technologies** | ČR (výrobce) | CNC plotry, lasery, plazma, routery | ✅ Partner | Český výrobce, možný reseller |
| **CNC Konečný** | Boršice u Buchlovic | Multifunkční CNC plotry | ✅ Partner | Vlastní My CNC systém, DXF/ISO/HPGL |
| **4cut** | ČR | LECTRA, Zund, KIMLA — servis + prodej | ✅✅ Partner | 20 let zkušeností, průmyslová řešení |
| **Proficut** (AccTek AKZ) | Dovozce ČR | Oscilační nože, kůže, textile | ✅ | Mají Ruida kontrolér |
| **RDI** | Brandýs nad Labem | CNC stroje + 3D laser + nástroje | ✅ | Možný reseller |

### 3.2 Odhad tržního potenciálu (Ruida/VCutWorks)

| Metrika | Hodnota |
|---------|---------|
| Počet firem v ČR s Ruida/VCF | ~15-25 |
| Cena modulu VCF parser (B2B) | 30-50 000 Kč |
| Cena implementace + customizace | 15-30 000 Kč |
| **Potenciál TAM** | **~600-1 500 000 Kč** |

---

## 4. Segment C — Textil / kůže / obalový materiál

**Technologie:** Různé (Ruida, LECTRA, Zund, vlastní)
**Stack fit:** ⚠️ Částečný — parsování formátů, KB engine
**Velikost trhu:** ~50+ firem (textil, obaly, automotive interiors)

### 4.1 Klíčoví hráči

| Firma | Specializace | Stack fit | Poznámka |
|-------|-------------|-----------|----------|
| **Prestar** | Textilní nůžky, automatické řezání | ⚠️ | Vlastní SW, export dat |
| **Böhm + partner** | Kůže, obuv, automotive | ⚠️ | Zund / Lectra systémy |
| **Automet** | Textil, technické textile | ⚠️ | Spíše výrobce než uživatel |

**Poznámka:** Tyto firmy často používají LECTRA nebo Zund — uzavřené ekosystémy. Synergie je nižší.

---

## 5. Segment D — Laserové řezání

**Technologie:** CO2 / Fiber laser, vlastní řídící systémy
**Stack fit:** 🟡 Střední — parsování G-kódu, time prediction, KB

### 5.1 Klíčoví hráči

| Firma | Specializace | Stack fit |
|-------|-------------|-----------|
| **Vanad** | Český výrobce laserů (BLUESTER, KOMPAKT, PROXIMA) | ✅ Partner — otevřený B&R Automation systém |
| **CNCWorld** | Prodejce CO2 + fiber laserů | ⚠️ Dealer, ne výrobce |

**Poznámka:** Vanad má otevřený řídící systém (B&R Automation) — teoreticky nejlepší partner pro integraci.

---

## 6. Segment E — ERP / MES / Industry 4.0 (konkurence)

**Poznámka:** Toto není cílová skupina, ale konkurence, která řeší PODOBNÝ problém (sběr výrobních dat, formalizace znalostí).

### 6.1 Konkurenční mapa

| Firma | Produkt | Cena | Srovnání se SYSTEQ |
|-------|---------|------|-------------------|
| **AutoERP** | Výrobní ERP + MES | 3 450 Kč/měsíc | Široký ERP, ne specializovaný na CAM |
| **Pharis** | MES (Express/Professional/Ultimate) | neuvedeno | Monitoring výroby, ne parser formátů |
| **Apptive MES** | MIS / výrobní informační systém | neuvedeno | Monitoring OEE, napojení na ERP |
| **Euklio** (Netajo) | Propojení strojů s ERP | neuvedeno | **NEJBLIŽŠÍ KONKURENT** — 14 let, PLC→ERP |
| **bm25 labs** | Industrial Troubleshooter (AI KB) | neuvedeno | **NEJBLIŽŠÍ TECHNOLOGIÍ** — agentic RAG, fault resolution |
| **SEMA** | Chytré štítky s návody | neuvedeno | Řeší přenos znalostí, ne technickou automatizaci |
| **DPS Software** | NC Shop Floor Programmer (cloud CAM) | neuvedeno | Cloudové CAM, ne ETL/KB |

### 6.2 Euklio — nejbližší konkurent

- **Co dělá:** Propojuje stroje (PLC, CNC, roboty) s ERP. Data tečou automaticky.
- **Technologie:** OPC-UA, Siemens S7, Omron, Beckhoff, Fanuc, Modbus, MQTT
- **Typ zákazníka:** Výrobní firmy, které chtějí data ze strojů do ERP
- **Cena:** Neuvedena, ale B2B
- **Klíčový rozdíl oproti SYSTEQ:** Euklio řeší konektivitu stroj→ERP, SYSTEQ řeší sémantické porozumění CNC formátům + knowledge base. Euklio je "pipe", SYSTEQ je "translator + brain".

### 6.3 bm25 labs — nejbližší technologie

- **Co dělá:** Agentic RAG pipeline pro industriální troubleshooting. Zpracovává PLC kód, manuály, schémata. Operátor se ptá přirozeným jazykem.
- **Technologie:** Agentic RAG, lokální modely, PLC data
- **Klíčový rozdíl:** bm25 řeší troubleshooting (reaktivní), SYSTEQ řeší formalizaci tacitních znalostí a optimalizaci (proaktivní). bm25 je "co je špatně", SYSTEQ je "jak to udělat lépe".

---

## 7. Syntéza — prioritní targety

### 7.1 Scorecard

| Firma | Stack fit | Pravděpodobnost | Výnos | Celkem | Priorita |
|-------|-----------|-----------------|-------|--------|----------|
| JAPS Elements (waterjet) | 10/10 | 70 % | 30-50k | **VYSOKÁ** | 🥇 |
| PTV (výrobce waterjet) | 9/10 | 40 % | partnerství | **VYSOKÁ** | 🥇 |
| AWAC (waterjet, 3 provozy) | 8/10 | 30 % | 50-100k | **VYSOKÁ** | 🥇 |
| Moodpasta (aktuální B2B) | 10/10 | 50 % | 70k Phase 1 | **AKTUÁLNÍ** | 🥇 |
| Hydroproduct (waterjet + CNC) | 8/10 | 30 % | 30-50k | STŘEDNÍ | 🥈 |
| Vanad (laser výrobce) | 7/10 | 20 % | partnerství | STŘEDNÍ | 🥈 |
| 4cut (servis + prodej) | 9/10 | 20 % | reselling | STŘEDNÍ | 🥈 |
| Stellis (waterjet + vlastní vývoj) | 6/10 | 20 % | 30-50k | NÍZKÁ | 🥉 |
| Pharmix (waterjet, 2 stroje) | 7/10 | 40 % | 20-30k | NÍZKÁ | 🥉 |
| Kimla Czech (výrobce plotrů) | 8/10 | 10 % | partnerství | NÍZKÁ | 🥉 |

### 7.2 Doporučená sekvence

**Fáze 1 — Teď (čekání na Moodpastu):**
- Udělat PoC s JAPS (bývalý kontakt, insider knowledge)
- Cíl: 1 měsíc zdarma → data → případová studie

**Fáze 2 — Po Moodpastě (3-6 měsíců):**
- AWAC — největší waterjet operace v ČR, 3 provozy
- PTV — partnerství pro add-on k jejich strojům

**Fáze 3 — Škálování (6-12 měsíců):**
- 4cut jako reseller (mají kontakty v obalu, textile, automotive)
- Vanad jako OEM partner

---

## 8. Závěr

| Metrika | Hodnota |
|---------|---------|
| Identifikovaných firem celkem | ~35 |
| Prioritních (score ≥ 8) | 6 |
| TAM odhad (reálný, první 2 roky) | 1-2 mil. Kč |
| Průměrná cena modulu | 30-50 000 Kč |
| Konkurence v přímém prostoru | **0** (nikdo neřeší RE CNC formátů + KB) |
| Konkurence v blízkém prostoru | Euklio (konektivita), bm25 labs (AI troubleshooting) |

**Klíčové zjištění:** Nikdo v ČR nedělá to co autor — reverzní inženýrství CNC formátů + knowledge base + formalizace tacitních znalostí operátora. Euklio řeší konektivitu (pipe), bm25 řeší troubleshooting (reactive). SYSTEQ řeší sémantické porozumění + optimalizaci (proactive). Trh není přeplněný.

---

## Metadata

| Atribut | Hodnota |
|---------|---------|
| **Verze** | 1.0 |
| **Datum** | 2026-06-28 |
| **Autor** | outpost2026 (LLM-assisted rešerše) |
| **Zdroje** | Firmy.cz, weby firem, NCStudio manuál, Alibaba/Ruida dodavatelé, vědecké publikace |
| **Klasifikace** | INTERNÍ |
| **Umístění** | 00_STRATEGIE/02_karierni_targety/ |
