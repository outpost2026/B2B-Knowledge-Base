# OUTPOST ELEKTRO INFRASTRUKTURA — živý kanon EL layeru objektu

**Datum:** 2026-09-24 | **Autor:** outpost2026
**Účel:** Trvalý (nedatovaný) kanon elektrické infrastruktury objektu Outpost 2026 — topologie EL layeru, registr složitějších elektrozařízení, jejich zdraví/incidenty a monitoring; doplněk k datovanému GT stavu (EL02).
**Status:** **živý kanon** — aktualizace průběžně při změně HW/provozu; nepodléhá P4 archivaci datového snapshotu.
**Provenance:** source-read (`IOT/report_incident_POW-HVM3.2H-24V_2026-07-25.md` v2.1, `IOT/.ai_state.json`, `outpost_security_perimeter/docs/poc_build_guide_v1.md`, GT EL02 v1.9, INDEX) + synthéza 2026-09-24
**Tagy KB:** elektro, infrastruktura, menic, POW-HVM, fault02, monitoring, offgrid, outpost, ground-truth

---

## 0. Rozsah a vztah k ostatním EL artefaktům

| Artefakt | Role | Vztah |
|---|---|---|
| **Tento soubor (EL03)** | Živý kanon **EL layeru celého objektu** — co je připojeno, zdraví, incidenty, monitoring | Master pro doménovou znalost zařízení |
| `OUTPOST_ELEKTRO_GT_stav_YYYY-MM-DD.md` (EL02) | Datovaný snapshot **stavu před revizí** (gapy, inventura, meritka, spatial) | GT odkazuje sem pro §2.3; sem patří jen odkaz zpět na aktuální GT generaci |
| `KVALIFIKACE_ELEKTRO_AGREGACE_*.md` (EL01) | Kvalifikační gap (vyhl. 50) | Mimo rozsah tohoto kanonu |
| `IOT/report_incident_*.md` | Plný incident report (mimo KB) | Shrnuje se zde; neklikuje se do kopie obsahu (P1) |

**Proč samostatný kanon (LLM eval 2026-09-24):** EL02 je datovaný snapshot → při další revizi se archivuje (P4). Zdraví měniče, registr zařízení a monitoring jsou **trvalá** znalost EL layeru — nesmí zmizet se snapshotem. Neduplikujeme topologické detaily GT (odkaz místo obsahu, P1).

---

## 1. Topologie EL layeru (shrnutí — detail v EL02 §2)

```
[FV String 1 — střecha M2, 2P2S ~1900 Wp]
        │ ~4 m 2×2,5 (G12: CYLY, před výměnou za solar)
        ▼
   [SPB1-63Z C32] ── jediný zapojený DC jistič FVE
        │ ~4 m 2×4 Cu
        ▼
┌───────────────────────────────────────────────┐
│  POW-HVM3.2H-24V-N  3200 W  ★ SRDCE EL       │  ← FAULT 02 viz §3
│  bulk 28,8 / float 27,2 / UVP 22,0 / max 80 A│
└───────────┬───────────────────┬───────────────┘
            │ DC 8 mm² (G10)    │ AC OUT (prohozené L/N — G14 OK)
            ▼                   ▼
   [JK BMS PB2A16S20P]   [PL7C16 → SV DIN → 1 zásuvka]
   200 A / 2 A bal.       (bez RCBO — G13; provizorní ≤1600 W)
            │
            ▼
   [LFP 8S2P 630 Ah / 15,12 kWh]
```

- **Jediná AC cesta budovy** = tento měnič (žádná DS/VTZ — ostrovní uzel).
- String 2 + Epever XTRA4210N: **mimo provoz** (historický MPPT, poškozená svorkovnice).
- Kompletní gapy G1–G15, inventura jističů, spatial: **v EL02**.

---

## 2. Registr složitějších elektrozařízení

| ID | Zařízení | Model | Role v EL layeru | Stav (2026-09-24) |
|---|---|---|---|---|
| **EL-DEV-01** | **Hybridní měnič** | POW-HVM3.2H-24V-N, 3200 W | **Srdce** — DC→AC, nabíjení z FV, UVP/bulk/float | **PROVOZNĚ RIZIKOVÝ** — viz §3 (FAULT 02 history, open T01/T02) |
| EL-DEV-02 | MPPT (aktivní) | — (v cestě String 1 přes měnič) | Část řetězce String 1 | Provoz dle GT §2.1 |
| EL-DEV-02b | MPPT (záložní) | Epever XTRA4210N | Historický String 2 | **MIMO PROVOZ** — svorkovnice, 27,6 V strop |
| EL-DEV-03 | BMS | JK-PB2A16S20P V19, 200 A | Master ochrana packu | Zapojena, balancer OK |
| EL-DEV-04 | Hlavní baterie | LiFePO4 8S2P 630 Ah, 15,12 kWh | Akumulace | Provoz; U≈26,78 V (2026-09-23) |
| EL-DEV-05 | Záložní baterie | GoKWh 100 Ah 24 V | Rezerva | **Odpojena, nedobita** (23,9 V) |
| EL-DEV-06 | IoT monitoring | D1 mini + DS18B20 + MAX3232/ESP32 | Telemetrie měniče/BMS | HW skladem; T02/T03 ve stavu PoC (viz §5) |
| EL-DEV-07 | Jističe/ochrany | SPB1 C32, PL7C16, PL7B32, B25, Ex9FP, MEGAFUSE | DC/AC ochrana | Viz EL02 §3 — většina nezapojena; **RCBO chybí** |

