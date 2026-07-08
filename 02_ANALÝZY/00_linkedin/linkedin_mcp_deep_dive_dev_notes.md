# Dev Notes: stickerdaniel/linkedin-mcp-server Deep Dive

## 1. Architecture Overview

```
server.py
  └── create_mcp_server()
       ├── register_person_tools()   → tools/person.py
       ├── register_company_tools()  → tools/company.py
       ├── register_job_tools()      → tools/job.py
       ├── register_messaging_tools()→ tools/messaging.py
       └── register_feed_tools()     → tools/feed.py

Each tool file registers @mcp.tool() decorated async functions.
Tools delegate to LinkedInExtractor (scraping/extractor.py).

Dependencies:
  - get_ready_extractor(ctx, tool_name) → LinkedInExtractor(browser.page)
  - LinkedInExtractor wraps Patchright Page
  - auth via cookie-based persistent profile (~/.linkedin-mcp/profile/)
```

## 2. Three-Layer Pattern

Every tool follows the same pattern:

**Layer 1 - Tool registration** (`tools/job.py`, `tools/person.py`, etc.):
```python
@mcp.tool(timeout=tool_timeout, ...)
async def get_job_details(job_id: str, ctx: Context, extractor=None):
    extractor = extractor or await get_ready_extractor(ctx, tool_name=...)
    result = await extractor.scrape_job(job_id)
    return result  # {url, sections: {name: text}}
```

**Layer 2 - Extractor method** (`scraping/extractor.py`):
```python
async def scrape_job(self, job_id: str) -> dict[str, Any]:
    url = f"https://www.linkedin.com/jobs/view/{job_id}/"
    extracted = await self.extract_page(url, section_name="job_posting")
    # ... build {url, sections, references, section_errors}
```

**Layer 3 - Core extraction** (`scraping/extractor.py`):
```python
async def extract_page(self, url, section_name, max_scrolls=None):
    await self._navigate_to_page(url)
    # detect rate limit → wait for <main> → dismiss modals → scroll → innerText → strip noise
```

**Return format** (all tools):
```json
{"url": "...", "sections": {"section_name": "raw_text"}, "references": {}, "section_errors": {}}
```

## 3. Key Files Analyzed

| File | Purpose | Lines |
|------|---------|-------|
| `server.py` | FastMCP setup, tool registration, browser lifecycle | 88 |
| `tools/job.py` | `get_job_details`, `search_jobs` tools | 151 |
| `tools/person.py` | `get_person_profile`, `get_my_profile`, `search_people`, `connect_with_person` | 368 |
| `scraping/extractor.py` | **Core: `LinkedInExtractor`** — navigate, scroll, innerText, noise strip | 3700+ |
| `scraping/fields.py` | `PERSON_SECTIONS`, `COMPANY_SECTIONS` configs | 88 |
| `scraping/__init__.py` | Exports `LinkedInExtractor`, `PERSON_SECTIONS`, etc. | 17 |
| `authentication.py` | Cookie/profile auth checks | 86 |
| `drivers/browser.py` | `BrowserManager` singleton, cookie bridge, profile lifecycle | 632 |
| `config/schema.py` | `BrowserConfig`, `ServerConfig`, `AppConfig` dataclasses | 206 |
| `dependencies.py` | `get_ready_extractor()`, `handle_auth_error()` | 106 |
| `core/__init__.py` | Exports `BrowserManager`, auth detectors, exception classes | 39 |

## 4. What Exists vs. What's Missing

### ✅ Existing in stickerdaniel v4.17.0

- `search_jobs(keywords, location, filters...)` → paginated job ID list
- `get_job_details(job_id)` → full posting text (title, company, description, seniority, employment type, etc.)
- Full person/company/feed/messaging suite
- Cookie-based auth with profile persistence
- Anti-detection via Patchright (Playwright fork)
- Noise stripping (footer, sidebar, rate-limit sentinel)
- Rate limit detection + retry
- Modal/dialog handling

### ❌ NOT in stickerdaniel (what we need)

| Feature | Implementation Effort | Complexity |
|---------|----------------------|------------|
| **Saved jobs extraction** | ~30 lines tool + ~20 lines extractor | Low |
| **EROI scoring engine** | ~200-400 lines (domain/tech/role matcher) | Medium |
| **Skill gap analysis** | ~100-150 lines (against portfolio_audit) | Medium |
| **KB write-back** | ~80 lines (report + metadata + git commit) | Low |
| **Config for EROI rules** | ~50 lines (config schema extension) | Low |

## 5. How to Add Saved Jobs (Recipe)

### 5.1 New extractor method (`scraping/extractor.py`)

Following the exact same pattern as `scrape_job` (line 2897):

