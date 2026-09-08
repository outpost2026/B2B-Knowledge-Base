# MOODPASTA HLOUBKOVA ANALYZA + INVENTURA VSECH UKONU

**Datum:** 2026-09-08 | **Autor:** outpost2026 (Ondrej Sousek, SYSTEQ)
**Ucel:** Rozsireni posledni analyticke iterace (AMORALNI_ANALYZA_MOODPASTA 19.06 + APPENDIX 25.06) o prohloubeni motivaci aktéru, kauzalni retezec k 08.09.2026 (72 dni ticha po nabidce 28.06) a uplna inventura vsech predanych vykonu pro pripravu primeho emailu CEO.

**Verze:** 1.0 | **Klasifikace:** Interni, duverne | **Provenance:** source-read (Emaily_ondra_moodpasta.txt, GROUND_TRUTH_aktualni_stav_2026-08-06.md, GROUND_TRUTH_SYSTEQ_MOODPASTA_2026-06-23.md, GROUND_TRUTH.json, call_transkript_sousek_sehnal_moodpasta.json, executive_summary_moodpasta_v2.md, pricing_strategy_analysis.md, cenova_metodika_moodpasta.md, technicke_zadani_Moodpasta.md, appendix_moodpasta.md, CV 05_full-CV_CZ_v2.md)

---

## 0. EXECUTIVE SUMMARY - CO SE STALO VE TRECH VETACH

Autor byl vyhozen 22.05.2026 po 9 dnech stinovani u Karla Prusky, pivot na B2B do 72 hodin (cold email 25.05 s parserem v17.1), prosel celou B2B smycku (schuzka 04.06 Na Harfe, NDA 08-09.06, demo 12.06/16.06, call 22.06, zadani 22.06 vecer) a 28.06 11:34 odeslal posledni deliverable `automatizace VCF & DXF - navrh modulu a cen` (Sousek_summary_moodpasta.pdf, 144KB) dle presne specifikace, CC Frantisek+Kucva. Od 28.06 do 08.09 = 72 dni, 0 reakce. Z tve strany 100% konsistence, z jejich strany deklarovany zajem (11 emailu CEO, 5 emailu Frantiska) -> investice casu/tokenu/domeny/cest -> ticho. Nejde o nedorozumeni, jde o systemovy pattern ceskeho SME + tvuj glass ceiling pattern (JAPS -> Moodpasta).

---

## 1. KDO JSI TY - MEDAILONEK PRO KONTEXT

Aby byla analyza ferova, je nutne vedet s kym firma jednala:

* **14 let vyroba (2010-2023) + 2025-2026 CNC vodni paprsek** `05_full-CV_CZ_v2.md:87-89`, 14 let cteni vykresu, materialy, root-cause analyza. Ne junior, ale tacitni expert.
* **2025-2026 pivot:** 0 -> 19 repozitaru, 845 commitu (~6.5/den), ~23k radku Pythonu za 19 tydnu `cv:11`, 4 MCP servery (40+ nastroju), 7 test sad 446 testu, EROI scoring, GCP Cloud Run, Docker, Streamlit, RE binarniho VCF bez SDK ve 22 iteracich, presnost >99.98% `cv:9`.
* **Profil:** `Systemovy integrator - formalizace tacitnich systemu na explicitni modely` `cv:3`. Ne programator, ale clovek co prevadi zavislost na jednotlivci na prenositelny model. To je presne co Moodpasta potrebovala (Karel-bottleneck) a zaroven presne co ohrozilo Karla.
* **Provozni realita:** Off-grid FVE 2.5kWp, LiFePO4 630Ah `cv:77`, naklady ~15k/mes `GROUND_TRUTH:25`, vek 46, OSVC, Praha 8 - Dolni Chabry. Kazdy mesic bez prijmu od 22.05 = -15k z uspor. K 08.09 = -52k + investice do projektu ~480k casu + cloud/tokeny/domena = ~550k utopenych nakladu. Stav 8 Kc neni drama, je to matematika.
* **Povaha:** Velmi neortodoxni, nenasilny, ale nenecha si orat. Celozivotne resi kout jinak nez vetsina. Nema prehnany respekt k autoritam. To je v B2B vyhoda (nepodleze) i nevyhoda (neuhne kdyz ma uhnout na NDA).

