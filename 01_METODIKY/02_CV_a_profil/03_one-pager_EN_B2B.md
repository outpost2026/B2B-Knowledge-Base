# ONDŘEJ SOUŠEK (Ondrej Sousek)
### Formalizing Tacit Manufacturing Know-How into Deterministic Systems

📍 Prague, Czech Republic | 📞 +420 735 045 256 | ✉️ sousek@systeq.cz | 🔗 github.com/outpost2026 | 🌐 systeq.cz

---

## THE PROBLEM I SOLVE

Manufacturing companies lose critical know-how when a key employee leaves, and stay locked into proprietary formats with no documentation. I take that entropy and convert it into **deterministic, transferable systems** — parsers, pipelines, data models — that work regardless of who's at the machine.

For 14 years, I was that person at the machine (CNC, off-grid construction). Now I use the same domain expertise to free companies from that dependency.

---

## PROOF: VCF/DXF Parser Engine — 2026

**Input:** B2B manufacturing client (CNC processing, 500+ orders/month) locked into a proprietary binary format, .VCF (Ruida/VCutWorks), with no public spec or SDK — and dependent on the tacit know-how of a departing technician.

**Process:** Binary structure reverse-engineered (hex analysis, IEEE 754) across 22 iterations, in parallel with systematic documentation of operational know-how.

**Result:**
- ✅ Toolpath extraction accuracy **>99.98%** (cross-validated against LightBurn, <0.02% deviation)
- ✅ Golden master regression **10/10 PASS**, determinism tests **2/2 PASS**
- ✅ Deployed on **GCP Cloud Run** (Docker, Artifact Registry) + Streamlit dashboard + Flask REST API for ERP
- ✅ Machine-time prediction and order-complexity classification computed directly from CAM data

**Value delivered:** Independence from a single individual, a transferable company asset, automated data input for production planning.

🔗 Live demo: vcf-parser-demo-537446704644.europe-west1.run.app

---

## WHAT I BRING TO B2B CLIENTS

| Area | Specifics |
|---|---|
| **Reverse Engineering** | Binary & proprietary formats with no spec/SDK (hex analysis, IEEE 754, pair-diff diagnostics) |
| **Know-How Formalization** | Tacit operational decision-making → structured documentation and rules |
| **Deterministic Pipelines** | CAD/CAM → JSON/ERP-ready output, zero hallucination, golden master tested |
| **Cloud Deployment** | GCP Cloud Run, Docker, Artifact Registry, Streamlit, Flask REST API |
| **CAM/CNC Domain** | G-code, NCstudio 10, VCutWorks, LightBurn, DXF processing |

---

## WHO THIS IS FOR

Manufacturing and CAM/CNC companies with:
- a proprietary format or software with no API/SDK,
- know-how concentrated in 1–2 people,
- manual ERP/planning data entry that could be automated.

---

**Available now** | Consulting, feasibility audit, pilot project, or long-term collaboration | Prague + remote
