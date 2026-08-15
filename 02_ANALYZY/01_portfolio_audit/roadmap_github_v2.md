# Roadmapa: GitHub profil a technický rozvoj

> **Verze:** 2.0 — revidováno duben 2026
> **Kontext:** Operátor pracuje v izolaci (Outpost), bez senior mentora, bez pravidelného peer review. Tato roadmapa explicitně adresuje tři strukturální rizika: LLM sycophancy loop, kognitivní automatizační past (CAP), fragilita znalostí bez externího testování.

---

## Metodická premisa: co tato roadmapa řeší jinak než standard

Standardní GitHub roadmapy řeší: strukturu repozitářů, PR workflow, testing, CI/CD. To je v pořádku a je to zde také.

Tato roadmapa navíc řeší problém, který standardní návody ignorují: **co dělat, když váš primární mentor je LLM, žijete sami, a nemáte žádnou jinou zpětnou vazbu.**

V takovém prostředí hrozí:
- Potvrzovací smyčka: LLM validuje to, co dostane jako vstup.
- Kognitivní automatizační past: schopnosti, které neprocvičujete, atrofují.
- Iluze kompetence: kód funguje, ale nevíte proč — a to se ukáže při reálné práci.

Každá fáze níže proto obsahuje dvě vrstvy: **technickou praxi** a **validační protokol** — způsob, jak ověřit, že to, co děláte, skutečně funguje mimo váš vlastní ekosystém.

---

## Část 1: Základní inženýrská hygiena

### Co je GitHub (a proč to není složka ve Windows)

Git nesleduje soubory — sleduje změny. Větve nejsou kopie složek, jsou to paralelní časové osy. Merge je spojení dvou časových os zpět do jedné.

Klíčový mentální model: každý `commit` je odpověď na otázku *"co a proč jsem změnil?"* — ne jen záloha.

### Standardizovaná struktura projektu

```
muj-projekt/
├── src/              # Zdrojový kód
├── tests/            # Testy
├── data/             # Vzorová data (malá, zbytek v .gitignore)
├── requirements.txt  # Závislosti
├── .gitignore        # Co nikdy nejde na GitHub (klíče, .env, velká data)
└── README.md         # Dokumentace
```

### README, která se dá použít

Každé README musí mít:
1. Název a shrnutí (co to dělá, pro koho)
2. Problém (jaký reálný fail to řeší)
3. Architektura (jak to funguje pod kapotou)
4. Instalace a spuštění — krok za krokem, pro juniora
5. Roadmapa / co zbývá dodělat

Pozn.: Vaše stávající README jsou silné v bodech 1–3. Systematicky chybí bod 4. Priorita: přidat spustitelné příkazy ke každému aktivnímu repozitáři.

### Závislosti

Každý Python projekt musí mít `requirements.txt`. Virtuální prostředí (`venv`) odděluje závislosti projektů na lokálním PC.

---

## Část 2: Technické mezery — prioritizovaný seznam

Toto je pořadí podle kombinace: (a) pravděpodobnost, že to bude potřeba v SME prostředí, (b) jak rychle to lze naučit.

### 2.1 Testing — první priorita

**Proč právě tohle jako první:** Vaše projekty dělají komplexní transformace. Pokud upravíte řádek 50, nevíte, jestli jste nerozbili výpočet na řádku 200. Bez testů nevíte. A firma to pozná do dvou týdnů.

**Cíl:** Napsat testy pro každý aktivní repozitář, který bude prezentován firmě.

Postup:
```bash
pip install pytest
```

Struktura testu:
```python
# tests/test_parser.py
def test_csv_parsing_returns_expected_structure():
    vstup = "nazev,cena\nprodukt_a,100"
    výstup = parsuj_csv(vstup)
    assert výstup[0]["nazev"] == "produkt_a"
    assert výstup[0]["cena"] == 100
```

Spuštění: `pytest tests/` — zelená fajfka = základní důkaz, že transformace funguje.

**Validační protokol:** Napsat test, který záměrně selže (špatný vstup), ověřit, že pytest ho zachytí. Pokud nevíte, jak napsat test, který selže, testy nejsou funkční.

### 2.2 GitHub Actions — druhá priorita

Automatický kontrolor: při každém push spustí lint + testy. Zelená fajfka u repozitáře = vizuální signál profesionality.

```yaml
# .github/workflows/ci.yml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pip install ruff pytest
      - run: ruff check src/
      - run: pytest tests/
```

