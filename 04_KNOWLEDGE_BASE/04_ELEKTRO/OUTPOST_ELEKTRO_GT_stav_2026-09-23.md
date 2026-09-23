# OUTPOST ELEKTRO — GROUND TRUTH STAVU A ZADANI NOVE INSTALACE

**Datum:** 2026-09-23 | **Autor:** outpost2026
**Ucel:** Deterministicky popisat soucasny stav elektroinstalace objektu Outpost 2026 (revize pred zimou) a slouzit jako zaklad ground truth pro navrh nove instalace s vyuzitim zkusenosti zprovozu od zimy 2025.
**Verze:** 1.4 | **Status:** zive GT — doplnuje se foty a meritky autora | **Provenance:** source-read (Source_raw/Outpost_kontext_master + KB 04_ELEKTRO) + author-live-update 2026-09-23 (zapojeni, jistice, cislovani mistnosti, provizorni AC, meritka O10) + photo-read 2026-09-23 (jistice.jpg, menic+BMS foto, SPB1 foto od autora)
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
[String 1 FV — STRECHA mistnosti 2 — pultova, MINIMALNI TILT (author 2026-09-23)]
        |
        |  kabel FV → jističe: ~4 m, 2×2,5 mm² CYLY  (G12: typ kable, ne solar)
        v
   DC jistic SPB1-63Z C32 (YQSHIPU, 2p, DC500V, 6000A)  <-- JEDINY zapojeny jistic
        |
        |  jistic → menic: ~4 m, 2×4 mm² plné Cu
        v
   [Hybridni menic POW-HVM3.2H 3200 W] <-- vyrabi E, nabiji
        |
        v
   [Hlavni LFP 8S2P 630 Ah / 15,12 kWh] --- [BMS JK-PB2A16S20P 200A — ZAJOJENA]
```

| Prvek | Stav | Detail |
|---|---|---|
| **String 1** | **ZAPOJEN, na strese mistnosti 2** | 4×475 Wp, 2P2S, az. ~173°; **tilt = pultova strecha, minimalni (author 2026-09-23)** — misto drivejsich 45° |
| **String 2** | **MIMO PROVOZ** (neuvedeno v zapojeni 2026-09-23) | 2×200 Wp 2S; historicky chybel DC jistic; Panel A 100% mikropraskliny; CYKY 1,5 mm² / ~6 m; Epever XTRA4210N poskozena svorkovnice, bez krytu, 27,6 V strop |
| **DC jistic FVE** | **SPB1-63Z C32 — zapojen** | YQSHIPU, **2p, DC 500 V, 6000 A, IEC 60898-2**, v boxu s krytem; cesta: panely → 4 m 2×2,5 CYLY → SPB1 → 4 m 2×4 Cu → menic |
| **Hybridni menic** | **Provoz** | POW-HVM3.2H-24V-N, 3200 W AC, idle ~52,6 W; bulk 28,8 V / float 27,2 V (upr. 18.3.2026) / UVP 22,0 V / max charge 80 A |
| **Hlavni LFP** | **Provoz, nabijena** | LiFePO4 8S2P (2P8S), 630 Ah, 15,12 kWh, nom. 25,6–26,4 V; **U = 26,78 V (odecet 2026-09-23)** |
| **BMS** | **Zapojena** | JK-PB2A16S20P V19, 200 A common port, 2 A aktivni balancer, BLE/GPS/TTL |
| **AC rozvody 230 V** | **PROVIZORNI — 1× zasuvka, BEZ RCBO** | Měnič AC OUT → CYKYLO 3×2,5 → **EATON PL7C16/1** → svorkovnice (L/N + PE věneček) → CYKY 3×1,5 (<2 m) → **1× zásuvka (kolík), vše 3 vodiče** — viz §2.1e; stále **bez RCD/RCBO (G13)** |
| **AC jisticeni** | **Castecne VE PROVOZU** | PL7C16/1 zapojen (provizorni AC); zbytek inventare dale nezapojen — viz §3 |
| **GoKWh zalozni LFP** | **ODPOJENA, NEDOBITA** | 24 V, 100 Ah, 2,4 kWh; **U = 23,9 V (2026-09-23)** — nizke, pred pripojenim overit stav celku |
| **DC rozvody vetevni (USB, step-down)** | Mimo tento GT stav — historicalne z Epever; nyni dle autorova popisu neupresneno (foto) |

### 2.1b Fotoproanalyza — hybridni menic + BMS (author foto 2026-09-23)

**Popis autora (priorita):** vlevo hnědý CYLY 3×1,5 mm² = vývod AC; uprostřed černý/červený = silové DC **8 mm²** do LFP/BMS; vpravo černý/červený = silové DC in z FVE do měniče **4 mm²**.

```
                    [POW-HVM3.2H — stena, mistnost 2]
  AC výlev (hnědý CYKY 3×1.5)          DC BATT (černý/červený 8 mm2)     DC PV IN (černý/červený 4 mm2)
  vlevo — MIMO PROVOZ                  uprostřed → BMS/LFP               vpravo ← ze strechy (pres SPB1)
       |                                      |                                |
   volne konce dole                     [JK BMS PB2A16S20P]              (trasa stecha→menic)
   (modry+hnedy videt)                       | P-/B- svorky
                                             v
                                       [LFP pack 8S2P]
