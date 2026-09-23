# OUTPOST ELEKTRO — GROUND TRUTH STAVU A ZADANI NOVE INSTALACE

**Datum:** 2026-09-23 | **Autor:** outpost2026
**Ucel:** Deterministicky popisat soucasny stav elektroinstalace objektu Outpost 2026 (revize pred zimou) a slouzit jako zaklad ground truth pro navrh nove instalace s vyuzitim zkusenosti zprovozu od zimy 2025.
**Verze:** 1.0 | **Status:** zive GT — doplnuje se foty a meritky autora | **Provenance:** source-read (Source_raw/Outpost_kontext_master + KB 04_ELEKTRO) + author-live-update 2026-09-23 (zapojeni, jistice, cislovani mistnosti)
**Tagy KB:** elektro, outpost, offgrid, FVE, LFP, BMS, jistenie, revize, ground-truth

---

## 0. Metodika a rozsah

**Kontext zadani:** Autor provadi revizi elektroinstalace pred zimnim obdobim. Dosud byly odstraneny veskere AC rozvody; system je ve stavu minimalni DC provozuschopnosti. Cil = ziskat ground truth soucasneho stavu (chyby koriguje autor formou popisu/fotografii s meritky) a navrhnout novou instalaci s vyuzitim rocnich zkusenosti s DIY off-grid provozem (zima 2025/2026).

**Zdroje:**
- Author-live-update 2026-09-23 (zapojeni stringu, mistnostni cislovani, inventura jisticu, topologie FVE jisticeni) — **priorita pred archivnimi daty**
- `Source_raw/Outpost_kontext_master/` (ingest_energeticky_uzel, FV_ingest_*, FV Diagnostic 2026-03-18, soupis, fyziko-env. profil, datasheet, JK_logs, Cornex health)
- KB: `04_KNOWLEDGE_BASE/04_ELEKTRO/KVALIFIKACE_ELEKTRO_AGREGACE_2026-09-04.md`
- Reference navrhu: `Zakazky/Dodavka_Kuba_Sladek/elektro_schema_boxer.html` (normy, prurezy, RCBO)

**Omezeni:** Bez formalni §50 kvalifikace (viz KVALIFIKACE_ELEKTRO). Prace na VTZ/DS mimo rozsah. Toto je GT pro vlastni ostrovni objekt.

---

## 1. Objekt a mistnostni cislovani (oprava 2026-09-23)

| Mistnost | Plocha | Role (AKTUALNI definice autora) |
|---|---|---|
| **Mistnost 1** | 25 m2 | Pergola — nedokoncena, bez izolace, fólie Guttafol |
| **Mistnost 2** | **10 m2** | **Energeticky a obytny uzel** — plne izolovane (7–10 cm MW), Battery Hub, kamna Priti Mini D, hlavni LFP + BMS + hybridni menic |

*Poznamka k revizi v1 (2026-09-23):* Puvodni zadani tasku uvadelo „mistnost 1 = obytna 10 m2“ — **nepravda**; kanon je **mistnost 2 = 10 m2 energeticky uzel**. Stary text v archivnich dokumentech (datasheet „Zona 1/2“) oznacuje pergolu jako Zonu 1 a utility uzel jako Zonu 2 — cislovani mistnosti vs zony se lisi, v tomto dokumentu plati tabulka vyse.

**Objekt:** dre stavba 7×5 m (35 m2 celkem), zaklady skvarobetonove patky, severni hrana 0,4 m pod terenem (hydroizolace nereshena). Lokalita: Drahanske udoli, Praha 8 — Dolni Chabry, 50.15087 N / 14.42343 E.

---

## 2. Soucasny provozni stav (author-live 2026-09-23)

### 2.1 Co JE zapojeno a provozovano

```
[String 1 FV — STRECHA mistnosti 2]
        |
        v
   DC jistic SPB1 63Z C32   <-- JEDINY zapojeny jistic v objektu
        |
        v
   silove DC kabele (do mistnosti 2)
        |
        v
   [Hybridni menic POW-HVM3.2H 3200 W] <-- vyrabi E, nabiji
        |
        v
   [Hlavni LFP 8S2P 630 Ah / 15,12 kWh] --- [BMS JK-PB2A16S20P 200A — ZAJOJENA]
```

