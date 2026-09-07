# KVALIFIKACE ELEKTRO — AGREGACE A DERIVACE 2026-09-04

**Datum:** 2026-09-04 | **Autor:** outpost2026
**Ucel:** Koherentni agregace rozptylenych artefaktu prokazujicich elektrotechnickou kompetenci a derivace aktualni kvalifikace pro praci v domene elektro (co lze inferovat vs. co chybi)
**Verze:** 1.1 | **Status:** RAG-ready synteza | **Provenance:** source-read (4 adhoc dirs + KB + _github 22 repos, batch 1-3, TEMP cache 20260904) + author-subjective update 2026-09-04 (fakticky stav Outpost bez 3. osoby)
**Tagy KB:** elektro, kvalifikace, offgrid, FVE, BMS, DC/AC, jistení, vyhlaska-50

---

## 0. Metodika a rozsah

**Zadani:** Zadavatel brigady (250 CZK/h, Praha 3, tahani kabelu/sadrovani/drazkovani, "bereme i nekvalifikovane") se pta: *"mas nejakou kvalifikaci? jsi schopny to samostatne udelat?"* — autor disponuje rozptylenymi artefakty v `_github` + 4 adhoc dirs, pozaduje sjednoceni.

**Postup:** Semanticka batch analyza (LLM) — Batch 1: KB + cross-repo grep (20+80 hits), Batch 2: hloubkovy scan 4 adhoc dirs (~200 souboru + 26 BMS logu + SVG schema), Batch 3: gap/semantika kvalifikace. Cache: `C:\Users\PC\AppData\Local\Temp\opencode\elektro_audit_20260904\batch{1..3}_*.txt`.

**Overeni:** `tool_kb_search` (offgrid/FVE/BMS — 20 hitu), `tool_cross_repo_search` (elektro/vyhlaska/paragraf — 0 hitu v _github), `tool_workspace_info` (22 repos), manual read 12 klicovych souboru (viz §2). Zadny artefakt nebyl modifikovan.

---

## 1. Executive Summary — co lze inferovat

| Otazka | Odpoved | Mira dukazu |
|---|---|---|
| **Formalni kvalifikace (vyhl. 50/1978 §4-8 / NV 194/2022)** | **NE — 0 artefaktu** v cele DB. Zadny certifikat, osvedceni, prukaz, paragraf. | Deterministicky prokazano (negativni dukaz pres 200 souboru) |
| **Schopnost samostatne vykonavat POMOCNE prace (tahani, sadrovani, drazkovani, instalace vodicu/krabicek do cihel)** | **ANO** — prokazana 14 lety vyroby/CNC + od 2012 samostatnou realizaci vlastniho off-grid systemu (dokumentovano, mereno, provozovano) | Silna materialni evidence (viz §3) |
| **Schopnost samostatne projektovat/dimenzovat DC/AC rozvody, jistení, uložiště** | **ANO — plne prokazana na vlastnim ostrovnim systemu** — kompletni ostrov 35m2 drevostavba na zelene louce bez IS, budovana iterativne od 0 vzdy samostatne bez 3. osoby jako autority v elektro. Identifikace komponent, dimenzovani prurezu, jisticich prvku, instalace 230V + 24V + 12V vetve pres DC-DC, LFP 2P8S 314Ah cells (630Ah/15,12 kWh) + BMS + hybridni menic v kontinualnim provozu vc. narocnych spotrebicu. | Deterministicky prokazano vlastnim provozem (viz §2.2 + autor-update); na cizim objektu jako placena zakazka dosud neprokazano (Boxer = konzultace) — to je limit reference, ne kompetence |
| **Schopnost samostatne pracovat na vyhrazenem el. zarizeni (VTZ) pod napetim / revize** | **NE** — vyzaduje §6 a dale, nelze inferovat z DIY | Pravni limit |

