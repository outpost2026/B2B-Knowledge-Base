# Ubuntu LTS adopce (dual boot) — prospektivni analyza SW stacku workspace

Datum: 2026-09-18 | Autor: outpost2026
Ucel: Kvalifikovane rozhodnuti o adopci Ubuntu LTS vedle Windows — kompletni inventura vyvojarskeho SW portfolia v _github vcetne balicku, nastroju a Windows-only blokeru.

Provenance: source-read (pyproject.toml x8, requirements.txt x13, package.json outprep, docker-compose.yml x2, CI yml, AGENTS.md, CONTEXT_REPOS.md, bash overeni 2026-09-18) + summary (KB GROUND_TRUTH_2026-08-06, SKILL_GAPS_v2, CI_CD_PROTOKOL, portfolio_audit_v2)
Verze: 1.1 | EROI: 9/10 | Modul: 02_ANALYZY/04_workspace_audit

---

## 1. Executive summary

- Workspace: **23 git rep**, ~600+ commitu, ~3M+ LOC (vcetne binarnich VCF/DXF dat). Solo dev, tempo ~4.5 commitu/den.
- Stack je **Linux-ready z ~90 %**: Python/MCP/Docker/Postgres/Node/CI uz dnes bezi na `ubuntu-latest` runnerech v GitHub Actions (MCP-Jobs matrix 3.11/3.12 + postgres:16 service).
- **Dual boot je spravna volba (P>0.8)**: Windows musi zustat pro CAM/Ruida retezec (VCutWorks, LightBurn, NCstudio, proprietarni .VCF) a pro Golden Master parity testy. Linux pro denni dev.
- **Doporucent LTS: 24.04 Noble (P>0.8)** — nativni Python 3.12, lepsi shoda s `requires-python >=3.12` (lichess, linkedin-mcp), podpora do 2029. 22.04 Jammy ma default Python 3.10 => nutny deadsnakes/uv pro cely stack.
- **Kriticke omezeni disku (P>0.9)**: Micron 2200 NVMe 256 GB, GPT, jedina datova particie C 254.9 GB (obsazeno 152 GB, volno 102 GB). Pro dual boot nutno zmensit C o min. 60–80 GB + externi backup. Bez uvolneni mista neinstalovat.

## 2. Portfolio — per-repo stack (overeno source-read)

### 2.1 MCP & agentic vrstva

| Repo | requires-python | Klicove deps (pin) | Poznamka pro Linux |
|---|---|---|---|
| `mcp-local-server` (cnc-tools, 21 nastroju) | >=3.11 | `mcp[cli]>=1.27`, `python-docx>=1.2` | Hatchling build; bez problemu |
| `linkedin-mcp-custom` | >=3.12 | `fastmcp>=3.0`, `patchright>=1.40`, `pyyaml`, `python-dotenv` | Patchright/Playwright na Linuxu vyzaduje `npx playwright install --with-deps` (apt zavislosti) |
| `MCP-Jobs` v0.5.0 | >=3.11 | `mcp>=1.10,<2.0`, `requests`, `bs4`, `pyyaml`, `psycopg[binary]>=3.1`, `pandas>=2,<3`, `streamlit>=1.38` (extra) | CI uz bezi na ubuntu-latest (3.11+3.12 + postgres:16 service). Referencni |
| `lichess-analyzer-mcp` | >=3.12,<3.14 | `mcp>=1.0`, `berserk>=0.14`, `chess>=1.11,<2`, `httpx>=0.28`, `python-docx` | Stockfish binarka se stahuje via `scripts/setup_stockfish.ps1` (Win) — na Linuxu `apt install stockfish` |
| `mcp-retrieval` | >=3.11 | `mcp[cli]>=1.27,<2` | Bez nativnich zavislosti |

### 2.2 Core engineering (CNC/CAM)

