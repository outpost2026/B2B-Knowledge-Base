# CI / GitHub Actions — imerzní výklad pro solo B2B vývojáře

> **Kontext:** 4 měsíce R&D, 0 dní s CI. Dev implementuje CI teprve T+24h.
> Cíl: pochopit CO, PROČ, JAK, EFEKT (EROI).

---

## 1. Proč jsi 4 měsíce žádné CI nepotřeboval?

Doteď jsi dělal **R&D a reverse engineering**. V té fázi:

- Hledáš, co funguje — ne jestli to pořád funguje
- Měníš věci každou hodinu — test by byl outdated za 20 minut
- Jediný "test" je: "spustil jsem to a viděl výstup"
- Produkt nemá zákazníka — není kdo by si stěžoval na rozbitou věc

**CI dává smysl až ve fázi, kdy:**

- Kód máš hotový a ladíš ho (stabilizace)
- Přidáváš nové featury a nechceš rozbít staré (regrese)
- Chystáš se poslat B2B zákazníkovi (důvěryhodnost)
- Pracuješ na více repozitářích a zapomínáš co kde děláš (solo dev paměť)

**Tvůj milestone:** `dxf_integrace` má 58 funkcí v 1 souboru, Vcf-compiler na něm runtime závisí. Tohle je přesně ten bod, kdy bez CI začneš rozbíjet věci, aniž bys to věděl.

---

## 2. Přehled implementovaných CI nástrojů (Tier 1)

```
Každý repozitář má nyní:
  ├── CI (continuous integration) — základ
  ├── CodeQL — security scanning
  ├── Dependabot — auto-update závislostí
  ├── Matrix — testování na více Python verzích
  ├── Nightly cron — automatické noční testy
  └── Cross-repo trigger — propojení dxf_integrace → Vcf-compiler
```

---

## 3. CI (Continuous Integration) — ZÁKLAD

### CO

Pokaždé, když pushneš commit na GitHub, automaticky se:

1. Spustí čistý Linux server (ubuntu-latest)
2. Naklonuje se tvůj kód
3. Nainstalují se závislosti (pip install)
4. Spustí se všechny testy (pytest)
5. Výsledek: ✅ green / ❌ red

### PROČ

**Tvůj mozek má limit ~7 věcí v krátkodobé paměti.** Když děláš 5 změn v různých repozitářích, NEmůžeš si pamatovat, jestli každá změna neco nerozbila. CI je tvůj externí mozek, který to hlídá.

**Bez CI:** uděláš změnu → zapomeneš → o 3 dny později zjistíš, že Vcf-compiler generuje blbé VCF → hledáš 2 hodiny kde je chyba

**S CI:** uděláš změnu → do 2 minut víš, že je něco rozbité → opravíš to hned, dokud máš kontext v hlavě

### JAK

```yaml
# .github/workflows/ci.yml
name: CI
on: [push]                                    # při každém pushi
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4             # stáhni kód
      - uses: actions/setup-python@v5         # nainstaluj Python
      - run: pip install -e ".[dev]"          # nainstaluj balíček + test deps
      - run: pytest                           # spusť testy
```

### EROI

| Faktor | Bez CI | S CI |
|--------|--------|------|
| Čas strávený hledáním regresí | ~2-4 h/týden | ~0 h (CI to řekne do 2 min) |
| Jistota, že kód funguje | "myslím že jo" | "vím že jo" |
| B2B prodejní argument | "testuju ručně" | "CI pipeline, 24/24 testů green" |

---

## 4. Matrix — testování na více Python verzích

### CO

Místo jednoho testu (Python 3.11) spouštíš 3 testy paralelně (3.10, 3.11, 3.12).