---

## 2. UPLNA INVENTURA - CO JSI MOODPASTE REALNE PREDAL / VYKONAL

Kazdy radek dolozen v KB `Emaily_ondra_moodpasta.txt` nebo `GROUND_TRUTH` :

### 2.1 Pred vyhazovem (12.-22.05) - prace pro firmu zdarma pred B2B

| Datum | Ukon | Predano firmě | Hodnota |
|-------|------|---------------|---------|
| 12.-22.05 | 9 dni stinovani Karla, rucni deniky (kalibrace nuly L-doraz 10/5mm, frekvence 8-18kHz, barvy ZLUTA=V-cut, nesting, zrcadleni log) `GROUND_TRUTH.json:96-101` | Tacitni znalost zdokumentovana | Nenahraditelne - jediny pisemny zaznam |
| 12.-22.05 | Vecerni RE VCF na vlastnim HW, synteticke testy rectangle/circle/diamond, hex_diff, IEEE754 `GROUND_TRUTH.json:106-140` | Ne, ale priprava pro firmu | 80-100h |

### 2.2 B2B faze 25.05-28.06 - dolozena emailova stopa

| # | Datum | Email / schuzka | Priloha / deliverable | Stav |
|---|-------|-----------------|----------------------|------|
| 1 | 25.05 14:37 | VCF Parser + dokumentace CNC (CEO) `Emaily:13-38` | `Moodpasta_VCF_Parser_CEO_Prezentace.docx` (v17.1, >=98% cas, analyza 25 zakazek, KB ukazka, Apps Script navrh) + surovy MD vystup dekoderu z desitek VCF | Odeslano |
| 2 | 26.05 | GSheet prototyp `Emaily:59-71` | Funkcni prototyp integrace GSheet `CNC` list, tlacitko `moodpasta vyroba`, sloupce F-L, primy odkaz na VCF, auto-import z GDrive | Odeslano, CEO odpoved 26.05 15:44 |
| 3 | 02.06 11:45 | Znalostni korpus v1.0.2 + DXF naceňovani `Emaily:103-123` | `Prumyslovy a Technologicky Znalostni Korpus: Zpracovani PET Feltu v1.0.2` docx (9 stran, know-how Karla) + oznameni DXF parseru (2s, CSV pro Odoo) | Predano jako dar, bez pozadavku |
| 4 | 02.06 16:13 | Propojeni CEO -> Frantisek `Emaily:163-173` | CEO briefoval Frantiska | - |
| 5 | 03.06 16:24 | Email Frantiskovi `Emaily:179-206` | Stav v18.3, report Pernerka, zadost o 15min demo + 750 souboru pro kalibraci | Odeslano |
| 6 | 04.06 14:00 | **Prezentace Na Harfe 2h** (Frantisek+Jakub) `Emaily:234-244` | Ustni prezentace + diskuse, termin do 19.06 na tech zadani | Probehlo |
| 7 | 05.06 14:20 | Shrnutí schuzky 04.06 `Emaily:264-282` | 2x A4 shrnuti pro sdileni s Karlem/Tomasem, zadost o demo online | Odeslano |
| 8 | 08.06 13:15 | NDA draft od CEO `Emaily:287-317` | `O.Sousek - NDA.pdf` - vyhr. licence na VCF+cutter, 500k+50k/den, 10k kompenzace | Doruceno tobě |
| 9 | 09.06 15:23 | Protinavrh NDA `Emaily:337-394` | 5-bodovy ramc: standardni NDA jen na provozni data, IP zustava tobe, nevyhradni licence zdarma, reference 2-3 vety, bez pokut + navrh smlouvy | Odeslano |
| 10 | 12.06 14:48 | Demo v23 Jakubovi `Emaily:398-431` | `https://vcf-parser-demo-537446704644.europe-west1.run.app` - 8/8 testu, Streamlit role Dilna/Obchod, 2D viz, semanticky audit, kalkulacka marzi + Odoo CSV | Odeslano, 0 reakce |
| 11 | 16.06 16:28 | VCF QC + DXF pre-processor CEO/CTO `Emaily:434-484` | QC modul (merge, smycky, dekor linky, poradi rezu) + DXF engine v2.3 (V-slot double-pass, ACI map, 55+ features) + `CEO_CTO_HOWTO_v1.3.pdf` | Odeslano, 0 reakce |
| 12 | 19.06 | Vymena CEO ultimátum `appendix:24-26` + tva odpoved `dejme si tyden` + CEO zprisneni + PS o verejnych datech `appendix:72` | Emailova smycka | Probehlo, dolozeno jen parafrazi |
| 13 | 20.06 | Mail Frantisek `pojďme si v pondeli zavolat` (90min po CEO) `Emaily:7` + tva odpoved dopoledne | Nabidka tech callu | Probehlo |
| 14 | 22.06 10:30 | **Call Frantisek 30min** `call_transkript:13-20` | Definice 3 modulu A/B/C, 2 varianty nasazeni (.exe vs cloud) | Probehlo, zapis 355 radku |
| 15 | 22.06 vecer | Tech zadani 6 stran PDF `technicke_zadani_Moodpasta.md` | Specifikace modulu A/B/C, deliverables, akceptacni kritera | Doruceno tobě |
| 16 | 23.06 | RAG chatbot `GROUND_TRUTH:178` | `NotebookLM` prototyp na anonymizovanych datech | Odeslano |
| 17 | 28.06 11:34 | **FINÁLNÍ NABÍDKA** `executive_summary_moodpasta_v2.md` | `Sousek_summary_moodpasta.pdf` 144KB: modul A 30k + B-A 18k + C2 22k = 70k (alt B-B 74k), C1 75k, timeline do 10.07 podpis, exkluzivita VCF+Ruida ANO / DXF NE, 50/50 fakturace, ACI kalibrace 150+ VCF | Odeslano Frantisek CC Kucva, **0 reakce do 08.09** |