| Repo | Stack | Linux status |
|---|---|---|
| `Vcf-compiler` (vcf-parser, v1.0.0) | >=3.11, zero runtime deps, `pytest>=8` | Plne prenositelne, Golden Master testy deterministicke |
| `vcf_parser_b2b` | `streamlit>=1.38`, `matplotlib>=3.8`, `pandas>=2.2` | OK; `deploy.ps1` + Dockerfile -> prepsat na `deploy.sh` |
| `vcf_color_service` v2.0.0 | >=3.8 (!), setuptools | Nejsirsi kompatibilita, OK |
| `dxf_integrace` | `streamlit`, `matplotlib`, `pandas`, `ezdxf>=1.3`, `numpy>=1.24`, `shapely>=2.0`, `scipy>=1.10` | Shapely/Scipy na Linuxu OK (wheels), CI `ci.yml` + `codeql.yml` pritomny |
| `vcf_integrace` (legacy) | `deploy/requirements.txt` + 3x historicky Dockerfile (v1.5/1.6/1.7) | Legacy, nemigrovat aktivne |
| `cad2llm`, `rag_indexer`, `scrapers` | `requests`, `bs4`, `pandas`, `lxml>=5` | OK |

### 2.3 Infra / web / IoT

| Repo | Stack | Linux status |
|---|---|---|
| `outprep` (reference standalone) | Node v22.23.1 (fnm), Next.js 16.2, React 19, TS 5, Tailwind 4, Vitest 4, Playwright 1.58, `postgres` npm pkg, `stockfish 18`, husky, `docker-compose.yml` (postgres:16) | Na Win chybi `node/npm` v system PATH (jen fnm multishell); na Linuxu standardni `fnm + corepack`. `postinstall: setup-stockfish.mjs` overit |
| `GCP` (cloud-run-mcp, gcloud-mcp monorepo, gcp_miner, Meteo_scraper_gcp_prod) | `functions-framework==3.5.0`, `flask==3.0.2`, `google-cloud-storage==2.14`, Dockerfile (cloud-run-mcp) | `gcloud CLI` v PATH (`google-cloud-sdk/bin`), ale `gcloud --version` hlasilo chybejici Python binding — na Linuxu cistejsi instalace |
| `web_integrace_systeq` | Hugo/HTML, `send.php`, Three.js | OK, zadna nativni zavislost |
| `outpost_security_perimeter` | `firmware/*` = 5x `.md` spec (bms_monitor, climate_station, ds18b20, modbus, perimeter) + `hardware.md`; zadne `.ino` ani `platformio.ini` | **Zaver: zadny aktivni ESP32 toolchain k migraci (P>0.8).** Az bude, tak `platformio`/`esptool` je primarne linuxovy nastroj — vyhoda |
| `Meteo_scraper_SQL`, `ML_Ops_edukace`, `TEMP_KULTURA_DB` | SQL + pandas pipeline | OK |

## 3. OS-level nastroje — Win vs Ubuntu (overeno bash 2026-09-18)

