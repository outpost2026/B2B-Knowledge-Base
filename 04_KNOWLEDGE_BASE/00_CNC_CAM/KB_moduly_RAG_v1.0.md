## Transformace znalostní báze: RAG-Ready Ontologie (v32) – Aktualizováno dle vývojových korekcí

Tento dokument představuje revidovanou a vyčištěnou dekonstrukci surových konfiguračních a procedurálních pravidel obsažených v souborech `rules.json` a `engine.py`. Znalostní báze byla podrobena **ontologickému ořezu (trimmingu)**, který odstraňuje nekompatibilní terminologii a precizuje fyzikální realitu stroje pro potřeby LLM/RAG systémů platformy systeq.cz.

### 1. Fyzikální a technologický rámec systému (Gantry Plotter Invariants)

Pro zajištění vysokého SNR (odstupu signálu od šumu) při sémantickém vyhledávání musí RAG prostředí striktně dodržovat následující technologické axiomy:

* **Nástrojová hlava a mechanismus:** Systém řídí výhradně mechanický řez prováděný dvouhlavým portálovým plotrem (gantry plotter). Nástroji jsou výhradně fyzické kovové nože: vibrační nůž (Vibrate cutter) a nůž pro V-drážky (V-Slot).
* **Kinematika řezu:** Proces využívá tlačný pohyb nože v porézním materiálu (PET felt). Nejedná se o rotaci ani termální rozpad. Jakákoli terminologie spojená s lasery (např. *výpalek*), frézami či vřeteny je v této doméně neplatná a je nahrazena pojmy **výřez, přířez, dílec nebo segment**.
* **Materiálová materiálová konstanta:** Tloušťka desek z PET feltu je standardizována na $12.0\,\text{mm}$ nebo $24.0\,\text{mm}$. Dělení materiálu je z principu mechanického nože prakticky bezztrátové (nedochází k prořezu/úbytku šířky stopy jako u laseru či frézy).

---

### 2. Dekonstrukce a formalizace pravidel

---

#### H2 Vertikální pravidla (Výška hrotu nástroje)

##### `RULE_H2_VIBRATE_12MM`

* **Status:** Aktivní
* **Spouštěč (Trigger / Matematická podmínka):** `cutter_type_id == 1` (Vibrační nůž) **AND** `material_thickness_mm == 12.0`
* **Závažnost (Severity):** * `CRITICAL`: Pokud je výška hrotu nad prahem $H_2 > 0.1\,\text{mm}$ při vysoké jistotě odhadu tloušťky materiálu (`ThicknessConfidence == HIGH`).
* `WARNING`: Pokud výška hrotu leží mimo doporučený interval $H_2 \notin [-0.5, 0.0]\,\text{mm}$, ale nepřesáhne kritický práh.
* `INFO`: Pokud je tloušťka detekována s nízkou jistotou (`ThicknessConfidence == LOW`) nebo pokud $H_2 == 0.0\,\text{mm}$.


* **Fyzikální dopad na CNC stroj:** Při překročení kritického prahu ($H_2 > 0.1\,\text{mm}$) mechanický nůž neprojde celou tloušťkou desky. Vzniká spodní nedořez v 12mm PET feltu. Výřez nelze čistě oddělit z desky a při manuálním vytrhávání dochází k potrhání textilních vláken a destrukci hrany hotového dílce.
* **Algoritmus nápravy:** Úprava cílového CAM parametru vrstvy na hodnotu v doporučeném pásmu $H_2 \in [-0.5, 0.0]\,\text{mm}$. Tím je vynucen mírný, bezpečný zářez nože do obětované podkladové desky plotru, což garantuje stoprocentní čisté proříznutí.

##### `RULE_H2_VIBRATE_24MM`

* **Status:** Aktivní
* **Spouštěč (Trigger / Matematická podmínka):** `cutter_type_id == 1` (Vibrační nůž) **AND** `material_thickness_mm == 24.0`
* **Závažnost (Severity):** * `CRITICAL`: Pokud $H_2 > 0.1\,\text{mm}$ za podmínky vysoké jistoty tloušťky materiálu.
* `WARNING`: Pokud výška hrotu leží mimo doporučený interval $H_2 \notin [-0.5, -0.2]\,\text{mm}$.
* `INFO`: Degradace při nízké jistotě vstupu (`ThicknessConfidence == LOW`).