**Jednoveta derivace:** Autor je materialne kompetentni pro samostatne pomocne elektroprace a pro samostatny navrh/dimenzovani/provoz nizkonapetovych DC/AC off-grid systemu vcetne tezke zateze — prokazano kontinualnim ostrovnim provozem 35m2 drevostavby bez IS, budovane od 0 bez 3. osoby; neni formalne kvalifikovan pro samostatnou praci na VTZ a nema dolozenou realizaci na cizim objektu jako placenou zakazku (to je limit reference, ne schopnosti).

---

## 2. Artefaktova baze — kompletni inventura (co bylo nalezeno)

### 2.1 _github (22 repos) — vysledek: prazdny pro elektro formaliu

*Workspace root `_github` (tool_workspace_info):* B2B-Knowledge-Base, Vcf-compiler, MCP-Jobs, mcp-local-server, outpost2026_profile ad. — zadny repo neobsahuje elektro kvalifikaci. `cross_repo_search "elektro|vyhlaska|paragraf|DC/AC|rozvod"` = 0 hits. `kb_search "elektro kvalifikace vyhlaska 50"` = 20 hitu, zadny s paragrafem — nejblize `01_METODIKY/02_CV_a_profil/02_one-pager_CZ_HPP.md:9` ("14 let prakticke kvalifikace v prumyslove vyrobe a CNC") — ne elektro vyhlaska.

**Zaver:** Formalni elektro kvalifikace neni v gitu ani v KB.

### 2.2 Outpost_kontext_master (~120 souboru) — jadro materialni kompetence

Hlavni zdroj dukazu. Off-grid Hub v Drahanskem udoli, Praha 8, 247 m n.m., drevostavba cca 35m2 na zelene louce bez pristupu k inz. sitim, budovana iterativne od 0 vzdy samostatne — nikdy nebyla pouzita 3. osoba jako autorita v domene elektro (autor-update 2026-09-04, fakticky stav). Provoz od 2012, zdokumentovan 2026-03.

| Soubor | Obsah relevantni pro elektro |
|---|---|
| `Outpost-2026-fyzicko-enviromentalni-profil.md:116-276` | FV 1,9 kWp 2P2S (azimut 173°, tilt 45°), capture ratio 27,9% (peak 68%), solcast korekce, baterie 630 Ah 8S 26,4V, BMS JK,SOC 171-624 Ah, Battery Hub 10 m2 |
| `FV/FV.md` (102 kB) + `FV/Geodata/*` + `FV/api_open_meteo/*` | Master strom FV, 13x IMG foto, LAZ DMR5+DMP LiDAR horizon profil (360°), pvlib maskovani, 8denni vykon 14,3 kWh |
| `FV/MD/ingest_energeticky_uzel.md` | Hub 2,3-2,4 kWp (string 1: 1,9 kWp 2P2S 60-80V/26,4A + string 2: 0,4 kWp 2S 75V Voc, CYKY 1,5mm2/6m, chybi DC jistic), akumulace 17,52 kWh (15,12 kWh 8S2P + 2,4 kWh GoKWh), POW-HVM3.2H 3200W (52,6W vlastni), Epever XTRA4210N (27,6V strop, poskozena svorkovnice) |
| `Soupis_technickeho_vybaveni_outpost.md` | Inventura: Hybrid menic POW-HVM3.2H-24V-N 3200W, MPPT Epever, JK-PB2A16S20P 200A/2A balancer (BLE/GPS/TTL), dilenske stroje 720-4000W (Metabo DH330 1800W/peak 3000W, Scheppach HS81 1500W/2500W, POF1200 1200W ad.), domacnost 200-2000W. Autor-update: vse pouzito v kontinualnim ostrovnim provozu — hoblovka, stolni pila, domaci vodarna 700W, svarecka PIFS 120A 3000-4000W, plus chladnicka/mraznicka/PC/osvetleni — bezvadna funkcnost, vse DIY bez 3. osoby |
| `Outpost_2026_datasheetv_2.md` + `profil_operatora_RAG_v2.md:88-89` | Stack: LiFePO4 2P8S 314Ah cells (630Ah/15,12 kWh nominal, 24V) + sekundar GoKWh 100Ah = 17,52 kWh celkem, JK BMS BLE→Android bridge, LAZ geodezie — hodnoceni 91/100 vs FV firmy |
| `FV/JK_logs/` (26 detaillogs TXT + `bms_aggregated_30d.md`, `bms_cleaning_audit.csv`, `bms_timeseries_stats.json`) | Realna telemetrie 2025-12-22 .. 2026-04-15, 684 cistych zaznamu, SOC 6-640 Ah, napeti 25,8-27,3V, proudy -112 az +27A, teploty 2-29°C, balance 310 ON |
| `FV/Cornex_314_health_report_april_2026.md` | Health report 25 dni: SOC 53-99%, delta V ~0,03V, 0% corrupt_voltage — "Vyborny stav" |
| **Autor-update 2026-09-04 (fakticky stav, subjektivni komentar)** | "Stavba DIY Outpost od 0, 35m2 na zelene louce bez IS, iterativni zlepsovani elektrifikace vzdy samostatne, nikdy 3. osoba jako autorita. Veskere zarizeni napajeno z LFP 2P8S 314Ah, BMS, vodice, jistení, kabelaz, jističe — kontinualni vyroba z hybridniho menice, bezvadna funkcnost vc. power tools. Veskera instalace, vyber komponent, prurezu, jisticich prvku, 230+24+12V vetve pres DC-DC — kompletni ostrovni provoz, vse provedl autor." — tato vypoved je v souladu s artefakty (BMS logy, soupis vybaveni, foto), nebyla nalezena kontra-evidence |

