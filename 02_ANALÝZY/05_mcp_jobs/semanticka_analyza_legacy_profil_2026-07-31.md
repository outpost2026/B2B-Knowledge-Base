# SÉMANTICKÁ ANALÝZA LEGACY-MANUAL PROFILU + NÁVRH KOREKCE

**Datum:** 2026-07-31 | **Autor:** opencode agent
**Účel:** Sémantická korelace legacy configu (config_legacy_manual.yaml) s výstupem (35 matched), návrh korekcí dle zájmů autora, + nový profilově odlišený formát výstupů

---

## 1. Co bylo implementováno: profilové odlišení výstupů

**Problém:** výstupy všech configů splývaly v `output/` pod generickým `etl_<ts>.json` — při skenu složky nešlo poznat, který artefakt patří kterému configu.

**Řešení (commit v MCP-Jobs):**

| Změna | Detail |
|-------|--------|
| `config.py` | `UserConfig.profile` pole (default "default") |
| `config.yaml` | `profile: "AI-NATIVE"` |
| `config_legacy_manual.yaml` | `profile: "LEGACY-MANUAL"` |
| `run_etl.py` | výstup `etl_{PROFILE}_{ts}.json/.md` + `etl_latest_{PROFILE}.json/.md` |
| `storage.py` | `CorrelationRecord.profile` → correlation_cache rozlišuje profily |

**Výsledný formát souborů v `output/`:**

```
etl_AINATIVE_20260731_154939.json        <- primární matice (8 AI query)
etl_latest_AINATIVE.json / .md
etl_LEGACY_MANUAL_20260731_161324.json   <- legacy (7 manual query)
etl_latest_LEGACY_MANUAL.json / .md
```

**Pravidlo:** název souboru = `etl_{PROFILE}_{timestamp}`. Sken složky = okamžitě zřejmé, které artefakty agregují které query. Correlation cache nese `profile` pole — SNR historie se per-profil neslije.

---

## 2. Legacy run: výsledky

**Run:** `etl_LEGACY_MANUAL_20260731_161324.json` (57.1s, 35 matched)

| Query | Matched | Portály | Poznámka |
|-------|---------|---------|----------|
| udrzbar | 22 | bazos, pracecz | dominantní (62 %) |
| zahradnik | 5 | bazos | |
| strechy | 3 | bazos | |
| truhlar | 2 | bazos | |
| cnc_jobs | 2 | bazos, pracecz | |
| elektrikar_prumysl | 1 | bazos | |
| spravce_budov | **0** | — | nulový trh |

---

## 3. Kvalita výstupu — manuální klasifikace 35 matched

| Kategorie | Počet | Podíl |
|-----------|-------|-------|
| ✅ Relevantní | 29 | 83 % |
| ❌ FP: "PRÁCE V NĚMECKU" spam | 5 | 14 % |
| ❌ FP: ostatní (ubytování, důchodci) | 1 | 3 % |

### 3.1 FP rozložení per query

| Query | FP | FP ady |
|-------|----|--------|
| elektrikar_prumysl | 1/1 | "ELEKTRIKÁŘ PRO FVE PROJEKTY V NĚMECKU" (100 %! query = 1 ad, a to FP) |
| strechy | 2/3 | "PRÁCE V NĚMECKU", "POKRÝVAČ - IZOLATÉR - V NĚMECKU" |
| truhlar | 1/2 | "PRÁCE V NĚMECKU - PRÁCE NĚMECKO" |
| zahradnik | 1/5 | "DLAŽDIČ - ZAHRADNÍK - PRÁCE V NĚMECKU" |
| udrzbar | 1/22 | "NABÍDKA PRÁCE S UBYTOVÁNÍM" |

**Diagnóza:** legacy exclude listy **nemají `nemecko` / `ubytovn` / `zprostredkovani`** pro bazos query. Bazos Praha je zahlcen německými pracovními agenturami (montáže, stavby, elektro).

---

## 4. Sémantická korelace config → výstup (zájmy autora)

### 4.1 Co legacy profil dělá dobře

- **udrzbar (22 match, 95 % OK)** — servisní technici, údržbáři, elektromechanici. Kvalitní záchyt v rozsahu 40–100k Kč. Koreluje s 14letým manual backstory.
- **zahradnik (5, 80 % OK)** — "ZAHRADNÍK - údržba zeleně", "Zahradník do party". OK.
- **cnc_jobs (2)** — "Montér výroby/operátor CNC stroje Praha" (43–46k) je **relevantní** — ale konflikt scope s AI-native `cnc_cam_automation` (programování CNC, CAM software).

### 4.2 Co je slabé / mimo zájem