* **Fyzikální dopad na CNC stroj:** U silného 24mm materiálu způsobuje kladná nebo nulová výška $H_2$ masivní nedořez. Vzhledem k vysokému mechanickému odporu stlačeného 24mm feltu je u spodní úvratě nutný hlubší zářez. Pokud nůž neprořízne spodní vrstvu, dochází navíc k jeho zvýšenému bočnímu namáhání a ohybu, což deformuje kolmost řezné hrany.
* **Algoritmus nápravy:** Automatický posun koncového bodu osy Z v CAM konfiguraci dané vrstvy do záporných hodnot, ideálně do technologického optima $-0.5$ až $-0.2\,\text{mm}$.

---

#### Sekvenční a hierarchická pravidla (Chronologie řezu)

##### `RULE_SEQ_OUTER_LAST`

* **Status:** Aktivní
* **Spouštěč (Trigger / Matematická podmínka):** Existuje aktivní výstupní vrstva obvodového ořezu vibračním nožem (`cutter_type_id == 1`, `is_output_yes == true`, `total_cut_length_mm > 0`) **AND** v binární struktuře souboru existuje element jiné technologické vrstvy (např. vnitřní výřezy, V-drážky), jehož adresní offset je větší než minimální offset obvodového ořezu: $\min(\text{offsets}_{\text{vibrate}}) < \max(\text{offsets}_{\text{active}})$.
* **Závažnost (Severity):** `CRITICAL`
* **Fyzikální dopad na CNC stroj:** Plotr provede finální vnější ořez dílce z maticové desky *před* dokončením vnitřních struktur a dekorů. Jakmile je obvod kompletně proříznut mechanickým nožem, podtlak (vákuum) stolu již nedokáže samostatný porézní panel spolehlivě zafixovat. Následný tlačný pohyb nože (např. při řezání V-drážek) uvolněný dílec posune, čímž dojde k okamžitému zmetkovitosti geometrie a hrozí mechanické zlomení nože v plotru.
* **Algoritmus nápravy:** Seřazení entit v exportním procesoru. Elementy patřící do vrstvy obvodového ořezu vibračním nožem musí být striktně zapsány na samotném konci binárního streamu (přidělení nejvyšších hexadecimálních adres/offsetů), čímž se vynutí jejich exekuce jako úplně poslední operace nad daným dílcem.

##### `RULE_SEQ_OUTER_LAST_NESTING_OFFSET`

* **Status:** Aktivní
* **Spouštěč (Trigger / Matematická podmínka):** `check_nesting_hierarchy == true` **AND** prvek má definovanou vazbu na nadřazený prvek (`parent_id`) **AND** hexadecimální offset vnitřního prvku v souboru je větší než offset jeho prostorového obalu (rodiče): $\text{offset}_{\text{child}} > \text{offset}_{\text{parent}}$.
* **Závažnost (Severity):** `WARNING`
* **Fyzikální dopad na CNC stroj:** Vnitřní segment (např. vnitřní výřez pro zásuvku nebo stavební otvor) se mechanicky vyřezává až po dokončení řezu jeho vnějšího obalu. Uvolněný okolní materiál ztrácí strukturální integritu a vnitřní vyřezávaný prvek se vlivem vibrací nože a proudu odsávání začne pohybovat, což vede k okousání hran a deformaci rozměrů vnitřního výřezu.
* **Algoritmus nápravy:** Re-indexace nestingové hierarchie v CAM parseru. Algoritmus musí provést topologické třídění geometrických entit tak, aby vnitřní elementy (potomci) měly v binární struktuře nižší offsety (byly řezány dříve) než jejich prostorové obaly (rodiče).

---

#### Fixační pravidla (Fyzika pracovního stolu)

##### `RULE_FIX_SMALL_PANEL`

* **Status:** Aktivní
* **Spouštěč (Trigger / Matematická podmínka):** Celková plocha výkresu (canvasu) vypočtená jako $S = (\text{width} \times \text{height}) / 10^6$ klesne pod limitní bezpečnou plochu: $S < 1.67\,\text{m}^2$.
* **Závažnost (Severity):**
* `WARNING`: Pokud plocha výkresu klesne pod kritickou hranici pro udržení podtlaku: $S < 0.5\,\text{m}^2$.
* `INFO`: Pokud se plocha nachází v suboptimálním intervalu $[0.5, 1.67)\,\text{m}^2$.


