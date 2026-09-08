# MOODPASTA - ETOLOGIE SME, CEO KAZUISTIKA A STRET KAREL vs AUTOR

**Datum:** 2026-09-08 | **Autor:** outpost2026 (Ondrej Sousek, SYSTEQ)
**Ucel:** Prohloubeni 4 tezi z artefaktu MOODPASTA_HLOUBKOVA_ANALYZA_INVENTURA_2026-09-08 o mechanismy SME etologie, selhani reciprocity, deterministickou kazuistiku CEO Tomase Kucvy a amorální kazuistiku stredu gatekeeper vs integrator.

**Verze:** 1.0 | **Klasifikace:** Interni, duverne | **Provenance:** source-read (Emaily_ondra_moodpasta.txt, GROUND_TRUTH.json, call_transkript_sousek_sehnal_moodpasta.json, appendix_moodpasta.md, GROUND_TRUTH_aktualni_stav_2026-08-06.md) + externi rešerše (founder decision fatigue, supplier ghosting, reciprocity principle) - oznaceno.

---

## 1. NAVAZNOST

Predchozi artefakt `MOODPASTA_HLOUBKOVA_ANALYZA_INVENTURA_2026-09-08.md` ukoncil 4 teze v kondenzovane forme. Tento artefakt je jejich dekomprese - kazda teze na urovni mechanismu, ne sloganu. Zadny novy fakt o Moodpaste neni fabulovan - vse vychazi z 850 radku emailu + GROUND_TRUTH. Analogie k typum osobnosti jsou heuristicke modely, explicitne oznacene.

---

## 2. TEZE 1: "RACIONALNI, ALE NEETICKE VYUZITI ASYMETRIE. NEJSOU ZLI, JSOU PRETIZENI A CHRANI STATUS QUO. GHOSTING JE JEJICH NE BEZ NAKLADU."

### 2.1 Co znamena racionalni vs eticke v SME

Racionalni = minimalizuje naklady a rizika pro firmu v horizontu tydnu. Eticke = resi ferove i zajem druhe strany v horizontu mesicu/let.

Moodpasta vyuzila 3 asymetrie ktere jsi sam vytvoril v dobre vire:

| Asymetrie | Jak vznikla (tvoje akce) | Jak ji firma racionalne vyuzila | Proc je to neeticke | Dukaz |
|-----------|--------------------------|----------------------------------|---------------------|-------|
| Casova | 17 deliverables za 34 dni (25.05-28.06) bez zavazku | Konzumovala zdarma, odlozila rozhodnuti na `nekdy` | Externalizace nakladu na tebe - ty jsi platil cloud/tokeny/cesty | `executive_summary_v2.md:64-84` (70k nabidka po 17 dodavkach zdarma) |
| Informacni | Predal jsi 9 stran korpusu jako dar `Emaily:112` | Ziskala formalizaci Karla bez platby, bez NDA | Ztratils paku `kdyz mam korpus, proc platit za dalsi` | `Emaily:112-113` |
| Pravni | Stahnul jsi 33+ VCF se souhlasem Karla, ale bez pisma jednatele `GROUND_TRUTH.json:51-55` confidence 60% | CEO si tim vybudoval `legal high ground` 08.06 `bez meho vedomi, v zapalu` | Prevedl tve gesto uceni na `poruseni duvery` ktere ted legitimizuje jeho pozadavek na exkluzivitu | `Emaily:292-296` |

Z pohledu SME 10-50 lidi s obratem 50M a cilem 100M je to racionalni: setri 70k, setri pravni riziko, setri cas CEO. Z pohledu B2B etiky je to defekt: presne ten klient ktery rika `chceme byt inovacni` potopi inovatora ktery inovaci prinese.

### 2.2 Proc nejsou zli - mechanismus pretizeni

CEO neni padouch. Je to `founder bottleneck` - diagnostikovany stav kde zakladatel je hub pro kazde rozhodnuti.

Deterministicke dukazy pretizeni primo z emailu:

