import sys

sys.path.insert(0, r"C:\Users\PC\Documents\Repozitar_Dev\_github\B2B-Knowledge-Base")
BASE = r"C:\Users\PC\Documents\Repozitar_Dev\_github\B2B-Knowledge-Base"
SRC = BASE + r"\04_KNOWLEDGE_BASE\01_MCP\MCP_GROUND_TRUTH_postmortem_agregovany_v2.md"
OUT = BASE + r"\TEMP_TRIMMING\gt_v2_parts"

with open(SRC, encoding="utf-8") as f:
    lines = f.read().splitlines()


def seg(a, b):  # 1-indexed inclusive
    return "\n".join(lines[a - 1 : b]) + "\n"


# --- sanity assertions ---
assert (
    lines[1810].startswith("## 4. Prurezova") or "Průřezová pravidla" in lines[1810]
), f"line 1811 mismatch: {lines[1810][:80]}"
assert "Diagnostický filtr" in lines[2103], f"line 2104 mismatch: {lines[2103][:80]}"
assert lines[2236].startswith("## 6."), f"line 2237 mismatch: {lines[2236][:80]}"
assert lines[2282].startswith("## 7."), f"line 2283 mismatch: {lines[2282][:80]}"

s4 = seg(1811, 2101).replace(
    "## 4. Průřezová pravidla P1-P83 + P-GCP-01..05 (konsolidovaná)",
    "## 4. Průřezová pravidla P1–P96 + P-GCP-01..05 (kanon; P84–P89 rezervovány epistemické řadě)",
)
s5 = seg(2104, 2234).replace(
    "## 5. Diagnostický filtr — 77 checkpoints",
    "## 5. Diagnostický filtr — 82 checkpointů",
)
s6 = seg(2237, 2280)
s7 = seg(2283, 2354)

for name, txt in [
    ("10_s4_rules.md", s4),
    ("12_s5_filter.md", s5),
    ("13_s6_eroi.md", s6),
    ("14_s7_checklist.md", s7),
]:
    with open(f"{OUT}\\{name}", "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(f"{name}: {len(txt)} chars")

print("titles patched:", "P1–P96" in s4, "82 checkpointů" in s5)