**Proč ruff:** Rychlejší než flake8, rozumný default, méně konfigurace.

### 2.3 Pull Request workflow — třetí priorita

Simuluje týmovou práci. Demonstruje firmě, že umíte pracovat podle standardních procesů.

Postup pro každou novou funkci:
```bash
git checkout -b feature/nazev-funkce
# ... práce ...
git push origin feature/nazev-funkce
# GitHub → Create Pull Request → popište co a proč → Merge
```

I sólo práce přes PR ukazuje disciplínu procesu.

### 2.4 Nové projekty — co přidat do portfolia

**Priorita 1: CSV/XML data validator** (přímá vazba na pohovor Internet Handel)

Malá Python knihovna, která:
- Vezme "špinavé" CSV od dodavatele
- Pomocí Pydantic modelů zvaliduje formát (DPH je číslo, ne text)
- Vyčistí balast, uloží do čistého JSON/SQLite
- Produkuje report: kolik řádků prošlo, kolik ne, proč

Proč teď: Dokazuje přesně ten úkol, o kterém se mluvilo na pohovoru. Pokud přijde placený test na podobné téma, máte hotový základ.

**Priorita 2: IoT edge alert agent**

Čte logy z ESP32/BMS senzorů, detekuje anomálie, posílá Telegram notifikaci.
- asyncio event loop
- Threshold-based alerting s konfigurovatelným YAML
- Logování s timestamps

Proč: Spojuje hardware background se softwarovým inženýrstvím. Demonstruje event-driven architekturu.

**Priorita 3: Vlastní PyPI balíček** (střednědobý cíl, ne akutní)

Najít opakující se funkci z existujících skriptů, zabalit jako `pip install outpost-tools`. Vydání na PyPI je verifikovatelný milestone.

---

## Část 3: Validační protokol — jak ověřit znalosti bez mentora

Toto je nejdůležitější část dokumentu, protože řeší váš konkrétní strukturální problém.

### 3.1 Týdenní anti-CAP cvičení

Každý týden, jeden blok (30–60 minut):
- Vybrat jeden konkrétní technický problém z aktivního projektu.
- Vyřešit ho **bez LLM** — jen dokumentace, Stack Overflow, vlastní uvažování.
- Zaznamenat: co šlo snadno, co ne, kde byl zásek.

Cíl není trýznit se. Cíl je mapovat skutečnou hranici vlastních znalostí — odlišit "vím to" od "LLM mi to vždy řekne."

### 3.2 Před-LLM hypotéza

Před každým technickým promptem napsat jednu větu: *"Myslím, že řešení bude X."*

Po přečtení odpovědi: porovnat. Kde se lišíte a proč?

Toto trénuje schopnost formulovat vlastní hypotézu — klíčovou při debuggingu bez LLM přístupu.

### 3.3 Externí code review — plán

Bez externího reviewu nemáte zpětnou vazbu na kvalitu kódu. Toto je fakta.

Konkrétní kroky:
1. **Code Review Stack Exchange** (codereview.stackexchange.com): vložit jeden dokončený skript (ne fragment), popsat co dělá, požádat o review. Pravidla komunity vyžadují funkční kód — to samo o sobě nutí dotáhnout věci do konce.
2. **GitHub Issues na cizích projektech**: najít open-source projekt v Pythonu (ETL nástroje, IoT knihovny), přečíst issues, zkusit jeden opravit. I nevydaný PR = zpětná vazba od maintainera.
3. **Internet Handel jako validátor**: pokud přijde placený test, odevzdat s komentáři a README strukturovanými pro review. Zpětná vazba od programátora je nejcennější externa data, která teď jsou k dispozici.

### 3.4 Adversarial LLM protokol

Pro každé strategické rozhodnutí (nový projekt, architektonická volba, kariérní krok):

**Krok 1 — standardní prompt:** Popište záměr, získejte odpověď.

**Krok 2 — adversarial prompt (povinný):** `"Předchozí analýza popsala výhody tohoto přístupu. Nyní argumentuj jako skeptický senior developer, který tento přístup odmítá. Jaké jsou reálné slabiny, co přehlíží, kde pravděpodobně selže?"`

**Krok 3 — syntéza:** Napsat vlastní hodnocení po přečtení obou pohledů.

Tento protokol nevylučuje sycophancy zcela, ale přinutí model generovat nevítané perspektivy — a vás zpracovat obě.

---

