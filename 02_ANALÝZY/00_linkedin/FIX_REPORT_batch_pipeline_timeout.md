# FIX REPORT — LinkedIn MCP `analyze_saved_jobs` MCP transport timeout (-32001)

**Datum:** 2026-07-09
**Repo:** `linkedin-mcp-custom` (větev `refactor`)
**Soubor:** `src/linkedin_mcp_custom/tools/job.py`
**Závažnost:** KRITICKÁ (pipeline nepoužitelná přes MCP — blokuje celý batch)

---

## 1. Symptom

Volání `analyze_saved_jobs` (batch pipeline) přes MCP server končilo:

```
MCP error -32001: Request timed out
```

i při `limit=3` i `max_seconds=45`. Single `analyze_job` fungoval, ale
občas timeoutl na 2. volání (navigační race).

## 2. Root cause

Batch používal:

```python
tasks = [_scrape_one(idx, jid) for idx, jid in enumerate(job_ids_to_process)]
results_list = await asyncio.gather(*tasks)
```

`asyncio.gather` čeká na **dokončení všech** úloh najednou. Deadline
kontrola uvnitř `_scrape_one` byla k ničemu — výsledek se stejně nevrátil
dřív, než všech 50 jobů (každý ~2–5 s scrape) doběhlo → 100–250 s →
MCP transport timeout (-32001). Parametr `max_seconds` byl v podstatě
mrtvý.

## 3. Oprava

Přepsáno na **sekvenční early-exit smyčku**:

```python
for jid in job_ids_to_process:
    if time.time() >= deadline:          # kontrola PŘED každým jobem
        unprocessed_ids.append(jid)
        continue
    detail = await extractor.scrape_job(jid, parallel=True)
    ...
```

- Server vrátí response do `max_seconds` (early-exit zastaví před
  dalším jobem).
- Nezpracované joby se vrátí v `unprocessed_ids` pro navazující volání.
- Odstraněn nepoužitý `asyncio` import a konstanty
  `DEFAULT_MAX_CONCURRENT` / `DEFAULT_DELAY_BETWEEN`.
- `parallel_config` → `batch_mode: {strategy: sequential_early_exit, ...}`.

## 4. Testy

Nový `tests/test_batch_pipeline.py` (3 testy, FastMCP in-memory client +
mock extractor):

| Test | Ověřuje |
|---|---|
| `test_batch_returns_within_deadline` | 50 jobů × 1 s, budget 10 s → response < 12 s, ~10 zpracováno |
| `test_batch_respects_limit` | `limit=3` → přesně 3 zpracováno, 47 remaining |
| `test_batch_no_sequential_gather_hang` | budget 1 s → response < 5 s, `batch_partial` |

**Výsledek:** `28 passed` (celá sada).

## 5. Stav ověření

- ✅ Unit testy (offline, mock) — fix potvrzen.
- ✅ Živý MCP test s `limit=4` vrátil 4 joby bez timeoutu.
- ⚠️ Živý MCP server stále běží se **starým kódem v paměti** → `limit=0`
  stále timeoutuje. **Vyžadován restart MCP server process** (znovu
  načíst modul), aby se projevil nový kód pro plný batch.

## 6. Doporučení pro komunitní release

1. Po restartu serveru otestovat `analyze_saved_jobs` s `limit=0`
   (plný batch 50 jobů) — měl by vrátit partial za ~45 s.
2. Do README přidat sekci "Batch pipeline & time budget" s vysvětlením
   `max_seconds` / `unprocessed_ids` loopu.
3. Přidat CI step: `pytest tests/` (nyní 28 testů).