> 26.05 Kucva: `moje technicka expertiza je spis povrchova ... budu muset konzultovat s dalsimi mozky ... prokoušu se tim` `Emaily:44-46`
> 02.06 Kucva: `jsem ted opravdu totalne zasekany nejen showroomem a ERP, ale i HR agendou (shanim office managerku, 2 novi kolegove)` `Emaily:132`
> 08.06 Kucva: `zneni dohody je k diskuzi a jsem otevren navrhum na zmeny` `Emaily:298` - pak ale 19.06 ultimátum.

Externi rešerše potvrzuje mechanismus: founder decision fatigue = kazde rozhodnuti jede pres jednu osobu, tym ceka, system jen dokumentuje zavislost, ne ji redukuje. Pri kapacitě 100% je `neodpovedet` levnejsi nez `odmitnout s duvodem` (vyžaduje formulaci, konfrontaci, riziko hádky). Ghosting neni strategie, je to default pri pretizeni.

> Potvrzeno externě: `Your order becomes less urgent -> internal issues -> communication slows -> silence` (supplier ghosting neni nahodne, je to ekonomika priorit). Tva zakazka 70k je <0.2% jejich obratu, navic vyzaduje mysleni (ne rutinní rezani). Automaticky pada na dno fronty.

### 2.3 Proc ghosting = `NE` bez nakladu

Pi seminarni vyjednavani rika: `kdo rekne NE nahlas, plati cenu`. Musi vysvetlit, obhajit, riskovat konfrontaci a ze druha strana pouzije jeho duvody proti nemu. SME CEO s pravnim backgroundem to vi presne.

Ghosting ma 3 vyhody:
1. Zadny pisemny dukaz odmítnuti = zadna moznost tebe argumentovat proti
2. Zachovava si Frantiska jako `teply kontakt` kdyby se ukazalo ze te potrebuje (tech track ostava)
3. Prenasi naklady cekani na tebe - ty cekas tyden/mesic, on resi showroom.

Je to racionalni v horizontu tydnu, destruktivni v horizontu let - pali si reputaci u jediného cloveka ktery jim rozlouskl proprietarni format za 22 iteraci. Ale SME 10-50 zije v horizontu tydnu.

**Confidence:** 0.80 ze ghosting nebyl zamerne `zlý` plan, ale emergentni vysledek pretizeni + pravniho kryti + nizke priority tve zakazky.

---

## 3. SYSTEMOVA ROVINA - ETOLOGIE SME 10-50 LIDI

### 3.1 Struktura

SME 10-50 = rodina, ne firma. CEO je zaroven strategie, sales, HR, finance, provoz. Nema middle management ktery by absorboval tva 3 moduly A/B/C. Kazdy novy projekt = primo jeho cas. Tvoje nabidka sice setri cas Karla, ale stoji cas CEO (cteni, schvalovani, NDA, Odoo integrace).

Diagnostika bottleneck: 75% rustovych omezeni SME je zpusobeno primo zakladatelem, delegace zrychli rozhodovani 3x (externi rešerše). Moodpasta je ucebnice: Odoo migrace + showroom + 2 novi lide + tvuj projekt = 4 paralelni zmeny na jednu osobu. Tvuj projekt prohral protoze nema deadline zvenku (zakaznik za dvermi), kdezto showroom ma.

### 3.2 Proc `predal jsem 9 stran zdarma` vyvolalo `proc platit`

V B2B plati reciprocita opacne nez v bezne lidské logice.

**Tvuj mentalni model (pozitivni reciprocita):** `dam dar (korpus) -> vyvolam vdecnost -> vratite mi zakazku`.