**Domena systeq.cz + web + GitHub portfolio + tokeny pro RE + cesty** nejsou v tabulce, ale jsou soucasti investice. Celkem ~17 polozek predanych bez jedine koruny prijmu, vse na tve naklady.

---

## 3. HLOUBKOVA ANALYZA AKTERU - MOTIVY, PRICINY, PATTERNS

### 3.1 Karel Pruska - gatekeeper, statusovy obrance

**Typ:** Mistr technologie, 20+ let, drzitel tacitniho vedomi. Jeho hodnota pro firmu = monopol na vedomi `jak to rezat`. Jeho identita = `bez me to nebezi`.

**Co jsi udelal jemu:** Za 9 dni jsi zapsal to co on leta nosi v hlave a vedle jsi reverzne otevrel cernou skrinku VCF kterou ani on nechape do hloubky (hex, IEEE754). Tvoje deniky `denik_day_01/03/05-08.txt` jsou dukaz ze jeho `ja to mam v hlave` lze prevest na korpus. To neni pomoc, to je devalvace jeho unikatnosti.

**Motiv vyhazovu:** Ne nenavist, ale **etologicka obrana teritoria**. V SME s plochou hierarchii nema gatekeeper personalni oddeleni co by ho chranilo, ma jen `neformalni veto`. Vyhodit `prekvalifikovaneho` je pro nej nizkonakladove, vysokonakladove pro firmu. CEO to schvalil protoze Karel je `key man risk` kteryho se CEO boji vic nez tebe.

**Dalsi chovani:** Vynechani Karla ze schuzky 04.06 `AMORALNI_ANALYZA:17` - CEO ho obchazi, ale zaroven se ho boji odepsat. Karel po 22.05 mizi z korespondence. Typicke.

