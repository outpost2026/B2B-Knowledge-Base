# OUTPOST ELEKTRO — GROUND TRUTH STAVU A ZADANI NOVE INSTALACE

**Datum:** 2026-09-23 | **Autor:** outpost2026
**Ucel:** Deterministicky popisat soucasny stav elektroinstalace objektu Outpost 2026 (revize pred zimou) a sluzit jako zaklad ground truth pro navrh nove instalace s vyuzitim zkusenosti zprovozu od zimy 2025.
**Verze:** 1.9 | **Status:** zive GT — doplnuje se foty a meritky autora | **Provenance:** source-read (Source_raw/Outpost_kontext_master + KB 04_ELEKTRO) + author-live-update 2026-09-23 (zapojeni, jistice, cislovani mistnost, provizorni AC, meritka O10, prohozeni AC OUT, uzavreni U1-U9) + photo-read 2026-09-23 (jistice.jpg, menic+BMS foto, SPB1 foto, AC output foto od autora) + sketchup-spatial-read 2026-09-23 (`cad2llm/examples/sketchup_model_v3.json`) + source-read IOT incident 2026-09-24 (§2.3 FAULT 02, reseni v OUTPOST_ELEKTRO_INFRASTRUKTURA.md)
**Tagy KB:** elektro, outpost, offgrid, FVE, LFP, BMS, jistenie, revize, ground-truth, spatial, sketchup, menic, fault02

---

## 0. Metodika a rozsah

**Kontext zadani:** Autor provadi revizi elektroinstalace pred zimnim obdobim. Dosud byly odstraneny veskere AC rozvody; system je ve stavu minimalni DC provozuschopnosti. Cil = ziskat ground truth soucasneho stavu (chyby koriguje autor formou popisu/fotografii s meritky) a navrhnout novou instalaci s vyuzitim rocnich zkusenosti s DIY off-grid provozem (zima 2025/2026).

**Zdroje:**
- Author-live-update 2026-09-23 (zapojeni stringu, mistnostni cislovani, inventura jisticu, topologie FVE jisticeni) — **priorita pred archivnimi daty**
- `Source_raw/Outpost_kontext_master/` (ingest_energeticky_uzel, FV_ingest_*, FV Diagnostic 2026-03-18, soupis, fyziko-env. profil, datasheet, JK_logs, Cornex health)
- **Spatial derivat (SketchUp → LLM-ready JSON):** `../cad2llm/examples/sketchup_model_v3.json` — půdorys M2, polohy prvků, metadata zone/energy/thermal/safety; pro deterministické plánování nové elektroinstalace a dispozičních úprav (viz §1.1)
- KB: `04_KNOWLEDGE_BASE/04_ELEKTRO/KVALIFIKACE_ELEKTRO_AGREGACE_2026-09-04.md`
- Reference navrhu: `Zakazky/Dodavka_Kuba_Sladek/elektro_schema_boxer.html` (normy, prurezy, RCBO)

**Omezeni:** Bez formalni §50 kvalifikace (viz KVALIFIKACE_ELEKTRO). Prace na VTZ/DS mimo rozsah. Toto je GT pro vlastni ostrovni objekt.

---

## 1. Objekt a mistnostni cislovani (oprava 2026-09-23)

| Mistnost | Plocha | Role (AKTUALNI definice autora) |
|---|---|---|
| **Mistnost 1** | 25 m2 | Pergola — nedokoncena, bez izolace, fólie Guttafol |
| **Mistnost 2** | **9,31 m²** (kanon dle autora; dříve zaokrouhleno 10) | **Energeticky a obytny uzel** — plne izolovane (7–10 cm MW), Battery Hub, kamna Priti Mini D, hlavni LFP + BMS + hybridni menic |

*Poznamka k revizi v1 (2026-09-23):* Puvodni zadani tasku uvadelo „mistnost 1 = obytna 10 m2“ — **nepravda**; kanon je **mistnost 2 = 10 m2 energeticky uzel**. Stary text v archivnich dokumentech (datasheet „Zona 1/2“) oznacuje pergolu jako Zonu 1 a utility uzel jako Zonu 2 — cislovani mistnosti vs zony se lisi, v tomto dokumentu plati tabulka vyse.

**Objekt:** dre stavba 7×5 m (35 m2 celkem), zaklady skvarobetonove patky, severni hrana 0,4 m pod terenem (hydroizolace nereshena). Lokalita: Drahanske udoli, Praha 8 — Dolni Chabry, 50.15087 N / 14.42343 E.

