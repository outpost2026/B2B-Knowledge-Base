# Chess MCP Analyzer — Strategic Plan v1

**Datum:** 2026-07-30 | **Status:** Phase 1-3 done, 17 tools, 93 tests
**Stack:** Python 3.12 + FastMCP + uv + berserk + python-chess + Stockfish

## Architektura

```
User (opencode/Claude)
    │
    ▼ JSON-RPC 2.0 (stdio)
    │
lichess-analyzer-mcp (Python FastMCP) — 17 MCP tools
    │
    ├──► Lichess API (berserk) ───► lichess.org
    ├──► Stockfish (UCI) ─────────► lokální binary (Threads=6, Hash=512)
    ├──► chess-api.com ───────────► cloud eval fallback (depth >=14)
    ├──► python-chess ────────────► FEN/PGN/SAN parsing
    └──► py-fsrs ─────────────────► spaced repetition cache
    │
    ▼
B2B-Knowledge-Base (perzistentní storage)
```

## Fáze

| Fáze | Co | Status |
|------|----|--------|
| **Phase 0** | Import patternů do KB | ✅ Hotovo |
| **Phase 1** | MVP MCP server (4 dny) | ✅ Hotovo |
| **Phase 2** | Pattern detekce engine + dual cache | ✅ Hotovo |
| **Phase 3** | Coaching tools (5 tools) | ✅ Hotovo |
| **Phase 4** | Depth policy + cloud fallback | ✅ Hotovo |
| **Phase 5** | FSRS SRS engine | ⏳ Po schválení |

## Aktuální toolset (17 tools)

### Data tools (12)
1. `lichess_fetch_games` — stáhnout N recent her
2. `lichess_analyze_game` — analyzovat jednu hru Stockfishem (dual cache white+black)
3. `lichess_analyze_position` — analyzovat FEN pozici
4. `lichess_opening_explorer` — prozkoumat openingu
5. `lichess_player_profile` — rating historie + statistiky
6. `lichess_diagnose_player` — weakness report přes N her
7. `lichess_match_patterns` — detekce patternů A-Q1
8. `lichess_import_pgn` — import a analýza PGN
9. `lichess_games_index` — cache přehled her
10. `lichess_analyze_anonymous_session` — batch analýza anonymních her
11. `lichess_analyze_pending` — dávkové dopočítání chybějících analýz
12. `lichess_workspace_info` — kontext pro LLM agenty

### Coaching tools (5)
13. `lichess_coaching_single_game` — deep coaching report jedné hry
14. `lichess_coaching_cross_game` — cross-game pattern analýza
15. `lichess_coaching_opponent_pool` — opponent perspective analýza
16. `lichess_coaching_training_plan` — personalizovaný tréninkový plán
17. `lichess_coaching_opening_report` — opening repertoire report

## Depth Policy

Auto-select depth dle time control: bullet=12, blitz=12, rapid=14, classical=14, ostatní=14
Cloud fallback: chess-api.com pro depth >= 14 (CHESS_API_CLOUD=1)
Local engine: Threads=6, Hash=512

## EROI scoring

| Kritérium | Váha | Skóre | Poznámka |
|-----------|------|-------|----------|
| Doména (Lichess + šachy) | 35% | 9/10 | stabilní API, koníček |
| Technologie (FastMCP + Python) | 25% | 9/10 | známý stack, reusable |
| Role (MCP expert) | 20% | 9/10 | 3 MCP servery + depth policy |
| Growth (coaching pipeline) | 10% | 8/10 | SRS + LLM coaching |
| Formal (OSS licence) | 5% | 6/10 | MIT |
| Location (remote) | 5% | 10/10 | 100% lokální |
| **Celkem** | **100%** | **8.7/10** | **doporučeno** |

## Next: Phase 5 FSRS SRS engine