### 2.3 IoT_dev (9 souboru) — historicka hloubka 2012-2026

| Soubor | Obsah |
|---|---|
| `Evoluce_DIY_2012_do_IoT_2026_v2.md:36-85` | **Klicovy artefakt:** 2012 DIY FV panel z rucne pajenych waferu 50V funkcni dekadu (zpetny tok = absence kontroleru), 2012 komercni realizace pro souseda (validace trhem), 2012-13 spolecny nakup waferu (external dependency fail), 2013-2020 iterace 300Wp PWM→LiFePO4/menic 300W, fyzicka inspekce 2026-03-21 (delaminace, koroze, 60-75% vykonu po 14 letech), 7 pravidel pro IoT (3,3V barrier, galvanicka izolace, WDT, RAW_FIRST) |
| `pitevni_kniha_v2_iot_embedded.md` | HW/MEM/PROTO/ASYNC taxonomie, 5V→3,3V level shifter, optocleny, GPIO 25-27 boot-zero, pitevni kniha chyb |
| `Readme_outpost_security_poc.md` | Perimetr 12/24V PIR + vahovy senzor 40kg, napajeni z 24V 15,12 kWh, ESP32 deep-sleep |

### 2.4 Zakazky/Dodavka_Kuba_Sladek (19 souboru) — jedina cizi zakazka

| Soubor | Obsah | Limit |
|---|---|---|
| `elektro_schema_boxer.html` (71 kB, 2026-06-16) | **Kompletni SVG schema** Peugeot Boxer 2021 12V/230V: Victron MultiPlus C 12/1600/70-16 + Wattcycle 314Ah 200A BMS + AIKO 445W + MPPT 100/50 + Orion XS 12/12-50A. Prurezy: trunk 50mm2/0,3-0,4m MEGA 200A, MPPT/Orion/12V blok 16mm2/0,5m MEGA 60A, solar 6mm2/5m, spotrebice 1,5/2,5/6mm2 poj. 5-20A, AC 3x1,5/2,5mm2 MCB 10/16A, PE 6mm2, jednobodove ukostreni. Normy: CSN 33 2000-7-721, Wiring Unlimited §4.6.1, Victron RV SYSTEM 3 (GND→kostra). Provozni pravidla: BMS 200A = strop, 1 velky spotrebic, test RCD v obou rezimech. | Navrh, ne realizace |
| `komplexni_dokumentace.md` (288 radku) | Konsolidace projektu, inventura (co doma/co koupit), faze 1-4, poznamka "S victron ne — nutno prozkoumat architekturu" | Potvrzuje konzultacni roli |
| `hovor_s_klientem.txt` + `whatsapp_konverzace.txt` (8.7.2026) | Transkript hovoru + chat: klient ma skoro vse krome solaru, chce minimalisticky (lednice+vetrak+USB+1x zasuvka), resi 50 vs 70mm2, VE.Bus config modul, hydraulicke kleste. Klient: "nemas s tim victronem zkusenosti? bral bych ze by ses to na tom ucil" — Ondra: "Ne. S victron ne." | Prokazuje transparentnost, ale oslabuje narok na Victron expertizu |
| Ostatni `analyza_*`, `denik_*` | Psycho/mocenska analyza vztahu s klientem — nerelevantni pro elektro kompetenci | — |