---

## 3. Zdraví měniče EL-DEV-01 — FAULT 02 (živý záznam)

### 3.1 Incident 2026-07-25 (uzavřený zásah, diagnóza otevřená)

- **Spouštěč:** vadná konvice ~2 kW × ~7 dní → opakované fault cykly → tepelný šok H-bridge.
- **Stav po čištění:** FAULT 02 (**over temperature / NTC**) konzistentně za **10–13 min** při 50–250 W — nezávisle na zátěži.
- **Revidovaná hypotéza v2.1 (high conf):** Rds(on) degradace MOSFETů + pasivní chlazení (ventilátor load-based **>600 W**); NTC kontakt pravděpodobně degradovaný.
- **Vyloučeno jako jediná příčina:** prach (vyčištěno), vadný NTC jako sole cause.

### 3.2 Otevřená verifikace (blokuje finální verdikt)

| ID | Test | Rozhodovací kritérium | Priorita |
|---|---|---|---|
| T01 | NTC odpor multimetrem (pokojová) | ~10 kΩ OK / OL = vadný | critical |
| T02 | DS18B20 na heatsinku v momentě faultu | **>90 °C → Rds(on) potvrzeno**; **<60 °C → vadný NTC** | **critical — CRITICAL v PoC guide** |
| T06 | Repaste H-bridge heatsinku | až po otevření (závisí T01) | po T01 |

### 3.3 Provozní opatření do verifikace

1. **Omezit dlouhodobou zátěž <600 W bez monitoringu teploty** — ventilátor neběží, riziko FAULT 02 za ~10–13 min.
2. Těžké starty (hoblovka, pila) = **jednorázově**, sledovat FAULT; preferovat zátěže >600 W kde ventilátor běží.
3. **T02 DS18B20 = nejvyšší priorita** před zimním provozem (práh 55/65/75 °C dle PoC firmware).
4. Náhradní NTC 10 kΩ (T04) — až po T01; nemusí fixnout root cause.
5. Reg. Modbus **5006** (auto restart při over-temp) a **4530** (error code) — cíl T03 telemetrie.

### 3.4 Cross-reference

| Zdroj | Cesta / ID |
|---|---|
| Plný incident report | `Repozitar_Dev/IOT/report_incident_POW-HVM3.2H-24V_2026-07-25.md` (v2.1) |
| Session state / tasky | `Repozitar_Dev/IOT/.ai_state.json` (T01–T07) |
| PoC build guide (T02 firmware) | `_github/outpost_security_perimeter/docs/poc_build_guide_v1.md` §Varianta 1 |
| Modbus map (fault regs) | `IOT/Stridac_POW-HVM3.2H-24V/registers-map.md` (4530, 5006, 5010) |
| OEM definice FAULT 02 | HVM11KP manual (přes report §10) |
| GT topologie + gapy | EL02 `OUTPOST_ELEKTRO_GT_stav_2026-09-23.md` §2.3 (krátký) |

---

## 4. Monitoring EL layeru (plán — živý)

| Úloha | MVP | Stav |
|---|---|---|
| T02 Thermal Sentinel | DS18B20 → heatsink, seriál 1 s, prahy 55/65/75 | **CRITICAL, HW skladem, firmware v PoC guide** |
| T03 GridWatch | MAX3232 + ESP32, Modbus **2400 baud**, reg. 4502–4557 | HIGH; čeká RJ45/kabel |
| T05 JK BMS | JST PH TTL | LOW; čeká kabel |
| T07 Dashboard | ESP32 → GCP → Telegram fault notify | future; závisí T02+T03+T05 |
| T01/T04 | Multimetr NTC + náhradní díl | critical / medium |

Detail schémat, kódů a inventáře HW: **PoC build guide** (externí repo — nekopírovat sem).

---

## 5. Otevřená rizika EL layeru do zimy (vstup z EL02 + §3)

| # | Riziko | EL vazba |
|---|---|---|
| R1 | **FAULT 02 při delší zátěži/nabíjení** — měnič = jediný AC zdroj | §3; blokuje plný zimní provoz bez T02 |
| R2 | **Bez RCBO (G13)** — ochrana osob | EL02 G13; provizorní AC ≤1600 W |
| R3 | **Otevřené terminály / holé dřevo (G9/G15)** | EL02; kryt + IP box |
| R4 | Trunk 8 mm² vs 80–200 A (G10) | EL02; přepočet / MEGAFUSE |
| R5 | GoKWh mimo bilanci (G8) | EL02 §2.1 |
| R6 | Bez telemetrie měniče (G6/DEBT) | §4 T03 |

---

## 6. Revize dokumentu

| Datum | Změna | Autor |
|---|---|---|
| 2026-09-24 | **V1.0 — vznik živého kanonu EL layeru**: eval oddělení od datovaného GT (P1/P4), topologie shrnutí, registr EL-DEV-01..07, FAULT 02 §3 (incident + T01/T02 + opatření), monitoring §4, rizika §5; GT EL02 bump V1.9 §2.3 krizový tahák | outpost2026 + agent |

---

*Poznámka RAG: Živý kanon — nemazat, nearchivovat datem; při změně HW/provozu update v místě (P1: žádné kopie `_v2`). Dated snapshot stavu = vždy jen EL02 `..._GT_stav_YYYY-MM-DD.md`. Práh FAULT: >90 °C / <60 °C = rozhodovací strom T02.*