* **Fyzikální dopad na CNC stroj:** Vákuový stůl nedokáže vyvinout dostatečnou přidržovací sílu na malé ploše. Vzhledem k vysoké poréznosti PET feltu dochází k masivnímu úniku podtlaku skrz materiál. Tlačný odpor nože při dopředném pohybu snadno utrhne malý dílec z pozice, posune celou geometrii a zničí polotovar.
* **Algoritmus nápravy:** Manuální zásah operátora na dílně vynucený hlášením systému. Je vyžadována fyzická aplikace mechanické fixace papírovou krycí páskou podél minimálně $80\,\%$ obvodu materiálu k okolní desce/stolu, čímž se zamezí podfukování a mechanickému posunu.

---

#### Geometrické a technologické anomálie (CAM validace)

##### `RULE_GEO_V1_EDGE_MERGE_MISSING`

* **Status:** Aktivní
* **Spouštěč (Trigger / Matematická podmínka):** `check_open_in_closed == true` **AND** prostorový index (`cKDTree`) identifikuje otevřenou dráhu (`element_id`), jejíž koncové body leží na/uvnitř uzavřeného rodičovského prvku, přičemž délka nepropojeného segmentu je $\le 200.0\,\text{mm}$.
* **Závažnost (Severity):** `WARNING`
* **Fyzikální dopad na CNC stroj:** * *Typ edge_adjacent:* Otevřená trajektorie lícuje s vnější hranou, ale není s ní vektorově sloučena. Mechanický nůž v tomto bodě namísto plynulého průjezdu zcela zastaví, zvedne se z materiálu, otočí se v ose a znovu se zapíchne. Na hraně dílce vznikají pohledové vady, záseky a otřepy.
* *Typ standalone_tab:* Otevřená křivka značí technologický můstek nebo výčnělek, který nebyl korektně spojen s hlavním obvodem, což vede k duplicitním nebo neukončeným drahám nože.


* **Algoritmus nápravy:** Geometrický modul (modul `vcf_geometry`) automaticky provede operaci "snap" koncových bodů v rámci povolené tolerance a sjednotí navazující entity do jedné uzavřené dráhy. *Poznámka: Validátor obsahuje cross-layer filtr, který toto varování potlačí, pokud se jedná o navazující V-slot dekorativní linie na různých vrstvách se shodnou hloubkou $H_2$ a shodným směrem.*

##### `RULE_GEO_V1_MICRO_SEGMENT`

* **Status:** **VYPNUTO (Deaktivováno v KB z důvodu nízkého SNR)**
* **Spouštěč (Trigger / Matematická podmínka):** `check_micro_segments == true` **AND** délka po sobě jdoucích segmentů (line/arc) je menší než nastavený práh: $L < 1.0\,\text{mm}$.
* **Závažnost (Severity):** `WARNING` / `INFO` (dle vyhodnocení hustotního filtru pro shluky).
* **Fyzikální dopad na CNC stroj:** Extrémní hustota bodů zahlcuje interpolátor řídicího systému (Ruida). Look-ahead plánování zrychlení selhává, což vyvolává mechanické chvění hlavy (stuttering). Výsledkem jsou potrhané, roztřepené hrany PET feltu a neúměrné mechanické namáhání gantry mechanismu.
* **Důvod vyřazení z KB:** Pravidlo generovalo vysoké množství falešně pozitivních detekcí (High False Positive Rate) u přirozených hladkých křivek a spline prvků. Došlo k jeho systémovému potlačení do doby plné rekalibrace filtru hustoty shluků křivek.

##### `RULE_GEO_V1_UNCLOSED_LOOP`

* **Status:** Aktivní
* **Spouštěč (Trigger / Matematická podmínka):** `check_unclosed_loops == true` **AND** geometrická mezera (gap) mezi počátečním a koncovým bodem předpokládané uzavřené smyčky je větší než informační práh: $\text{gap} > 0.1\,\text{mm}$.
* **Závažnost (Severity):** * `CRITICAL`: Pokud je mezera $\text{gap} \ge 5.0\,\text{mm}$ (`unclosed_critical_mm`).
* `WARNING`: Pokud se mezera nachází v intervalu $\text{gap} \in [1.0, 5.0)\,\text{mm}$ (`unclosed_warn_mm`).
* `INFO`: Ignorováno systémem, pokud je gap pod hranicí $1.0\,\text{mm}$ (sémantická degradace při detekci překryvu/overcutu).


