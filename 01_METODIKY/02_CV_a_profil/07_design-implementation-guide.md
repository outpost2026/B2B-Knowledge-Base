# Design & implementační guide — CV/One-Pager balíček

Doprovodný dokument k 6 textovým souborům (CZ/EN × one-pager B2B/HPP × full CV).


## 1. Proč dvě varianty one-pageru

**B2B varianta** mluví jazykem klienta, který řeší konkrétní bolest ("ztrácíme know-how", "máme formát bez SDK"). Otevírá se problémem, ne tvým CV. Case study je nahoře, ne dole. Tabulka "co přináším" je orientovaná na služby, ne na technologie.

**HPP/recruiter varianta** mluví jazykem náborového procesu — recruiter/HR scanuje 6–8 sekund a hledá: titul/seniority, tech stack, roky praxe, lokalita, dostupnost. Proto je nahoře titul "Python Developer | Automatizace, CAM/CNC integrace & Cloud (GCP)" — konkrétní, ATS-friendly, ne metaforický ("Domain-Driven Automation Engineer" zní zajímavě lidem, ale ATS a recruiteři ho nemají v searchi).

Obě varianty sdílí faktickou bázi (žádné nekonzistence v číslech/datech), liší se jen framing a pořadí sekcí.


## 2. Layout & typografie (pro Canva/Word/LaTeX)

### Barevná paleta

- **Primární tmavě modrá:** `\#1B3A5C` (nadpisy, hlavní akcent) — důvěra, technologie

- **Šedá:** `\#4A4A4A` (běžný text), `\#8A8A8A` (sekundární info jako lokace/kontakt)

- **Zelený akcent:** `\#2E7D5B` (checkmarky, klíčové metriky, CTA prvky) — manufacturing/growth konotace

- **Pozadí:** bílé, případně velmi světle šedá `\#F7F8FA` pro boxy/tabulky

### Typografie

- **Nadpisy:** Arial / Helvetica Neue / Inter — bold, 14–18 pt

- **Tělo textu:** stejná rodina, regular, 10–11 pt (one-pager musí být hustý, ale čitelný)

- **Zachovej jednu rodinu fontů** napříč dokumentem — žádné mixování serif/sans

### Hierarchie a whitespace

- One-pager: max 2 úrovně nadpisů (H1 jméno+titul, H2 sekce). Žádné H3 — nevejde se to.

- Mezi sekcemi minimálně 12–16 pt mezera — dokument nesmí působit jako stěna textu.

- Tabulka "Co přináším" / "Core Skills" — použij 2sloupcovou tabulku se světle modrým/šedým podkladem hlavičky, ne čistý seznam odrážek. Lépe skenovatelné.

- Emoji - vynechat/neimlementovat.

### Konkrétní postup exportu

**Canva (doporučeno pro vizuální one-pager):**

1. Vyber šablonu "Professional Resume" nebo "Corporate One-Pager", smaž defaultní obsah.

2. Nastav barevnou paletu výše jako brand kit (Canva → Brand Kit → Colors).

3. Vlož text sekci po sekci z .md souboru — Canva markdown needs manual bullet/heading conversion, ale struktura nadpisů je už hotová v souboru.

4. Export: PDF Print (ne PDF Standard) pro tisk-kvalitní výstup, nebo PNG pro LinkedIn Featured.

**Word → PDF (doporučeno pro full CV, ATS-friendly):**

1. Mohu rovnou vygenerovat `.docx` s nastylovanými nadpisy, tabulkami a barvami podle palety výše — stačí říct a připravím soubor pomocí docx skillu (přesné DXA rozměry, žádné ruční odrážky, validované).

2. Pro ATS kompatibilitu (HPP varianta!) drž se jednoho sloupce, žádné textboxy ani vložené obrázky s textem — ATS parsery je neumí přečíst.

**LaTeX (pokud chceš nejvyšší typografickou kontrolu):**