```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

### PROČ

Tvůj vývojový stroj má Windows a Python 3.11 nebo 3.12. Tvoji zákazníci (SME) můžou mít:
- Starší Ubuntu server s Python 3.10
- Docker image s Python 3.12
- Jinou verzi, kterou sis nikdy neotestoval

Klasická chyba: `f-string` syntaxe, `match-case`, `walrus operator` — každá Python verze přidává novinky. Pokud použiješ něco, co 3.10 nemá, na tvém stroji to funguje, u zákazníka to padá.

**`fail-fast: false`** = pokud 3.10 spadne, 3.11 a 3.12 běží dál. Bez toho by ti CI zabil všechny testy při první chybě a nevěděl bys, jestli ostatní verze procházejí.

### EROI

Čas investice: +2 řádky do YAML (2 minuty)
Hodnota: chytí version-specific bug dřív, než se dostane k zákazníkovi

---

## 5. Nightly cron — noční automatické testy

### CO

Každý den v 6:00 UTC (8:00 našeho času) se spustí CI, i když jsi nic nepushnul.

```yaml
on:
  schedule:
    - cron: "0 6 * * *"
```

### PROČ

Jako solo developer:
- **Neděláš commity každý den** — někdy pracuješ 2 dny na jedné změně
- **Závislosti se mění samy** — Dependabot ti aktualizuje balíčky, ale může to něco rozbít
- **GitHub může mít výpadek** — CI v tu chvíli neběžel, ale ty to nevíš

Nightly run je tvoje "ranní kontrola": přijdeš k PC, podíváš se na mail/GitHub a vidíš, jestli je všechno zelené. Pokud ne, víš že něco není v pořádku — a řešíš to hned, ne až za týden.

### EROI

Čas investice: +3 řádky (2 minuty)
Hodnota: chytí problémy, které by jinak zůstaly skryté týdny

---

## 6. CodeQL — security scanning

### CO

GitHub automaticky prohledá tvůj kód na bezpečnostní chyby:
- SQL injection (u tebe nehrozí)
- OS command injection (subprocess bez sanitizace)
- Credential leak (heslo v kódu)
- Nezabezpečené importy

```yaml
permissions:
  contents: read
  security-events: write
```

### PROČ

**B2B důvěryhodnost.** Když řekneš zákazníkovi "mám CI pipeline", první otázka bude "a co security scanning?". CodeQL je průmyslový standard (používá ho Microsoft, Google, celý GitHub).

Taky: v RE kódu se snadno stane, že necháš v komentáři cestu k serveru, API klíč, nebo jiný credential. CodeQL to chytí dřív, než to pushneš do public repa.

### EROI

Čas investice: 10 minut na vytvoření YAML, zkopírovat do 3 rep
Hodnota: chrání před únikem credentialů, B2B prodejní argument

---

## 7. Dependabot — auto-update závislostí

### CO

Jednou týdně GitHub zkontroluje, jestli tvoje závislosti (pytest, ezdxf, numpy...) nemají novější verzi. Pokud ano, vytvoří Pull Request s aktualizací.

```yaml
# .github/dependabot.yml
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

### PROČ

Jako solo developer **nemáš kapacitu ručně sledovat aktualizace balíčků**. Zároveň:
- Stará verze = bezpečnostní díra
- Stará verze = chybí nové featury
- Nová verze = může rozbít tvůj kód

Dependabot ti pošle PR s aktualizací. CI se spustí na tom PR a ukáže, jestli testy procházejí. Pokud green → mergneš. Pokud red → víš, že nová verze není kompatibilní.

### EROI

Čas investice: 5 minut na konfiguraci
Hodnota: automatická údržba závislostí bez tvojí pozornosti

---

## 8. Cross-repo trigger — propojení dxf_integrace → Vcf-compiler

### CO

Když pushneš změnu do `dxf_integrace` a CI projde, automaticky se spustí CI i v `Vcf-compiler`.

### PROČ

Tohle je **nejdůležitější nástroj pro tvůj specifický problém**.

Vcf-compiler volá `dxf_integrace.index_dxf()` za běhu. To znamená:
- Změníš něco v dxf_integrace
- Vcf-compiler o tom neví
- Příští spuštění compile_dxf() vygeneruje špatné VCF
- Ty to zjistíš až když to někdo reklamuje

Cross-repo trigger zajišťuje: změna v dxf_integrace → automatický test Vcf-compiler → okamžitá zpětná vazba.

