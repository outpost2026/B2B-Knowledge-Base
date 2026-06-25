---
title: "Dokumentace_Zpracovani_PET_Feltu_v1.0.2"
source: "c:\Users\PC\Documents\Repozitar_Dev\_github\KB\Dokumentace_Zpracovani_PET_Feltu_v1.0.2.docx"
---

## Obsah

- Zpracování PET Feltů v1.0.2
  - 1. Materiálová Ontologie: ECHOBLOCK®
  - 2. Rozměrové Archetypy a Formáty Desek
  - 3. Parametrické Třídy V-CUT Operací (V-drážkování)
    - A) Standardní dekorativní drážkování (12 mm felt)
    - B) Hluboké drážkování a sendviče (21–24 mm felt)
    - C) Výjimky a specifické stavy
  - 4. Sémantická Taxonomie Fazet (Obvodové zkosení hran)
  - 5. V dílně (Tacitní znalosti)
    - A) Vakuová a fixační rizika (Vacuum Loss Prevention)
    - B) Návaznost vzorů, orientace a šaržování
    - C) Exekutivní dílenské workflow & kalibrace nuly & sekvencování
    - D) Údržba stroje a mechanická diagnostika
  - 6. Slovník Produktových Rodin a Barevných Kódů
    - Produktové rodiny a geometrické charakteristiky:
    - Barevných kódy (Reference: Fyzický vzorník HUGO na stěně dílny, příklady):
  - 7. Globální Technologické Srovnání Zpracování PET Plstí
  - 8. Technologický Appendix: R&D Projekty a Digitální Pipeline
    - Digitální řetězec dat:
    - Strategický rozvoj a integrace:

# Zpracování PET Feltů v1.0.2
Autor: Ondřej Soušek, vypracováno pro interní účely autora na základě stínování hlavního technologa CNC firmy Wynwood (Moodpasta)

Účel dokumentu: Institucionalizace firemního know-how, standardizace technologických postupů na dílně a zrychlení procesu onboarding nových zaměstnanců na pozici CNC technologa / operátora oscilačního plotru.

## 1. Materiálová Ontologie: ECHOBLOCK®
Základním stavebním prvkem celého produktového portfolia společnosti Moodpasta je ECHOBLOCK® – netkaná lisovaná textilie vyrobená z recyklovaných polyesterových (PET) vláken dodávaná z interního závodu v Chomutově.

Materiálové složení: Minimálně 60 % tvoří recyklovaná PET vlákna, což podtrhuje ekologický rozměr a zapojení do cirkulární ekonomiky.

Hustota a plošná hmotnost: Hustota činí 202 kg/m³ při plošné hmotnosti 2400 g/m². Tyto parametry dodávají materiálu vysokou akustickou pohltivost a strukturální tuhost.

Tloušťky desek: Solo panely jsou dodávány v nominálních tloušťkách 12 mm. Vícevrstvé sendvičové panely (kombinace různých barevných vrstev) dosahují celkové tloušťky 21 až 24 mm.

Dílenská terminologie (Upozornění): V provozu operátoři v poznámkách často nesprávně zaměňují termín „tloušťka“ pro označení hloubky řezaných drážek (např. „řezat v tloušťce 6 mm“). Pro jednoznačnost na dílně se striktně rozlišuje Tloušťka desky a Hloubka řezu/drážky.

Vakuové chování a poréznost: Vzhledem k poréznosti plstí je vakuová fixace na plotru nerovnoměrná. Dochází k úniku podtlaku skrz sacrifikální (obětovanou) textilii instalovanou na plotru. To vyžaduje doplňkovou mechanickou fixaci papírovou lepicí páskou.

Abrazivita a opotřebení nástrojů: Recyklovaná PET vlákna obsahují mikroskopické nečistoty a tvrdé tavné shluky z recyklace. To způsobuje otupování a lámání jemných špiček řezných nástrojů.