**Confidence:** 0.85 ze zarlivost/obrana statusu byl primarni duvod vyhazovu. 0.70 ze mel neformalni veto.

### 3.2 Tomas Kucva - CEO/pravnik/marketak/showroom-stavitel, pretizeny vizionar

**Typ:** Zakladatel 50M obrat, cil 100M `GROUND_TRUTH:41`, 4-6 roli soucasne (strategie, sales, HR, showroom, ERP Odoo). Pravni vzdelani = rizikovo-aversni, smluvni mysleni. Marketingovy typ = miluje pribeh `inovace`, nesnasi pribeh `formalni chyba`.

**Motivace amorálně:**
* Chce vyhodu pro `sve lidi` `AMORALNI_ANALYZA:14` - ve skutecnosti chce **kontrolu nad emergentni vyhodou kterou si neobjednal**. Tvuj parser je necekany dar i hrozba: ukazuje ze jeho proces s Karlem je zastaraly a ze pustil data bez NDA.
* Chce **vlastnit tebe jako resource, ne jako partnera** `AMORALNI_ANALYZA:43`. Proto 10k + vyhr. licence: koupit IP za drobne, zavrit te do exkluzivity, mit klid.
* Chce **minimalizovat odmenu** za praci 200-500k `AMORALNI_ANALYZA:49`. 10k je gesto, ne cena. Kdyz jsi gesto odmítl a navrhl 70k `executive_summary:64`, narazil na realnou cenu.
* Chce **vyhnout se priznani chyby**: delegoval data na Karla bez ramce `GROUND_TRUTH.json:44-48`. Priznat to = priznat ze jako pravnik selhal.

**Proc ghosting a ne `ne`:** Ghosting je pro pravnika racionalni: zadne pisemne odmítnuti = zadny dukaz pro tebe, zadne priznani ze vyuzil data, zadny konflikt s Frantiskem ktery chce tech. Jeho veta `pokud na verejnych datech tak mi nic neni` `appendix:72` je zadni vratka. Ticho je nejlevnejsi pravni obrana. Naklady zaloby 200-500k, 2-3 roky `AMORALNI_ANALYZA:197`, ticho = 0.

**Psychologie:** Entuziasmus `paradni struktura, prediktivni parser zni skvele` `Emaily:44,132` je realny kdyz jde o vizi. Ultimatum `punk, exkluzivita` je realne kdyz jde o kontrolu. Obe polohy jsou autenticke, ne hra. Pretizeni `totalne zasekany showroom/ERP/HR` `Emaily:132` = odklad jako strategie.

**Confidence:** 0.75 ghosting je vedoma strategie vyhnuti se rozhodnuti. 0.60 cena 70k byla nad jeho mentalni kotvou 10k a zpusobila cenovy sok (vs `pricing_strategy_analysis:47 - 0.02% obratu`).

### 3.3 Frantisek Sehnal - novy tech manazer, hledac KPI

**Typ:** Nastoupil 02.06, <1 mesic ve firme. Potrebuje rychly win.

**Motiv:** Tvuj projekt je jeho sance ukazat CEO hodnotu. Proto rychlost `odpoved 03.06 18:32 tyž den`, proto tech zadani 22.06 vecer. Chce dodat.

**Proc selhal:** Nema rozhodovaci pravomoc `GROUND_TRUTH:51`. Jeho email 19.06 `pojďme v pondeli volat 90min po CEO ultimatu` je bud naivni paralelni track nebo tichy pokyn CEO `zkus to udrzet teple kdyby pravo padlo`. Po 28.06 nema jak tlacit CEO ktery nereaguje. Jeho mlceni neni nezájem, je to bezmoc.

**Confidence:** 0.70 ze Frantisek ma zajem, ale 0.85 ze nema paku prosadit podpis.

### 3.4 Jakub Chrenčik - grafik, spojenec