| Prvek | Stav | Detail |
|---|---|---|
| **String 1** | **ZAPOJEN, na strese mistnosti 2** | 4×475 Wp, 2P2S, az. ~173°, tilt dle posledni zmeny (45° k 18.3.2026 — overit aktualni foto) |
| **String 2** | **MIMO PROVOZ** (neuvedeno v zapojeni 2026-09-23) | 2×200 Wp 2S; historicky chybel DC jistic; Panel A 100% mikropraskliny; CYKY 1,5 mm² / ~6 m; Epever XTRA4210N poskozena svorkovnice, bez krytu, 27,6 V strop |
| **DC jistic FVE** | **SPB1 63Z C32 — zapojen** | Jediný zapojeny jistic; cesta: panely → SPB1 → silove kabele → hybridni menic |
| **Hybridni menic** | **Provoz** | POW-HVM3.2H-24V-N, 3200 W AC, idle ~52,6 W; bulk 28,8 V / float 27,2 V (upr. 18.3.2026) / UVP 22,0 V / max charge 80 A |
| **Hlavni LFP** | **Provoz, nabijena** | LiFePO4 8S2P (2P8S), 630 Ah, 15,12 kWh, nom. 25,6–26,4 V |
| **BMS** | **Zapojena** | JK-PB2A16S20P V19, 200 A common port, 2 A aktivni balancer, BLE/GPS/TTL |
| **AC rozvody 230 V** | **ODSTRANENY / NEZAPOJENE** | Zadne zasuvky, zadne jisticne skupiny AC v provozu |
| **AC jisticeni** | **FYZICKY K DISPOZICI, NEZAPOJENO** | Viz §3 |
| **GoKWh zalozni LFP** | **ODPOJENA, NEDOBITA** | 24 V, 100 Ah, 2,4 kWh; U okolo 24 V (hluboke vybiti — pred pripojenim overit stav celku, nelze nabijet pod 0 °C) |
| **DC rozvody vetevni (USB, step-down)** | Mimo tento GT stav — historicalne z Epever; nyni dle autorova popisu neupresneno (foto) |

### 2.2 Zimni provoz 2025/2026 — co se osvedcilo / lekce (zdroj: JK_logs, diagnostic session)

| Pozorovani | Hodnota | Dopad na novou instalaci |
|---|---|---|
| Zimni minimum SOC | **171 Ah (27 %), 10.2.2026** | Rezerva kapaciny funguje; pred zimou zajistit plny SOC start |
| Teplota celku | Nikdy < 0 °C v logovanem obdobi (min 8 °C v 30d okne 2/3–3/2026) | Zakaz nabijeni < 0 °C = absolutni stop; mistnost 2 jako temperovany uzel se osvedcil |
| Capture ratio | Prumer ~28 % (zemni montaz, stineni udoli) | Po premisteni na strechu mistnosti 2 ocekavat narust — overit novymi BMS logy |
| Nabijeci proud | Peak 26,4 A baterie (= fyz. limit 2P stringu ~710 W) | Neni bottleneck menic; plne 1900 Wp vyzada zmenu topologie stringu |
| Nočni odběr | 1,5–2,0 A (~40–53 W) + idle menice 52,6 W | Dimenzovat rezimu nočního provozu do bilance |
| Tezke zatěže | Hoblovka 1800/3000W, pila 1500/2500W, svaracka (externi), vodarna 700W; konvice+indukce 4000W > 3200W menic | **Blokace soubehů nutna** — softwarova nebo hardwarova (relay/RCBO logika) |
| Balancér | Aktivni pri nabijeni > ~300 Ah; delta V ~0,03 V | Zdravi LFP vyborne (Cornex 4/2026: „vyborny stav“) |
| DEBT_IOT_004 | DC jistic String 2 historicky chybel | Nová instalace: **kazdy string vlastnim jisticem** |

---

## 3. Inventura jistici techniky (fyzicky k dispozici, NEZAPOJENO krome SPB1)

| Polozka | Pocet / specifikace | Predpokladana role v nove instalaci |
|---|---|---|
| **SPB1 63Z C32** | 1 ks — **ZAPOJEN** | Hlavni DC jistic FVE string 1 (63A rada?, C32 — overit oznaceni na souboru: zda jde o MCB C32 nebo pojistkovu nahradu) |
| **PL7C16/1** | 1 žila (1-pólový), C křivka 16 A | AC okruh male zateze / pomocny |
| **PL7B32/1** | 1 ks, B křivka 32 A | AC okruh vyssi zateze / zasuvkova vyhrada |
| **B25/1** | 1 ks | B25 — typicky MCB B 25 A (1p) nebo pojistkovy prvok — **overit typ na foto** |
| **Noark Ex9FP/2** | 1 pouzdro 2p + **2× 20 A valcove pojistky** | Dvoupólové jištění (AC vypinač/pojistkova ochrana) |
| **Pouzdro MEGAFUSE** | 1 ks + **2× 250 A valcove pojistky** | **DC strana baterie / menic trunk** — high-current ochrana (AIC dle BMS 200 A) |

**Stav:** Jistice **nejsou zapojeny** — fyzicky lezi v zasobe. Vyjimka = SPB1 na FVE větvi (viz §2.1).

---

## 4. Gap analyza — soucasny stav vs. bezpecnostni pozadavky

