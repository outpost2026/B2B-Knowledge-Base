# Návrh Technické Architektury: Web pro GT-Pravidla

**Účel:** Transformace `MCP_GROUND_TRUTH_postmortem_agregovany_v1.md` do interaktivního webového rozhraní s vyhledáváním a navazujícími funkcemi.

---

## 1. ARCHITEKTURA SYSTÉMU: HYBRIDNÍ STATICKÝ WEB S DYNAMICKÝM BACKENDEM

Navrhovaná architektura kombinuje výhody statických stránek (rychlost, bezpečnost, nízké náklady na hosting) s flexibilitou dynamického backendu pro pokročilé funkce (sémantické vyhledávání, LLM integrace).

```mermaid
graph TD
    A[Uživatel] -->|HTTP Request| B(CDN / Edge)
    B -->|Static Assets (HTML, CSS, JS)| C[Frontend (Next.js/React)]
    C -->|API Call (REST/GraphQL)| D[Backend (Python/FastAPI)]
    D -->|Search Query| E[Search Engine (Elasticsearch/MeiliSearch)]
    D -->|LLM Query| F[LLM Service (OpenAI/DeepSeek)]
    D -->|Data Access| G[Knowledge Base (Git Repo / GCS)]
    G -->|Markdown Files| H[Build Process (Next.js SSG)]
    H -->|Static HTML, JS| B
```

### 1.1 Frontend (Prezentační vrstva)

-   **Framework:** `Next.js` (s Reactem) nebo `Vue.js` (s Nuxt.js).
    -   **Důvod:** Podpora Static Site Generation (SSG) pro generování HTML z Markdownu během build-time. To zajišťuje extrémně rychlé načítání a SEO optimalizaci. Zároveň umožňuje hydrataci JavaScriptem pro interaktivní prvky (filtry, vyhledávání, dynamické komponenty).
    -   **Alternativa:** `SvelteKit` pro menší bundle size a jednodušší reaktivitu, ale s menším ekosystémem.
-   **Styling:** `Tailwind CSS`.
    -   **Důvod:** Rychlý vývoj UI, konzistentní design, snadná adaptace na responzivní zobrazení.

### 1.2 Backend (Aplikační logika a Data)

-   **Framework:** `Python` s `FastAPI`.
    -   **Důvod:** Využití stávající Python expertízy. FastAPI je moderní, rychlý, asynchronní a má automatickou OpenAPI dokumentaci. Ideální pro API, které bude obsluhovat frontend a integrovat se s dalšími službami.
-   **Nasazení:** `GCP Cloud Run` nebo `Cloud Functions`.
    -   **Důvod:** Bezserverové řešení pro škálovatelnost a efektivitu nákladů. Snadná integrace s ostatními GCP službami.

### 1.3 Search Engine (Vyhledávání)

-   **Primární volba:** `MeiliSearch`.
    -   **Důvod:** Open-source, rychlý, snadno nasaditelný (Docker), nabízí relevantní výsledky s tolerancí překlepů. Může běžet jako samostatná služba nebo být integrován do backendu.
-   **Alternativa pro pokročilé RAG:** `Elasticsearch` (s `LangChain` nebo `LlamaIndex`).
    -   **Důvod:** Pro sémantické vyhledávání a komplexní dotazy, které by využívaly embeddingy a RAG (Retrieval-Augmented Generation) s LLM. Vyšší komplexita nasazení.

### 1.4 Datová vrstva (Knowledge Base)

-   **Primární zdroj:** Stávající `Git repozitář` (`B2B-Knowledge-Base`).
    -   **Důvod:** Single Source of Truth. Markdown soubory jsou parsovány během build-time nebo indexovány do search engine.
-   **Perzistence pro index:** `GCP Cloud Storage` nebo `Firestore` (pro metadata).
    -   **Důvod:** Ukládání indexu pro MeiliSearch/Elasticsearch a dalších metadat.

---

## 2. MECHANISMY PŘENOSU DAT A TRANSFORMACE

### 2.1 Markdown → Strukturovaná data

