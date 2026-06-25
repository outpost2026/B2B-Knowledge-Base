# ONDŘEJ SOUŠEK

### Formalizace tacitního know-how → deterministické systémy pro výrobu

Praha | +420 735 045 256 | ✉️ [sousek@systeq.cz](mailto:sousek@systeq.cz) | 🔗 github.com/outpost2026 | 🌐 systeq.cz

## CO ŘEŠÍM

Výrobní firmy ztrácejí know-how, když odchází klíčový člověk, a zůstávají závislé na proprietárních formátech bez dokumentace. Beru tuhle entropii a převádím ji na **deterministické, přenositelné systémy** — parsery, pipeline, datové modely — které fungují bez ohledu na to, kdo je u stroje.

14 let jsem byl ten člověk u stroje (CNC, off-grid stavby). Teď stejnou doménovou znalost používám k tomu, abych firmy té závislosti zbavil.

## DŮKAZ: VCF/DXF Parser Engine — 2026

**Vstup:** B2B výrobní klient (CNC, 200+ zakázek/měsíc) závislý na proprietárním binárním formátu .VCF (Ruida/VCutWorks) bez veřejné specifikace a SDK — a na tacitním know-how odcházejícího technika.

**Proces:** Reverzní inženýrství binární struktury (hex analýza, IEEE 754) ve 22 iteracích, souběžně se zdokumentováním provozního know-how.

**Výsledek:**

- ✅ Přesnost extrakce dráhy **\>99,98 %** (cross-validace proti LightBurn, odchylka \<0,02 %)

- ✅ Golden master regrese **10/10 PASS**, determinism testy **2/2 PASS**

- ✅ Nasazeno na **GCP Cloud Run** (Docker, Artifact Registry) + Streamlit dashboard + Flask REST API pro ERP

- ✅ Predikce strojového času a klasifikace komplexity zakázky přímo z CAM dat

**Hodnota pro klienta:** Nezávislost na jednotlivci, přenositelné firemní aktivum, automatizovaný vstup do plánování výroby.

🔗 Live demo: vcf-parser-demo-537446704644.europe-west1.run.app

## CO PŘINÁŠÍM B2B KLIENTŮM

| Oblast | Konkrétně |
| - | - |
| **Reverzní inženýrství** | Binární a proprietární formáty bez specifikace/SDK (hex, IEEE 754, pair-diff diagnostika) |
| **Formalizace know-how** | Tacitní provozní rozhodování → strukturovaná dokumentace a pravidla |
| **Deterministické pipeline** | CAD/CAM → JSON/ERP-ready výstupy, bez halucinací, s golden master testy |
| **Cloud nasazení** | GCP Cloud Run, Docker, Artifact Registry, Streamlit, Flask REST API |
| **CAM/CNC doména** | G-kód, NCstudio 10, VCutWorks, LightBurn, DXF processing |


## PRO KOHO TO DÁVÁ SMYSL

Výrobní a CAM/CNC firmy, které mají:

- proprietární formát nebo software bez API/SDK,

- know-how vázané na 1–2 lidi,

- ruční vstup dat do ERP/plánování, který by šel automatizovat.

**Dostupný ihned** | Konzultace, audit proveditelnosti, pilotní projekt nebo dlouhodobá spolupráce | Praha + remote

