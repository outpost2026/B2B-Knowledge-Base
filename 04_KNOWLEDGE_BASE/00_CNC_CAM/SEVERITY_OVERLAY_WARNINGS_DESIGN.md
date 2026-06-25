# SEVERITY OVERLAY — Vizuální varovný systém pro 2D výkres
## Konceptuální vize a implementační plán pro features/2D_visual_warnigs

**Verze:** 1.0 (Červen 2026)  
**Branch:** `features/2D_visual_warnigs`  
**Stav:** PoC návrh  

---

## 1. EXECUTIVE SUMMARY

Stávající dashboard zobrazuje sémantická varování (KB engine) **pouze textově** — pod 2D výkresem.
CNC operátor musí: (1) vidět výkres, (2) scrollovat k warningům, (3) mapovat "Element_7" na geometrii.

**Cíl:** Vizuální overlay přímo na 2D výkrese. HUD v letectví, Siemens MindSphere, GE Predix.

**Klíč:** High SNR — overlay se zobrazí POUZE při varování. Bez varování = čistý výkres.

---

## 2. TEORETICKÝ FUNDAMENT

Z `PRINCIPLES_DASHBOARD_DESIGN.md`:

| Princip | Aplikace |
|---------|----------|
| Preattentivní | #F43F5E = CRITICAL, #F59E0B = WARNING, <200ms detekce |
| TMI alarm overload | Jen 2 severity (CRITICAL/WARNING), INFO se nezobrazuje |
| Normalizace deviace | Overlay zmizí pri 0 varování — neni permanentní |
| Miller (5+-2) | Max 3 typy overlay prvku |
| Hick (0 voleb) | Uživatel nerozhoduje, jen vnímá |

**Inspirace z Průmyslu 4.0:**
- Siemens MindSphere: barevné kruhy na komponentách → BBOX overlay
- GE Predix: anomaly heatmap → canvas border
- Rockwell FactoryTalk: sequence arrows → cut_order čísla
- Dassault DELMIA: NC code color coding → severity-based line color

---

## 3. VRSTVOVÁ ARCHITEKTURA

```
+----------------------------------------------------------+
|                   2D plátno (1920x1080)                    |
|                                                           |
|  +--- V1: BASE --- zorder=1 -----------------------------+|
|  | Všechny elementy, barva dle vrstvy, lw=0.9, alpha=0.95||
|  |  +--- V2: SEVERITY LINE --- zorder=5 -----------------+||
|  |  | Cervená/oranžová tlustá cára, lw=4, alpha=0.45    |||
|  |  | Jen problematické elementy                         |||
|  |  |  +--- V3: NESTING BBOX --- zorder=6 ---------------+|||
|  |  |  | Cárkovaný obdélník + cut_order číslo           ||||
|  |  |  | Jen SEQUENCE_NESTING_ERROR                      ||||
|  |  |  +------------------------------------------------+|||
|  |  |  +--- V4: ANNOTATION --- zorder=8 -----------------+|||
|  |  |  | Text "CHYBA SEK." u centroidu, jen CRITICAL    ||||
|  |  |  +------------------------------------------------+|||
|  |  +----------------------------------------------------+||
|  +--------------------------------------------------------+|
|                                                           |
|  +--- V5: CANVAS-LEVEL --- zorder=0 --------------------+|
|  | Oranžová linka okolo celého canvasu, VACUUM_FIXATION ||
|  +------------------------------------------------------+|
|                                                           |
|  +--- V6: LEGENDA --- zorder=10 -------------------------+|
|  | ■ Critical  ■ Warning   (jen pokud existují)          ||
|  +------------------------------------------------------+|
+----------------------------------------------------------+
```

### Vrstvy — co a kdy

| # | Vrstva | Matplotlib | Trigger |
|---|--------|-----------|---------|
| 1 | BASE | `ax.plot(xs,ys, color=layer, lw=0.9)` | vždy |
| 2 | SEVERITY LINE | `ax.plot(xs,ys, color=sev, lw=4, alpha=0.45, zorder=5)` | element s varováním |
| 3 | NESTING BBOX | `matplotlib.patches.Rectangle` + `ax.text(cut_order)` | SEQUENCE_NESTING_ERROR |
| 4 | ANNOTATION | `ax.annotate("CHYBA", xy=centroid)` | jen CRITICAL |
| 5 | CANVAS | `Rectangle(canvas_bbox, ec=amber, ls="-.")` | VACUUM_FIXATION_RISK |
| 6 | LEGENDA | `ax.legend()` | jen pri has_critical/has_warning |

