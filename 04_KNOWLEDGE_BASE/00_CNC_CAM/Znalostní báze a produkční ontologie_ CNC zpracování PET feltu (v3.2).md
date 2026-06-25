# **Znalostní báze a produkční ontologie: CNC zpracování PET feltu (v3.2)**

Tento dokument slouží jako formalizovaný znalostní artefakt připravený pro indexaci v RAG systémech a Google NotebookLM. Definuje technologické invarianty, materiálové registry, matici řezných rychlostí a exekutivní pravidla pro zpracování desek ECHOBLOCK® pomocí portálového plotru.

## **1. Technologický a kinematický rámec (Portálový plotr)**

**Portálový plotr (Gantry Plotter):** Proces zpracování je založen výhradně na mechanickém řezu za použití dvouhlavého portálového plotru s řídicím systémem Ruida. Používají se výhradně fyzické ocelové nože: vibrační nůž (Vibrate cutter) a nůž pro V-drážky (V-Slot).  
**Kinematika řezu:** Tlačný a oscilační pohyb nástroje v materiálu zajišťuje čisté, prakticky bezztrátové dělení bez úbytku materiálu (prořezu). Jakákoli laserová nebo frézovací terminologie (např. "výpalek") je v tomto kontextu neplatná.

## **2. Datový tok a prevence GIGO (Inkoherence)**

Pro eliminaci chyb typu Garbage In, Garbage Out (GIGO) byly vyřešeny následující procesní střety v dokumentaci:

| Identifikovaný konflikt | Původní stav v dokumentech | RAG Ground Truth (Odeva) |
| - | - | - |
| **CAM Software** | Zmínka o LightBurn v1.7.08 a souborech .LBRN2 | LightBurn je zakázán (laserový SW). Jedinou CAM autoritou je **VCutWorks v2.00.34** s exportem do binárního formátu **.VCF**. |
| **Terminologie** | Používání výrazu "výpalek" | Výraz "výpalek" je ze systému smazán a nahrazen sémanticky přesnými pojmy: **výřez, přířez, dílec**. |
| **Tloušťka vs. H2 pravidla** | Sendviče 21–24 mm vs. striktní rovnost na tloušťku 24 mm | Pravidla pro osu Z (H2) pracují s dynamickým intervalovým větvením namísto absolutní shody tloušťky, aby nedošlo k poškození stolu u sendvičů. |


## **3. Registr barev (Vzorník HUGO) a produktových vzorů**

Sémantické barevné tóny desek ECHOBLOCK® (lisovaný PET recyklát s hustotou 202 kg/m³ a plošnou hmotností 2400 g/m³), které jsou fyzicky mapovány na vzorník HUGO na stěně dílny:

- **Dark Knight:** Černá / Tmavě antracitová. Vysoká hustota materiálu, minimální viditelnost drobných otřepů.

- **Silver Fox:** Světle šedá / Stříbrytá. Vysoký vizuální kontrast hran při kontrole drah.

- **Matcha:** Světle zelená / Pastelová. Náchylná na pohledové vady při suboptimálním přítlaku.

- **Savanna:** Olivová / Tmavě zelená. Standardní tón pro interiérovou akustiku.

- **Camel:** Písková / Světle hnědá. Texturovaný povrch se specifickým mechanickým odporem při řezu.

- **Ice Blue / Blue Sky:** Světle modrá. Často využívaná v sendvičových kombinacích.

- **Sunflower:** Sytě žlutá. Výrazný pigment, vysoké riziko znečištění, vyžaduje absolutně čistý pracovní stůl.

- **Pink Panther:** Růžová / Magenta. Specifická zakázková šarže.

- **Marsala / Terracotta:** Cihlově červená / Vínová. Vyšší podíl pojiva, vyžaduje stoprocentně ostrý břit nože.

## **4. Matice řezných rychlostí dle geometrické složitosti**

Tato tabulka definuje doporučené rychlosti řezu a chování interpolátoru Ruida v závislosti na charakteru geometrie. Formát umožňuje přímou editaci a doplňování empirických dat z výroby.