```python
async def scrape_saved_jobs(self) -> dict[str, Any]:
    """Scrape LinkedIn saved jobs tracker."""
    url = "https://www.linkedin.com/jobs-tracker/"
    extracted = await self.extract_page(url, section_name="saved_jobs")

    sections = {}
    references = {}
    section_errors = {}
    if extracted.text and extracted.text != _RATE_LIMITED_MSG:
        sections["saved_jobs"] = extracted.text
        if extracted.references:
            references["saved_jobs"] = extracted.references
    elif extracted.error:
        section_errors["saved_jobs"] = extracted.error

    # Extract job IDs from saved job cards
    job_ids = await self._extract_saved_job_ids()

    result = {"url": url, "sections": sections}
    if job_ids:
        result["job_ids"] = job_ids
    if references:
        result["references"] = references
    if section_errors:
        result["section_errors"] = section_errors
    return result

async def _extract_saved_job_ids(self) -> list[str]:
    """Extract job IDs from saved job cards on /jobs-tracker/."""
    # Same pattern as _extract_job_ids — query a[href*="/jobs/view/"]
    return await self._page.evaluate("""() => {
        const links = document.querySelectorAll('a[href*="/jobs/view/"]');
        const seen = new Set();
        const ids = [];
        for (const a of links) {
            const match = a.href.match(/\\/jobs\\/view\\/(\\d+)/);
            if (match && !seen.has(match[1])) {
                seen.add(match[1]);
                ids.push(match[1]);
            }
        }
        return ids;
    }""")
```

### 5.2 New tool registration (`tools/job.py`)

Following the same pattern as `get_job_details`:

```python
@mcp.tool(
    timeout=tool_timeout,
    title="Get Saved Jobs",
    annotations={"readOnlyHint": True, "openWorldHint": True},
    tags={"job", "scraping"},
    exclude_args=["extractor"],
)
async def get_saved_jobs(
    ctx: Context,
    extractor: Any | None = None,
) -> dict[str, Any]:
    """
    Get saved jobs from LinkedIn's /jobs-tracker/ page.

    Returns dict with url, sections (raw text), and job_ids list
    that can be passed to get_job_details for full info.
    """
    try:
        extractor = extractor or await get_ready_extractor(
            ctx, tool_name="get_saved_jobs"
        )
        result = await extractor.scrape_saved_jobs()
        return result
    except AuthenticationError as e:
        try:
            await handle_auth_error(e, ctx)
        except Exception as relogin_exc:
            raise_tool_error(relogin_exc, "get_saved_jobs")
    except Exception as e:
        raise_tool_error(e, "get_saved_jobs")
```

### 5.3 EROI analysis module (new file)

Create `linkedin_mcp_server/analysis/eroi_scorer.py`:

```python
"""EROI scoring engine — domain/tech/role matching per golden rules."""

# Weights: domain 35%, tech 25%, role 20%, growth 10%, formal 5%, location 5%
# Thresholds: >=65% SLEDOVAT, 50-64% medium, <40% NESLEDOVAT
# Input: raw job text (from get_job_details sections)
# Output: score dict + skill gaps + recommendation

# This is where the user's KB methodology gets embedded.
# The existing golden rules from synteticky_report_analyza.md
# and skill matrix from portfolio_audit_a_match.md define the scoring.
```

## 6. Fork Ecosystem Analysis

| Fork | Added Value | Diff from upstream |
|------|-------------|-------------------|
| `stickerdaniel/linkedin-mcp-server` | **Original** — 2.6k★, 466 forks, 1053 commits, v4.17.0 | — |
| `pauling-ai/linkedin-mcp-server` | Messaging, post engagement | Small |
| `mvanhorn/linkedin-mcp-server` | `get_inbox`, `get_conversation`, `connect_with_person` | Small |
| `hubertusgbecker/mcp-linkedin-server` | Notifications, full post extraction, profile analytics | Small |
| `sanu495/linkedin-mcp-server` | `close_browser` utility | Trivial |
| `wlyonscat/server-mcp-linkedin` | Resume/CL generation, application tracking | Different use case |
| `akvinayaktiwari/LinkedIn-MCP-Server` | Basic profile + search | Trivial |

**Verdict: No fork adds EROI analysis, saved jobs scraping, or KB integration.**

## 7. Central Question: Can stickerdaniel be extended with the KB backend?

**Answer: Yes, absolutely. The integration is straightforward and there are two viable paths.**

### Path A — Fork + extend (recommended for user control)

**Effort:** ~150-200 lines of Python code total for the scraping part, plus ~300-500 lines for the EROI analysis engine (already designed in the pipeline doc).

