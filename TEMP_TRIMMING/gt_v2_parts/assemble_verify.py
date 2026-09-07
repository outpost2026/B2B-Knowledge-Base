import re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"C:\Users\PC\Documents\Repozitar_Dev\_github\B2B-Knowledge-Base"
P = BASE + r"\TEMP_TRIMMING\gt_v2_parts"
DST = BASE + r"\04_KNOWLEDGE_BASE\01_MCP\MCP_GROUND_TRUTH_postmortem_agregovany_v2.md"

order = [
    "01_header_intro.md",
    "02_gt_001_014.md",
    "03_gt_015_029.md",
    "04_gt_030_044.md",
    "05_gt_045_057.md",
    "06_gt_058_070.md",
    "07_gt_071_081.md",
    "08_gt_083_098.md",
    "09_gt_099_gcp.md",
    "10_s4_rules.md",
    "11_s4_new_rules.md",
    "12_s5_filter.md",
    "13_s6_eroi.md",
    "14_s7_checklist.md",
    "15_stats_footer.md",
]
sep_before = {
    "10_s4_rules.md",
    "12_s5_filter.md",
    "13_s6_eroi.md",
    "14_s7_checklist.md",
    "15_stats_footer.md",
}

parts = []
for name in order:
    with open(f"{P}\\{name}", encoding="utf-8") as f:
        txt = f.read().strip("\n")
    if name in sep_before:
        parts.append("---")
    parts.append(txt)

doc = "\n\n".join(parts).rstrip() + "\n"
doc = re.sub(r"\n{4,}", "\n\n\n", doc)  # max 2 blank lines

with open(DST, "w", encoding="utf-8", newline="\n") as f:
    f.write(doc)

# ================= VERIFICATION =================
ok = True


def chk(label, cond, detail=""):
    global ok
    print(f"[{'OK' if cond else 'FAIL'}] {label} {detail}")
    if not cond:
        ok = False


gt_headers = re.findall(r"^#### (GT-[A-Z0-9-]+)", doc, re.M)
chk("GT záznamů", len(gt_headers) == 108, f"= {len(gt_headers)}")
chk("GT unikátních ID", len(set(gt_headers)) == len(gt_headers))
missing = [f"GT-{i:03d}" for i in range(1, 106) if f"GT-{i:03d}" not in set(gt_headers)]
chk("Číslování mezery jen 082/084", missing == ["GT-082", "GT-084"], str(missing))
prov = len(re.findall(r"Provenance:", doc))
chk("Provenance polí", prov >= 48, f"= {prov}")
chk("Header verze 20", "**Verze:** 20" in doc)
chk("Footer verze 20 konzistentní", "Header/footer verze 20 konzistentní" in doc)

# P-rule integrity: každý odkazovaný PXX musí mít definici ### PXX (nebo být rezervovaný)
refs = set()
for m in re.finditer(r"\*\*Pravidl[ao]:\*\*\s*(P-GCP-\d{2}|P\d{2})", doc):
    refs.add(m.group(1))
defined = set(re.findall(r"^### (P-GCP-\d{2}|P\d{2}) ", doc, re.M))
reserved = {f"P{n}" for n in range(84, 90)}
undef = sorted(refs - defined - reserved)
chk(
    "Všechna odkazovaná pravidla definována",
    not undef,
    f"undef={undef} refs={len(refs)} defs={len(defined)}",
)

# žádný duplicitní changelog (starý footer text nesmí existovat více než v git referenci)
chk("Starý changelog odstraněn", doc.count("Pridano GT-071 az GT-077") == 0)
# titulky opraveny
chk("Titulek §4", "## 4. Průřezová pravidla P1–P96" in doc)
chk("Titulek §5 = 82 checkpointů", "## 5. Diagnostický filtr — 82 checkpointů" in doc)
# BOM
raw = open(DST, "rb").read()
chk("Bez BOM", not raw.startswith(b"\xef\xbb\xbf"))
print(
    f"\nSize: {len(raw)} B | Lines: {doc.count(chr(10)) + 1} | Reduction vs v1: {(1 - len(raw) / 181966) * 100:.1f} %"
)
sys.exit(0 if ok else 1)