| Nastroj | Windows stav (overeno) | Ubuntu 22.04 Jammy | Ubuntu 24.04 Noble | Akce |
|---|---|---|---|---|
| Python 3.11.9 system + pip 26.1.2 | OK | default 3.10 => **nutny uv/deadsnakes** pro >=3.11/3.12 stack | default **3.12** => sedi s lichess/linkedin | Pouzivat `uv` (0.11.26 jiz na Win) pro `.venv` regeneraci; `.venv` nikdy nekopirovat mezi OS |
| `uv 0.11.26`, `fnm 1.39.0`, Node v22.23.1 (fnm default) | OK, ale `npm` nefunguje mimo fnm shell (hypoteza: profil neexportuje PATH) | `apt` node zastaraly, pouzit fnm | Stejne, fnm preferovan | Na Linuxu `fnm install 22 + corepack enable` |
| `git 2.53`, `Docker 29.5 + compose v5.1.4` | OK (Docker Desktop) | Docker Engine + compose plugin (apt) | Stejne, novejsi kernel/cgroup v2 | `postgres:16` compose soubory bez zmen |
| `gcloud SDK` v PATH | Pritomen, volani vyzaduje `CLOUDSDK_PYTHON` fix | Nativni `apt` instalace | Stejne | Prepsat env fix |
| `pip freeze` global: mcp 1.28, fastmcp 3.4.4, streamlit 1.38, pandas 2.3.3, playwright 1.58, psycopg 3.3.4, ezdxf 1.4.4, shapely 2.1.2, scipy 1.17.1, chess 1.11.2, ruff 0.16.4, pytest 9.0.3 | Globalne zneis-tene prostredi (mcp-jobs 0.2.0 editable) | Izolovat do `.venv` | Stejne | Na Linuxu striktne `.venv` + `uv`, global nechat cisty |
| `opencode` CLI | **Nenalezen v PATH**; config `~/.config/opencode/opencode.jsonc` existuje; spousti se via desktop/fnm multishell; skill dirs `.opencode/{commands,skills}` pritomny | `npm i -g opencode` / bun | Stejne | Po instalaci prekopirovat `opencode.jsonc` + `.opencode` |
| Cursor, GitHub Desktop, `dotnet`, PowerShell 5.1 | Pritomny (PATH) | Cursor .deb/AppImage OK; GitHub Desktop **chybi** (naharada: `gh` CLI + git); PS 5.1 -> `pwsh` 7 | Stejne | Naucit se `gh` CLI; PS skripty (`.scripts/*.ps1`, `deploy.ps1`, `db.ps1`) postupne prepsat na `.sh` |
| Java/JDK, gcc, `wmic` | Chybi (Android build blokovan — viz session_state 2026-09-13) | `apt install openjdk-17-jdk` | `openjdk-21-jdk` | Vyhoda Linuxu |
| SecureBoot / BitLocker / disk | GPT, 1x NVMe 256GB; `Confirm-SecureBootUEFI` bez admin prav nelze overit; `bcdedit` pristup odepren | Dual boot vyzaduje SecureBoot handling + Fast Startup OFF | Stejne | Viz §5 checklist |

## 4. Windows-only blokery — proc dual boot, ne wip

1. **Ruida/VCutWorks retezec (P>0.9):** produkcni parser .VCF (22 iteraci, >99.98 % presnost), `VCF_files_moodpasta/` (35 samplu), DXF palety s barevnou divergenci. VCutWorks/LightBurn/NCstudio jsou Windows-only; Wine neoveren a pro zakaznickou produkci (Moodpasta, 50M Kc obrat) neprustrelne. **Windows particie zustava.**
2. **CAM validace:** Golden Master JSON diffy vznikly na Win float stacku (IEEE 754, `MSC v.1938`); po migraci spustit plny `pytest` na Linuxu a porovnat baseline — ocekavan shoda, ale overit.
3. **Playwright/Patchright browsery:** na Linuxu dodatecny krok `install --with-deps`; webless scrapery (MCP-Jobs: 4 CZ portaly) jsou primarne `requests+bs4` => nizke riziko.
4. **GCP deploy z Linuxu je vyhodnejsi** (Docker Engine bez Desktop overheadu, `gcloud` cistejsi).

## 5. Dual boot checklist (Micron 2200 256GB, GPT, Win10 Pro)