```

| Prvek na foto | Pozorovani | Jistota |
|---|---|---|
| Tělo menice | „SOLAR INVERTER CHARGER“, zeleny LED, displej — typ POW-HVM3.2H family | P>0.95 |
| Spodní kryt terminálů | **ODEBRANÝ / otevřený** — vnitřní PCB a svorkovnice přístupné, zelený blok viditelný | P>0.95 |
| AC strana | Hnědý CYLY 3×1,5 mm² vlevo; dole volné modré/hnědé konce — **AC není zapojeno do rozvodu** | P>0.9 (dle popisu + foto) |
| DC battery | Černý/červený 8 mm² střed → BMS; na BMS **P−/B− svorky s objímkami**, tlustý černý vodič k packu | P>0.9 |
| DC PV in | Černý/červený 4 mm² vpravo — **DC in z FVE** (string 1 přes SPB1) | P>0.95 (autor) |
| BMS | Bílá deska „锂电池保护板“ / jk-bms.com, QR, tenké červené vodiče = měřicí větve článků, zelené svorkovnice | P>0.95 |
| PE | Žlutozelený vodič přítomen (spodní část, směrem dolů) | P>0.8 |
| Montáž | Na dřevěné stěně — **bez rozvaděčové skříně, bez krytu terminálů, bez průchodek** | P>0.95 |
| Tepelný/požární kontext | Dřevostavba + otevřené svorky + vysoké proudy (trunk 8 mm²) = gap G9 | — |

**Dimenzovani (kontrola):**
- **DC battery 8 mm²** při Imax měniče 80 A (nab.) / BMS 200 A: 8 mm² Cu je na ~50–60 A při běžných teplotách v uzavřeném prostoru — **pro 80 A nabíjení hraniční/spíše nedostatečná bez deratingu**; pro nárazové vybíjení těžkých spotřebičů (jmenovitě težká díla ~100 A+) **poddimenzována vůči BMS 200 A**. Trunk musí být dimenzován na min(Imax měniče, AIC/AIC pojistky, I_predpokydany zatěž) — viz G2/G9.
- **DC PV 4 mm² (jistic→menic, ~4 m)**: Imp stringu 1 (2P2S, ~1900 Wp) je v radu ~20–23 A — 4 mm² plné Cu **na hraně** dle zatížení/teploty; 2×2,5 CYLY (panely→jistic, ~4 m) je **stejne hraniční až poddimenzované** pro plný Imp + navíc CYLY neni solarni kabel (UV) — **G12**.
- **AC 3×1,5 mm²** na 3200 W (~14 A): 1,5 mm² je na 16–19 A → **na hraně pro plný výkon měniče**; pro 16 A okruh dostačuje, pro 32 A ne (B32 by vyžadoval 2,5 mm²+).

### 2.1d Fotoproanalyza — SPB1 detail (author foto 2026-09-23)

| Prvek | Pozorovani | Jistota |
|---|---|---|
| Typ | **YQSHIPU SPB1-63Z C32**, 2p (spojena paka), CE | P>0.98 (cena z foto) |
| Spec | **DC 500 V=, IEC 60898-2, 6000 A**, křivka C, 32 A | P>0.98 |
| Schéma na štítku | 1+/2−, 3+/4− (obě poloviny), plus minus význam | P>0.95 |
| Stav | V boxu s **průhledným krytem** (nasazený), montáž na dřevo | P>0.95 |
| Konektory (dole) | Červený/černý kabel ze spodního průchodu (DC ven k měniči) | P>0.9 |
| Zapojení | **ON** (zelená okénka, páka dolů = OFF u těchto; dle foto červená paka ve spodní poloze — overit stav ON/OFF pri dalsim meritku) | P>0.8 |

### 2.1c Fotoproanalyza — inventura jisticu (jistice.jpg, author 2026-09-23)

Poreadi shora dolu na drevene desce:

| # | Prvek na foto | Specifikace (cena z foto / autora) | Stav |
|---|---|---|---|
| 1 | **MEGAFUSE článek** (cerny blok + Cu zlavicky s otvory) | Vysoce proudova pojistka/článek, Cu zlavicky | **Mimo pouzdro**, volny |
| 2 | **MEGAFUSE drzak/zakladna** (cerny plast + 2× M6 matice, CE — Wenzhou … Energy Technology) | Pouzdro mega pojistky, šroubové připojení | **Bez krytu**, pojistka nevložena |
| 3 | **EATON PL7 C16/1** (modre logo, bily) | 1p MCB, **křivka C, 16 A** | Volny, nezapojeny |
| 4 | **MCB B25** (rucne psano „FAS/F85“, černý páčkový ovladač, červena paska) | 1p, **křivka B, 25 A** — typ potvrzen z pole B25 | Volny, nezapojeny |
| 5 | **Noark Ex9FP** (zeleny pruh, oranzove ukazatele) | **2p**, 1000 V, **10×38 mm** valcove pojistky, art. **101767**, 36 A max | Volny; pojistky 20 A dle autora v zasobe |
| 6 | **Bily box s sroubovaci sběrnicí + EATON PL7 B32/1** | 1p MCB, **křivka B, 32 A**; box = bud budoucí minirazvadec nebo jiný účel | Volny, nezapojeny |

**Odpoved na O5:** B25 potvrzen jako MCB B 25 A/1; PL7C16/1 a PL7B32/1 potvrzeny jako EATON MCB (C16, B32); Ex9FP = Noark 2p 10×38; MEGAFUSE = držák + článek zvlášť (nekompletní sestava bez krytu).

**Nalezene odchylky vuci popisu autora:** zadna zasadni — inventura sedi; doplneno typove oznaceni z foto.

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

### 2.1e Provizorni AC — ZAPOJENO (author 2026-09-23)

**Topologie (realizovano):**

```
[Hybridni menic AC OUT]
   L, N ──► CYKYLO 3×2,5 mm² (Cu, z 30 m venkovni prodluzovacky, neposkozeny)
   PE  ──► symbol ZEME na menici
              │
              ▼
        [EATON PL7C16/1]  (1p, C 16 A)  ◄── modry vodic rozpojen a veden pres jistic
              │
              ▼
   ┌── Svorkovnice L/N ──┐
   │  Svorkovnice PE     │  (= "venecek", krabice s DIN listou)
   └──────────┬──────────┘
              │  CYKY 3×1,5 mm² (L/N/PE), dalka < 2 m
              ▼
        [1× zasuvka / kolík]  — zapojena VSECHNY 3 vodice (L, N, PE)
