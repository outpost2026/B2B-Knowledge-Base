# Mechanizmy Transformace Dat: Markdown na Strukturovaná Data

**Účel:** Detailní popis procesu převodu nestrukturovaného Markdown textu z `MCP_GROUND_TRUTH_postmortem_agregovany_v1.md` do formátu vhodného pro indexaci vyhledávacím enginem a prezentaci ve webovém rozhraní.

---

## 1. VÝCHODISKO: SEMI-STRUKTUROVANÝ MARKDOWN

Dokument `MCP_GROUND_TRUTH_postmortem_agregovany_v1.md` je psán v semi-strukturovaném Markdownu. Ačkoliv není striktně JSON, obsahuje konzistentní vzory (např. `#### GT-ID (ORIG-ID): Název chyby`, `**Symptom:**`, `**Root cause:**`, `**Fix:**`, `**Pravidlo:**`). Tato konzistence je klíčová pro automatizovanou extrakci.

---

## 2. FÁZE TRANSFORMACE DAT

Proces transformace lze rozdělit do tří hlavních fází:

### 2.1. Parsování Markdownu do AST (Abstract Syntax Tree)

Prvním krokem je převod Markdown textu do programově zpracovatelné datové struktury, která reprezentuje hierarchii a typy elementů dokumentu (nadpisy, odstavce, seznamy, tabulky).

-   **Nástroje (Python):**
    -   `markdown-it-py`: Robustní a flexibilní parser, který generuje AST. Umožňuje snadnou manipulaci s jednotlivými uzly dokumentu.
    -   `mistune`: Další rychlý Markdown parser v Pythonu.
-   **Nástroje (JavaScript/TypeScript - pro build-time v Next.js):**
    -   `remark` a `rehype`: Ekosystém pluginů pro zpracování Markdownu a HTML. `remark-parse` pro parsování Markdownu do `mdast` (Markdown Abstract Syntax Tree) a `rehype-stringify` pro převod `hast` (HTML Abstract Syntax Tree) zpět na HTML. Mezi nimi lze vkládat vlastní transformační pluginy.

### 2.2. Extrakce Strukturovaných Entit (GT-Pravidla)

Jakmile je Markdown převeden na AST, je možné procházet strom a extrahovat specifické informace, které tvoří jednotlivá GT-pravidla. Každé GT-pravidlo bude reprezentováno jako samostatný objekt.

-   **Mechanismus:**
    1.  **Identifikace GT-pravidla:** Hledání nadpisů čtvrté úrovně (`####`) s regulárním výrazem `GT-(\d+) \((.+?)\): (.+)`. Tím se získá `GT-ID`, původní ID a název chyby.
    2.  **Extrakce polí:** Pro každý identifikovaný nadpis se prohledávají následující odstavce a seznamy pro klíčová slova jako `**Symptom:**`, `**Root cause:**`, `**Fix:**`, `**Pravidlo:**`. Text následující po těchto klíčových slovech se extrahuje.
    3.  **Normalizace:** Odstranění nadbytečných mezer, formátování a případné konverze datových typů (např. `Status: Fixed` na boolean `is_fixed: true`).
-   **Výstup:** Kolekce JSON objektů, kde každý objekt reprezentuje jedno GT-pravidlo s definovanými poli (např. `gt_id`, `original_id`, `title`, `symptom`, `root_cause`, `fix`, `rule`, `server`, `status`).

### 2.3. Transformace do Indexovatelného Formátu

Posledním krokem je převod extrahovaných JSON objektů do formátu, který je optimální pro vyhledávací engine (např. MeiliSearch) a pro frontendovou prezentaci.

-   **Nástroje:** Standardní Python/JavaScript knihovny pro práci s JSON.
-   **Mechanismus:**
    1.  **Flatting:** Zajištění, že každý dokument pro indexaci je plochý (bez hluboce vnořených struktur), což usnadňuje vyhledávání.
    2.  **Tokenizace a Embedding (volitelné):** Pro pokročilé sémantické vyhledávání (např. s Elasticsearch a RAG) by bylo možné generovat textové embeddingy pro každé GT-pravidlo a ukládat je spolu s dokumentem.
    3.  **Indexace:** Odeslání JSON dat do vyhledávacího enginu přes jeho API.

---

## 3. PŘÍKLAD STRUKTUROVANÉHO VÝSTUPU (JSON)

```json
[
  {
    "gt_id": "GT-001",
    "original_id": "CNC-001",
    "title": "Sekvenční bottleneck — Cross-repo paralelizace",
    "server": "cnc-tools",
    "status": "Fixed",
    "symptom": "MCP error -32001: Request timed out při tool_git_status_all a tool_cross_repo_search. Audit log: duration_s: 61.7-62.4 — přesně nad 60s MCP client timeout.",
    "root_cause": "Oba nástroje iterovaly 14 repozitářů sériově v jedné for smyčce. 14 x 4.4s = 61.7s.",
    "fix": "ThreadPoolExecutor(max_workers=4). 14 repo / 4 vlakna x 4.4s = ~15.4s.",
    "rule": "P1 — Jakmile nástroj iteruje N>1 nezávislých zdrojů, musí být paralelizován."
  },
  {
    "gt_id": "GT-002",
    "original_id": "CNC-002",
    "title": "Vnořené timeouty bez signalizace",
    "server": "cnc-tools",
    "status": "Fixed",
    "symptom": "tool_git_diff vrací error až po 60s, subprocess timeout byl 30s. Dvojité čekání: 30s subprocess + 30s client = 60s ztraceného času.",
    "root_cause": "Subprocess timeout (30s) byl příliš blízko client timeoutu (60s).",
    "fix": "Subprocess timeout ≤ 15s. Fail fast: error za 15s je lepší než timeout za 60s.",
    "rule": "P2 — Subprocess timeout v MCP toolu musí být max 25% MCP client timeoutu."
  }
  // ... další GT-pravidla
]
```

---

## 4. INTEGRACE S LLM PRO SÉMANTICKÉ OBOHACENÍ (VOLITELNÉ)

Pro zvýšení kvality vyhledávání a generování odpovědí lze využít LLM k obohacení extrahovaných dat:

-   **Kategorizace:** LLM může automaticky přiřadit každému GT-pravidlu kategorie (např. `Performance`, `Reliability`, `Security`, `Usability`).
-   **Summarizace:** Generování kratších, srozumitelnějších shrnutí pro rychlý přehled.
-   **Tagování:** Extrakce klíčových slov a technologií pro lepší filtrování.

Tyto obohacené informace by byly uloženy spolu s původními daty a indexovány do vyhledávacího enginu.

---

## 5. ZÁVĚR

Transformace Markdownu na strukturovaná data je proveditelná a klíčová pro úspěch webové aplikace. Díky konzistentnímu formátu `MCP_GROUND_TRUTH` je proces extrakce relativně přímočarý. Výsledkem bude bohatá, indexovatelná datová sada, která umožní efektivní vyhledávání a navigaci v GT-pravidlech.