* **Fyzikální dopad na CNC stroj:** Dráha nože se geometricky nedovře. Vnitřní nebo vnější vyřezávaný segment zůstane viset na nedoříznutém kusu materiálu (můstku) o velikosti daného gapu. Operátor je nucen díly z desky vytrhávat silou (což ničí strukturu feltu), nebo je ručně dořezávat skalpelem, což radikálně zvyšuje produkční čas a chybovost.
* **Algoritmus nápravy:** Pokud kód detekuje záměrný překryv drah (overcut) v identických koncových bodech, anomálie je degradována. V opačném případě algoritmus automaticky uzavře smyčku protažením koncových bodů (endpoint snap) nebo vložením chybějícího lineárního segmentu, pokud hodnota gapu nepřesáhne kritickou mez.

##### `RULE_GEO_V1_ORPHAN_ELEMENT`

* **Status:** Aktivní
* **Spouštěč (Trigger / Matematická podmínka):** `check_orphans == true` **AND** prvek dosahuje celkové délky $L > 50.0\,\text{mm}$ **AND** jeho prostorová vzdálenost od jakýchkoli jiných prvků na pracovní ploše je větší než limit: $D > 500.0\,\text{mm}$.
* **Závažnost (Severity):** `WARNING`
* **Fyzikální dopad na CNC stroj:** Hlava plotru provádí dlouhý přejezd rychloposuvem na zcela izolované místo desky, kde vyřeže osamocenou entitu. Zpravidla se jedná o zapomenutou geometrii z předchozích revizí výkresu (např. zapomenuté ořezové značky, kousky pomocných čar nebo textové fragmenty rozložené na křivky). Způsobuje to zbytečné prodloužení strojního času a nevratné znehodnocení čisté plochy materiálu desky.
* **Algoritmus nápravy:** Generování vizuálního varování (flag) v uživatelském rozhraní platformy. Validátor vyžaduje explicitní potvrzení od operátora či zadavatele data, zda má být izolovaný prvek z produkčních dat vymazán (`drop`), nebo zda jde o legitimní součást zakázky.

##### `RULE_GEO_V1_5_UNCONNECTED_INTERNAL_DECOR`

* **Status:** Aktivní (V režimu zpřísněné kalibrace)
* **Spouštěč (Trigger / Matematická podmínka):** `check_unconnected_internal_decor == true` **AND** prvek dekorativní vrstvy (nůž pro V-drážky se směrovým parametrem `left` nebo `both`) má volný koncový bod uvnitř bounding boxu panelu, přičemž jeho vzdálenost k nejbližšímu sousednímu vektoru splňuje podmínku: $1.0\,\text{mm} < \Delta \le 3.0\,\text{mm}$.
* **Závažnost (Severity):** `CRITICAL`
* **Fyzikální dopad na CNC stroj:** Nástroj pro V-drážku (V-cutter) nedotáhne dekorativní designovou linii až k průsečíku s jinou linií nebo k samotné hraně akustického panelu. Na hotovém akustickém prvku vzniká fatální estetická vada. Designová linie končí slepě těsně před svým cílem, což je lidským okem okamžitě identifikovatelné jako chyba přípravy dat (grafik nedotáhl čáru v CADu).
* **Algoritmus nápravy:** Geometrický modul aplikuje na volný endpoint dekorativní linie operaci `snap` – automaticky ji prodlouží ve směru jejího posledního vektoru a ukotví ji k nejbližší hraně či linii.
* **Kalibrační poznámka (Dev Alert):** Současné nastavení algoritmu vykazuje limitaci (slepé místo) – **nedokáže spolehlivě zachytit a ošetřit neprotažené dekorativní křivky, u kterých je vzdálenost (gap) menší než $3.0\,\text{mm}$** vzhledem k nastavenému parametru `max_snap_distance_mm` a chování prostorového filtru. Pravidlo je v produkčním jádru ponecháno pod dohledem a probíhá úprava detekčního větvení pro sub-3mm anomálie.