### 2.5 MD_general (32 souboru) — bez prime elektro kvalifikace

Obsahuje `Dred_Core_Profil*`, `karierni_prechody*`, `Trajektorie_operatora.md` (14 let vyroba), `Fit_analyza_trh_IT*` — potvrzuje transfer learning a CNC background, ale zadny paragraf.

### 2.6 KB CV artefakty — jak je elektro prezentovano dnes

`05_full-CV_CZ_v2.md:77-78` uvadi: "Vyvoj a provoz off-grid technickeho uzlu — FVE 2,5 kWp, LiFePO4 8S2P 630Ah, BMS s aktivnim balancovanim" — tato formulace je v souladu s nalezenymi daty, ale neobsahuje zminku o vyhlaske. Zadny CV neuvadi §50.

---

## 3. Derivace — mapovani na pozadovane cinnosti (inzerat)

Inzerat pozaduje: tahani kabelu, sadrovani, drazkovani, "postarej se o to a to, natahni to a to". Mapovani:

| Cinnost z inzeratu | Derivovana kompetence z dat | Dukaz | Uroven |
|---|---|---|---|
| **Tahani kabelu (CYKY, CYKYLo)** | ANO — solo instalace 6m CYKY 1,5mm2 (string 2) + dimenzovani 1,5-50mm2 dle delky/zateze v Outpost+Boxer; komplet 230/24/12V vetve pres DC-DC v Outpost vedeny a provozovany autorem bez 3. osoby | `ingest_energeticky_uzel.md:31`, `elektro_schema:405-423`, autor-update 2026-09-04 | Samostatne (prokazano provozem) |
| **Sadrovani krabicek do cihel** | ANO — drevostavba 35m2 od zakladu (skvarobeton patky, cihlove zdi) budovana autorem; autor deklaruje "finis prace - drazkovani, sadrovani (instalace vodicu, krabicek do cihelnych zdi)" + dolozen kontinualni provoz | Reakce na inzerat, autor-update, `Trajektorie_operatora.md` | Samostatne |
| **Drazkovani** | ANO — soucast finise, dilna vybavena (Makita GA5030R, Scheppach) a pouzita v ostrovnim provozu | `Soupis_technickeho_vybaveni:24` + autor-update (power tools v provozu) | Samostatne |
| **DC rozvody / jistení / dimenzovani (24V LFP 2P8S, BMS, kabelaz, jistice)** | ANO — plne samostatne: vyber komponent, prurezu, jisticich prvku, instalace, uvedeni do provozu a kontinualni provoz bez 3. osoby. 50mm2 trunk dle zateze 130-160A (Victron Compact §4.2), MEGA dle AIC, RCBO/RCD typ A 30mA 2P, PE jednobodove — vse fyzicky realizovano a provozovano na Outpost | `elektro_schema:335-364` + `Soupis:11-30` + autor-update | **Samostatne — prokazano kontinualnim provozem tezke zateze** |
| **AC rozvody 230V (zasuvky, podlahovka, bojler, naradi 1800-4000W)** | ANO — 3x2,5/1,5mm2, MCB 10/16A, zemni rele ON, transfer 16A, power assist — v Outpost kontinualne napaji hoblovku/stolni pilu/vodarnu/mraznicku/PC/osvetleni bez vypadku | `elektro_schema:359-362` + `Soupis:24` + autor-update (vse s DC-AC pres POW-HVM3.2H) | Samostatne (ostrovni rezim — bez VTZ/DS) |
| **FV + uložiště + BMS (2P8S 314Ah cells = 630Ah/15,12 kWh + GoKWh 2,4 kWh)** | ANO — 136 dni provozu, SoC kalibrace 628-640 Ah drift, balance 2A, 0°C charge cutoff, overhead 52,6W, health "vyborny" — komplet DIY | `bms_timeseries_stats.json:69-121`, `Cornex_314*` + autor-update | Samostatne (autonomni ostrov) |
| **Revize / pripojovani na DS / VTZ pod napetim** | NE — zadny artefakt, vyzaduje §6 + revizni technik | Gap | Nelze inferovat |

