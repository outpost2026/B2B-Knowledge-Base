### P80 — Unicode-aware parsing regionálních formátů
Při parsování textových dat s regionálními formáty testuj regex proti reálným datům včetně Unicode variací (en-dash U+2013, non-breaking space U+00A0, různé quote znaky). Nikdy nepředpokládej ASCII-only vstup v multilingual scraping pipeline. En-dash a hyphen-minus jsou vizuálně identické — nutný DB audit, ne vizuální kontrola kódu. Reference: GT-095.

### P81 — Cross-portal dedup signál: title+company, ne URL
Cross-portal analytika nikdy nepoužívá URL jako dedup klíč (každý portál má unikátní URL schéma → overlap metrika vždy 0). Používej title+company (nebo fuzzy_title+fuzzy_company). URL-based dedup platí jen uvnitř jednoho portálu. Reference: GT-096.

### P82 — Modular refactor: žádné vzájemné importy
Při refactoru na balíčky: závislosti se předávají jako parametry (dependency injection), ne importem. Vzor: `tabs/*.py` importuje `metrics`, `filters`, `components`, nikdy `app.py`. Reference: GT-097.

### P83 — Contract testy při package splitu mandatory
Contract testy jsou součástí kroku package split, ne backlogu. Povinné vrstvy: (a) purity (zakázané importy), (b) interface (signatury funkcí), (c) layers (směry importů). Bez nich je modulární architektura křehká. Reference: GT-098.

> **Rezervace P84–P89:** epistemická řada — Gate protokol destruktivních operací. Kanon: `05_EPISTEMIKA/02_agentni_pravidla/EPISTEMICKE-PRAVIDLA-AGENTNI-PRACE.md` §5.4. (P78/P79 nebyly přiděleny.)

### P90 — Frontend smoke test gate + reintrodukce fixu
UI layout změny kolem interaktivních komponent ověř ručním smoke testem — pytest nerenderuje frontend. Znovu-povolení dříve odstraněného triggeru bez reprodukce originálního selhání = reintrodukce bugu; fix bez post-fix verifikace na stejném scénáři není fix. Reference: GT-099.

### P91 — Print-before-raise defense
API s print-before-raise side efektem se neprobouzí „dotykem a try/except" — proběhlý výstup nelze chytit výjimkou. Ověř stav přímo (existence souboru / dokumentovaný flag) nebo potlač konkrétní logger. Reference: GT-100.

### P92 — Dependency kontrakt = jeden zdroj pravdy
pyproject = kontrakt; requirements/deploy soubory = ručně synchronizované deriváty. Po každém version bumpu `pip install -e .` (dist-info metadata se nepřegenerují sama). Verification gate obsahuje `pip check`. Při „u mě padá, u tebe ne" porovnej i `pip list`, ne jen kód. Reference: GT-101.

### P93 — Package-data build verification
Data soubory vedle modulu deklaruj v `[tool.setuptools.package-data]` A ověř build inspekcí (`pip wheel` + namelist) — konfigurace sama není důkaz. Broad-except kolem kritické funkce bez logování maskuje totální rozpad funkce (komplement P55). Reference: GT-102.

### P94 — Structural dispatch over name matching
Když rodina funkcí nemá stabilní jmenný kontrakt, váž strukturou (pozice/arity), ne jmény parametrů — jména jsou v Pythonu jen doporučení. Dispatcher pokrývající rodinu ověř runtime smoke testem celé rodiny, ne vzorkem. Reference: GT-103.

### P95 — Framework logger direct attach + idempotentní setup
Loggery s vlastním chainem (`propagate=False`) potřebují handler připojený přímo na svůj uzel — root config nestačí. Setup funkce volané z render cyklu musí být idempotentní (guard flag), jinak duplicity handlerů/registrací. Reference: GT-104.

### P96 — Žádný live I/O v unit testech
Async/background cesty v testech vždy stubovat (monkeypatch runneru před submittem). Unit testy nesmí provádět live network I/O. Flaky test = determinismus bug, ne „občas se stane" — dvě zelená pásma full-suite za sebou = minimum gate. Reference: GT-105.

### P-GCP-01 — Při 403 v GCP ověřit všech 5 autentizačních vrstev
IAM role → Access Scopes (nejčastější příčina) → Metadata Server identity → Workspace vs Cloud scope mismatch → Service Account quota. Nejčastější selhání: vrstva 2 nebo 4. Reference: GT-GCP-001.

### P-GCP-02 — Crontab ≠ SSH
Absolutní cesty ke všemu: Python interpret, systémové binárky, pracovní adresář. `sudo` jen s NOPASSWD v sudoers.d. GCP region explicitní, ne default. Reference: GT-GCP-002.

### P-GCP-03 — Serverless = Immutable
Uložení souboru ≠ nasazení; oprava za běhu = nemožná. Každá změna = `gcloud deploy`. Reference: GT-GCP-003.

### P-GCP-04 — GCS je jediná trvalá paměť
GCP Cloud Functions: `/tmp/` = RAM, po doběhu smaže vše. Start = download z GCS, konec = upload do GCS. Žádný trvalý stav v kontejneru. Reference: GT-GCP-004.

### P-GCP-05 — Hard Reset protokol
Při zacyklení v chybách >30 minut: smazat poškozený soubor → vložit ověřený blok kódu → smazat data → začít z nuly. Reset není prohra, je optimalizace času. Reference: GT-GCP-005.