- [ ] **Backup:** cely `_github` (23 rep) + `VCF_files_moodpasta/` + `B2B/` na externi disk; overit `git status` clean (nyni 6 dirty rep — commit/stash pred delenim disku).
- [ ] **Uvolnit misto:** C ma 102 GB volnych — pro 2 OS tesne. Cil: uvolnit na min. 130 GB volnych (vycistit `node_modules` v outprep, Docker images, `.venv` cache) + shrink C o 60–80 GB v Disk Management.
- [ ] **BIOS:** Fast Startup OFF, BitLocker suspend/decrypt, SecureBoot: Ubuntu 24.04 podepsany shim funguje; pri potizich docasne vypnout.
- [ ] **Instalace:** Ubuntu 24.04 LTS desktop, manual partitioning (EFI ponechat, `/` 50–60 GB ext4, `swap` volitelne, `/home` zbytek), bootloader na EFI particie (209 MB).
- [ ] **Post-install (vyhoda 24.04):** `apt install git curl stockfish postgres-client openjdk-21-jdk pwsh gh`; `uv`, `fnm` (Node 22), Docker Engine (official repo), `gcloud CLI` (apt), `playwright install --with-deps`, regenerace `.venv` pres `uv sync/pip install -e .`, `npm ci` v outprep.
- [ ] **Sdileni dat:** NTFS/exFAT datova particie pro VCF/DXF samply (vyhnout se zapisu z Linuxu do `C:` bez nutnosti); Git remote (GitHub) jako primarni sync mezi OS.
- [ ] **Fallback:** WSL2 jako docasny mezikrok pokud shrink selze; live USB test HW (WiFi, BT, GPU) pred ostrym delenim.

## 6. Doporuceni a dalsi krok

1. **Go pro dual boot s 24.04 Noble (P>0.8).** 22.04 jen pokud by selhal ovladac HW na 24.04 (overit z live USB).
2. Dalsi krok (mimo tento dokument): uvolnit disk + backup + live USB HW test; pote instalace + regenerace `.venv` + plny `pytest` + `ruff` + `tsc --noEmit` + `vitest` parity run.
3. Skill gapy beze zmeny (SKILL_GAPS_v2): TS/Next.js 9/10, Postgres 8.5/10, DevOps 8/10 — Linux adopce primo podporuje gap ❷ a ❸.

## 7. Verdikt vhodnosti + scope-creep posouzeni (doplneno 2026-09-18, v1.1)

**Verdikt: ano, ale ne ostrym dual bootem ted — nejdriv WSL2 (P>0.8).**

Neni to scope creep z principu, ale ostry dual boot v aktualnim stavu scope creep je:

- **Proti creepu:** gapy ❷ (Postgres) a ❸ (DevOps: cron, docker-compose, monitoring) bez Linux-like prostredi nezacelis; CI uz bezi na `ubuntu-latest`, takze dnes vyvijis na Win a testujes na Linuxu — chyba parity. Linux je enabler standalone produktu (outprep model), ne "hezky mit".
- **Pro creep (casovani):** 6 dirty rep + 102 GB volna na 256GB disku + 0 Kc prijmu. Rezani particie ted = hazard s daty a ztrata 8–15 h fakturovatelneho casu pri velocity 4.5 commitu/den.

**Stanovena sekvence:**

- **Faze 0 — ted (2 h, nulove riziko):** `wsl --install -d Ubuntu-24.04`, Docker Desktop WSL2 backend (29.5 jiz pritomen), `uv` + `fnm` + Node 22, `apt install stockfish postgresql-client gh`, regenerace 1 testovaciho `.venv` (doporuceno `mcp-retrieval` — zero nativnich deps), `pytest` parity vs Win. Cil: 80 % benefitu za 10 % nakladu.
- **Faze 1 — podminky pro ostry dual boot:** vsech 23 rep clean + backup na externi disk + min. 130 GB volna + kryti tydne (zakazka/brigada). Pak shrink 60–80 GB + instalace 24.04 dle §5.
- **Stop-podminka:** pokud se WSL2 po 2 tydnech denne nepouziva → dual boot rusit, byl by to creep. Meritelne, ne pocitove.
- Windows particie zustava trvale (CAM/Ruida/Golden Master).

---
*Teams: cnc-tools (workspace_info, kb_overview/search/read, list_directory, search_files, git_status_all, session_state, read_file, write_file), skills: workspace-guardrails, kb-workflow. Zadny `.env`/secret cten ani zapsan. Zadne destruktivni operace.*