## 2. Rozměrové Archetypy a Formáty Desek
Následující tabulka definuje exaktní rozměrové mantinely standardních a zakázkových formátů využívaných ve výrobě:

| Kategorie formátu | Nominální rozměry (X × Y mm) | Technologický kontext a využití |
| --- | --- | --- |
| Standardní velkoformát | 1200 × 2790 mm | Základní formát (Echoblock). V surových datech od grafiků bývá často zapsán jako otočený formát 2790 × 1200 mm – technolog musí před nářezem ověřit orientaci vláken. |
| Standardní maloformát | 600 × 2790 mm | Nejčastěji řezaný formát vzniklý podélným půlením velké desky. Využívá se primárně pro lineární obklady. |
| Surové formáty | 1220 × 2900 mm | Surový rozměr plstí přivážených z Chomutova či Budenína. Využívá se pro čisté formátování bez dalšího detailního opracování. |
| Zakázkové výšky | 600 × 2800 / 2850 / 2880 mm | Atypické prodloužené výšky používané u specifických projektů (např. zakázková výška 2800 mm pro produkt Manchester 100). |
| Architektonické formáty | 1200 × 2390 mm / 1170 × 2340 mm | Specifické rozměry upravené na míru pro velké stavební a architektonické projekty. |
| Paravány a dividery | 1090 × 2050 / 1600 × 850 / 900 × 2500 mm | Závěsné a stolní předěly. Formát 1600 × 850 mm vyžaduje zaoblené rohy, rozměr 900 × 2500 mm slouží pro spojované dividery. |
| Úzké dořezy a lišty | Šířky: 395, 320, 215, 150, 44 mm | Ukončovací lišty (např. šíře 44 mm) a dořezy řezané bud' na plnou délku 2790 mm, nebo zakázkovou délku např. 2580 mm. |

## 3. Parametrické Třídy V-CUT Operací (V-drážkování)
Technologické standardy pro tvorbu V-drážek jsou rozděleny do tří základních tříd podle typu materiálu a účelu:

### A) Standardní dekorativní drážkování (12 mm felt)
Nominální úhel: Striktně 45° (dominantní). Minoritně se využívá úhel 30° (spojen se specifickými zakázkovými roztečemi, např. při hloubce 9.5 mm).

Nominální hloubka řezu: Nejčastěji 6 mm. Odpovídá přesné polovině tloušťky standardní desky, což zaručuje pohledovou drážku = vzory (ze současného výrobního portfolia firmy, například  Botanik, Manchester, Fishbone, Big/Small Coffe)

Custom úpravy: Hloubky 2 mm, 3 mm, 3.5 mm a 5 mm. Využívají se pro jemné svislé linky s vysokou hustotou (např. rozteč 30 mm osa-osa při V-cut 45°). Dále se vyskytuje specifická hloubka 4 mm (rozteč 28 mm) a hloubka 8 mm.

### B) Hluboké drážkování a sendviče (21–24 mm felt)
Hloubka řezu: Standardně 9.5 mm, 12 mm, 14 mm a 14.5 mm.

Logika sendvičů: Tyto hloubky se aktivují výhradně u vícevrstvých lepených materiálů (Sandwich – např. kombinace vrchního dekoru Carbonara a spodního základu Monarch Blood). Hloubka 14 mm nebo 14.5 mm umožňuje kompletně proříznout celou vrchní desku a odhalit kontrastní barvu spodního feltu, což vytváří žádaný designový efekt u vzorů i ukončovacích lišt.

### C) Výjimky a specifické stavy
Požadavek na maximum: Indikuje požadavek na maximální možný průřez V-nože bez poškození sacrifikální podložky (proříznutí těsně k spodní tkanině, např. u zakázek Eviso s úhlem 30°). Vyžaduje precizní kalibraci osy Z (hladina H2 v programu „Vcutwork)

Absence V-cutu: Pokud není V-drážka vyžadována, vrstva je omezena pouze na kolmý ořez vibračním nožem (čisté formátování nebo panely bez povrchového opracování).