```

| Prvek | Hodnota | Poznamka |
|---|---|---|
| Hlavni usek | **CYKYLO 3×2,5 mm² Cu** | Stary neposkozeny vodic z 30 m prodluzovacky |
| Jistic | **EATON PL7C16/1** (1p, C 16 A) | V serii na **modrem (N)** vodicu — overeno meritkem (O10) |
| Svorkovnice | L/N + PE věneček, DIN krabice | Rozvadecove krabicky |
| Posledni usek | **CYKY 3×1,5 mm²**, <2 m | Na hraně pro 16 A; pro kratkej usek prijatelne |
| Zasuvka | 1× kolik, **vse 3 vodice** | PE=colik propojen |
| RCD/RCBO | **CHYBI** | **G13 stale otevreny — vysoka zavaznost** |

**Provozni limit (dokud neni RCBO):** max **~1500–1600 W** (nabijeni, svetlo, notebook). **NE** konvice, indukce, pila, hoblivka.

**O10 — meritka na zasuvce (author, multimetr, 2026-09-23):**

| Stav | Měření | Výsledek | Výklad |
|---|---|---|---|
| Jistič **ON** (provoz) | L–N | **~230 V** | Normální provozni napeti menice |
| Jistič **OFF** | **L–PE** | **~150 V** | **G14 POTVRZENO** — L ziva, jistič spíná N, ne L |
| Jistič **OFF** | **N–PE** | **~150 V** | N plovouci za rozpojenim; stejna hodnota jako L |
| Jistič **OFF** | **N–L** | **~0 V** | L i N na stejnem potencialu vuci PE (obe "jedou" z L / fantom) |
| drive (rano) | na zasuvce | ~30 V | Fantom bez zateze; po pripojeni zateze spadne |

**Interpretace 150 V při OFF (jistota P>0.8):**
1. **Nebezpecne** — dle CSN/IEC se bezpecny dotykove proud povazuje od **~50 V AC** v suchem prostredi; 150 V vůči PE je **jednoznacne nebezpecne** (i kdyby castecne fantom — chybet muze zatěžní schopnost, ne potencial).
2. **Proc 150 V a ne 230 V:** ostrovní výstup měniče byva **plovouci** (N neni pevne svazan s PE) + vysoka impedance DMM → kapacitni/kmitocova vazba, ne plna faze; rozdil L-PE vs L-N vysvetluje chybejici reference.
3. **N-L = 0 pri OFF:** N otevreny u jističe, oba vývody na zasuvce potencialove stejne vuci PE (spolecna vazba na L strane mene / fantom).
4. **Test fantom vs real:** připoj žárovku 40–60 W mezi L–PE (měnič ON, jistič OFF) — pokud zustane ~150 V pod zatizenim, jde o realni napeti; pokud spadne na ~0, byl to ghost. **Bezpečnější: předpokládat realni a neposahovat.**

**Bezpecnostni poznamky:**
- **G13 (RCD chybi):** stále priorita — dokoupit RCBO 16 A/30 mA typ A; do te doby pouze mala zatez + PE musi byt spojite (je).
- **G14 potvrzeno meritkem:** spinani na N — **přepojit na L (hnedy)**; pak pri OFF musi byt **L-PE = ~0 V**.
- Do opravy G14 je i „vypnuty“ stav **nebezpecny na dotyk** (L ziva vůči PE).

---

## 3. Inventura jistici techniky (fyzicky k dispozici, NEZAPOJENO krome SPB1)

| Polozka | Pocet / specifikace | Predpokladana role v nove instalaci |
|---|---|---|
| **SPB1-63Z C32** | 1 ks — **ZAPOJEN**; YQSHIPU, 2p, DC 500 V, 6000 A, IEC 60898-2, v boxu | Hlavni DC jistic FVE string 1 (detail viz §2.1d) |
| **EATON PL7C16/1** | 1 ks, C 16 A, 1p (foto §2.1c) | **ZAPOJEN** v provizorni AC vetvi (§2.1e) |
| **EATON PL7B32/1** | 1 ks, B 32 A, 1p (v bilem boxu se sběrnicí) | AC okruh vyssi zateze — B32 vyzaduje 2,5 mm²+ (G11) |
| **B25/1** | 1 ks, B 25 A, 1p (potvrzeno z foto) | AC okruh stredni zateze |
| **Noark Ex9FP 101767** | 1 pouzdro 2p 10×38 + 2× 20 A valcove pojistky (dle autora) | Dvoupolova pojistkova ochrana (umisteni neurceno) |
| **MEGAFUSE** | 1 držák (2× M6, CE) + 1 článek Cu — **bez krytu, článek mimo pouzdro** | DC bat/trunk — high-current dle AIC; doplnit 250 A článek |

**Stav:** Jistice **nejsou zapojeny** — fyzicky lezi v zasobe. Vyjimky: **SPB1 na FVE** (§2.1) a **EATON PL7C16/1 v provizorni AC** (§2.1e).

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
| G9 | **Otevreny kryt terminálu menice + montáž na holé dřevo bez skříně** (foto 2026-09-23) | Vysoka | Osadit kryt, průchodky, základní rozvaděč/box IP na stěnu; oddělit od hořlavé konstrukce dle požadavků |
| G10 | **Trunk 8 mm² DC battery vs. BMS 200 A / menič 80 A** — možné poddimenzování při plném odběru | Vysoka | Přepočítat I_valid pro 8 mm²; případně 16–25 mm² na BAT trunk + MEGAFUSE dle AIC |
| G11 | **AC výlev CYLY 3×1,5 mm²** — na hraně pro 3200 W; nelze krýt B32 | Stredni | Pro HIC 16 A OK; pro vetev 32 A 2,5 mm²; popsat barvy L/N/PE |
| G12 | **FV kabel panely→SPB1: 4 m 2×2,5 mm² CYLY** — CYLY neni solar/UV kabel; průřez na hraně pro Imp 2P2S | Vysoka | Nahradit UV solarnim kablem min. 4–6 mm² dle Imp + 1,25; CYLY jen pro AC |
| G13 | **Provizorni AC zapojena BEZ RCD/RCBO** (PL7C16 + 1 zasuvka, §2.1e) | **Vysoka — trva** | Dokoupit **RCBO 16 A/30 mA typ A** (1 modul) mezi menic a svorkovnici; do te doby jen mala zatez; trvale rozvadec M2 §5.4/§5.9 |
| G14 | **Jistic na N (modry) misto L (hnedy)** — pri OFF **L-PE ~150 V (O10 potvrzeno)** | **Vysoka — potvrzeno meritkem** | Prepojit spinani na **L**; po oprave overit L-PE pri OFF = ~0 V |

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
9. **Provizorni AC (REALIZOVANO 2026-09-23 — viz §2.1e):** Zapojeno: měnič → CYKYLO 3×2,5 → **PL7C16** → svorkovnice → CYKY 3×1,5 → 1 zasuvka. **Chybi RCBO (G13)** — primo mezi menic a svorkovnici doplnit **RCBO 16 A/30 mA typ A**; zároveň **prepnout spinani na L (G14)**. Provozni limit ~1500–1600 W, jen mala zatěž. Trvale = §5.4 rozvadec M2.

---

## 6. Otevřené položky — doplni autor (foto + meritka)

| ID | Co doplnit | Forma |
|---|---|---|
| O1 | Aktuální půdorys mistnosti 2 s polohou menice, LFP, BMS, rozvaděče | Foto + rozměr (pás měřítka nebo známá vzdálenost) |
| O2 | Detail zapojeni SPB1 63Z C32 — průřez vodičů, směr (±), skutečné označení | **HOTOVO — §2.1d (YQSHIPU SPB1-63Z C32, 2p, DC500V, 6000A); směr ±/stav ON-OFF doplnit pri dalsim odecitani** |
| O3 | Trasa silovych kabelu strecha→mistnost 2 (průřez, typ, délka) | **HOTOVO — ~4 m 2×2,5 CYLY panely→SPB1; ~4 m 2×4 Cu SPB1→menic (G12)** |
| O4 | Stav AC kabeláže po demontáži — co zůstalo ve stěnách, krabice, vesty | Foto mistnost 1 i 2 |
| O5 | Ověření typu B25/1 a PL7* (MCB vs. pojistková) | **HOTOVO — viz §3** |
| O6 | Aktuální tilt/orientace stringu 1 po premistění na strechu | **HOTOVO — pultova strecha, minimalni tilt (author 2026-09-23)** |
| O7 | SOC/napětí hlavní LFP a GoKWh v den revize | **HOTOVO — LFP 26,78 V; GoKWh 23,9 V nezapojena (2026-09-23)** |
| O8 | Dispozice zásuvek a spotřebičů, ktere se mají vratit do provozu | **CASTECNE — 1 provizorni zasuvka hotova (§2.1e); final seznam dale** |
| O9 | Detail AC výlevu u menice (kam jdou volne konce CYLY), PE continuity | **CASTECNE — PE na menici symbol ZEME, topologie §2.1e; zbyva overit L/N/PE na zasuvce multimetrem (cast O10) + foto** |
| O10 | Stav spinani pri OFF: je na zasuvce ziva L? (jistic na N) | **HOTOVO — meritka 2026-09-23: OFF L-PE ~150 V, N-PE ~150 V, N-L ~0 V; ON L-N ~230 V → G14 potvrzeno. Zbyva: PREPojit na L a overit L-PE pri OFF = 0** |

---

## 7. Revize dokumentu

| Datum | Změna | Autor |
|---|---|---|
| 2026-09-23 | V1.0 — vznik GT: author-live update (string1 strecha, GoKWh odpojena, inventura jisticu, SPB1), gap analyza, navrhove principy | outpost2026 + agent |
| 2026-09-23 | V1.1 — fotoproanalyza menic+BMS (§2.1b) a jisticu (§2.1c/§3), O5 hotov, G9–G11, trunk 8 mm² a AC 3×1,5 dimenze | outpost2026 + agent (photo-read) |
| 2026-09-23 | V1.2 — SPB1 foto §2.1d (YQSHIPU), trasa 4+4 m, tilt pultova/min, SOC 26,78/23,9, G12–G13, §5.9 provizorni 1 zasuvka; O2/O3/O6/O7 hotovo | outpost2026 + agent (photo-read) |
| 2026-09-23 | V1.3 — provizorni AC ZAPOJENO (§2.1e): CYKYLO 3×2,5 + PL7C16 + svorkovnice + CYKY 3×1,5 → 1 zasuvka; PL7C16 ve inventari = ON; G13 zustava, G14 spinani N misto L, O10 | outpost2026 + agent |
| 2026-09-23 | V1.4 — O10 meritka (OFF L-PE/N-PE ~150 V, N-L 0; ON L-N 230 V); G14 potvrzeno + zvysena na Vysoka; §2.1e presunuta zpet do §2 (struktura); interpretace 150 V nebezpecna | outpost2026 + agent |

---

*Poznamka RAG: Kanon pro „stav elektroinstalace Outpost pred revizi 2026“. Duplicity netvorit (P1). Pri nove generaci presunout tuto verzi do _ARCHIVE/ (P4). Navrh nove instalace se bude rozsirovat v ramci §5 po doplneni §6.*
