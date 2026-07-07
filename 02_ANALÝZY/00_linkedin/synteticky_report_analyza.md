# Syntetický report — Analýza LinkedIn tržních signálů (v2)

**Autor profilu:** Ondřej Soušek — Systems Integrator (industrial automation, formalizace, reverse engineering, CAM/CNC)
**Zpracováno:** 2026-07-07
**Vzorek:** 49 nabídek, Praha/CZ trh, červenec 2026 (2× oproti v1)

---

## 1. Přehledová statistika

| Metrika | Hodnota |
| --- | --- |
| Celkem nabídek | 49 |
| 🟢 SLEDOVAT (≥65 %) | 6 |
| 🟡 MEDIUM (50–64 %) | 27 |
| 🟡 HRANIČNÍ (40–49 %) | 12 |
| 🔴 NESLEDOVAT (<40 %) | 4 |
| Precision (relevantní / celkem) | 6/49 = 12.2% |
| Míra inženýrských rolí | 40/49 (82%) |
| Z toho falešný engineer | 0 |
| Strategičtí employeři | 10 |

---

## 2. Tech Stack Frequency Matrix (z 49 nabídek)

### CORE (≥4 výskyty)

```
  AI                        █████████████████████████████████████████████████ 49×
  Git                       ████████████████████████████████ 32×
  Python                    ████████████████████████ 24×
  C++                       ████████████████ 16×
  Azure                     ████████████ 12×
  CI/CD                     ███████████ 11×
  CAM                       ███████████ 11×
  Linux                     █████████ 9×
  IoT                       █████████ 9×
  AWS                       █████████ 9×
  PLC                       ████████ 8×
  LLM                       ████████ 8×
  scripting                 ██████ 6×
  machine learning          ██████ 6×
  GCP                       █████ 5×
  Kubernetes                ████ 4×
  data pipeline             ████ 4×
  Docker                    ████ 4×
  agentic                   ████ 4×
```

### SECONDARY (3 výskyty)

```
  CNC                       ███ 3×
  REST API                  ███ 3×
  Terraform                 ███ 3×
  ETL                       ███ 3×
  TypeScript                ███ 3×
```

### TERCIÁRNÍ (2 výskyty)

```
  DevSecOps                 ██ 2×
  middleware                ██ 2×
  test automation           ██ 2×
  MCP                       ██ 2×
```

### EDGE (1 výskyt)

`C#, ESP32, JavaScript, KVM, Playwright, deployment automation, virtualization`

### Signal-to-Noise Ratio (technologie s ≥2 výskyty)

| Technologie | Výskyt | Z toho SLEDOVAT | SNR |
| --- | --- | --- | --- |
| IoT | 9 | 5 | 56% |
| scripting | 6 | 3 | 50% |
| middleware | 2 | 1 | 50% |
| test automation | 2 | 1 | 50% |
| CAM | 11 | 4 | 36% |
| ETL | 3 | 1 | 33% |
| PLC | 8 | 2 | 25% |
| Kubernetes | 4 | 1 | 25% |
| agentic | 4 | 1 | 25% |
| Linux | 9 | 2 | 22% |
| C++ | 16 | 3 | 19% |
| Git | 32 | 5 | 16% |
| Python | 24 | 3 | 12% |
| AI | 49 | 6 | 12% |
| CI/CD | 11 | 1 | 9% |
| Azure | 12 | 1 | 8% |
| DevSecOps | 2 | 0 | 0% |
| LLM | 8 | 0 | 0% |
| machine learning | 6 | 0 | 0% |
| GCP | 5 | 0 | 0% |
| data pipeline | 4 | 0 | 0% |
| AWS | 9 | 0 | 0% |
| CNC | 3 | 0 | 0% |
| REST API | 3 | 0 | 0% |
| Docker | 4 | 0 | 0% |
| MCP | 2 | 0 | 0% |
| Terraform | 3 | 0 | 0% |
| TypeScript | 3 | 0 | 0% |

---

## 3. Doménová distribuce

| Doména | Počet | Podíl |
| --- | --- | --- |
| Industrial_automation | 25 | 51% |
| Enterprise_it | 12 | 24% |
| Ai_ml | 6 | 12% |
| Other | 5 | 10% |
| Automotive | 1 | 2% |

---

## 4. Mismatch dimenze (kritické gapy)

| Dimenze | Počet výskytů | Podíl |
| --- | --- | --- |
| growth | 42 | 86% |
| formal | 32 | 65% |
| tech | 20 | 41% |
| location | 14 | 29% |
| domain | 9 | 18% |

---

## 5. LinkedIn Algorithm Performance