| # | Gap | Zavaznost | Navrhovane reseni (vstup pro GT nove instalace) |
|---|---|---|---|
| G1 | AC rozvody uplne odstraneny — zadna ochrana osob pred dotykem, zadne RCD | Vysoka (po dokonceni AC) | RCBO/RCD typ A 30 mA na kazdem okruhu; PE system jednobodove (referencne Boxer schema) |
| G2 | MEGAFUSE 250A nezapojen — baterie/menic trunk bez dedikovaneho proudu omezeni dle AIC | Vysoka | Series pojistka 150–250 A na bateriove strane dle AIC BMS + katalogu menice |
| G3 | String 2 mimo provoz + historicky bez DC jisticu + poskozeny Epever | Stredni (pokud bude reaktivovan) | Buď vyřadit, nebo nove jisticeni + oprava/nahrazeni MPPT |
| G4 | Zadny spinaci/prvotni jistic na AC strane menice (vse odpojeno) | Stredni | Navrhnout rozvadec mistnosti 2: hlavni vypinac, vetve L/N/PE, popisovani |
| G5 | Soubeh 4000W konvice+indukce > 3200W menic | Provozni | Interlock (relay s prioritou) nebo soft limit + dokumentovane pravidlo „1 velky spotrebic“ |
| G6 | Bez meritelneho napeti/proudu na DC trase panely→jistic→menic (krome BMS) | Stredni | INA226 / RS232 bridge (DEBT_IOT_002, DEBT_001) — viz Diagnostic §7 |
| G7 | Hydroizolace severu, tepelne mosty — soudrznost s elektro (vlhkost u rozvaděče) | Stredni | Rozvadec/vse v mistnosti 2, mimo severni stenu; kondenzat/odvodneni |
| G8 | Zalozni GoKWh nedobita a odpojena | Nizka | Pred zimou: overit U celku, balanc, pripojit pres vlastni jistic/udrzovaci nabijeni nebo vyraďit z bilance |

---

## 5. Navrhove principy NOVE instalace (vstup z rocnim provozem)

1. **Topologie uzlu:** Vse hlavni v mistnosti 2 (10 m2); mistnost 1 = pergola = pouze oddelene DC/AC vetve s vlastnim jistenim, ne energeticky uzel.
2. **DC architektura:** FV stringy → **kazdy vlastni DC jistic** (dimenzovat dle Voc/Imp, ne 63A domyslene) → MPPT/menic → BMS → trunk s MEGAFUSE dle AIC → rozvadec DC.
3. **BMS jako master ochrana:** 200 A = strop; vsechny AC vetve pod min(menic 3200 W, BMS 200 A).
4. **AC architektura:** Rozvadec mistnosti 2: HIC 16A/32A podle skutecne zateze (C/B křivka dle char spotrebicu), RCBO 30 mA typ A, oddelene okruhy: (a) zasuvky dilna, (b) zasuvky obytne, (c) server/kriticke, (d) topeni/voda — dle finalniho dispozicniho planu.
5. **Dimenzovani prurezu:** AC 3×2,5/1,5 mm² (referencne Boxer: MCB 10/16 A); DC trunk min. dle 1,25×Imax + teplotni korekce; CYKY jen pro AC, ne pro FV string (pouzit solar kabel UV-odolny).
6. **Zimni provoz:** Termostat/nabijeci interlock pri < 0 °C; teplotni cidla na baterii (DS18B20 plan); Priti Mini D jako predohrev pred nabojim po mrazove noci.
7. **Monitoring:** RS232/Modbus z menice + BLE BMS → jednotna telemetrie (uzavrit DEBT_001/002/IOT_002).
8. **Bezpecnostni pravidla provozu:** Blokace souběhu >3200 W; 1 velky spotrebic soucasne; dokumentovany start/stop postup pred zimou.

---

## 6. Otevřené položky — doplni autor (foto + meritka)

| ID | Co doplnit | Forma |
|---|---|---|
| O1 | Aktuální půdorys mistnosti 2 s polohou menice, LFP, BMS, rozvaděče | Foto + rozměr (pás měřítka nebo známá vzdálenost) |
| O2 | Detail zapojeni SPB1 63Z C32 — průřez vodičů, směr (±), skutečné označení | Foto čitelné štítku |
| O3 | Trasa silových kabelů strecha→mistnost 2 (průřez, typ, délka) | Foto + popis |
| O4 | Stav AC kabeláže po demontáži — co zůstalo ve stěnách, krabice, vesty | Foto místnost 1 i 2 |
| O5 | Ověření typu B25/1 a PL7* (MCB vs. pojistková) | Foto štítku |
| O6 | Aktuální tilt/orientace stringu 1 po premistění na střechu | Foto + kompas |
| O7 | SOC/napětí hlavní LFP a GoKWh v den revize | Odečet BMS / multimetr |
| O8 | Dispozice zásuvek a spotřebičů, které se mají vratit do provozu | Seznam + místo |

---

## 7. Revize dokumentu

| Datum | Změna | Autor |
|---|---|---|
| 2026-09-23 | V1.0 — vznik GT: author-live update (string1 strecha, GoKWh odpojena, inventura jisticu, SPB1), gap analyza, navrhove principy | outpost2026 + agent |

---

*Poznamka RAG: Kanon pro „stav elektroinstalace Outpost pred revizi 2026“. Duplicity netvorit (P1). Pri nove generaci presunout tuto verzi do _ARCHIVE/ (P4). Navrh nove instalace se bude rozsirovat v ramci §5 po doplneni §6.*
