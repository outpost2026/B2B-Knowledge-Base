# CI/CD Integrační protokol — evoluční roadmapa

> **Status:** Plánovací fáze (pre-implementace)
> **Autor:** PC / agentní workflow
> **Datum:** 20.06.2026
> **Kontext:** Výstup z evaluace pracovního repozitáře — identifikace CI/CD jako největšího gapu
> **Účel:** Zachycení racionale, rozhodovacího rámce a implementační strategie CI/CD v kontextu autorovy metodologie

---

## 1. Identifikace gapu (ground truth)

### 1.1 Současný stav

```text
push do main → (nic) → ruční spuštění deploy.ps1
```

Všechny operace jsou manuální: testy se spouští ad-hoc, deploy vyžaduje přítomnost v terminálu, Docker Desktop, gcloud CLI. Každý deploy = kognitivní load ~3–5 minut + kontext switch.

### 1.2 Co už existuje (nezpochybnitelná východiska)

- Funkční `deploy.ps1` s error handlingem, guard clauses, validací
- pytest test suite (777 řádků, 8 test modulů)
- Golden master regression testing (7 baseline JSONů)
- Determinism testing, smoke testing, geometry/config unit testy
- Dockerfile → GCP Cloud Run deploy pipeline
- pyproject.toml s konfigurací pytestu

### 1.3 Co neexistuje (gap)

- `.github/workflows/` — zero
- Automatizovaný trigger testů při pushi
- Automatizovaný build/deploy pipeline
- Badge / vizuální indikátor stavu repa

---

## 2. Rozhodovací rámec (proč neimplementovat vše najednou)

### 2.1 Kognitivní tempo vs. Zlatý standard

B2B standard zahrnuje: GitHub Actions → pytest → coverage → Docker build → Artifact Registry → Cloud Run deploy → Slack notifikace → SonarQube → dependabot.

**Tento standard nelze implementovat jednorázově**, protože porušuje autorovy principy:

| Princip | Důvod |
|---------|-------|
| **Imerzní učení** | Nový nástroj musí být pochopen skrze ground truth, ne skrze abstraktní "best practice" |
| **Transfer learning** | Koncepty musí navazovat na existující znalostní bázi (deploy.ps1 → CD, pytest → CI) |
| **High SNR** | Každý nástroj musí mít prokazatelný marginální přínos, ne být "hezké mít" |
| **Iterační workflow** | Každá fáze musí být reverzibilní a samostatně hodnotitelná |

### 2.2 Rizika předčasné integrace

| Riziko | Manifestace |
|--------|-------------|
| Nulové porozumění | YAML syntax debug → ztráta 2+ hodin na nepochopeném CI failu |
| Falešný pocit bezpečí | CI green = kód je OK (ale testy nestačí pokrývají jen zlomek) |
| Vendor lock-in | GitHub-specific syntax → migrace na GitLab = přepisování |
| Kognitivní přetížení | Debug CI + debug kódu + debug deploy = triple load |

### 2.3 Podmínka integrace (filtr)

> **"Dokud nemám odpovědi na CO, PROČ, JAK, EFEKT — neintegrovat."**

- **CO** = co přesně nástroj dělá (ne marketing, ale mechanismus)
- **PROČ** = jaký ground truth problém řeší (ne "dělá to každý")
- **JAK** = jaké jsou vnitřní mechanismy (co se stane když kliknu/pushnu)
- **EFEKT** = marginální přínos oproti současnému stavu (ušetřený čas / eliminované riziko)
- **RIZIKO** = co se může rozbít, jak vrátit zpět

---

## 3. Fázový plán (evoluční roadmapa)

### Fáze 0: Transfer learning (současnost)

**Akt:** Pochopení patternu skrze existující znalosti.

| Autorův kontext | CI/CD ekvivalent |
|-----------------|-------------------|
| `deploy.ps1` (error handling, guard clauses) | = CD pipeline script |
| `pytest tests/` (manuální spuštění) | = CI test step |
| `git push → gcloud run deploy` | = celý CD flow |
| `Dockerfile` build | = build step |
| `SESSION_HANDOFF_V31.json` | = pipeline artifact / audit trail |

CI/CD = stejný kód, který už autor píše, ale spouštěný gitem místo terminálu.

### Fáze 1: CI — první kontakt (navrhovaná implementace)

**Cíl:** Automatické spuštění pytest při každém pushi.
**Riziko:** Nulové (nemění deploy, pouze testuje).
**Přínos:** Feedback loop do 60s po pushi.
**Učení:** YAML syntax, GitHub Actions runner, co znamená red/green.

**Co vznikne:**
```
vcf_parser_b2b/
└── .github/
    └── workflows/
        └── ci.yml              ← 25 řádků YAML
```

**Co se reálně stane při pushi:**
```
1. GitHub detekuje push
2. Spustí Ubuntu runner
3. git checkout vcf_parser_b2b
4. Python 3.11 setup
5. pip install -r requirements.txt + pytest
6. pytest tests/ -v --tb=short
7. Výstup: PASS / FAIL v GitHub UI
```

**Co se NESTANE (vědomé omezení):**
- Žádný build Docker image
- Žádný deploy na Cloud Run
- Žádná změna produkčního prostředí
- Žádná notifikace (kromě GitHub UI)

### Fáze 2: CD na staging (podmíněně — až bude znám pattern)

**Akt:** Build Docker image na push do feature branch + deploy na staging URL.
**Podmínka:** Autor rozumí YAML syntaxi, trigger mechanismu, environment variables, secrets management.
**Riziko:** Nízké (staging = neprodukční, viditelné pouze autorovi).