**What to fork:**
- Add `get_saved_jobs` tool (~30 lines in `tools/job.py`)
- Add `scrape_saved_jobs()` + `_extract_saved_job_ids()` to extractor (~30 lines in `scraping/extractor.py`)
- Create `analysis/` module with EROI scoring, skill matching, KB write-back
- Optionally add `analyze_saved_jobs` and `write_saved_jobs_report` tools

**Why it works:**
- The codebase has a clean, consistent three-layer pattern (tool → extractor → page)
- Adding a new tool that navigates to `/jobs-tracker/` and extracts innerText is ~50 lines
- The EROI analysis is pure business logic (no browser needed), completely orthogonal to the scraping layer
- The KB writes are local filesystem + git operations — no LinkedIn interaction

**Integration points:**
| Layer | Where | What |
|-------|-------|------|
| Tool registration | `tools/job.py` | New `get_saved_jobs` tool |
| Extractor method | `scraping/extractor.py` | New `scrape_saved_jobs()` method |
| Analysis engine | `analysis/eroi_scorer.py` (new) | EROI scoring, skill gaps |
| KB writer | `analysis/kb_writer.py` (new) | Report + metadata + git |
| Config | `config/schema.py` | EROI weight config (optional) |

### Path B — Keep separate (simpler, no fork needed)

**Effort:** Same as Pipeline Variant A (~4-6h).

- Use stickerdaniel via `uvx mcp-server-linkedin` for auth + scraping
- Write a standalone Python script that calls the MCP tools programmatically
- The EROI analysis + KB writing logic is the same either way

### Recommendation

**Path A** if you want:
- A single `uvx` command to do everything
- To publish your own fork with the EROI capability
- Tight integration (e.g., `analyze_saved_jobs` returns structured EROI data directly)

**Path B** if:
- You want to move faster on the pipeline (no fork maintenance)
- The KB backend is already well-structured as standalone Python modules
- You prefer loose coupling between scraping and analysis

Both paths share the same EROI engine design — the business logic (domain/tech/role matching, skill gaps, weighted scoring) is the same regardless of how you get the raw job text.

## 8. Unique Value of KB Backend

The user's KB backend provides what no fork in the ecosystem offers:

1. **Domain intelligence** — Industrial automation focus, crossover rate calculation
2. **Weighted EROI scoring** — 35% domain / 25% tech / 20% role / 10% growth / 5% formal / 5% location
3. **Skill gap analysis** — Direct match / partial match / no match against `portfolio_audit_a_match.md`
4. **Structured reporting** — `agregovany_report.md` + `metadata_stacku.json` + git commit
5. **Decision thresholds** — ≥65% SLEDOVAT, 50-64% medium, <40% NESLEDOVAT

This is genuinely unique — **no fork or alternative MCP server has any of this**.

## 9. Session 6 Post-Mortem (2026-07-08) — Quality Gates, CI/CD, Cookie Lifecycle

### Completed

| Area | Change | Files |
|------|--------|-------|
| Linting | ruff 0 errors (UP017 datetime.UTC fix) | `auth.py` |
| Typing | mypy 0 errors — SkillConfig TypedDict, type casts | `schemas.py`, `config.py`, `tech.py` |
| Quality gate | pre-commit hook installed (ruff --fix + ruff-format) | `.pre-commit-config.yaml` |
| Tests | 28 new scorer unit tests (6 dimenzí, 38 total) | `tests/test_scorer.py` |
| Cookie lifecycle | `get_session_age()`, `session_needs_refresh()`, health_check warning | `auth.py`, `server.py`, `core/__init__.py` |
| CI/CD | `.github/workflows/weekly-scrape.yml` — cron + workflow_dispatch | `.github/workflows/` |
| Cookie export | `scripts/export_cookies.py` — Playwright API export do JSON | `scripts/export_cookies.py` |
| Post-mortem | Záznam 021-024 v pitevni_kniha_v1.md | `docs/pitevni_kniha_v1.md` |

### New Bug Discoveries (Záznam 021-024)

1. **021 — CI/CD cookie export**: Cookies nejsou JSON v profilu, ale Chromium SQLite. Nutný export přes Playwright API.
2. **022 — PAT workflow scope**: Push .github/workflows/ vyžaduje `workflow` scope v PAT.
3. **023 — Session compact directory**: working dir cnc-tools vs. source code linkedin-mcp-custom — dokumentovat mapping.
4. **024 — Scorer unit test discovery**: 6 testů selhalo — testy jako living documentation odhalily nuance scorer logiky.

### Pending

- LINKEDIN_COOKIES + KB_PAT secrets v GitHub repo → workflow_dispatch test
- V2 multi-user architektura (plan_v2_integrace.md)
- Cookie refresh process (monthly re-export linkedin cookies)

---

*Generated: 2026-07-05. Updated: 2026-07-08 — Session 6 post-mortem (quality gates, CI/CD, Záznam 021-024). Active branch: main*