- Doporučený balíček: `moderncv` (styl `classic` nebo `banking`) s custom barvami přes `\\definecolor` podle palety výše.

- Pro B2B variantu zvaž spíš čistý `article` + `titlesec`/`tabularx` — moderncv vizuálně křičí "životopis", což na B2B klienta může působit jako přihláška do zaměstnání, ne jako nabídka spolupráce.


## 3. SEO/LinkedIn klíčová slova (zakomponovaná do textů)

V dokumentech jsou cíleně použita tato spojení (LinkedIn fulltext search i lidské skenování): `Manufacturing Automation`, `Reverse Engineering`, `CAM/ERP Integration`, `Deterministic Parser`, `Python Developer`, `GCP / Cloud Run`, `CNC`, `DXF`, `B2B`, `Industrial Automation`

**Doporučení pro LinkedIn profil samotný** (mimo tyto dokumenty):

- Headline: použij přesně titul z HPP one-pageru — "Python Developer | Automatizace, CAM/CNC integrace & Cloud (GCP)" — recruiter search na LinkedIn váží headline nejvíc.

- Featured sekce: nahraj B2B one-pager jako PDF/PNG (vizuálně silnější, pro lidi co kliknou na profil) + odkaz na live demo zvlášť jako "Link".

- About sekce: použij odstavec z PROFIL sekce full CV, mírně zkrácený.


## 4. Integrace na systeq.cz

Doporučená struktura:

**`/profile`** (nebo `/o-mne`)

- HPP-style obsah, ale jako web stránka ne PDF — plynulý text z PROFIL + Co přináším + Pracovní zkušenosti.

- CTA na konci: tlačítko "Stáhnout CV (PDF)" → linkuje na hostovaný PDF export full CV.

- Druhé CTA: "Stáhnout one-pager" pokud chceš nabízet i kratší verzi ke stažení.

**`/portfolio`**

- Postav primárně kolem case study struktury z "KLÍČOVÝ PROJEKT" sekce (Vstupní stav → Proces → Výsledek → Hodnota) — tenhle framework je silný a opakovatelný, použij ho jako šablonu i pro budoucí projekty (cad2llm, RAG indexer), jakmile budou mít vlastní změřitelné výsledky.

- Vlož přímo embed nebo screenshot Streamlit dashboardu vedle textu, ne jen odkaz — vizuální důkaz zvyšuje konverzi víc než text.

- Live demo link prominentně jako tlačítko, ne jako text v odstavci.

**Obecně:**

- Texty z B2B one-pageru jsou psané tak, aby šly téměř 1:1 použít jako landing page kopie pro `/portfolio` nebo `/sluzby` — strukturа "Co řeším → Důkaz → Co přináším → Pro koho to dává smysl" je standardní a fungující B2B conversion framework (problem-solution-proof-CTA).

- Anonymizace klienta ("B2B výrobní klient, 200+ zakázek/měsíc") je na webu v pořádku i dlouhodobě, dokud nebude NDA spor s Wynwood vyřešený nebo dokud nezískáš jiného klienta, kterého můžeš jmenovat s jeho souhlasem.


## 5. Co bych doporučil příště

- Až budeš mít druhého jmenovaného klienta (i menšího), nahraď anonymizovaný case druhým, jmenovaným — jmenovaná reference vždy konvertuje líp než anonymizovaná, i když je menší.

- cad2llm a RAG indexer jsou v CV zmíněné jen jednou větou (one-pager v1.1) — pokud mají change měřitelný výsledek (přesnost, rychlost, počet zpracovaných dokumentů), zaslouží si vlastní mini-case-study po vzoru VCF parseru.

- Zvaž jednu větu navíc do "Hledám" sekce, která explicitně zmiňuje hodinovou/projektovou sazbu nebo rozsah (i orientačně) — B2B kontakty často odpadnou hned na první emailu kvůli nejasnosti rozpočtu, a tys to nikde neuvedl.