⚠️ **Aktuální stav:** vyžaduje `PAT_CROSS_REPO` secret v dxf_integrace (GitHub Personal Access Token). Bez něj se step přeskočí. Viz nastavení níže.

### EROI

Čas investice: 15 minut + vytvoření PAT
Hodnota: ochrana proti rozbití závislého repa — kritické pro tvou architekturu

---

## 9. Workflow_dispatch — ruční spuštění

### CO

Můžeš spustit CI ručně z GitHub UI, i když jsi nic nepushnul.

```yaml
on:
  workflow_dispatch:
```

### PROČ

Užitečné když:
- Chceš otestovat větev, kterou jsi stáhl z remote (ne tvoje změny)
- Opravil jsi něco na GitHubu přes web UI
- Nightly run selhal a ty chceš zkusit znovu bez čekání do rána

Stačí jít na GitHub → Actions → vybrat workflow → "Run workflow".

---

## 10. Vztahy mezi nástroji — jak to do sebe zapadá

```
Push do dxf_integrace
  │
  ├── CI spustí matrix (3.10, 3.11, 3.12)
  ├── CodeQL scan
  │
  ├── [pokud CI green] → repository_dispatch → Vcf-compiler
  │                                               │
  │                                               ├── CI spustí matrix (3.11, 3.12)
  │                                               └── CodeQL scan
  │
  └── Dependabot (jednou týdně) → PR s aktualizacemi → CI na PR

Nightly cron (6:00 UTC) → všechny CI bez ohledu na push
```

---

## 11. Nastavení PAT pro cross-repo trigger

Cross-repo trigger je jediná věc, která vyžaduje ruční zásah:

1. Jdi na https://github.com/settings/tokens
2. Klikni "Generate new token (classic)"
3. Dej název: `PAT_CROSS_REPO`
4. Zaškrtni: `repo` (vše)
5. Generovat a zkopíruj token
6. Jdi na `https://github.com/outpost2026/CNC_2_LLM/settings/secrets/actions`
7. "New repository secret" → název `PAT_CROSS_REPO`, vlož token

---

## 12. Co jsi získal (souhrn)

| Nástroj | Čas investice | Roční EROI (ušetřený čas) |
|---------|--------------|--------------------------|
| CI (pytest) | 15 min | ~200 h/rok (neřešíš regrese) |
| Matrix | 2 min | ~10 h/rok (version bugy) |
| Nightly | 2 min | ~5 h/rok (skryté problémy) |
| CodeQL | 10 min | ~5 h/rok (security incidenty) |
| Dependabot | 5 min | ~10 h/rok (ruční update) |
| Cross-repo | 15 min | ~20 h/rok (rozbité závislosti) |

**Celkem: ~50 minut investice → ~250 h/rok ušetřeného času a stresu.**

---

## 13. Slovníček

| Pojem | Význam |
|-------|--------|
| **CI** | Continuous Integration — každá změna se automaticky otestuje |
| **CD** | Continuous Deployment — po testech se automaticky nasadí (u tebe zatím není) |
| **Pipeline** | Celý řetězec: push → test → deploy |
| **Matrix** | Testování na více konfiguracích (Python verze, OS) |
| **Cron** | Časovač — "0 6 * * *" = každý den v 6:00 |
| **Fail-fast** | Pokud jedna varianta matrixu selže, zabít ostatní |
| **PAT** | Personal Access Token — bezpečnostní klíč pro API |
| **Dependabot** | GitHub robot na aktualizaci závislostí |
| **CodeQL** | GitHub security scanner |
| **Workflow dispatch** | Ruční spuštění workflow z UI |
| **Repository dispatch** | Spuštění workflow z jiného repa |
| **Runner** | Server, který CI spouští (ubuntu-latest) |
| **Green/Red** | Testy prošly / testy selhaly |

---

*Vytvořeno: 2026-07-02, Session 11c*
*Kontext: imerzní učení, solo B2B dev, 4 měsíce R&D bez CI*