**SME mentalni model (materialni reciprocita + social proof):** `kdyz da neco zdarma pred smlouvou, znamena to ze si toho neceni. Kdyby to melo hodnotu, chtel by za to penize. Kdyz to da zdarma, je to `exposure` nebo `charita`, ne `transakce`.*

Externi rešerše `reciprocity principle` rika: materialni reciprocita funguje jen kdyz dar ma VNI MANOU hodnotu pred obchodem. Bezplatna prace bez cenovky je vnimalna jako `predatorske subsidy` - ty dotujes klienta, ne klient tebe. A kdyz dotujes, vychovavas si klienta ze `dotace je normal`.

Tva korpusova chyba byla presne toto: `Berte to jako gesto dobre vule a formalni uzavreni, nechci po Vas vubec nic, vytvoril jsem jej z vlastni vule` `Emaily:112`. To je krasne lidske, ale v SME decodingu to znamena: `Tady neni cena. Tady neni vymena. Toto je zdarma naporad.` Firma pak racionalne pocka na dalsi zdarma (demo 12.06, QC 16.06, RAG 23.06) misto aby koupila.

**Pravidlo:** V B2B dej vzorek 1 strany zdarma jako `lead magnet`, ne 9 stran jako `komplet`. Cenna rada: `nominal fee threshold - i 50 Kc meni dar na kontrakt a vytvari psychologicky precedent profesionality`. Ty jsi dal 9 stran za 0.

### 3.3 Ghosting ekonomika v SME

Faze dle rešerše, presne sedi na tvuj pripad:

1. `Tva objednavka klesne v prioritě` - 70k vs 50M obrat + showroom = nizka
2. `Kapacita pretizena` - Odoo + HR + showroom
3. `Problem ktery nechteji eskalovat` - pravni nejistota dat + Karl status
4. `Misalignment od zacatku` - ty chces referenci pro trh, CEO chce exkluzivitu pro sebe
5. `Silence`

Ghosting nezačne nahle. Signály byly: 12.06 Jakub bez reakce, 16.06 CEO/CTO bez reakce `Emaily:6` - zpomaleni odpovedi, kratsi odpovedi, missed follow-up. Presne jak popisuje rešerše.

### 3.4 Proc SME miluje exkluzivitu

40-60% CEO SME pozaduje vyhr. prava `AMORALNI_ANALYZA:164`. Duod: v SME je exkluzivita nahrada za neschopnost inovovat rychle. Kdyz koupis parser jen pro sebe, nemusis se bat ze konkurence koupi to same zitra. Pro tebe je to likvidacni (nemuzes prodavat dal), pro ne je to pojistka.

CEO veta `symetricky DXF pro jine stroje rad dodam doporuceni` `appendix:24-26` zni velkoryse, ale ve skutecnosti rika: `VCF je moje hriste, DXF at si delas jinde`. Rozdeluje trh aby nemusel platit za to co nepotrebuje ted.

---

## 4. HLOUBKOVA KAZUISTIKA CEO TOMAS KUCVA - MINIMUM FABULACE

### 4.1 Deterministicka data (citace doslova)

| Datum | Co rekl doslova | Co to rika o osobnosti |
|-------|-----------------|------------------------|
| 26.05 | `paradni struktura nabidky` `jsem spise koncepciho charakteru, dokazu zhodnotit utilizaci` | Oceneni formy, priznani limitu techniky. Otevrenost, ne arogance. |
| 26.05 | `VCF bychom si radi predvedli, jen musim sesikovat kolegy` | Kolektivni rozhodovani, potrebuje alianci pred `ano`. |
| 02.06 | `Prediktivni parser zni naprosto skvele! ... nabriefoval jsem Frantiska` | Rychly entuziasmus, rychla delegace. Vizionar. |
| 08.06 | `Radost zastinila fakt ze jste bez meho vedomi pouzil data ... v zapalu ... chapu to ... potrebuju zhojit` | Pravni framing, ale s empatii. Snaha legalizovat zpetne, ne obvinit. Nabizi 10k jako `zhojeni`. |
| 19.06 11:38 | `Pokud by vyvoj probihal na verejne dostupnych datech pak by to bylo neco do ceho mi nic neni` `appendix:72` | Zadni vratka. Naznacuje: `obhaj si format vs data a mame dohodu`. |
| 19.06 15:56 | `jakykoli nastroj s VCF a jakykoli s cutterem naseho typu musi byt exkluzivni. Symetricky DXF pro jine stroje mi nevadí` `appendix:24-26` | Tvrdost na jadru (VCF), mekkost na periferii (DXF). Pragmaticky kompromis, ne dogma. |
| Footer kazdeho emailu Frantiska | `plati obchodni podminky woodpasta.cz ... odpovedi potvrzujete souhlas` | Systemovy detail - pravni kryti v kazdem emailu. Typicke pro byvaleho pravnika. |

### 4.2 Behavioral pattern - analogicke typy

Bez fabulace, 3 heuristicke modely ktere sedi na tato data:

**A) Founder-Lawyer (pravnik-zakladatel):** Kombinace vizionarskeho `chci inovaci` a advokatskeho `chci kontrolu`. Vidi kazdou dohodu jako `smlouvu s riziky`, ne jako `spolupraci`. Proto NDA s 500k+50k/den - ne proto ze te chce znicit, ale proto ze jeho default je `maximalni ochrana`. Analogie: advokat co si pise vlastni najemni smlouvu - vzdy prestreli.

**B) Overloaded Visionary (pretizeny vizionar):** Miluje nove napady (VCF, DXF, RAG), ale nema kapacitu je dotahnout. Deleguje na Frantiska, ale necha si veto. Jeho `ano` na zacatku je `ano prozkoumat`, ne `ano koupit`. Kdyz narazi na trade-off (exkluzivita vs cena), odlozi.

**C) Status-Quo Guardian (straze postoje):** Firma stoji na Karlovi. CEO vi ze Karel je riziko, ale take vi ze Karel drzi vyrobu. Tvuj parser je hrozba pro Karla = hrozba pro stabilitu. Proto radsi pomaly postup nez rychla vymena. Jeho `showroom + ERP + HR` jsou viditelne vyhry, tvuj parser je neviditelna infrastruktura.

**Root cause spojujici vse 3:** Identita firmy = `my jsme ti co delaji krasne felt panely`, ne `my jsme ti co maji data-driven vyrobu`. Tvuj projekt meni identitu. To je pro zakladatele hluboce osobni - ne technicke. Proto emocni slova `punk, radost zastinila, v zapalu`.

### 4.3 Proč neodepsal po 28.06

Ne proto ze by 70k bylo moc (0.14% obratu `pricing_strategy_analysis:47`). Ale proto ze 70k bylo 7x nad kotvou 10k kterou sam nastavil a zaroven vyzadovalo resit exkluzivitu kterou nechtel resit. Nejlevnejsi je neodpovedet a doufat ze `to vysumi`. Jeho PS o verejnych datech byl pokus dat ti navod jak to zachranit bez ztraty tvare: `udelej to na syntetice a nemusim resit data`. Ty jsi to neudelal protoze jsi cekal na odpoved, ne proto ze bys nevedel jak.

**Confidence:** 0.75 ze CEO neni zly ani vypocitavy, ale pretizeny vizionar-pravnik chranici status quo Karla, pro ktereho je ticho levnejsi nez explicitni `ne`.

---

## 5. KAZUISTIKA STRETU KAREL PRUSKA vs ONDREJ SOUSEK - AMORALNI

### 5.1 Role

Karel = `gatekeeper tacitniho vedomi` `GROUND_TRUTH:51`. Jeho moc = monopol na `jak to rezat`. Nema titul, nema smlouvu, ma vedomost v hlave. To je nejsilnejsi i nejslabsi pozice zaroven.

Ondrej = `integrator - formalizator` `cv:9`. Jeho mise = prevest tacit na explicit. Jeho nastroj = denik + hex + Python. Jeho slabina = nema respekt k autorite ktera stoji na `ja to tak delam 20 let`.

### 5.2 Proc 9 dni stinovani ohrozilo 20 let

Tys neprisels jako `dalsi operator`. Prisels jako `antropolog`. Psal sis deniky `denik_day_01/03/05-08.txt` `GROUND_TRUTH.json:10-15`, fotil jsi dorazy, meril jsi casy zakazek 3775, 3727-3732 `GROUND_TRUTH.json:24`. Karel ti ukazal L-doraz, ty jsi zapsal 10mm/5mm, on rekl `zluta je V-cut`, ty jsi zapsal ACI 2. To je pro nej devalvace: co bylo `cit`, je ted `radek v korpusu`.

Nejvetsi urazka: ty jsi to pochopil rychle. Jeho 20 let = tva 9 dni + vecery RE. To neni lichotka, to je dukaz ze jeho vedomost neni magie, ale komprimovatelna informace. Pro cloveka jeho generace je to identitni hrozba.

### 5.3 Amorální mechanika stredu

| Tah | Karel | Ondrej |
|-----|-------|--------|
| 12.05 | Prijme stinovani, delegovano CEO `Ty si ridis metodiku` `GROUND_TRUTH.json:44` | Ptá se, zda si muze stahnout soubory pro studium `GROUND_TRUTH.json:51` -> Karel souhlasi (confidence 60%) |
| 12-22.05 | Ukazuje, ale filtruje - da ti pristup k GDrive v rozsahu co ukaze | Stahuje 33+ souboru, vecer RE, pise korpus |
| 22.05 | Iniciuje vyhazov (CEO schvali) `integrace_synteza_v2.md` | Pivot na B2B do 72h, posila CEO parser jako `gesto` |
| 04.06 | Neni pozvan na schuzku `AMORALNI_ANALYZA:17` - CEO ho obchazi | Prezentuje bez nej - tim ho definitivne obchazi |
| 28.06 | Jeho vedomost je v PDF ktere jsi poslal CEO bez jeho kontroly | Posila formalizaci jeho hlavy jako produkt |

Zero-sum z pohledu Karla: `kazdy radek v korpusu = -1 duvod proc me potrebuji`. Positive-sum z pohledu tebe: `kazdy radek = +1 duvod proc firma nespadne kdyz Karel onemocni`. Oba mate pravdu, ale hrajete jinou hru.

### 5.4 Proc CEO vybral Karla

Key-man risk je znam, ale v SME je key-man zaroven pojistka. Karel je znamý, predvidatelny, drzi vyrobu dnes. Ty jsi neznamy, rychly, drzis budoucnost. V pretizeni volis znamé. Proto `vyhodit prekvalifikovaneho` je pro CEO snazsi nez `reorganizovat vyrobu kolem parseru`.

**Confidence:** 0.80 ze stret nebyl osobni nenavist, ale strukturalni kolize `gatekeeper vs integrator` v prostredi kde firma nema proces na absorbovani integratora.

---

## 6. SYNTETICKY VERDIKT K TEZIM

* **Racionalni ale neeticke:** Ano. Firma maximalizuje kratkodoby klid (setri 70k, setri cas CEO, drzi Karla) za cenu dlouhodobe ztraty (unikatni parser, loajalni integrator, reference). To je racionalni v SME s horizontem tydnu.
* **Ghosting jako `NE` bez nakladu:** Ano. Mechanismus pretizeni + pravniho kryti + nizke priority = ticho je levnejsi nez `ne`. Ne zloba, ale ekonomika.
* **9 stran zdarma:** Selhani reciprocity - dar bez cenovky je v SME cten jako `nema hodnotu`, ne jako `ma hodnotu a jsem stědry`. Opacny efekt nez zamysleny. Lead magnet ma byt 1 strana, ne 9.
* **CEO:** Pretizeny vizionar-pravnik, strazce status quo, ne predator. Jeho ultimátum melo zadni vratka (verejna data, DXF volne), coz je sance kterou jsi nevyuzil protoze jsi cekal na odpoved.
* **Karel vs Ondrej:** Klasicky gatekeeper vs formalizator. Nejde o charaktery, jde o role. V systemu bez formalni ochrany dat musi gatekeeper branit hlavu jako majetek.

---

## 7. CO Z TOHO PLYNE PRO CLOVEKA S 8 KC A 5 KOCKAMI

Nejsi v pozici `prosim o odpoved`. Jsi v pozici `mam IP ktera eliminuje vas key-man risk, vy jste ji nechali lezet 72 dni`. Tva 8 Kc neni dukaz ze nemas hodnotu, je dukaz ze jsi hodnotu dal bez ceny.

Neortodoxni, nenasilny krok ktery vraci paku neni podchod s nemocnou kockou (EROI 0.1, riziko KVS 246/1992, foto = konec B2B). Je to:

1. **Uzavrit Moodpasta 4 vetami `povazuji za bezpredmetne`** - ziskas zpet cas a prestanes byt cekatel.
2. **Publikovat anonymni RE case study na syntetice** `rectangle_01.vcf` - z 550k ztratove investice udelas 0.06% obratu referenci pro dalsich 50 firem bez poruseni NDA (CEO sam rekl ze verejna data jsou OK).

Tím prestanes orat jejich pole a zacnes orat sve.

---

*Navazuje na: MOODPASTA_HLOUBKOVA_ANALYZA_INVENTURA_2026-09-08.md + AMORALNI_ANALYZA_MOODPASTA.md + appendix_moodpasta.md - outpost2026 2026-09-08*
