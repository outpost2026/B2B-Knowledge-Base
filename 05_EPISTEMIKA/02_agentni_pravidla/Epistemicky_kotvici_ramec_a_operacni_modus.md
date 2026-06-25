# EPISTEMICKÝ KOTVÍCÍ RÁMEC & OPERAČNÍ MODUS

**Meta-handoff v3.0 // Prevence informační entropie a kognitivního overfittingu**
**Subjekt/Autor:** Architekt systému (Ondřej Soušek)
**Kontext nasazení:** SYSTEQ Parser (Iterace geometrických anomálií) & Obecná kognitivní architektura
**Datum platnosti:** Od června 2026

---

## 1. Jádrový axiom: Komprese vs. Akumulace

Inteligence systému nespočívá v množství zpracovaných dat, ale ve schopnosti najít **minimální možný algoritmus (generátor)**, který realitu spolehlivě vysvětlí.
Přidávání dalších proměnných, vrstev a výjimek do detekčního modelu nezvyšuje jeho přesnost; zvyšuje jeho informační entropii, snižuje Signal-to-Noise Ratio (SNR) a vede k přeučení (overfitting).

**Pravidlo 0:** Složitost je parazit. Dokonalosti není dosaženo tehdy, když už není co přidat, ale tehdy, když už nelze nic odebrat, aniž by se model zhroutil.

---

## 2. Model hrozby: "The Rabbit Hole" & Statistický drift

Současná iterace SYSTEQ parseru (flagování geometrických anomálií) čelí specifickému epistemickému riziku:

1. **Pokušení detailu:** Snaha ošetřit každou mikroskopickou odchylku DXF/VCF geometrie vede k explozi počtu pravidel.
2. **Statistický drift:** Pokud geometrická a fyzikální pravidla selhávají, vzniká tendence kompenzovat to vhozením obrovského množství surových dat do statistického modelu.
3. **Ztráta kontextu:** Přechod od role "tvůrce struktur" do role "čističe anomálií". Možnosti selhání reality jsou nekonečné; nelze je všechny algoritmizovat.

**Řešení:** Zastavit akumulaci dat. Krok zpět k abstrakci.

---

## 3. Ohraničení interakce s LLM (Mantinely kognitivní fúze)

LLM (konverzační i agentní AI) je ze své podstaty pravděpodobnostní textový motor. Bez pevných hranic bude generovat nekonečné množství kódu, pokrývat edge-cases ad absurdum a navrhovat zbytečně komplexní matematické knihovny.

Tento dokument definuje fixní role pro hybridní vývoj:

* **Autor (Architekt):** Definuje fyzikální baseline (mantinely CNC stroje, vlastnosti V-slotu, podtlak). Vynucuje redukci dimenzionality. Drží konečný B2B cíl. Udržuje "Ground Truth".
* **LLM (Syntaktický kompilátor):** Píše boilerplate, regexy, refaktoruje, navrhuje syntaxi. **Nesmí** svévolně přidávat novou logickou komplexitu bez explicitního příkazu.

**Když LLM navrhne složité ML řešení nebo integraci obří knihovny pro banální problém, Architekt musí návrh okamžitě zamítnout a vyžádat si deterministické, geometrické řešení.**

---

## 4. Provozní protokoly pro aktuální vývoj (Geometric Anomaly Flagging)

Při vývoji logiky pro detekci geometrických defektů (křížící se řezy, nemožné úhly, chybějící offsety) se Architekt řídí striktní posloupností:

### KROK 1: Absolutní fyzikální determinismus

Dříve než je do systému vpuštěna statistika nebo heuristika, musí být aplikována nekompromisní fyzika stroje.

* *Otázka:* Lze anomálii popsat čistou euklidovskou geometrií?
* *Příklad:* V-slot nůž má fyzickou šířku. Ostrý úhel pod určitou hranici způsobí destrukci materiálu. Toto je fyzikální fakt, ne pravděpodobnost. Pravidlo musí být hardcoded (IF úhel < limit THEN fatal_error).

### KROK 2: Redukce dimenzionality (Makro > Mikro)

Zákaz analyzování každého bodu v polyčáře, pokud to není absolutně nezbytné.

* Vytvořit **makro-deskriptory**. Vypočítat globální metriky (poměr obvodu a plochy, bounding box, hustota bodů).
* Většina defektních výkresů (např. roztříštěné entity, duplicitní čáry) se prozradí sama abnormálním makro-deskriptorem (obří počet elementů na extrémně malé ploše). Není nutné mapovat každý průsečík.

### KROK 3: Graceful Degradation & Flagování

Přijmout fakt, že systém nedokáže automaticky vyřešit 100 % případů.

* Jakmile pravděpodobnost správné interpretace anomálie klesne pod 85 % (začíná overfitting na specifické případy), **vývoj na dané větvi se zastavuje**.
* Systém místo složitého hádání vygeneruje `FLAG: HUMAN_REVIEW`.
* B2B hodnota nespočívá v absolutní bezchybnosti stroje, ale v tom, že stroj spolehlivě ukáže prstem na 5 % problematických míst a zbylých 95 % propustí.

### KROK 4: Sanitizace vstupů (Ochrana SNR)

Před přidáním jakéhokoliv nového datového vstupu (feature) do parseru probíhá test:

* *Snižuje tato proměnná entropii systému?*
* Pokud nová proměnná (např. analýza tloušťky čáry z DXF) pomůže vyřešit 1 anomálii z 1000, ale zanese šum do zbylých 999 případů, proměnná se zahodí. Ochrana poměru Signál/Šum je absolutní prioritou.

---

## 5. Závěrečný kotvící princip pro Architekta

Kdykoliv se během vývoje dostaví kognitivní zahlcení, pocit "nekonečné králičí nory" nebo ztráta architektury v detailech kódu, platí povel k zastavení exekuce a aplikace tohoto invariantu:

> **Tvou primární rolí není ošetřit všechny myslitelné chyby grafika nebo CNC operátora. Tvou primární rolí je postavit síto s tak exaktní geometrií, že propadne jen to, co má reálnou tržní a fyzikální hodnotu, a zbytek uvízne jako jasně identifikovatelný šum.**

*Při interakci s LLM používej tento dokument jako iniciální kontext pro resetování generativních vzorců modelu a jeho návrat k deterministické, kompresní logice.*