### 1.1 Spatial derivat Mistnosti 2 — SketchUp JSON (LLM-ready, 2026-09-23)

**Zdroj:** `../cad2llm/examples/sketchup_model_v3.json` (cad2llm, formát v3, jednotky m, export 2026-04-16, `mistnost_2_sk24_v2`).
**Učel:** Deterministický prostorový kontext pro plánování nové elektroinstalace (rozvaděč, trasy, vzdálenosti) a dispozičních úprav — bez nutnosti znovu číst foto. **Transform matrix: posledních 7 hodnot = placeholder, nepoužívat; orientace jen z origin/center/size.**

**Obálka M2 (půdorys 4,548 × 2,048 = 9,31 m² — kanon U1, výška stropu ~2,09 m):**

| Vrstva | Rozměr (m) | Poznámka |
|---|---|---|
| Podlaha dřevo | 4,55 × 2,05 × 0,02 | nad izolací |
| Izolace podlaha | 4,55 × 2,05 × 0,10 | Isover Domo, λ 0,038 |
| Izolace strop | 4,50 × 2,21 × 0,10 | + textilní podhled Guttafol 135 |
| Stěny izolace | 4 strany × 0,07 | minerální 7 cm |
| Stropní trám | 5,0 × 0,08 × 0,08 | překlad pozednice, výška ~2,0 |
| Vchod | 1,65 × 2,0 | východní stěna (y=2,0); **bez dveří — současná rekonstrukce (U4)**; model bez křídla odpovídá realitě |
| Okna | 2× jih (dvoj), 2× západ (dvoj) | bez rámu v modelu |

**Orientace stěn (author 2026-09-23, U5/U7 — kolmo ke světové straně):**
- **Delší osa M2 (x, 4,55 m) = směr SJ/JS** → x=0 = **sever** (vstup), x=4,5 = **jih** (kamna + okno).
- **Kratší osa (y, 2,05 m) = směr Z/V** → y=0 = **západ** (okna), y=2,0 = **východ** (vchod, energetický uzel).
- Názvy stěn v JSON jsou přesné (south wall = jižní atd.); transform-matrix placeholder se **nepoužívá**, orientace je dána jmény stěn.

**Prostředí M2 (author 2026-09-23, U8):** teplota **~25 °C**, RH **26 %** (den revize) — suchý režim, nízké riziko kondenzace; metadata modelu (postel 21 °C / 50 % RH) = **setpoint zóny, ne měření**.

**Shluk energetického uzlu — linie y ≈ 1,76–1,95 (u východní stěny):**

| Prvek | id | origin (x,y,z) | size (x,y,z) | metadata |
|---|---|---|---|---|
| Měnič HVM3.2H | 3354 | 1,79 / 1,90 / 1,075 | 0,27 × 0,10 × 0,35 | na stěně, z≈1,08–1,43 — AC OUT směrem dolů ke CB |
| Pracovní deska | 3347 | 1,52 / 1,76 / 0,745 | 2,26 × 0,20 × 0,05 | dřevo, tag Shelves |
| Police pod LFP | 3350 | 1,69 / 1,76 / 0,49 | 2,09 × 0,24 × 0,035 | pod deskou |
| Hlavní LFP 630 Ah | 3369 | 1,785 / 1,828 / 0,525 | 1,146 × 0,172 × 0,205 | **fire_risk=true**, min_distance 0,5 m, 5–35 °C; 16 článků (id 304–319) |
| GoKWh 100 Ah | 3353 | 2,055 / 1,76 / 0 | 0,525 × 0,24 × 0,22 | na podlaze pod deskou; 24 V / 100 Ah |
| Kamna Priti Mini D | 3349 | 3,99 / 1,61 / 0 | 0,43 × 0,31 × 0,68 | x≈4,2 (u jihu), zóna bed/stove, wood fuel |
| Postel | 3348 | 2,495 / 0 / 0 | 2,0 × 0,97 × 0,18 | zone sleep; socket_load 50 W; temp 21 °C |
| Stůl | 3351 | ~0 / 0,08 / 0 | 0,68 × 0,75 × 0,67 | u severu (x≈0) |

