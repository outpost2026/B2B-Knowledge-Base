# ONTOLOGIE PET FELT RAG v4.0

**Datum:** 2026-08-01 | **Autor:** outpost2026 | **Verze:** 4.0
**Účel:** Jediný kanonický registr doménové znalosti CNC zpracování PET feltu (ECHOBLOCK®) — materiál, barvy, vzory, V-cut parametry, rychlostní matice, validační pravidla engine a dílenské tacitní znalosti.
**Supersedes:** Dokumentace_Zpracovani_PET_Feltu_v1.0.2.md, Znalostní báze a produkční ontologie v3.2.md, KB_moduly_RAG_v1.0.md (archivováno v _ARCHIVE/04_KNOWLEDGE_BASE/)
**Registr barev:** kanon = f-kódy (fyzický vzorník HUGO na stěně dílny)

---

## 1. Materiálová ontologie: ECHOBLOCK®

Základním stavebním prvkem produktového portfolia Moodpasta je ECHOBLOCK® — netkaná lisovaná textilie z recyklovaných polyesterových (PET) vláken, dodávaná z interního závodu v Chomutově.

| Parametr | Hodnota |
|---|---|
| Materiálové složení | Min. 60 % recyklovaná PET vlákna (cirkulární ekonomika) |
| Hustota | 202 kg/m³ |
| Plošná hmotnost | 2400 g/m² |
| Tloušťky desek | Solo panely 12 mm; sendviče (vícevrstvé barevné kombinace) 21–24 mm |
| Vakuové chování | Porézní — únik podtlaku skrz materiál, nerovnoměrná fixace; vyžaduje doplňkovou mechanickou fixaci páskou |
| Abrazivita | Recyklovaná vlákna obsahují tvrdé tavné shluky — otupování a lámání špiček nástrojů |

**Dílenská terminologie (upozornění):** Operátoři v poznámkách zaměňují „tloušťka" (desky) a „hloubka" (řezu/drážky) — např. „řezat v tloušťce 6 mm" znamená hloubku drážky. Striktně rozlišovat.