| Třída složitosti | Charakter geometrie | Příklady vzorů / produktové řady | Nástroj | Doporučená rychlost (mm/s) | Look-Ahead / Kinematika stolu |
| - | - | - | - | - | - |
| **Třída 1 (Nízká)** | Plynulé polylines, dlouhé přímé linie, obvodové ořezy panelů. | Manchester, Baffly (Lamelové stropy), Groove vzory | Vibrate cutter / V-Slot | 100 – 200 | Maximální plynulost, plynulé zrychlení bez vibrací portálu plotru. |
| **Třída 2 (Střední)** | Vlnovité trajektorie, mírné prostorové zakřivení, křížené polygonální sítě drážek. | Wave, Chevron, Diamond, Maze, Hexa vzory | Vibrate cutter / V-Slot | 100 – 150 | Vyžaduje look-ahead plánování pro zamezení chvění gantry portálu v ohybech. |
| **Třída 3 (Vysoká)** | Komplexní kontury, mikroskopické a krátké segmenty, texty, firemní loga, přerušované zářezy. | Gills (Žábry), Geometrie textového loga, Beehive, Roma | Vibrate cutter | 40 – 80 | Striktní omezení rychlosti pro zamezení chvění hlavy (stuttering) a potrhání vláken feltu. |


## **5. Validační matice pravidel (KB Engine Rules)**

Strukturovaný přehled aktivních pravidel pro validační engine integrovaný do platformy systeq.cz:

### **5.1 Vertikální pravidla (Osa Z)**

- **RULE\_H2\_VIBRATE\_12MM:** Spouští se pro 12mm materiál. Cílové pásmo $H\_2 \\in \[-0.5, 0.0\]\\,\\text\{mm\}$ pro bezpečný zářez do obětovaného podkladu. Vyšší hodnoty ($H\_2 \> 0.1\\,\\text\{mm\}$) způsobují spodní nedořez.

- **RULE\_H2\_VIBRATE\_24MM:** Spouští se pro 24mm materiál a sendviče. Cílové pásmo $H\_2 \\in \[-0.5, -0.2\]\\,\\text\{mm\}$ kvůli vysokému mechanickému odporu lisovaného feltu.

### **5.2 Sekvenční pravidla (Chronologie řezu)**

- **RULE\_SEQ\_OUTER\_LAST:** Obvodový ořez musí mít nejvyšší adresní offset v binárním souboru .VCF. Zamezuje uvolnění dílce před dokončením vnitřních drážek, což by vedlo k selhání vákuové fixace.

- **RULE\_SEQ\_OUTER\_LAST\_NESTING\_OFFSET:** Topologické třídění nestingové hierarchie. Vnitřní prvky (potomci) musí mít v binárním streamu nižší offset (řezány dříve) než jejich prostorový obal (rodič).

### **5.3 Fixační a geometrická pravidla**

- **RULE\_FIX\_SMALL\_PANEL:** Aktivuje se při ploše výkresu \< 1.67 m². Vyžaduje mechanické olemování páskou z minimálně 80 % obvodu jako obranu proti úniku podtlaku skrz porézní strukturu.

- **RULE\_GEO\_V1\_EDGE\_MERGE\_MISSING:** Detekuje nepropojené otevřené dráhy do 200 mm lícující s hranou. Spouští automatický geometrický snap, aby se zamezilo zvedání a otáčení nože v materiálu.

- **RULE\_GEO\_V1\_UNCLOSED\_LOOP:** Validuje nedovřené smyčky. Kritická mez geometrické mezery (gapu) je \>= 5.0 mm. Vyžaduje automatické protažení koncových bodů, jinak hrozí nutnost ručního dořezávání skalpelem.

- **RULE\_GEO\_V1\_ORPHAN\_ELEMENT:** Detekuje izolované prvky delší než 50 mm ve vzdálenosti nad 500 mm od zbytku geometrie (zapomenuté pomocné čáry či ořezové kříže z CADu).

- **RULE\_GEO\_V1\_5\_UNCONNECTED\_INTERNAL\_DECOR:** Detekuje nedotažené linie V-drážek v toleranci 1.0 až 3.0 mm od hran. Automaticky aplikuje prodloužení a snap k hraně. *Kalibrační poznámka: Aktuálně pod zvýšeným dohledem, neprotažené dekorativní křivky sub-3mm vyžadují rekalibraci prostorového filtru.*

- **RULE\_GEO\_V1\_MICRO\_SEGMENT:** *DEAKTIVOVÁNO.* Vyřazeno ze znalostní báze z důvodu nízkého SNR a vysokého výskytu falešně pozitivních detekcí (High False Positive Rate) u hladkých křivek/splines.