**Prostorové souvislosti s elektro GT:**
1. **Trasa provizorní AC (§2.1e):** měnič (z≈1,25) → CB → svorkovnice → zásuvka jde **pod pracovní deskou (z=0,745)** směrem k východu (y=2,0) — odpovídá foto (oranžový 3×2,5 nahoru ke CB, pak dolů).
2. **Umístění trvalého rozvaděče (§5.4/§5.9):** logicky **mezi měničem a vchodem** na východní stěně (y≈2,0), v linii energetického uzlu — minimální délky tras, mimo sever (G7 hydroizolace).
3. **Kamna (x≈4,2) vs. LFP (x≈1,8–2,9):** vzdálenost ~1,3–2,4 m > min 0,5 m; směr tepla/kouřovodu ověřit; postel ve stejné zóně jako kamna (bezpečnostní kontext G7/G9).
4. **Pergola (room#1, id 3377):** y=2,07–4,57 — **mimo M2**, venkovní prostor; neplést s elektro uzlem.
5. **Chybí v modelu (gaps U2/U3):** (a) **BMS a rozvaděč zatím nemodelovány** — poloha není ve spatial datu, doplnit do SketchUp; (b) **žádná elektroinstalační vrstva** (zásuvky, CB, SV, kabeláž) — GT §2.1e doplňuje derivát, ne naopak.
6. **GPS v JSON** (50,1509 / 14,4234) odpovídá lokalitě §1; **definition_name ";"** u jižní stěny = chyba exportu (U6 skip), použít instance_name.
7. **Délka AC trasy měnič→zásuvka celkem: GAP (U9)** — bude změřena; dosud jen úsekové odhady (&lt;1 m prohození + &lt;2 m poslední úsek).

**Otevřené spatial gaps (author 2026-09-23):**

| ID | Gap | Status |
|---|---|---|
| U2 | BMS + rozvaděč **nemodelovány** v SketchUp | Otevřeno — doplnit |
| U3 | **Bez elektrovrstvy** v modelu | Otevřeno — budoucí vrstva |
| U9 | Celková délka AC kabeláže | Otevřeno — změřit |

*Uzavřeno: U1=9,31 m² kanon; U4 dveřní prostor bez dveří = rekonstrukce; U5/U7 orientace stěn dle jmen, delší osa SJ; U6 skip; U8 ~25 °C / RH 26 %.*

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
| **AC rozvody 230 V** | **PROVIZORNI — 1× zasuvka, G14 OPRAVEN, BEZ RCBO** | Měnič AC OUT (**prohozené L/N u měniče**) → CYKYLO 3×2,5 → **EATON PL7C16/1 (nyní na L)** → svorkovnice DIN (můstky L/N popsány) → CYKY 3×1,5 (<2 m) → **1× zásuvka, vše 3 vodiče** — viz §2.1e; stále **bez RCD/RCBO (G13)** |
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

### 2.1e Provizorni AC — ZAPOJENO + G14 OPRAVENO (author 2026-09-23)

**Topologie (realizovano, po prohozeni AC OUT u menice):**

```
[Hybridni menic AC OUT]
   L  ──► MODRY vodic  (<1 m) ──► [EATON PL7C16/1] ──┐   ◄── spinany conductor = L (oprava G14)
   N  ──► HNEDY vodic  (<1 m) ───────────────────────┤
   PE ──► ZLUTOZLENY (GD/SE) ────────────────────────┤
                                                      ▼
                                    ┌── Svorkovnice DIN (2 sockety, 2 mustky) ──┐
                                    │  mustky popsany fixou: symbol N a L       │
                                    └──────────────────┬─────────────────────────┘
                                                       │  CYKY 3×1,5 mm² (L/N/PE), dalka < 2 m
                                                       ▼
                                              [1× zasuvka / kolík]
                                              hnědá=L, modrá=N, ŽZ=PE
```

| Prvek | Hodnota | Poznamka |
|---|---|---|
| Hlavni usek | **CYKYLO 3×2,5 mm² Cu** | Z 30 m venkovni prodluzovacky, neposkozeny |
| Prohozeni u menice | **L=modra, N=hneda** (jen <1 m od AC OUT) | **Ucelena zmena pro G14** — spinany vodic = L |
| Jistic | **EATON PL7C16/1** (1p, C 16 A) | **Nyni na L (modry vodic)** — G14 OPRAVENO |
| Svorkovnice | DIN box, 2 sockety, **2 můstky** | Můstky **popsány fixou** symbolem N/L pro orientaci |
| Posledni usek | **CYKY 3×1,5 mm²**, <2 m | hnědá=L, modrá=N, ŽZ=PE — korektni barvy k zasuvce |
| Kryty boxu | **CHYBI** — 2× DIN box otevřený, PE věneček na holém dřevě | **G15 novy — vysoka zavaznost** |
| RCD/RCBO | **CHYBI** | **G13 stale otevreny — vysoka zavaznost** |

**Photo-read AC output (author foto 2026-09-23):**

| Prvek na foto | Popis | Jistota |
|---|---|---|
| Měnič | POW-HVM (SOLAR INVERTER CHARGER), display, INV/CHG LED; **spodní kryt terminálů ODEBRANÝ** (G9) | P>0.95 |
| Oranžový kabel | **3×2,5 mm² CYLY** (oranžový plášť) — z terminálů měniče nahoru ke CB | P>0.9 |
| Levý DIN box | **EATON PL7C16/1** (C16), 1p; oranžový vstup, černý/modrý výstup; **bez krytu** | P>0.95 |
| Prostřední prvek | **PE věneček** (kroužková svorkovnice, ~8 šroubů) — ŽZ + hnědý vodic; **montáž přímo na holé dřevo, bez boxu** | P>0.9 |
| Pravý DIN box | **Svorkovnice s můstky** (zelený + modrý blok), **N L** popsáno fixou na krabici; hnědý + modrý vodiče od CB; **bez krytu** | P>0.95 |
| Výstup dolů | **CYKY 3×1,5 hnědý** → zásuvka (celá trasa mimo záběr) | P>0.9 |
| Montáž | Vše na **holé dřevěné stěně** (prkna), žádný IP rozvaděč, žádné průchodky | P>0.95 |

**Provozni limit (dokud neni RCBO):** max **~1500–1600 W** (nabijeni, svetlo, notebook). **NE** konvice, indukce, pila, hoblivka.

**O10 — meritka na zasuvce (author, multimetr, 2026-09-23):**

| Stav | Měření | Výsledek | Výklad |
|---|---|---|---|
| Jistič **ON** (provoz) | L–N | **~230 V** | Normální provozni napeti menice |
| Jistič **OFF** (PRED opravou) | L–PE / N–PE | **~150 V / ~150 V** | G14 potvrzeno — spinani na N, L ziva |
| Jistič **OFF** (PO oprave, prohozeni) | **L–PE** | **~35 V** | Výrazný pokles — L nyní přerušena jističem; zbytkový fantom |
| Jistič **OFF** (PO oprave) | **N–PE** | **~35 V** | Stejná hodnota jako L–PE — plovoucí/bez reference |
| Jistič **OFF** (PO oprave) | **L–N** | **~0 V** | Oba vývody potenciálově stejné vůči PE (fantom) |
| Jistič **ON** | L–N | **~230 V** | Provérka OK |

**Interpretace 35 V po opravě (jistota P>0.85):**
1. **Pokles 150→35 V potvrzuje, že jistič nyní přerušuje L** — hlavní účel opravy G14 splněn.
2. **35 V je stále fantom** (vysoká impedance DMM, plovoucí výstup měniče bez pevného N–PE svazku) — pod hranicí běžného nebezpečí v suchu (~50 V), ale **raději ověřit zátěží**: žárovka 40–60 W L–PE při OFF; měla by zhasnout / U spadnout na ~0.
3. **Bez RCBO (G13) zůstává ochrana osob nedostatečná** — 35 V fantom neopravňuje k dotyku svorek; při poruše může být na L plných 230 V.
4. **Doporuceni:** po dokoupení RCBO přeměřit OFF L–PE; s RCBO + opraveným L by mělo být ~0 V bez fantomu (RCBO/PE svazek).

**Bezpecnostni poznamky:**
- **G14 OPRAVENO (2026-09-23):** prohozeno AC OUT u měniče (L=modrá na jističi); spinany vodic = L. Ověřeno měřením (OFF L-PE ~35 V vs. predchozích ~150 V).
- **G13 (RCD chybi):** stále priorita — dokoupit RCBO 16 A/30 mA typ A; do te doby pouze mala zatez + PE musi byt spojite (je).
- **Barvy:** u měniče <1 m prohozeny (modrá=L); od svorkovnice korektní (hnědá=L). Můstky na SV popsány fixou.

### 2.3 Provozni zdravi menice — incident FAULT 02 (kontext 2026-07-25, overeno 2026-09-24)

**Kanon pro zive detaily EL infrastruktury (zdravi zaizeni, incidenty, monitoring):** `OUTPOST_ELEKTRO_INFRASTRUKTURA.md` (EL03). Tato sekce je pouze krizovy tahak uvnitr GT stavu.

| Polozka | Hodnota |
|---|---|
| Zarizeni | POW-HVM3.2H-24V-N, 3200 W — **srdce EL layeru** (jediny zdroj AC 230 V + nabijeci cesta z FV) |
| Incident | 2026-07-25: opakovane FAULT 02 po 7 dnech s vadnou konvici 2 kW (term. sok); po ocisteni **FAULT 02 trva za 10–13 min i pri 50–250 W** |
| FAULT 02 (OEM HVM11KP) | "Over temperature or NTC is not connected well" |
| Revidovana diagnóza v2.1 | **Rds(on) degradace H-bridge MOSFETu** (kalcel: +25 % ≈ +10 °C case) + **pasivni chlazeni pri nizke zatezi** (ventilator load-based, start >600 W); NTC pravdepodobne degradovany tepelny kontakt |
| Potvrzeno | prach/vyteceno (vycisteno); ventilator OK pri 1 kW (46→39 °C); konstantni cas do faultu |
| NEpotvrzeno (blokuje verdikt) | T01 NTC odpor (multimetr); T02 skutecna teplota heatsinku (DS18B20: >90 °C = Rds(on), <60 °C = vadny NTC) |
| Plny zdroj | `Repozitar_Dev/IOT/report_incident_POW-HVM3.2H-24V_2026-07-25.md` (mimo KB — shrnuto v EL03) |
| Dopad na zimu | Thermal monitoring (DS18B20 T02) = CRITICAL pred provozem pod zatizi; viz §5.6/§5.7 |

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
| G14 | ~~Jistic na N misto L~~ — **OPRAVENO 2026-09-23** prohozenim AC OUT u menice | **UZAVRETO** | Spinany vodic = L (modra <1 m); overeno: OFF L-PE ~35 V (pred ~150 V); ON L-N 230 V |
| G15 | **Otevřené DIN boxy bez krytů + PE věneček na holém dřevě** (foto AC output 2026-09-23) — 2× svorkovnicový box přístupný, věneček bez krytu | **Vysoka — nova** | Osadit kryty DIN boxů; věneček do IP boxu; celé do rozvaděče IP na stěnu (navazuje G9) |

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
9. **Provizorni AC (REALIZOVANO + G14 OPRAVENO 2026-09-23 — viz §2.1e):** Zapojeno: měnič (**prohozené L/N u AC OUT**) → CYKYLO 3×2,5 → **PL7C16 na L** → svorkovnice DIN (můstky popsány) → CYKY 3×1,5 → 1 zasuvka. **G14 hotovo** (OFF L-PE ~35 V). **Chybi RCBO (G13)** — primo mezi menic a svorkovnici doplnit **RCBO 16 A/30 mA typ A**. Provozni limit ~1500–1600 W, jen mala zatěž. Trvale = §5.4 rozvadec M2.

---

## 6. Otevřené položky — doplni autor (foto + meritka)

| ID | Co doplnit | Forma |
|---|---|---|
| O1 | Aktuální půdorys mistnosti 2 s polohou menice, LFP, BMS, rozvaděče | **CASTECNE — spatial derivat §1.1: půdorys 9,31 m², menic/LFP/GoKWh/kamna/stul; **chybí BMS+rozvaděč (U2 gap)**; doplnit do SketchUp + foto s měřítkem** |
| O2 | Detail zapojeni SPB1 63Z C32 — průřez vodičů, směr (±), skutečné označení | **HOTOVO — §2.1d (YQSHIPU SPB1-63Z C32, 2p, DC500V, 6000A); směr ±/stav ON-OFF doplnit pri dalsim odecitani** |
| O3 | Trasa silovych kabelu strecha→mistnost 2 (průřez, typ, délka) | **HOTOVO — ~4 m 2×2,5 CYLY panely→SPB1; ~4 m 2×4 Cu SPB1→menic (G12)** |
| O4 | Stav AC kabeláže po demontáži — co zůstalo ve stěnách, krabice, vesty | Foto mistnost 1 i 2 |
| O5 | Ověření typu B25/1 a PL7* (MCB vs. pojistková) | **HOTOVO — viz §3** |
| O6 | Aktuální tilt/orientace stringu 1 po premistění na strechu | **HOTOVO — pultova strecha, minimalni tilt (author 2026-09-23)** |
| O7 | SOC/napětí hlavní LFP a GoKWh v den revize | **HOTOVO — LFP 26,78 V; GoKWh 23,9 V nezapojena (2026-09-23)** |
| O8 | Dispozice zásuvek a spotřebičů, ktere se mají vratit do provozu | **CASTECNE — 1 provizorni zasuvka hotova (§2.1e); final seznam dale** |
| O9 | Detail AC výlevu u menice (kam jdou volne konce CYLY), PE continuity | **HOTOVO — topologie §2.1e, PE symbol ZEME, můstky SV popsány; barvy korektni od SV** |
| O10 | Stav spinani pri OFF: je na zasuvce ziva L? (jistic na N) | **HOTOVO — pred opravou OFF L-PE ~150 V (G14); po prohozeni AC OUT: OFF L-PE/N-PE ~35 V, N-L 0; ON L-N 230 V → G14 UZAVRETO** |

---

## 7. Revize dokumentu

| Datum | Změna | Autor |
|---|---|---|
| 2026-09-23 | V1.0 — vznik GT: author-live update (string1 strecha, GoKWh odpojena, inventura jisticu, SPB1), gap analyza, navrhove principy | outpost2026 + agent |
| 2026-09-23 | V1.1 — fotoproanalyza menic+BMS (§2.1b) a jisticu (§2.1c/§3), O5 hotov, G9–G11, trunk 8 mm² a AC 3×1,5 dimenze | outpost2026 + agent (photo-read) |
| 2026-09-23 | V1.2 — SPB1 foto §2.1d (YQSHIPU), trasa 4+4 m, tilt pultova/min, SOC 26,78/23,9, G12–G13, §5.9 provizorni 1 zasuvka; O2/O3/O6/O7 hotovo | outpost2026 + agent (photo-read) |
| 2026-09-23 | V1.3 — provizorni AC ZAPOJENO (§2.1e): CYKYLO 3×2,5 + PL7C16 + svorkovnice + CYKY 3×1,5 → 1 zasuvka; PL7C16 ve inventari = ON; G13 zustava, G14 spinani N misto L, O10 | outpost2026 + agent |
| 2026-09-23 | V1.4 — O10 meritka (OFF L-PE/N-PE ~150 V, N-L 0; ON L-N 230 V); G14 potvrzeno + zvysena na Vysoka; §2.1e presunuta zpet do §2 (struktura); interpretace 150 V nebezpecna | outpost2026 + agent |
| 2026-09-23 | V1.5 — G14 OPRAVENO prohozenim AC OUT u menice (L=modra na jistici); nove meritka OFF ~35 V (z 150), ON 230 V; svorkovnice DIN s popsanymi mustky; O9/O10 HOTOVO | outpost2026 + agent |
| 2026-09-23 | V1.6 — photo-read AC output: potvrzena topologie (EATON C16, 2 DIN boxy, PE věneček, mustky N/L, CYLY 3×2,5+3×1,5); **novy G15** (otevrene boxy bez krytu, věneček na holém dřevě); navazuje G9 | outpost2026 + agent (photo-read) |
| 2026-09-23 | V1.7 — **§1.1 spatial derivat** ze sketchup JSON (cad2llm): půdorys M2 4,55×2,05, linie energetického uzlu y≈1,76–1,95, metadata LFP/kamna/postel, odkaz na zdroj; O1 částečně hotovo | outpost2026 + agent (sketchup-spatial-read) |
| 2026-09-23 | V1.8 — uzavreni U1–U9 (author): plocha **9,31 m² kanon**, orientace stěn dle jmen (delší osa SJ), dvere = rekonstrukce, ~25 °C/RH 26 %; gaps U2 (BMS/rozvaděč nemodelován), U3 (bez elektrovrstvy), U9 (délka AC trasy) | outpost2026 + agent |
| 2026-09-24 | V1.9 — **§2.3 provozni zdravi menice (FAULT 02)**: krizovy tahak incidentu 2026-07-25, odkaz na novy zivy kanon EL03 `OUTPOST_ELEKTRO_INFRASTRUKTURA.md` (srdce EL layeru, monitoring, katalog zařízení) | outpost2026 + agent |

---

*Poznamka RAG: Kanon pro „stav elektroinstalace Outpost pred revizi 2026“. Duplicity netvorit (P1). Pri nove generaci presunout tuto verzi do _ARCHIVE/ (P4). Navrh nove instalace se bude rozsirovat v ramci §5 po doplneni §6. Zive EL zařízení/zdraví/incidenty = EL03 OUTPOST_ELEKTRO_INFRASTRUKTURA.md (nedatovaný, trvalý).*