---

## 4. DATOVÝ MODEL

### Vstup (z KB engine)
```python
semantic_warnings[i] = {
    "code": "SEQUENCE_NESTING_ERROR",
    "severity": "CRITICAL",
    "message": "Vnejsi prvek Element_0 se reze PRED vnitrnim Element_1",
    "traceable_context": {
        "parent_id": "Element_0",
        "element_ids": ["Element_0", "Element_1"]
    }
}
```

### Transformace
```python
alerted_ids: Dict[str, str] = {}  # element_id -> worst severity
nesting_warnings: List[dict] = []  # SEQUENCE_NESTING_ERROR + CRITICAL
canvas_warnings: List[dict] = []   # VACUUM_FIXATION_RISK
```

### Severity rank
```python
_severity_rank = {"CRITICAL": 3, "WARNING": 2, "INFO": 1}
```

---

## 5. MPLEMENTACNÍ PLÁN (PoC)

| # | Krok | Odhad |
|---|------|-------|
| P1 | Parsování semantic_warnings -> alert_sev + nesting_warnings | 15 min |
| P2 | Vrstva 2: Severity line overlay | 25 min |
| P3 | Vrstva 3: Nesting BBOX + cut_order | 20 min |
| P4 | Vrstva 4: Anotace pro CRITICAL | 15 min |
| P5 | Vrstva 5: Canvas-level border | 10 min |
| P6 | Vrstva 6: Legenda | 10 min |
| P7 | Test s demo soubory (fluenz_l=137 el., knight=755 el.) | 15 min |
| P8 | Golden masters | 5 min |
| **Celkem** | | **~2 h** |

### Performance pro velké soubory
Batchování přes `LineCollection` místo 755x `ax.plot`:
```python
from matplotlib.collections import LineCollection
segments = [(xs[:-1], ys[:-1], xs[1:], ys[1:]) for el in critical_els]
lc = LineCollection(zip(...), colors="#F43F5E", lw=4, alpha=0.45, zorder=5)
ax.add_collection(lc)
```

---

## 6. VIZUALNÍ PALETA

| Severity | Hex | Tailwind | Význam |
|----------|-----|----------|--------|
| CRITICAL | #F43F5E | rose-500 | Poskození materiálu, spatná sekvence |
| WARNING | #F59E0B | amber-500 | Suboptimální H2, malá plocha |
| INFO | — | — | Nezobrazuje se (alarm overload) |

Konzistentní se stávajícími CSS trídami `.hero-status-badge`.

---

## 7. ANTI-PATTERNS

| NEDELAT | DELAT |
|---------|-------|
| Zobrazovat overlay pri 0 varování | `if has_warnings:` |
| 5+ barev pro ruzné kódy | Max 2 barvy: CRITICAL, WARNING |
| mplcursors v PoC | Cekat na zpetnou vazbu operátora |
| Legenda pri 0 varování | `if legend_patches:` |
| Změnit parsed_data | Overlay data jsou derived, ne stored |

---

## 8. VALIDACE

| Princip | Splneno | Dukaz |
|---------|---------|-------|
| High SNR | ANO | Overlay NENI permanentní |
| Preattentive | ANO | Cervená = <200ms detekce |
| Alarm overload | ANO | 2 severity, INFO nezobrazeno |
| Normalizace deviace | ANO | Overlay zmizí pri 0 varování |
| Miller | ANO | 3 typy prvku (cára + bbox + text) |
| SYSTEQ palette | ANO | rose-500 / amber-500 |

---

## 9. STRETCH GOALS (v2+)

- **AUTO-ZOOM**: Extra figura s výrezem problematického elementu
- **HOVER TOOLTIP**: mplcursors — najetí myší na element -> zobrazí warningy
- **FILTER**: Checkbox "Jen CRITICAL" / "Jen nesting"
- **DIFF OVERLAY**: Modrá (raw) + cervená (reconstructed) pro ladění
- **EXPORT PDF**: Výkres s overlayem pro technickou dokumentaci

---

*Dokument: features/2D_visual_warnigs — SYSTEQ B2B CAM Automation Platform — Cerven 2026*