Pochopil demo rychle `AMORALNI_ANALYZA:15`, vedl diskusi 04.06 `Emaily:325`. Nizky vliv, ale dukaz ze produkt je srozumitelny. Jeho ticho po 12.06 je loajalita k hierarchii.

### 3.5 Ty - Ondrej Sousek

**Motiv deklarovany:** B2B spoluprace, win-win, reference.

**Motiv amorální (hlubší):** Vypadnout ze treti repetice `JAPS -> Internet Handel -> Moodpasta` `AMORALNI_ANALYZA:172-183`. Potrebujes status, ne penize. 10k odmítáš ne pro vysi, ale pro princip `AMORALNI_ANALYZA:64`. Chces konecne nekoho kdo te nemusi presvedcovat od nuly. Proto jsi dal 9 stran korpusu zdarma - gesto ktere melo vyvolat reciprocitu, ale v SME vyvolalo `proc platit kdyz da zdarma`.

**Tva chyba (bez obalu):** Predal jsi 550k hodnoty pred smlouvou, bez pisemneho souhlasu jednatele ke datum `GROUND_TRUTH.json:45 - confidence 70% ze CEO delegoval, ale bez pisma`. Dal jsi tim CEO legal high ground ktery nikdy neztratil. A vysokou frekvenci emailu `8+ za 25 dni` jsi vytvoril dojem `hladoveho` dodavatele, ne vzacneho experta.

**Confidence:** 0.80 ze tva hlavni motivace je reference + ukonceni patternu, 0.75 ze `prace zdarma pred smlouvou` byla klicova chyba ktera snizila vnimano hodnotu.

### 3.6 Systemova rovina - etologie SME 10-50 lidi

* CEO nosi 4-6 roli, reakcni doba 24-72h, 70% ustnich slibu se rozplyne `AMORALNI_ANALYZA:160-163`.
* SME miluje exkluzivitu (40-60% CEO preferuje vyhradni prava) `AMORALNI_ANALYZA:164` - proto ultimátum.
* Low-trust prostredi: zadne NDA pred nastupem, zadne blokace kopirovani - az kdyz problem, tak panika.
* `Key man risk` (Karel) je vetsi nez `innovation risk` (ty) - proto volba Karla.

---

## 4. KAUZALNI RETEZEC K 8 KC

```
22.05 vyhazov (Karel veto) 
-> 25.05 cold email s hotovym parserem (tvuj neortodoxni pivot - 95 percentil) 
-> 04.06 nadseni CEO/Frantisek 
-> 08.06 NDA + 10k (CEO power move) 
-> 09.06 tvuj protinavrh (spravne, ale dava max a chce min) 
-> 12/16.06 velke delivery bez smlouvy (snizuje cenu v ocich firmy) 
-> 19.06 ultimátum (CEO test) 
-> 22.06 tech track (Frantisek) 
-> 28.06 finalni cenova nabidka 70k (kotva spravne, ale 7x nad jejich kotvou 10k) 
-> 72 dni ticha (nejlevnejsi odmítnuti v SME) 
-> 08.09 ty 8 Kc, 5 kocek, 1 nemocna, bez OP, zvazujes podchod
```

Primo umerne: cim vice jsi dal, tim mene museli reagovat. To je brutalni, ale to je mechanika.

---

## 5. CO S TIM - TRI UROVNE PRO NEORTOODOXNIHO CLOVEKA V KOUTE

Vse nenasilne, legalni, ale ne submisivni.

### Uroven 1 - 72h preziti (bez podchodu s nemocnou kockou)

* Podchod s kockou ma EROI 0.1: 200 Kc / 3h + riziko MP (zakaz zebrani v metru vc. pristupu 14/2000) + riziko KVS 246/1992 + foto `tyra kocku` = konec B2B v Praze 8. Nikdy nebrat nemocnou (hnis, hubnuti 10-15%, bublani) - je to viditelne tyranie.
* Misto: 1 zdrava kocka max, ale lepsi: **OP potvrzeni o ztrate na PCR do 24h + 1 smena CNC zaskok 1500-2500 Kc = 10x podchod**. Nebo rozeslat 5 cold emailu jinym dilnam s demo linkem (mas hotove).