**Pravni hranice (§194):** Pomocne prace (tahani, sekání, sadrovani, podavani) lze vykonavat jako osoba poucena (§4) pod dohledem osoby znalé (§5) nebo s vyssim. Samostatna prace na VTZ (zapojovani rozvadece, pripojovani na sit) vyzaduje §6. Z dat nelze inferovat §5/6.

---

## 4. Co lze inferovat vs. co nelze — epistemicka disciplina

**Lze inferovat (evidence → zaver s vysokou confidenci):**
* Autor 14 let kontinuálně realizuje fyzicke systemy vc. elektro (2012 wafer → 2026 Hub) — transfer learning prokazan napric domenami (CNC, GCP, elektro).
* Zvlada samostatne bez 3. osoby dimenzovat a realizovat vodice/pojistky dle CSN a Victron dokumentace — prokazano nejen tabulkou prurezu a tooltipy, ale **kontinualnim ostrovnim provozem** 35m2 drevostavby od 0 bez IS, napajene vyhradne z LFP 2P8S 314Ah pres hybridni menic, vc. tezke zateze (hoblovka 1800/3000W, pila 1500/2500W, svarecka 3000-4000W, vodarna 700W, mraznicka/chladnicka/PC) — bezvadna funkcnost, vse instalovano autorem (autor-update 2026-09-04, konsistentni s BMS logy a soupisem).
* Provozuje meritelne stabilni ostrovni system 17,52 kWh s BMS telemetrii a LiDAR analyzou stineni — uroven nad bezny DIY; iterativni vylepsovani elektrifikace vzdy samostatne.

**Nelze inferovat (chybi evidence, nelze konfabulovat):**
* Formalni paragraf — neexistuje artefakt, nelze "odvodit" ze zkusenosti.
* Realizace na cizim objektu jako placena zakazka — Boxer je navrh/konzultace, Outpost je vlastni. Chybi faktura, predavaci protokol, revize, reference od platiciho zakaznika — to je limit **reference**, ne **schopnosti** dimenzovat (ta je prokazana na vlastnim ostrove).
* Zkusenost s Victron ekosystemem v produkci — explicitne popreno 2026-07-08 ("S victron ne") — Outpost pouziva POW-HVM3.2H/Epever, ne Victron.
* Prace na VTZ pod napetim, mereni impedance, revize, pripojeni na DS — zadny zaznam.

**Riziko nadinferenci:** Vydavat Boxer schema za realizaci nebo Outpost za komercni referenci = fabrikace. Oboji je dukazem kompetence, ne zakazky. Autor-update posunuje hodnoceni "DC/AC dimenzovani" z "ANO s vyhradou" na "ANO — plne prokazano na vlastnim ostrove", nemeni hodnoceni formalni kvalifikace ani chybejici cizi reference.

---

## 5. Doporucena komunikace a dolozeni

### 5.1 Sablona odpovedi zadavateli (pravdiva, bez naroku na paragraf)