## 4. Sémantická Taxonomie Fazet (Obvodové zkosení hran)
Nastavení nájezdů tangenciálního V-nože pro vytvoření obvodového zkosení hran se řídí následující stavovou metodikou:

Celistvá fazeta (ANO): Aktivuje obvodové zkosení na všech 4 hranách výsledného panelu (aplikuje se univerzálně na velkoformáty i maloformáty).

Jen Svislé: Fazetování probíhá striktně na dlouhých hranách (osa Y). Krátké hrany (šířka desky) zůstávají kolmé, což je vyžadováno pro čisté napojení panelu na sokl, strop či navazující prvky bez vzniku nevzhledných mezer.

Jen horizontální: Fazetování probíhá výhradně na krátkých hranách (využíváno u specifických horizontálních rastrů, např. u série 14x 600×2760).

Jen ve spoji: Nůž provádí zkosení pouze na té konkrétní hraně, která se bude fyzicky dotýkat sousedního panelu. Slouží jako prevence viditelného spoje u parametrických stěn.

Bez fazet (NE): Obvod panelu je řezán výhradně kolmým oscilačním nožem na čistý rozměr bez jakéhokoliv zkosení hran.

Jen jedna svislá: Výjimečný stav pro specifické úzké dořezy (např. 150 mm šíře ze zbytku materiálu), kde se zkosení provádí pouze na jedné dlouhé hraně, zatímco druhá zůstává kolmá.

## 5. V dílně (Tacitní znalosti)
Tato kapitola obsahuje klíčové provozní zkušenosti operátorů CNC plotru. Jejich zanedbání vede k poškození materiálu nebo může vést k poškozená řezné hlavy.

### A) Vakuová a fixační rizika (Vacuum Loss Prevention)
Riziko malých obrobků: Masová produkce malých dílů (např. 150ks čtverců 78×78 mm, závěsné baffle nebo série kostek 600×600 mm) představuje riziko ztráty přítlaku. Jakmile plotr vyřízne první řadu, podtlak uniká přes sacrifikální textilii a hrozí posun dílů nožem.
Tyto díly vyžadují povinné obvodové páskování.

Fixace odřezků a zbytků: Malá deska nebo zbytkový materiál nemá dostatečnou plochu pro přítlak vývěvy plotru. Tyto díly musí být povinně zafixovány lepicí páskou ze všech stran – minimálně 80–90 % jejich obvodu musí být pevně upevněno k flatbedu.

Pravidlo jemného naznačení (Engraving/Marking): přiklady > U kostek 600×600 mm s kruhovým výřezem (D360) nůž nesmí materiál proříznout v celé tloušťce materiálu. Hloubka řezu  – tzn. výška osy Z (H2 v programu Vcutwork) je nastavena těsně nad povrch materiálu (+0.2 mm). Tento vnitřní se musí vždy provádět jako první, před obvodovým formátováním čtverce.

### B) Návaznost vzorů, orientace a šaržování
Návaznost vzorů (Pattern Alignment): U komplexních zakázek (např. Sandwich Carbonara s požadavkem na kontinuitu textury) musí operátor před spuštěním vizuálně zkontrolovat rozvržení na displeji a striktně zafixovat počátek souřadnic (Anchor Point).

Šaržování feltů a metamerie: Zápisy v zakázkách typu „použity 3 šarže“ nebo „1x jiná barevnost ve stejné šarži“ (např. u série 26ks panelů) indikují vysoké riziko barevných odchylek na stěně. Pokud jdou panely v instalaci bezprostředně vedle sebe, operátor musí před spuštěním cyklu fyzicky zkontrolovat shodu šarže na hraně desky.

Pravidlo orientace desky: Číslo šarže natištěné výrobcem na hraně desky musí být při pokládce na stůl vždy orientováno standardně čitelně (nesmí být vzhůru nohama). To garantuje, že lícová a rubová strana (směr vláken) sedí napříč sousedními panely.
- pravidlo orientace PET felt desek lze zanedbat pouze u barvy “Dark knight” = černá barva je homogenní napříč různými šaržemi