**Technologický rámec (invarianty):** Mechanický řez dvouhlavým portálovým plotrem (gantry) s řídicím systémem Ruida. Nástroje: vibrační nůž (Vibrate cutter) a nůž pro V-drážky (V-Slot). Tlačný pohyb nože v porézním materiálu, prakticky bezztrátové dělení (bez prořezu šířky stopy). Laserová/frézovací terminologie („výpalek") je v doméně neplatná — pojmy: **výřez, přířez, dílec, segment**.

## 2. Rozměrové archetypy a formáty desek

| Kategorie formátu | Nominální rozměry (X × Y mm) | Technologický kontext |
|---|---|---|
| Standardní velkoformát | 1200 × 2790 | Základní formát; v surových datech bývá zapsán otočeně (2790 × 1200) — ověřit orientaci vláken |
| Standardní maloformát | 600 × 2790 | Nejčastěji řezaný; podélné půlení velké desky; lineární obklady |
| Surové formáty | 1220 × 2900 | Surový rozměr z Chomutova/Budenína; čisté formátování |
| Zakázkové výšky | 600 × 2800 / 2850 / 2880 | Atypické výšky (např. 2800 mm pro produkt Manchester 100) |
| Architektonické formáty | 1200 × 2390 / 1170 × 2340 | Úpravy pro stavební projekty |
| Paravány a dividery | 1090 × 2050 / 1600 × 850 / 900 × 2500 | 1600 × 850 vyžaduje zaoblené rohy; 900 × 2500 pro spojované dividery |
| Úzké dořezy a lišty | Šířky 395, 320, 215, 150, 44 | Ukončovací lišty (44 mm) a dořezy na délku 2790 nebo zakázkovou (2580) |

## 3. Registr barev (kanon — vzorník HUGO)

Kódování produktů a zakázek: `e[VZOR] - f[BARVA] - [VARIANTA / SÉRIE]`.

| Kód | Název barvy | Poznámka |
|---|---|---|
| fDAR | Dark Knight | Černá/tmavě šedá; homogenní napříč šaržemi (jediná barva, kde lze zanedbat kontrolu šarže) |
| fCAR | Carbonara | Středně šedá |
| fMAT | Matcha | Olivově zelená |
| fREN | Renaissance | Cihlově červená |
| fSAV | Savanna | Pískově žlutá |
| fDUN | Dune | Šedobéžová |
| f fjord | Fjord | Ledově modrá |
| f salmon | Salmon | Lososová |
| f weimar | Weimar | Šedá Weimar |
| f dandelion | Dandelion | Pampelišková (žlutá) |
| f pope | Pope | Královská fialová |
| f terracotta | Terracotta | Terakota |
| f foggy | Foggy | Mlhavě šedá |
| f asphalt | Asphalt | Asfaltová |
| f dentist | Dentist | Bílá |
| f lazy frog | Lazy Frog | Světle zelená |
| f aston green | Aston Green | Tmavě lesní zelená |
| f foie gras | Foie Gras | Šedohnědá |
| f scarlett | Scarlett | Šarlatově červená |

**Merge poznámka (konflikt v3.2 vyřešen):** Registr v ontologii v3.2 používal deskriptivní názvy (Silver Fox, Camel, Ice Blue, Sunflower, Pink Panther, Marsala), které nemají jednoznačné mapování na f-kódy. Kanonickým registrem jsou výhradně f-kódy výše. Žádné barvy nelze identifikovat bez f-kódu.

**Technologické poznámky z v3.2 (jednoznačná vazba f-kód ↔ název):**
- fDAR: minimální viditelnost drobných otřepů (homogenní hustota).
- fMAT: náchylná na pohledové vady při suboptimálním přítlaku.
- fSAV: standardní tón pro interiérovou akustiku.

## 4. Produktové rodiny a vzory

### Lineární rodina (Manchester — kód eMAN)
Vzory definované roztečí (pitch): 17, 20, 30, 31.5, 50, 75, 100, 150 mm.
- Manchester 20: hustý vzor, rozteč 20 mm, mnoho změn směru — intenzivní vibrace hlavy.
- Manchester 50/100: rychlé dlouhé tahy, minimální penalizace rychlosti.
- **Výstraha záměny os:** striktně rozlišovat rastr HORIZONTÁLNÍ (např. 14× 600×2760, 40 mm) vs VERTIKÁLNÍ (např. 50× 600×2790, 44 mm). Záměna = znehodnocení desky.

### Organická a designová rodina
- Big Cube / B.cube / Small Cube: 3D krychlový efekt, obousměrný nájezd V-nože, tisíce koordinačních bodů.
- Stem Bloom / Musica new (eMUS): organické splines — nutné snížení feedrate dle tvarové složitosti (ochrana hran před trháním).
- Standardní vzory: Botanik (eBOT), Fishbone, Big/Small Coffee, Kubista Simple, Envelope, Diamond Row, Cross, Grand Arc, Staria, Sofistica, Vitrage, Rainbow, Rustic Tile.

### Svítidlová rodina (Pendanty — kód eZSV)
Pendant Válec S/M/L, Fluenz Bold (S/M), Fluenz (M/L/XL). Vysoce náročné na nesting (kružnice, montážní otvory, ložiska; lamelové úzké polygony). Náchylné na deformace vibracemi (8–18 kHz). Řez: snížená rychlost 70–100 mm/s, vysoký zdvih H1 = 24 mm.

## 5. Parametrické třídy V-CUT operací (V-drážkování)

### A) Standardní dekorativní drážkování (12 mm felt)
- Úhel: striktně 45° (dominantní); minoritně 30° (specifické rozteče, např. hloubka 9.5 mm).
- Hloubka: nejčastěji 6 mm (= polovina tloušťky desky; vzory Botanik, Manchester, Fishbone, Big/Small Coffee).
- Custom: 2, 3, 3.5, 5 mm (jemné svislé linky, např. rozteč 30 mm osa-osa při 45°); dále 4 mm (rozteč 28 mm) a 8 mm.

### B) Hluboké drážkování a sendviče (21–24 mm felt)
- Hloubky: standardně 9.5, 12, 14, 14.5 mm.
- Logika sendvičů: aktivace pouze u vícevrstvých lepených materiálů (např. vrchní dekor Carbonara + spodní základ Monarch Blood). Hloubka 14/14.5 mm kompletně prořízne vrchní desku a odhalí kontrastní spodní barvu (designový efekt vzorů a lišt).

### C) Výjimky a specifické stavy
- Požadavek na maximum: maximální průřez V-nože bez poškození sacrifikální podložky (těsně ke spodní tkanině, např. Eviso s úhlem 30°). Vyžaduje precizní kalibraci osy Z (hladina H2 ve VCutWorks).
- Absence V-cutu: pouze kolmý ořez vibračním nožem (čisté formátování, panely bez povrchové úpravy).

## 6. Sémantická taxonomie fazet (obvodové zkosení hran)

| Stav | Aplikace |
|---|---|
| Celistvá fazeta (ANO) | Zkosení všech 4 hran (velkoformáty i maloformáty) |
| Jen svislé | Jen dlouhé hrany (osa Y); krátké kolmé — čisté napojení na sokl/strop |
| Jen horizontální | Jen krátké hrany (např. série 14× 600×2760) |
| Jen ve spoji | Zkosení jen hrany dotýkající se sousedního panelu (prevence viditelného spoje u parametrických stěn) |
| Bez fazet (NE) | Kolmý řez na čistý rozměr |
| Jen jedna svislá | Úzké dořezy (např. 150 mm šíře), zkosení jen jedné dlouhé hrany |

## 7. Matice řezných rychlostí dle geometrické složitosti

| Třída | Geometrie | Příklady | Nástroj | Rychlost (mm/s) | Look-ahead / kinematika |
|---|---|---|---|---|---|
| 1 (nízká) | Plynulé polylines, dlouhé linie, obvodové ořezy | Manchester, Baffly, Groove | Vibrate / V-Slot | 100–200 | Maximální plynulost bez vibrací portálu |
| 2 (střední) | Vlnovky, mírné zakřivení, křížené polygonální sítě | Wave, Chevron, Diamond, Maze, Hexa | Vibrate / V-Slot | 100–150 | Look-ahead plánování proti chvění gantry v ohybech |
| 3 (vysoká) | Komplexní kontury, mikro segmenty, texty, loga, přerušované zářezy | Gills, textová loga, Beehive, Roma | Vibrate | 40–80 | Striktní omezení proti stuttering a trhání vláken |

Texty a loga: řez z rubové strany (zrcadlení), posuv 45 mm/s.

## 8. Validační pravidla engine (KB Engine Rules)

Spouštěče odpovídají parametrům validátoru systeq.cz; každé pravidlo = trigger + severity + fyzikální dopad + algoritmus nápravy.

### 8.1 Vertikální pravidla (osa Z, výška hrotu H2)

**`RULE_H2_VIBRATE_12MM`** (Aktivní)
- Trigger: `cutter_type_id == 1` (vibrační nůž) AND `material_thickness_mm == 12.0`
- Severity: CRITICAL — H2 > 0.1 mm při `ThicknessConfidence == HIGH`; WARNING — H2 mimo [-0.5, 0.0] mm bez překročení kritického prahu; INFO — nízká jistota tloušťky nebo H2 == 0.0
- Dopad: spodní nedořez v 12mm feltu; výřez nelze čistě oddělit, vytrhávání potrhá vlákna a hranu dílce
- Náprava: úprava cílového CAM parametru vrstvy na H2 ∈ [-0.5, 0.0] mm (bezpečný zářez do obětovaného podkladu = 100 % čisté proříznutí)

**`RULE_H2_VIBRATE_24MM`** (Aktivní; trigger rozšířen na sendviče 21–24 mm)
- Trigger: `cutter_type_id == 1` AND `material_thickness_mm == 24.0` (sendviče 21–24 mm — dynamické intervalové větvení namísto absolutní shody tloušťky, prevence poškození stolu)
- Severity: CRITICAL — H2 > 0.1 mm při vysoké jistotě; WARNING — H2 mimo [-0.5, -0.2] mm; INFO — degradace při nízké jistotě
- Dopad: u 24 mm materiálu kladná/nulová H2 = masivní nedořez; při proříznutí spodní vrstvy hrozí ohyb nože a deformace kolmosti hrany
- Náprava: automatický posun koncového bodu osy Z do technologického optima −0.5 až −0.2 mm

### 8.2 Sekvenční a hierarchická pravidla (chronologie řezu)

**`RULE_SEQ_OUTER_LAST`** (Aktivní, CRITICAL)
- Trigger: aktivní výstupní vrstva obvodového ořezu vibračním nožem (`cutter_type_id == 1`, `is_output_yes == true`, `total_cut_length_mm > 0`) AND v binárním souboru existuje element jiné vrstvy s nižším offsetem než min offset obvodového ořezu
- Dopad: obvod proříznut před dokončením vnitřních struktur → vakuum nezafixuje porézní panel, tlačný pohyb nože posune uvolněný dílec → zmetek + riziko zlomení nože
- Náprava: elementy obvodového ořezu musí mít nejvyšší hexadecimální offsety v binárním streamu (exekuce úplně poslední)

**`RULE_SEQ_OUTER_LAST_NESTING_OFFSET`** (Aktivní, WARNING)
- Trigger: `check_nesting_hierarchy == true` AND prvek má `parent_id` AND `offset_child > offset_parent`
- Dopad: vnitřní segment řezán po dokončení vnějšího obalu → uvolněný materiál ztrácí integritu, vibrace + odsávání pohybují prvkem, okousané hrany, deformace rozměrů
- Náprava: topologické třídění v CAM parseru — potomci s nižšími offsety (řezáni dříve) než prostorové obaly

### 8.3 Fixační pravidla (fyzika pracovního stolu)

**`RULE_FIX_SMALL_PANEL`** (Aktivní)
- Trigger: plocha výkresu S = (width × height)/10⁶ < 1.67 m²
- Severity: WARNING — S < 0.5 m²; INFO — S ∈ [0.5, 1.67) m²
- Dopad: vakuový stůl nevyvine dostatečnou přidržovací sílu na malé ploše; únik podtlaku porézním materiálem; tlačný odpor nože utrhne dílec a posune geometrii
- Náprava: manuální fixace papírovou krycí páskou podél min. 80 % obvodu k okolní desce/stolu (masová produkce malých dílů — např. 150 ks čtverců 78×78, baffle, kostky 600×600 — povinné obvodové páskování)

### 8.4 Geometrické a technologické anomálie (CAM validace)

**`RULE_GEO_V1_EDGE_MERGE_MISSING`** (Aktivní, WARNING)
- Trigger: `check_open_in_closed == true` AND cKDTree identifikuje otevřenou dráhu s koncovými body na/uvnitř uzavřeného rodiče AND délka nepropojeného segmentu ≤ 200.0 mm
- Dopad: typ edge_adjacent — nůž zastaví, zvedne se, otočí a znovu zapíchne → pohledové vady, záseky, otřepy; typ standalone_tab — technologický můstek bez spojení s obvodem → duplicitní/neukončené dráhy
- Náprava: modul `vcf_geometry` provede snap koncových bodů v rámci tolerance (cross-layer filtr potlačí varování u navazujících V-slot linií se shodnou hloubkou H2 a směrem)

**`RULE_GEO_V1_UNCLOSED_LOOP`** (Aktivní)
- Trigger: `check_unclosed_loops == true` AND gap mezi počátečním a koncovým bodem > 0.1 mm
- Severity: CRITICAL — gap ≥ 5.0 mm; WARNING — gap ∈ [1.0, 5.0) mm; INFO — gap < 1.0 mm (degradováno při záměrném překryvu/overcutu)
- Dopad: nedovřená smyčka = můstek nedoříznutého materiálu; operátor vytrhává silou (ničí strukturu) nebo dořezává skalpelem (čas, chybovost)
- Náprava: endpoint snap nebo vložení chybějícího segmentu (pokud gap nepřesáhne kritickou mez); záměrný overcut degradován

**`RULE_GEO_V1_ORPHAN_ELEMENT`** (Aktivní, WARNING)
- Trigger: `check_orphans == true` AND L > 50.0 mm AND vzdálenost od ostatních prvků > 500.0 mm
- Dopad: rychloposuv na izolované místo desky (zapomenutá geometrie z předchozích revizí) → prodloužení strojního času, znehodnocení čisté plochy
- Náprava: vizuální flag v UI; explicitní potvrzení operátora (drop vs legitimní součást zakázky)

**`RULE_GEO_V1_5_UNCONNECTED_INTERNAL_DECOR`** (Aktivní — zpřísněná kalibrace, CRITICAL)
- Trigger: `check_unconnected_internal_decor == true` AND dekorativní vrstva (V-drážky, směr `left`/`both`) má volný koncový bod uvnitř bounding boxu panelu AND 1.0 mm < Δ ≤ 3.0 mm k nejbližšímu vektoru
- Dopad: fatální estetická vada — designová linie končí slepě před průsečíkem/hranou (viditelná chyba grafiky)
- Náprava: automatický snap — prodloužení ve směru posledního vektoru a ukotvení k nejbližší hraně/linii
- Kalibrační poznámka (Dev Alert): slepé místo — nedokáže ošetřit neprotažené křivky s gapem < 3.0 mm (limit `max_snap_distance_mm`); probíhá úprava detekčního větvení pro sub-3mm anomálie

**`RULE_GEO_V1_MICRO_SEGMENT`** (VYPNUTO)
- Trigger: `check_micro_segments == true` AND délka segmentů < 1.0 mm
- Dopad: zahlcení interpolátoru Ruida, look-ahead selhává → chvění hlavy, potrhané hrany, namáhání gantry
- Důvod vyřazení: vysoká míra falešně pozitivních detekcí u hladkých křivek/splines; potlačeno do rekalibrace hustotního filtru

## 9. Datový tok a prevence GIGO

```
[CAD] .DXF/.DWG ──> [LightBurn v1.7.08] .LBRN2 ──> [VCutWorks v2.00.34] .VCF ──> [CNC Plotter (Ruida)]
```

- Přenos dat bez G-kódu — binární instrukce přímo pro řadič Ruida (.vcf/.vc). Offline režim s hardwarovým bufferem (max 10 souborů).
- **CAM autorita:** jediným CAM kompilátorem je VCutWorks v2.00.34 (mapuje vrstvy, směry řezu, hloubky, pojezdy; generuje .VCF). LightBurn NENÍ CAM autorita — slouží jako nástroj úprav rozvržení, zaoblení rádiusů a operativních malých zakázek s exportem do .dxf (nikdy negeneruje řídicí data).
- **Terminologie:** „výpalek" je neplatný výraz; pojmy výřez, přířez, dílec, segment.
- **Zakázané operace (process):** LightBurn nikdy negeneruje .VCF; výraz „výpalek" v dokumentaci zakázek je sémanticky nesprávný.

## 10. Dílenské tacitní znalosti (V dílně)

### 10.1 Vakuová a fixační rizika (Vacuum Loss Prevention)
- Masová produkce malých dílů (150 ks 78×78, závěsné baffle, kostky 600×600) = riziko ztráty přítlaku → povinné obvodové páskování.
- Zbytkový materiál bez dostatečné plochy: fixace páskou ze všech stran, min. 80–90 % obvodu k flatbedu.
- Pravidlo jemného naznačení (Engraving/Marking): u kostek 600×600 s kruhovým výřezem (D360) nůž nesmí proříznout materiál v celé tloušťce — H2 nastaveno +0.2 mm nad povrch. Vnitřní výřez vždy PŘED obvodovým formátováním čtverce.

### 10.2 Návaznost vzorů, orientace a šaržování
- Pattern Alignment: u komplexních zakázek (Sandwich Carbonara, kontinuita textury) vizuální kontrola rozvržení + striktní fixace počátku (Anchor Point).
- Šaržování a metamerie: zápisy „3 šarže" / „1x jiná barevnost ve stejné šarži" = riziko barevných odchylek na stěně; u sousedících panelů fyzická kontrola shody šarže na hraně desky.
- Orientace desky: číslo šarže na hraně vždy čitelně (ne vzhůru nohama) — garantuje shodný směr vláken napříč panely. Výjimka: fDAR (černá je homogenní napříč šaržemi).

### 10.3 Exekutivní workflow, kalibrace nuly, sekvencování
- Srovnání s L-dorazem (plstěný, rysky fixem): kontrola koty delší hrany od okraje plotteru = 25 cm (tolerance 24–27 cm) → vyloučení zkosení v ose Y.
- Standardní nulování: laserový kříž na L-doraz, aretace na rysce 10 mm. Podélné dělení (1200 → 2× 600): nulový bod v ose X posunout na rysku 5 mm (kompenzace úbytku prořezem).
- Sekvencování drah (VCutWorks, „edit cut property"): 1) geometrická priorita — nejprve malé vnitřní otvory/díly, jinak ztráta podtlaku po vyříznutí obvodu; 2) prostorová sekvence — od Anchor pointu k protilehlému bodu (optimalizace pojezdů); 3) zrcadlení textu — řez z rubové strany, 45 mm/s.
- Pravidlo kotevního bodu: výchozí pozice výhradně Anchor Point; režimy Current position / Machine zero / Absolute coordinate fatálně posunou nulový bod.
- Mapování vrstev: černá vrstva (C00) = Vibrate cutter, feed 200 mm/s; barva C02 = technologické poznámky a kóty — Output = No (nikdy se neřeže).

### 10.4 Údržba stroje a mechanická diagnostika
- Diagnostika V-slot nože: pokud nelze V-odpad z drážky ručně vyloupnout, špička je ulomená → okamžitá výměna (jinak nedoriznutí spodních vláken, třepe se). Stejně u Vibrate cutteru — kontrola stavu, po instalaci kalibrační test na odřezku.
- Vibrace a příruby: vibrační hlava uvolňuje vnitřní příruby; anomální zvuk → okamžité zastavení a dotažení (riziko destrukce hlavy). Nosné vodicí prvky promazávat silikonovým sprejem.

## 11. Technologický appendix

### 11.1 Srovnání metod řezání PET plstí

| Technologie | Výhody | Limity |
|---|---|---|
| CNC plotr s oscilačním nožem (standard) | Čisté hrany, nulové tepelné zatížení, přesné V-drážkování, ekologická šetrnost | Otupování nožů (abrazivita), rychlostní limity u drobných prvků (rotační zpoždění C-osy) |
| CNC laser (CO2) | Rychlost, mikro detaily, bezkontaktní řez | Tavení okrajů, sklovatění, zažloutlý lem, toxický zápach (chemická filtrace) |
| Vodní paprsek (Waterjet) | Čistý chladný řez, tlusté bloky (50+ mm) | Nasákavost pórů, náročné sušení, riziko plísní |
| Tvarový výsek (Die Cutting) | Produktivita u velkosériové výroby | Velká investice do matric, nulová flexibilita |

### 11.2 R&D projekty a digitální pipeline
- ERP Odoo: samostatný DXF/VCF parser měří dráhy, počítá čas, generuje CSV → import do Odoo (BOM, naceňování Sale Order Lines). Zákaz custom kódu uvnitř Odoo — pouze CSV importy.
- Termotvarování a lisování (Pressed & Molded Felt): hydraulický lis 50 t (1000×900 mm), pec + chiller (Huajia). Projekty: Cocoon, Umbra (stínidla), 3D dlaždice (beehive, hexa, roma), waferování (textura betonu).
- Lamelové stropy a baffly: vývoj dle HeartFelt Hunter Douglas + LED profily, ohybové stoly.
- Recyklace odřezků: drtička 500DS (pražský závod) → rozvláknění → slisování zpět do Echoblock desek.

## 12. Rozhodnutí o konfliktech (merge log v4.0)

| Konflikt | Řešení |
|---|---|
| Registr barev v3.2 (Dark Knight/Silver Fox/Camel…) vs f-kódy v1.0.2 | Kanon = f-kódy (sekce 3); deskriptivní názvy v3.2 bez jednoznačné vazby na f-kódy vyřazeny |
| LightBurn „zakázán" (v3.2 GIGO) vs aktivní použití (v1.0.2) | LightBurn = layout/úpravy + DXF export, NENÍ CAM autorita; .VCF generuje výhradně VCutWorks (sekce 9) |
| Sendviče 21–24 mm vs trigger RULE_H2_VIBRATE_24MM (== 24.0) | Trigger rozšířen na dynamické intervalové větvení 21–24 mm (sekce 8.1) |
| Rychlost textu 45 mm/s | Jednotné: řez textu zrcadleně z rubu, 45 mm/s (sekce 7) |