- **elektrikar_prumysl (1/1 FP)** — jediný záchyt je "V NĚMECKU". Trh pražských průmyslových elektrikářů na bazos ≈ prázdný; prace.cz ho má (ale query nemá pracecz? **má** — portals: bazos, pracecz, jobs). Nízká aktivita trhu.
- **strechy (2/3 FP)** — 67 % šumu, a zbylý OK ("Hydroizolace Krnov") je **mimo Prahu** (region). Query má `locations: []` = žádný lokalitní filtr. Bazos Prahu → Krnov = filtr nedává smysl.
- **spravce_budov (0)** — nulový trh v obou bězích (110454 i 161324). Query reálně mrtvá.
- **truhlar (2, 1 FP)** — trh je na bazos minimální (montáže, ne truhlářství).

### 4.3 Scope konflikt: cnc_jobs (legacy) vs cnc_cam_automation (AI)

| | legacy cnc_jobs | AI-native cnc_cam_automation |
|--|-----------------|------------------------------|
| boolean | `(cnc OR frezar OR programovani OR serizovani)` | programátorské CNC (CAM, SprutCAM, Mastercam) |
| výstup | operátor CNC stroje (43–46k) | seřizovač vstřikolisů (borderline) |
| portály | bazos, pracecz | pracecz, bazos |

Návrh: sjednotit na jeden "CNC-manual" scope (CNC obsluha/seřizování) vs "CNC-CAM programování" — legacy nechá obsluhu, AI-native programování.

---

## 5. Návrh korekce config_legacy_manual.yaml (dle zájmů autora)

### 5.1 Povinné: blokace německého spam trhu (EROI 9/10)

Přidat do **všech bazos query** exclude termy:

```yaml
exclude: [..., "nemecko", "německo", "v nemecku", "nemecku", "fve", "ubytovn", "ubytování"]
```

Konkrétně dotčené: elektrikar_prumysl, zahradnik, truhlar, strechy. (`nemecko` + `v nemecku` zachytí "V NĚMECKU" i "PRÁCE NĚMECKO".)

### 5.2 strechy: lokalitní filtr (EROI 7/10)

`locations: []` → `["praha"]` — odfiltruje "Hydroizolace Krnov" (region mimo). Po přidání exclude nemecko zbude z 3 ad jen ~1 relevantní (pokrývači v Praze jsou přes prace.cz, ne bazos).

### 5.3 spravce_budov: deaktivace nebo rozšíření scope (EROI 6/10)

0 match ve 2 bězích = 0 EROI. Buď:
- (a) rozšířit boolean o `(technik OR sprava) AND (budov OR arealu OR nemovitosti)` — chytí facility management
- (b) deaktivovat (nevhodné pro autora — facility správa ≠ zájem)

### 5.4 elektrikar_prumysl: přidat prace.cz friendly terminy (EROI 5/10)

Trh na bazos prázdný, ale prace.cz má elektro-technické pozice. Rozšířit boolean o `elektrotechnik OR elektro` + locations už má `[praha]`.

### 5.5 Zahradnický průnik FP

"ZAHRADNÍK - údržba zeleně" sedí zároveň do udrzbar i zahradnik (multi-query overlap) — to je OK, ne FP.

---

## 6. Doporučené finální stav legacy profilu

| Query | Akce | Odhad dopadu |
|-------|------|--------------|
| udrzbar | + exclude nemecko/ubytovn | 22 → ~20 match, precision 95→98 % |
| zahradnik | + exclude nemecko | 5 → 4 match, 100 % precision |
| strechy | + exclude nemecko + locations [praha] | 3 → 1 match, 100 % precision |
| truhlar | + exclude nemecko | 2 → 1 match |
| elektrikar_prumysl | + exclude nemecko/fve + rozšířit scope | 1 → ~1–3 match |
| cnc_jobs | bez změny (ok) | 2 match |
| spravce_budov | rozhodnout: rozšířit nebo deaktivovat | 0 → 0–2 |

**Cíl:** legacy profil = čistá rezerva pro manual trh (B2B, přechodné potřeby) s precision >90 %, bez německého šumu.

---

## 7. Metadata

- **EROI:** 8/10
- **Tags:** `#mcp-jobs`, `#legacy-manual`, `#semanticka-analyza`, `#profilovy-vystup`, `#korekce`, `#bazos-spam`
- **Vstupní data:** `output/etl_LEGACY_MANUAL_20260731_161324.json` (35 matched), `config_legacy_manual.yaml`
- **Pipeline:** 57.1s, 103 testů prochází
- **Související:** `srovnani_er_pipeline_2026-07-31.md`, `evaluace_ai_native_era_2026-07-31.md`