### C) Exekutivní dílenské workflow & kalibrace nuly & sekvencování
Srovnání s L-dorazem: Deska se srovná s plstěným L-dorazem, který vyrobil operátor (obsahuje rysky fixem). Pomocí svinovacího metru se změří dvě kontrolní kóty – vzdálenost delší hrany desky od okraje plotteru musí být standardně přesně 25 cm (v toleranci 24–27 cm dle rozměrů desky). Tím se vyloučí zkosení desky při pojezdu v ose Y.

Standardní nulování vs. Podélné dělení: Pomocí laserového kříže se najede na L-doraz. Standardní nulování se aretuje na rysce 10 mm. Pokud však probíhá podélné dělení (půlení desky 1200 mm na 2x 600 mm), dochází k úbytku materiálu vlivem prořezu nože. Aby se zabránilo nedořezu hran, nulový bod se v ose X posouvá na rysku 5 mm, čímž se kompenzuje tolerance okrajového offsetu a dráha se posune bezpečně dovnitř materiálu.

Pravidla sekvencování drah (workflow v programu Vcutwork):
- tato pravidla operátor CNC nastavuje v programu pomocí funkce “edit cut property”

Geometrická priorita: Vždy se nejprve řežou malé vnitřní otvory a díly. Pokud by se jako první vyřízl obvod velkého dílu, vakuový stůl ztratí podtlak a díl se posune.

Prostorová sekvence: Optimalizace pojezdů. Hlava postupuje systematicky – zaplňuje desku řezy od Anchor pointu směrem k protilehlému bodu.

Zrcadlení textu: Texty a logické prvky se v programu vždy zrcadlí (řežou se z rubové strany). Tím se zaručí, že lícová pohledová strana je dokonale čistá, bez otřepů. Řez textu probíhá sníženým posuvem 45 mm/s.

LightBurn: Úpravy rozvržení desek, zaoblení rádiusů, operativní malé zakázky (small jobs) bez asistence grafika. Export geometrie do .dxf.

VCutWorks: Klíčový CAM kompilátor. Načítá CAD data, mapuje vrstvy, definuje směry řezu, hloubky zanoření a pojezdy. Generuje výsledný binární soubor .VCF.

Pravidlo kotevního bodu: Výchozí pozice v programu musí být nastavená výhradně na Anchor Point. Režimy Current position, Machine zero či Absolute coordinate fatálně posunou nulový bod drah a znehodnotí materiál.

Standardní mapování vrstev: Černá vrstva (C00) je přiřazena nástroji Vibrate cutter (oscilační nůž), standardní feed 200 mm/s. Barva C02 slouží výhradně pro technologické poznámky a kóty – status v CAM musí být striktně nastaven na Output = No (nikdy se neřeže).

### D) Údržba stroje a mechanická diagnostika
Diagnostika poškození V-slot nože: Nehomogenita recyklovaných vláken způsobuje náhlé ulomení jemné špičky nože. Pokud po dokončení cyklu nelze vyříznutý V-odpad z drážky snadno ručně vyloupnout, špička nože V-slot je ulomená. Je nutná okamžitá výměna, jinak nedochází k doříznutí spodních vláken a materiál se třepí. To samé platí také pro nástroj Vibrate cutter - nutná pravidelná kontrola stavu oscilačního nože. V dílně jsou k dispozici náhradní nové nože, po instalaci je nutné zkontrolovat kalibraci nože nejlépe na odřezku PET feltu testovacím řezem

Mechanické vibrace a příruby: Vibrační hlava generuje vysokofrekvenční rázy, které postupně uvolňují vnitřní příruby a upínací šrouby. Jakýkoliv anomální zvuk signalizuje uvolnění hlavy. Stroj je nutné okamžitě zastavit a dotáhnout vnitřní příruby, jinak hrozí mechanická destrukce hlavy. Nosné vodicí prvky se pravidelně promazávají silikonovým mazivem ve spreji.

