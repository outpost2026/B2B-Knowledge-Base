---------------------
## SYSTEQ: Technický stav vývoje a operační jádro (Verze v31)
Tento dokument shrnuje aktuální stav vývoje platformy SYSTEQ k červnu 2026. Zachycuje reálné parametry systému, architekturu kódu, pravidla znalostní báze a strategické směřování projektu po dokončení vývojové fáze B2B. Dokonale doplňuje teoretickou vizi empirické shody modelu s realitou o reálná provozní data.
------------------------------
## 1. Souhrn stavu projektu a strategický směr

* Autor dokumentu: Ondřej Soušek (SYSTEQ / Outpost2026)
* Datum revize: 19. června 2026
* Aktuální vývojová větev: features/2D_visual_warnigs (65 commitů celkem, 87 commitů před hlavní větví main)
* Strategické rozhodnutí: Po vypršení termínu pro dodání formálních specifikací dochází k izolaci projektu. Spouští se ochranné protokoly. Veškerá kapacita vývoje se přesouvá na generickou SaaS architekturu dostupnou na webu systeq.cz.
* Provozní principy: Platí přísná pravidla pro ochranu hodnoty (Axiom 04). Interaktivní přístup je podmíněn zálohou. Veškerá dokumentace a zaškolení jsou vyčleněny jako samostatně zpoplatněná služba, nikoli jako automatický bonus k softwaru.

------------------------------
## 2. Technologický stěžeň (Tech Stack) a Nasazení
Aplikace běží na stabilním a moderním inženýrském základu:

* Jazyk: Python 3.11
* Webový framework: Streamlit 1.58.0 (včetně optimalizace pro stabilní udržení webových spojení)
* Klíčové knihovny: matplotlib 3.8.0 pro vizualizaci a pandas 2.2.0 pro analýzu dat.
* Infrastruktura: Celý systém je zabalen v Dockeru. Přes službu Artifact Registry je nasazen do Google Cloud Run (lokace europe-west1).
* Demo prostředí: Funkční verze běží jako Cloud Run aplikace. Rozhraní Streamlit se správně vykresluje a komunikuje.

------------------------------
## 3. Výsledky testování a technické dluhy

* Stav testů: Všechny testy úspěšně prošly (8 z 8). Jsou pokryty základní funkční testy, testy determinismu i takzvaný "Golden Master" test.
* Známé softwarové chyby: V samotném kódu nejsou žádné známé chyby. Přetrvává pouze drobná chyba s nesprávným typem souboru (MIME typ) u stahovacího tlačítka, jejíž oprava zabere asi 15 minut.
* Technologické dluhy:
1. Chybí automatické nasazování (CI/CD pipeline).
   2. Nesoulad v označení verzí (konfigurace uvádí verzi 1.7, reálně je nasazena verze 1.3-demo).
   3. Chybí automatické sledování zdraví aplikace (Health check) a monitoring provozu.

------------------------------
## 4. Mapa softwarových modulů (Struktura kódu)
Systém SYSTEQ je striktně rozdělen do specializovaných souborů. Kód se drží zásady čistoty – nepoužívá složitou dědičnost, ale přímé a srozumitelné třídy.

* src/app.py: Hlavní panel (dashboard). Má 1082 řádků. Obsahuje rozhraní rozdělené podle rolí (pro obchodníky a pro dílnu s CNC stroji).
* src/vcf_parser_v20.py: Jádro celého parseru (RuidaVcfEngineV20). Zajišťuje samotné čtení a zpracování souborů.
* src/vcf_binary_reader.py: Binární čtečka. Zpracovává specifické verze souborů, pracuje se segmenty o velikosti 74B a mapuje 14 základních barev.
* src/vcf_geometry.py: Geometrické výpočty (1197 řádků). Obsahuje více než 20 funkcí pro vyhledávání blízkosti objektů.
* src/vcf_time_predictor.py: Model pro předpověď času řezání. Dosahuje vysoké přesnosti s odchylkou pouhých +- 2 až 5 %.
* src/vcf_config.py: Načítání konfigurace. Stará se o parametry stroje, oceňování a přepisování pravidel.
* src/Knowledge_base/engine.py: Srdce znalostní báze. Obsahuje 8 hlavních validačních metod, které v kódu hledají výrobní vady (např. neuzavřené smyčky nebo mikrosegmenty).
* src/Knowledge_base/models.py a rules.json: Definice datových struktur pro pravidla a jejich konkrétní nastavení.

------------------------------
## 5. Pravidla znalostní báze a závažnost chyb (KB Rules)
Znalostní báze SYSTEQ automaticky vyhodnocuje geometrii výrobku a varuje před riziky:

* CRITICAL (Kritická chyba) – NEUZAVŘENÁ SMYČKA (UNCLOSED_LOOP): Detekuje smyčky, které na sebe nenavazují. Pokud však prvky sdílí koncové body s jinými díly, systém hrozbu automaticky sníží pouze na informativní.
* WARNING (Varování) – CHYBĚJÍCÍ CAM HRANY (EDGE_MERGE_MISSING): Chybějící hrany. Systém obsahuje speciální algoritmus, který dokáže tyto hrany sám dopočítat a zrekonstruovat.
* WARNING (Varování) – RIZIKO PODTLAKOVÉ FIXACE (VACUUM_FIXATION_RISK): Spustí se, pokud je plocha dílu menší než 200 mm² nebo celý panel menší než 0.2 m². Varuje operátora, že díl se může při frézování posunout a je nutné ho zajistit páskou.
* WARNING (Varování) – OSIŘELÝ PRVEK (ORPHAN_ELEMENT): Označuje osamocené prvky, které jsou dále než 500 mm od nejbližšího objektu.
* WARNING (Varování) – NEPROPOJENÝ INTERNI DEKOR (UNCONNECTED_INTERNAL_DECOR): Detekuje vnitřní ozdoby, které nejsou napojené na hlavní dráhu (při vzdálenosti nad 3 mm).
* INFO (Informativní) – MIKROSEGMENT (MICRO_SEGMENT): Detekuje extrémně malé úseky pod 1 mm. Jsou automaticky filtrovány hustotním filtrem.

------------------------------
## 6. Dokončené funkce v nejnovější verzi (v31)
V rámci posledního vývojového cyklu byly úspěšně nasazeny a ověřeny tyto funkce:

* Pokročilé slučování vrstev: Propojení technologických skupin pro kontrolu chybějících hran a vnitřních dekorů.
* Nový vizuální dashboard: Kompletní redesign rozvržení. Obsahuje rychlý přehled, fixovaný záhlavní panel a hlavně vizuální overlay vrstvu, která vykresluje zjištěné geometrické vedy přímo přes 2D model výrobku.
* Logování chyb: Frontend aplikace nyní automaticky ukládá veškeré chyby do přehledných textových souborů JSON v adresáři docs/Frontend_logs/.
* Audit shody s realitou: Úspěšně proběhl audit, který odhalil a opravil 7 nesrovnalostí mezi kódem a dokumentací. Příručka pro vedení projektu nyní stoprocentně odpovídá reálnému stavu kódu.