-   **Proces:** Během build-time (Next.js SSG) nebo při indexaci do search engine (Python script).
-   **Nástroje:**
    -   `remark` / `rehype` (JavaScript) nebo `markdown-it` (Python) pro parsování Markdownu do AST (Abstract Syntax Tree).
    -   Vlastní skripty pro extrakci strukturovaných dat (GT-ID, Symptom, Root Cause, Fix, Pravidlo) z AST. To je klíčové pro sémantické vyhledávání.
    -   Transformace do `JSON` formátu pro snadnou indexaci a konzumaci frontendem.

### 2.2 Vyhledávání a zobrazení

-   **Indexace:** Python script načte JSON data a indexuje je do MeiliSearch/Elasticsearch.
-   **Frontend:** Uživatel zadá dotaz → Frontend volá FastAPI backend → Backend volá Search Engine → Výsledky jsou zobrazeny ve frontendu.
-   **Highlighting:** Search engine by měl podporovat zvýrazňování nalezených termínů ve výsledcích.

---

## 3. STRATEGICKÁ VHODNOST PRO FÁZI T+4M (ROI/LEARNING)

### 3.1 ROI (Return on Investment)

-   **Vysoké ROI (P>0.8):** Tento projekt má potenciál výrazně zvýšit hodnotu vaší `B2B-Knowledge-Base` a `MCP_GROUND_TRUTH` jako externího validačního zdroje.
    -   **Pro klienty/zaměstnavatele:** Interaktivní web je mnohem přístupnější a působivější než surový Markdown soubor. Demonstruje schopnost "productizace" interních procesů.
    -   **Pro vás:** Zefektivní vyhledávání v GT-pravidlech, což povede k rychlejšímu řešení problémů a menšímu opakování chyb.

### 3.2 Learning Path (Učební křivka)

-   **Optimalizovaná učební křivka (P>0.9):** Projekt vás donutí prohloubit znalosti v klíčových oblastech moderního webového vývoje, které doplňují váš stávající Python/GCP/Agentic stack:
    -   **Frontend Framework:** React/Vue (nová doména, ale vysoce žádaná).
    -   **Static Site Generation:** Optimalizace výkonu a nasazení.
    -   **Search Engine Integration:** Práce s fulltextovými indexy a relevantním vyhledáváním.
    -   **API Design:** Návrh robustního API pro komunikaci mezi frontendem a backendem.

-   **Synergie s existujícími dovednostmi:** Python backend pro indexaci a případné RAG integrace je přirozeným rozšířením vašich stávajících kompetencí.

---

## 4. FINÁLNÍ DOPORUČENÍ A ROADMAPA

**Doporučení:** **Projekt je strategicky vhodný a má vysoké ROI pro vaši současnou fázi (T+4m).** Posílí vaši pozici "Systémového stavitele" a "AI-Augmented Developera" tím, že produktizuje vaši metodiku.

### Roadmapa (Fáze 1-3)

1.  **Fáze 1: Data Extraction & Indexace (Python)**
    -   Vytvořit Python skript pro parsování `MCP_GROUND_TRUTH_postmortem_agregovany_v1.md`.
    -   Extrahovat strukturovaná data (GT-ID, Symptom, Root Cause, Fix, Pravidlo) do JSON formátu.
    -   Napsat skript pro indexaci JSON dat do `MeiliSearch` (běžícího v Dockeru lokálně).

2.  **Fáze 2: Frontend MVP (Next.js/React)**
    -   Inicializovat Next.js projekt.
    -   Vytvořit základní UI pro zobrazení GT-pravidel (seznam, detail).
    -   Implementovat jednoduché vyhledávací pole, které volá MeiliSearch API (přes FastAPI backend).
    -   Zobrazit výsledky vyhledávání s highlightingem.

3.  **Fáze 3: Backend API & Deployment (FastAPI/GCP)**
    -   Vytvořit FastAPI aplikaci, která bude sloužit jako proxy mezi frontendem a MeiliSearch (a případně LLM).
    -   Nasazení FastAPI na `GCP Cloud Run`.
    -   Nasazení Next.js aplikace jako statického webu (např. na `GCP Cloud Storage` s CDN nebo `Vercel`).

**Actionable závěr:** Začněte s Fází 1. Je to čistě Pythonová úloha, která navazuje na vaše stávající dovednosti a připraví data pro další kroky. Bude to také dobrý test robustnosti vaší `MCP_GROUND_TRUTH` struktury. 