### Fáze 3: CD na produkci (podmíněně — až bude znám pattern)

**Akt:** CD trigger pouze na `main` s podmínkou průchodu všemi CI testy.
**Podmínka:** Autor rozumí celému řetězci včetně rollback strategie.
**Riziko:** Střední (automatický deploy = rychlejší šíření chyb, pokud testy nestačí).

---

## 4. Známá úskalí (mitigace)

| Úskalí | Pravděpodobnost | Mitigace |
|--------|-----------------|----------|
| Linux/Windows path rozdíly (`/` vs `\`) | Střední | Testy používají `os.path.join`, `pathlib` — ošetřeno |
| Case-sensitive filesystem (`.VCF` vs `.vcf`) | Vysoká | `test_golden_master.py` používá `f"{stem}.VCF"` — `25_circles_only.vcf` (malé) failne. Nutno opravit na `stem.upper()` nebo obě varianty |
| Streamlit import crash při testování | Střední | Pokud `app.py` volá `st.*` na module level → crash. Nutno ověřit, že testy neimportují `app.py` |
| Dlouhá doba běhu integračních testů | Střední | Golden master + determinism testy parsují reálná VCF data → 30s–2 min. Možnost oddělit `-m "not integration"` |

---

## 5. Reverzibilita a escape strategie

Každá fáze je **plně reverzibilní**:

```
Fáze 1: smazat .github/workflows/ci.yml → stav před implementací
Fáze 2: smazat staging deploy workflow → deploy.ps1 zůstává jako fallback
Fáze 3: ruční disable workflow v GitHub UI → návrat k manuálnímu deploy
```

Deploy.ps1 zůstává **vždy** jako fallback. Automatizace je nadstavba, ne náhrada.

---

## 6. Vztah k existujícím artefaktům

| Artefakt | Vztah k CI/CD |
|----------|---------------|
| `KB/EPISTEMICKE-PRAVIDLA-AGENTNI-PRACE.md` | CI/CD nesmí porušovat guardrails (API keys, zakázané cesty) |
| `KB/LLM_routing.txt` | Debug CI selhání = úloha pro specifický model |
| `vcf_parser_b2b/deploy/deploy.ps1` | CD fáze 3 = tento skript, ale automatizovaný |
| `vcf_parser_b2b/tests/` | Vstup pro CI fázi 1 |
| `CONTEXT_REPOS.md` | Nutno aktualizovat o CI/CD aspekt |

---

## 7. Decision log

| Rozhodnutí | Rationale |
|------------|-----------|
| Začít pouze s `vcf_parser_b2b` | Jediný repozitář s testy = jediný kandidát na CI |
| CI před CD | Testování je read-only operace → nejnižší riziko |
| Všechny branche (`on: push: ["**"]`) | Autor potřebuje vidět chování i na feature větvích |
| Ubuntu runner | GitHub standard, žádná konfigurační režie |
| Python 3.11 | Shodný s lokálním prostředím |
| Žádný coverage v Fázi 1 | Coverage vyžaduje pochopení metrik → až v iteraci |

---

## 8. Edge cases a fenomenologie vývoje

Autorova metodologie vytváří specifické fenomény, které standardní CI/CD pipeline neošetřuje:

### 8.1 Agentní workflow vs. CI determinismus

Standardní předpoklad: kód píše člověk → commit → test. Autorův režim: kód píše LLM agent → review → commit → test. Pokud agent produkuje kód, který lokálně projde testy, ale na GitHub runneru failne (path issues, encoding), CI zachytí regresi dřív, než se dostane do produkce.

**Dopad:** CI slouží jako druhá vrstva validace po agentním review.

### 8.2 Session handoff jako CI artifact

Session handoffy (V16–V31) jsou aktuálně manuální JSON soubory. CI pipeline by v budoucnu mohla automaticky generovat artifact: "Tento commit vznikl v session V31, testy prošly, deploy OK."

**Status:** Identifikováno, neplánováno — vyžaduje pochopení GitHub Actions artifact upload.

### 8.3 Duplicitní KB/ vs git repa

Aktuální duplicity mezi `KB/` (lokální) a `kazuistiky_llm_sprint/` (git trackovaný) nejsou CI/CD problémem. CI pracuje pouze s git repozitáři. KB/ zůstává mimo scope.

### 8.4 `nul` artifact files

Windows `nul` soubory v repozitářích jsou již v `.gitignore` (`vcf_parser_b2b/.gitignore` řádek 28). CI na Ubuntu tyto soubory nevidí → žádný dopad.

---

## 9. Kontrolní seznam před implementací Fáze 1

- [ ] Rozumím YAML syntaxi (indentace, key-value, array)
- [ ] Vím, co je `on: push: branches: ["**"]`
- [ ] Vím, co je `runs-on: ubuntu-latest`
- [ ] Vím, co je `actions/checkout@v4` a `actions/setup-python@v5`
- [ ] Vím, že GitHub Actions běží na Linuxu, ne na Windows
- [ ] Vím, jak číst output v GitHub UI (Actions tab → workflow run → step detail)
- [ ] Vím, že testy můžou na Linuxu selhat i když na Windows procházejí (a naopak)
- [ ] Vím, jak workflow zastavit (GitHub UI → Cancel run)
- [ ] Vím, že toto nemění deploy proces (produkce zůstává nedotčena)

---

## Revize

| Datum | Změna | Autor |
|-------|-------|-------|
| 20.06.2026 | Vytvoření dokumentu | PC |

---

*Tento dokument je živý. Aktualizuj ho po každé fázi implementace nebo novém poznatku.*
