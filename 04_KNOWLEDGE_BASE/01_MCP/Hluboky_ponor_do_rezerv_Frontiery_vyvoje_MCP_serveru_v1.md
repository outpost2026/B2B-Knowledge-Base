# Hluboký ponor do rezerv — Komprimovaný akční plán (v2)

**Datum:** 2026-08-01 | **Autor:** outpost2026 | **Verze:** 2.0
**Účel:** Akční plán z rezerv vývoje MCP serveru (3 týdny) — komprese v1.1 (2026-07-20); plná analýza v git historii, duplicity s MCP_GROUND_TRUTH (bod 4) odstraněny.
**Kontext:** Navazuje na `MCP_GROUND_TRUTH_postmortem_agregovany_v1.md` — Bod 4.

---

## 1. REZERVY A MVP AKCE (6 gapů)

| Gap | Priorita | Akce | Náročnost / čas |
|---|---|---|---|
| Resilience (server padá v noci) | **VYSOKÁ** | winsw (Windows Service, `startMode=Automatic`, `onFailure=restart`) + dummy tool `ping()` s notifikací | Střední / 2 h |
| Security (supply chain) | **VYSOKÁ** | `uv pip-audit --requirement pyproject.toml` jako krok v CI | Snadná / 30 min |
| Observability (chyby ano, zdraví ne) | Střední | Metrics endpoint (prometheus_client, HTTP 9090): `mcp_requests_total`, `mcp_latency_seconds` — měřit per tool | Střední / 3 h |
| Feature flags (pomalý feedback loop) | Střední | Provideri přes `ENABLED_PROVIDERS` env var; test izolovaně; aktivace bez release | Snadná / 1 h |
| Terminologie (znáš věc, neznáš jméno) | Nízká | `GLOSSARY.md` — mapování vlastních pojmů na SWE ontologii (Fowler, Refactoring.guru) | Snadná / 2 h |
| Internals (nevíš, proč to nejede) | Nízká (až při bugu) | Při deadlocku/timeoutu: číst zdrojový kód knihovny, 3 věty do postmortem — ne obalovat try/except | Těžká / průběžně |

## 2. TŘÍTÝDENNÍ PLÁN

| Týden | Cíl | Výstup |
|---|---|---|
| W1 | Auto-restart + Health Check (spadlý server = největší nepřítel) | Server běží jako služba; notifikace při výpadku |
| W2 | Observability | `/metrics` endpoint, p50/p95/p99 latency per tool |
| W3 | Security audit + Feature flags | pip-audit zelený v CI; provideri přes env |

**Po dokončení W1:** zapsat do MCP_GROUND_TRUTH nová pravidla **P46–P48**. Posun: tvůrce nástroje → správce služby (Service Owner).

## 3. PRAVIDLA A PONAUČENÍ

**P-rule (async dekorátory):** Každý dekorátor logující/zpracovávající návratovou hodnotu musí detekovat `asyncio.iscoroutinefunction(func)`; async funkci obalit async wrapperem a počkat `await func(*args)`. Nikdy neposílat coroutine do textových/číselných operací — `'coroutine' object has no attribute 'startswith'`.

**Case study (vazba na GT):** `@auditable` sync wrapper → 4 tooly padaly (2026-07-20). Fix = async detekce. Duplicitní detail s GT bod 4 — viz GT. Metrics endpoint by odhalil 100 % error rate okamžitě.

---

*Komprimováno z v1.1 (2026-07-20, 280 řádků). Plné znění: git historie.*