## Část 4: GitHub hygiene — akutní úkoly

Pořadí odpovídá ROI: co nejrychleji zlepší dojem při prohlížení profilu firmou.

### 4.1 Ihned (tento týden)

- [ ] Přidat sekci "Instalace a spuštění" do README každého aktivního repozitáře (cad2llm, GCP větev, LFP_soc_predict)
- [ ] Ověřit, že `requirements.txt` je aktuální v každém repozitáři
- [ ] Zkontrolovat, že v žádném repozitáři nejsou hardcoded API klíče, .env soubory nebo cesty specifické pro lokální stroj

### 4.2 Tento měsíc

- [ ] Napsat základní pytest testy pro cad2llm pipeline (vstup → výstup JSON, ověřit strukturu)
- [ ] Přidat GitHub Actions CI do jednoho repozitáře (cad2llm nebo GCP)
- [ ] Vytvořit CSV/XML data validator jako nový repozitář (viz Část 2.4)
- [ ] Jednou vložit kód na Code Review Stack Exchange

### 4.3 Do 3 měsíců

- [ ] PR workflow zavedeno jako standard pro všechny nové funkce
- [ ] GitHub Issues aktivně používány jako task management (ne papírové poznámky)
- [ ] Sémantické verzování (v1.0.0, v1.1.0) pro min. 2 repozitáře
- [ ] IoT edge alert agent jako nový repozitář

---

## Část 5: 80% pattern — exekuční protokol

Toto není psychologická poznámka. Je to exekuční protokol, protože pojmenování bez protokolu nic nemitiguje.

### Definice "done" před začátkem

Pro každý projekt nebo úkol: před prvním řádkem kódu napsat jednu větu ve formátu:

> *"Tento projekt je dokončen, když [konkrétní, externě ověřitelná podmínka]."*

Příklady:
- ❌ "Když to bude fungovat." (vágní, nelze ověřit)
- ✅ "Když `pytest tests/` projde bez chyb a README obsahuje funkční `pip install` + `python src/main.py --help`."
- ✅ "Když CSV s 1000 řádky projde validátorem a výstupní JSON lze načíst bez chyby v dalším skriptu."

### Checkpoint struktura

Pro projekty delší než 3 dny: nastavit explicitní checkpoint každý druhý den.

Checkpoint otázka: *"Je současný stav projektu v podobě, kterou bych mohl odevzdat jako 'funkční minimum' firmě?"*

Pokud ne — co přesně chybí? Zapsat jako seznam (ne mentální reprezentaci — fyzický seznam).

### Signál pro zastavení práce

Přirozeným instinktem po dosažení funkčního minima je přejít na další zajímavý problém. Toto je přesný moment, kdy je potřeba:
1. Zastavit se.
2. Zkontrolovat definici "done" z kroku výše.
3. Dokončit balení (README, testy, komentáře) před zahájením čehokoliv nového.

---

## Část 6: GitHub Projects a Issues jako kognitivní nástroj

Nepoužívat Issues jen jako task list — používat je jako externalizo­vanou paměť a demonstraci procesu.

**Pro každý aktivní projekt:**

Vytvořit Issues pro:
- Každý known bug ("Skript selhává na CSV s prázdnými řádky")
- Každý plánovaný improvement ("Přidat confidence threshold do klasifikátoru")
- Každý výsledek post-mortem analýzy ("Chyba v transformaci matice — viz pitevní kniha záznam #47")

Commity odkazující na Issues (`Fixes #3`) automaticky zavírají issues při merge — to je viditelný trail procesu.

**GitHub Projects (Kanban):** Sloupce To Do / In Progress / Done / Blocked. Na pohovoru nebo v placeném testu: přirozené místo, kde ukázat jak řídíte práci.

---

## Poznámka k tempu

Tato roadmapa je záměrně hustá. Není určena k dokončení najednou — je to referenční dokument.

Doporučené pořadí pro první 2 týdny:
1. README sekce "Instalace a spuštění" pro všechny aktivní repo.
2. Pytest testy pro cad2llm.
3. GitHub Actions CI pro cad2llm.
4. Zahájit CSV/XML validator jako nový projekt — s definicí "done" zapsanou před prvním řádkem kódu.

Zbytek podle kapacity a podle toho, co vyplyne z placeného testu nebo dalšího pohovoru.

---

*Verze 2.0 — duben 2026. Rozšířeno o validační protokoly, CAP mitigaci a 80% pattern exekuci.*