| Metrika | Hodnota | Poznámka |
| --- | --- | --- |
| Precision | 12.2% | 6/49 relevantních |
| Noise (mimo doménu) | 47% | Enterprise IT + AI/ML + other |
| Falešný engineer rate | 0/40 | Titul Engineer ale náplň support/sales |
| Strategický employer rate | 20% | Siemens, ABB, Thermo Fisher, ... |

---

## 6. Inferované klastry a patterny

### Klastr 1: Industrial Automation Core (sweet spot)

Python + PLC + CAM + IoT + CI/CD → nejvyšší EROI scory
Top score: #003 Thermo Fisher 76.5%, #013 Siemens 67.6%, #015 Siemens 65.9%, #031 Renesas 65.5%
Tento klastr tvoří jádro autorovy konkurenční výhody.

### Klastr 2: AI/ML Hype (noise)

AI Engineer, ML Developer, Data Science — 6 nabídek, vesměs MEDIUM až NESLEDOVAT
LinkedIn testuje AI zájem napříč všemi profily. Ignorovat jako false signal.

### Klastr 3: Enterprise IT (mimo focus)

Solution Architect, SW Developer, DevOps — 12 nabídek
Většina v MEDIUM/HRANICNÍ pásmu. Nízký crossover do industrial automation.

### Klastr 4: Embedded & Manufacturing (adjacent)

Embedded SW Engineer, FW vývojář, Zkušební technik — role blízké industrial automation
Vyšší fit než enterprise IT, ale nižší než čistě industrial role.

---

## 7. Skill Gaps & CV Optimization

### Nejčastější no-match (gaps)

- **C++**: 16× — nejčastější chybějící skill
- **Azure**: 12× — nejčastější chybějící skill
- **AWS**: 9× — nejčastější chybějící skill
- **PLC**: 8× — nejčastější chybějící skill
- **Kubernetes**: 4× — nejčastější chybějící skill
- **Terraform**: 3× — nejčastější chybějící skill
- **TypeScript**: 3× — nejčastější chybějící skill
- **KVM**: 1× — nejčastější chybějící skill
- **C#**: 1× — nejčastější chybějící skill
- **JavaScript**: 1× — nejčastější chybějící skill

### Nejčastější direct match (autorovy silné stránky)

- **Git**: 32× — tržně potvrzená kompetence
- **Python**: 24× — tržně potvrzená kompetence
- **CI/CD**: 11× — tržně potvrzená kompetence
- **CAM**: 11× — tržně potvrzená kompetence
- **Linux**: 9× — tržně potvrzená kompetence
- **IoT**: 9× — tržně potvrzená kompetence
- **scripting**: 6× — tržně potvrzená kompetence
- **GCP**: 5× — tržně potvrzená kompetence
- **data pipeline**: 4× — tržně potvrzená kompetence
- **Docker**: 4× — tržně potvrzená kompetence

---

## 8. Závěr a doporučení

Ze 49 analyzovaných nabídek: **6 SLEDOVAT** (12% precision), **27 MEDIUM**, **12 HRANIČNÍ**, **4 NESLEDOVAT**.

Industrial automation + Python/CAM/IoT zůstává nejsilnější kombinací.
Strategičtí employeři (Siemens, ABB, Thermo Fisher, Renesas, Schneider Electric) tvoří jádro follow leadů.
AI/ML role jsou konzistentní noise — nenechat se rozptýlit.

### Doporučené akce

- 🔴 Aplikovat na #003 Thermo Fisher (System Integration Engineer, 76.5%)
- 🔴 Aplikovat na #013 Siemens (Technical Test Engineer, 67.6%)
- 🔴 Aplikovat na #015 Siemens (Embedded tools, 65.9%)
- 🔴 Aplikovat na #019 Siemens (RAM/LCC Engineer, 69.4%)
- 🔴 Aplikovat na #031 Renesas (Digital Design Engineer, 65.5%)
- 🔴 Aplikovat na #001 Desoutter (Light Automation Specialist, 65.7%)
- 🟡 Sledovat #046 Adamantem/DevOps for Embedded (59.7%) — nový pattern DevOps+embedded
- 🟡 Sledovat #044 La Fosse/Robotics Engineer (57.4%) — industrial robotics crossover
- 🟡 Sledovat #043 Adamantem/Embedded SW (56.2%) —embedded je adjacent k industrial
- 📊 LinkedIn precision klesla z 21 % (v1, 24 nabídek) na 12 % (v2, 49 nabídek). Hlavní problém: Skills sekce (pouze 5 položek).
- 📊 Přidat TypeScript/Playwright (objevuje se v no_match) — gap pro industrial cloud testing role.

---

*Report generován: 2026-07-07*
*Vstupní data: metadata_stacku.json (49 entries)*
*Metodika: EROI scoring (6 dimenzí) + frequency analysis + confusion matrix*