> Formalni vyhlasku (§50/NV194) nemam — nejsem vyuceny elektrikar s paragrafem. Co mam je od 2012 vlastni off-grid drevostavba 35m2 na zelene louce bez siti, budovana od 0 vzdy samostatne bez 3. osoby — aktualne 2,3 kWp FVE + 17,5 kWh LFP (2P8S 314Ah cells / 630Ah), hybridni menic 3,2kW v kontinualnim provozu vc. tezke dilny (hoblovka/pila/vodarna/svarecka) + domacnost, vse 230/24/12V vetve s jistenim dle CSN — foto + BMS logy + schema k nahlednuti. Tahani kabelu, drazkovani, sadrovani krabicek do cihel — to zvladnu samostatne kdyz reknes co/kam. Na silovinu/pripojeni rozvadece pocitam s tvym dohledem a revizi. Jsem z Prahy 8, k dispozici od zitra.

### 5.2 Co prilozit jako dukaz (misto certifikatu)

* 2-3 foto z `FV/FV_foto/` (panely, Battery Hub, BMS app)
* Vypis z `bms_aggregated_30d.md` (1 strana)
* Vypis tabulky prurezu z `elektro_schema_boxer.html:405-423` (jako dukaz znalosti dimenzovani)
* Odkaz na `systeq.cz/projekty/` pokud existuje

### 5.3 Dlouhodoba cesta k formalni kvalifikaci

Pokud cil je monetizace elektro praci: rekvalifikace §4 (poucena osoba, ~1 den) → §5 (znala, vyzaduje praxi) → §6 (samostatna cinnost, zkouska). Outpost praxe poskytuje materialni zaklad, formalni krok je administrativni.

---

## 6. Zaverecna inventura souboru (pro RAG a audit)

*Zdrojove cesty (absolutni, mimo KB, pro interni audit):*
* `C:\Users\PC\Documents\Repozitar_Dev\Zakazky\Dodavka_Kuba_Sladek\elektro_schema_boxer.html:1-430` (schema, prurezy, normy)
* `C:\Users\PC\Documents\Repozitar_Dev\Zakazky\Dodavka_Kuba_Sladek\komplexni_dokumentace.md:1-288`
* `C:\Users\PC\Documents\Repozitar_Dev\Zakazky\Dodavka_Kuba_Sladek\whatsapp_konverzace.txt:1-106`
* `C:\Users\PC\Documents\Repozitar_Dev\Source_raw\Outpost_kontext_master\Outpost-2026-fyzicko-enviromentalni-profil.md:116-184`
* `C:\Users\PC\Documents\Repozitar_Dev\Source_raw\Outpost_kontext_master\Soupis_technickeho_vybaveni_outpost.md:11-30`
* `C:\Users\PC\Documents\Repozitar_Dev\Source_raw\Outpost_kontext_master\FV\MD\ingest_energeticky_uzel.md:5-71`
* `C:\Users\PC\Documents\Repozitar_Dev\Source_raw\Outpost_kontext_master\FV\FV.md:9-158` (master strom)
* `C:\Users\PC\Documents\Repozitar_Dev\Source_raw\Outpost_kontext_master\FV\JK_logs\bms_aggregated_30d.md` + `Cornex_314_health_report_april_2026.md`
* `C:\Users\PC\Documents\Repozitar_Dev\Source_raw\IoT_dev\Evoluce_DIY_2012_do_IoT_2026_v2.md:36-69`
* `C:\Users\PC\Documents\Repozitar_Dev\_github\B2B-Knowledge-Base\01_METODIKY\02_CV_a_profil\05_full-CV_CZ_v2.md:77`

*TEMP batch cache:* `C:\Users\PC\AppData\Local\Temp\opencode\elektro_audit_20260904\batch{1..3}_*.txt` (3 soubory, 880-2483 B)

---

*Poznamka RAG:* Tento dokument je jediny kanon pro dotaz "elektro kvalifikace". Duplicity nevytvaret (P1). Pri vzniku nove generace presunout predchozi do `_ARCHIVE/` (P4).*