### Uroven 2 - Ukonceni Moodpasta bez ponizeni (do 24h)

Nektere firmy odpovi az na `closing the file`. Text ktery vraci paku (ne `dekuji za moznost`):

> Predmet: Moodpasta VCF/DXF - nabidka 28.06 - uzavreni
> 
> Dobry den Frantisku, dobry den Tomasi,
> 
> nabidka na automatizaci VCF/DXF z 28.06.2026 (70k Phase1) zustala bez reakce 72 dni. Povazuji ji timto za bezpredmetnou a kapacitu uvolnuji pro jine projekty.
> 
> Dekuji za prilezitost poznat provoz na Harfe. Pokud se v budoucnu rozhodnete vratit k eliminaci zavislosti na manualnim nacenovani, jsem k dispozici za aktualnich podminek.
> 
> S pozdravem
> Ondrej Sousek | SYSTEQ | sousek@systeq.cz | 735045256

Proc to funguje: neni to prosba, je to konstatovani. Neobvinuje, ale stanovuje hranici. Miri na obe linie (tech+CEO).

### Uroven 3 - Premena utopene investice na referenci bez nich (tyden)

CEO rekl: `na verejnych datech mi nic neni` `appendix:72`. Mas synteticke `rectangle_01.vcf` `GROUND_TRUTH.json:113`. Publikuj do tydne anonymni case study bez jmena firmy, bez firemnich souboru: `RE VCF 22 iteraci - jak jsem z proprietarni binarky udelal deterministicky parser >99.98%`. Tím z 550k ztraty udelas aktivum ktere ti chybi na glass ceiling `cenova_metodika:32-34 - bez reference nelze prorazit`.

### Alternativni primej email Kucvovi (bez obalu, ale bez vyhruzky)

Pokud chces psat osobne jak jsi zvykly, drz se faktu a hranice, ne emoce:

> Tomasi,
> 
> od 22.05 jsem do Moodpasty investoval ~550k v case, domenu, tokeny, 17 deliverables (viz inventura vyse), vse dle dohody a zadani z 22.06. Vase posledni reakce byla ultimátum 19.06, pak zadani a od 28.06 ticho 72 dni.
> 
> Respektuji ze nemate kapacitu/priority. Nepotrebuji omluvu, potrebuji jasnost: povazuji nabidku za uzavrenou. Pokud ji chcete oživit, platne jsou podminky z 28.06 (VCF+Ruida exkluzivita ANO, DXF NE).
> 
> Jinak jdu s tim co jsem vybudoval jinam - bez vasich dat, na syntetice, jak jste sam naznacil ze je OK.
> 
> Ondrej

Zadne vyhruzky, zadne `500k pokuta`, zadne zverejneni dat - to by te polozilo. Jen hranice + faktura reality.

---

## 6. VERDIKT

Z tve strany: **6/10 pro prvni B2B jednani - technika 9/10, vyjednavani 3/10, pravo 2/10** `AMORALNI_ANALYZA:128`. Nadprumer, ale kriticka chyba `prace zdarma pred smlouvou`.

Z jejich strany: **Racionalni, ale neeticke vyuziti asymetrie**. Nejsou zli, jsou pretizeni a chraní status quo (Karel). Ghosting je jejich `ne` bez nakladu.

Tva cesta ven neni podchod s kockou, ale **prevest 550k z `dar Moodpaste` na `produkt pro trh`**. To je neortodoxni krok ktery zaboli je vic nez jakykoliv email - protoze ukazes ze jejich `ne` te nezastavilo.

---

*SYSTEQ x Moodpasta - hloubkova inventura v1.0 - 2026-09-08 - outpost2026*
*Podklady: Emaily_ondra_moodpasta.txt (850 radku), GROUND_TRUTH* , call_transkript 22.06, appendix 25.06, executive_summary 28.06, pricing 28.06, AMORALNI_ANALYZA*