## 6. Slovník Produktových Rodin a Barevných Kódů
Kódování produktů a zakázek v současnosti (stav k 22.05.2026) sleduje formát: e[VZOR] - f[BARVA] - [VARIANTA / SÉRIE].

### Produktové rodiny a geometrické charakteristiky:
Lineární rodina (Manchester / Drážkování - kód eMAN): Vzory definované roztečí (pitch) v šíři 17, 20, 30, 31.5, 50, 75, 100 a 150 mm.

Manchester 20: velmi hustý vzor s roztečí 20 mm. Generuje vysoký počet změn směru a intenzivní vibrace hlavy stroje.

Manchester 50 / 100: Rychlé, dlouhé tahy s minimální penalizací rychlosti řezu.

Výstraha před záměnou os: Je kritické striktně rozlišovat rastr HORIZONTÁLNĚ (např. 14x 600×2760, 40mm) vs. VERTIKÁLNĚ (např. 50x 600×2790, 44mm). Záměna os znamená znehodnocení celé desky.

Organická a designová rodina:

Big Cube / B.cube / Small Cube: Komplexní geometrické křížení drah tvořící 3D krychlový efekt. Vyžaduje obousměrný nájezd V-nože a generuje tisíce koordinačních bodů.

Stem Bloom / Musica new (kód eMUS): Obsahuje organické zakřivené křivky (Splines). Pro zachování plynulosti řezu a zamezení trhání hran vyžadují tyto křivky automatické či manuální snížení posuvu hlavy (feedrate) na základě tvarové složitosti.

Další standardní vzory: Botanik (eBOT), Fishbone, Big/Small Coffee, Kubista Simple, Envelope, Diamond Row, Cross, Grand Arc, Staria, Sofistica, Vitrage, Rainbow, Rustic Tile.

Svítidlová rodina (Pendanty - kód eZSV):

Pendant Válec S/M/L, Fluenz Bold (S/M), Fluenz (M/L/XL): Produkty vysoce náročné na vnitřní uspořádání drah (nesting). Obsahují kružnice (montážní otvory a ložiska) a lamelové úzké polygony (vertikální paprsky svítidel). Tyto prvky jsou náchylné na deformace způsobené mechanickými vibracemi hlavy (8–18 kHz). Řežou se sníženou rychlostí (70–100 mm/s) s vysokým zdvihem (H1 = 24 mm).

### Barevných kódy (Reference: Fyzický vzorník HUGO na stěně dílny, příklady):
| Kód | Název barvy | Kód | Název barvy |
| --- | --- | --- | --- |
| fDAR | Dark Knight (černá/tmavě šedá) | fCAR | Carbonara (středně šedá) |
| fMAT | Matcha (olivově zelená) | fREN | Renaissance (cihlově červená) |
| fSAV | Savanna (pískově žlutá) | fDUN | Dune (šedobéžová) |
| f fjord | Fjord (ledově modrá) | f salmon | Salmon (lososová) |
| f weimar | Weimar (šedá Weimar) | f dandelion | Dandelion (pampelišková) |
| f pope | Pope (královská fialová) | f terracotta | Terracotta (terakota) |
| f foggy | Foggy (mlhavě šedá) | f asphalt | Asphalt (asfaltová) |
| f dentist | Dentist (bílá) | f lazy frog | Lazy Frog (světle zelená) |
| f aston green | Aston Green (tmavě lesní zelená) | f foie gras | Foie Gras (šedohnědá) |
| f scarlett | Scarlett (šarlatově červená) | - | - |

## 7. Globální Technologické Srovnání Zpracování PET Plstí
Přehled průmyslových metod řezání PET panelů sloužící pro pochopení limitů a výhod naší interní technologie:

| Technologie řezu | Klíčové výhody | Limity a rizika |
| --- | --- | --- |
| CNC plotr s oscilačním nožem (Moodpasta standard) | Čisté hrany, nulové tepelné zatížení materiálu (nedochází k tavení, žloutnutí ani zápachu). Možnost přesného V-drážkování pod úhly. Vysoká ekologická šetrnost. | Rychlé otupování a zalamování nožů z důvodu abrazivity recyklovaného materiálu. Rychlostní limity u drobných, detailních prvků (vlivem rotačního zpoždění C-osy). |
| CNC laserové řezání (CO2) | Vysoká rychlost pojezdu, schopnost vyřezat mikroskopické detaily, bezkontaktní řez (nástroj se mechanicky neopotřebovává). | Tepelný řez taví okraje plsti (dochází ke sklovatění hran). Vytváří tvrdý, ostrý a zažloutlý lem. Generuje silný toxický zápach spáleného polyesteru (vyžaduje masivní chemickou filtraci). |
| Řezání vodním paprskem (Waterjet) | Čistý a chladný řez bez otřepů a tavení. Schopnost řezat tlusté sendvičové bloky (50 mm a více). | Voda okamžitě nasákne do pórů plsti (houbový efekt). Vyžaduje následné energeticky vysoce náročné mikrovlnné nebo horkovzdušné sušení, jinak hrozí rozvoj plísní. |
| Tvarový výsek (Die Cutting) | Vysoká produktivita u velkosériové výroby (tisíce kusů identických malých podložek či prvků). | Nutnost obrovské počáteční investice do drahých ocelových výsekových matric. Nulová flexibilita při jakékoliv změně designu. Zcela nevhodné pro zakázkovou custom výrobu. |

## 8. Technologický Appendix: R&D Projekty a Digitální Pipeline
### Digitální řetězec dat:
Přenos dat probíhá bez standardního G-kódu, software generuje binární instrukce přímo pro řadič Ruida (soubory vcf/vc).
Stroj pracuje v offline režimu s hardwarovým zásobníkem (buffer max 10 souborů). Lze tedy zpracovávat zakázky bez nutnosti propojení s PC, pokud jsou data nahraná v plotru.

[CAD] .DXF/.DWG ──> [LightBurn v1.7.08] .LBRN2 ──> [VCutWorks v2.00.34] .VCF ──> [CNC Plotter (Ruida)]

### Strategický rozvoj a integrace:
ERP Odoo a automatizace naceňování: Perspektivní možnost využití samostatného standalone DXF/VCF Parseru pro asynchronní integraci. Skript naměří dráhy, vypočte čas a vygeneruje CSV, které se importuje do Odoo k tvorbě výrobních kusovníků (BOM) a naceňování (Sale Order Lines). Ve firmě platí striktní zákaz psaní custom kódu přímo uvnitř Odoo. Veškeré automatizace lze aspiračně implementovat pouze formou importů CSV tabulek s daty.

Termotvarování a lisování feltů (Pressed & Molded Felt): Technologický skok překonávající limity plochého řezání. Vybavení zahrnuje hydraulický lis o síle 50 tun (1000 × 900 mm), ohřívací pec a chiller (dodavatel Huajia, Čína). Projekty: Hluboké výlisky stínidel (Cocoon, Umbra), lisované designové dlaždice (3D bloky beehive, hexa, roma) a plošné waferování (prolisování textury betonu do velkých desek).

Lamelové stropy a lapače hluku (Baffly): Vývoj lisovaných akustických lamel inspirovaných systémem HeartFelt Hunter Douglas a světelné baffly s integrovanými LED profily a ohybovými stoly.

Ekologická recyklace odřezků (Drtička 500DS): Instalace průmyslové drtičky plstí v pražském závodě. Cílem je rozvláknění odpadních odřezků z plotteru a jejich následné slisování zpět do nových Echoblock desek (uzavření ekologického cyklu bez odpadu).