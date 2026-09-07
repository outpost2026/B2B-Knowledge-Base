# Azure Migration Plan — Multi-projekt migrace z GCP na Azure free tier

**Datum:** 2026-08-25 | **Autor:** outpost2026
**Účel:** Centrální migrační plán pro celé portfolio — GCP free tier vyčerpán, Azure free tier jako náhrada
**Klasifikace:** Interní, provozní dokument
**Provenance:** source-read (azure_free_tier_edukace.md, deploy.bicep, pitevni_kniha_v8, SKILL_GAPS_ROZBOR_Q3_2026_v2)
**Navaznost:** SKILL_GAPS_ROZBOR_Q3_2026_v2 §❹, eroi_chronologicky_plan §❹, azure-mcpjobs temp balíček

---

## 1. Motivace

| Faktor | GCP (současnost) | Azure (cíl) |
|--------|------------------|-------------|
| **Free tier** | Vyčerpán (stovky Kč/měsíc) | 12 měsíců $0 (B1ms PG + B1s VM + 750h každý) |
| **Náklady** | e2-small VM 3×/den + hourly cron = ~500-800 Kč/měsíc | $0 (free tier) |
| **GCP chyby** | VM shutdown selhalo (67 postmortemů v pitevní knize) | Bicep IaC = deklarativní, bez manuálního shutdown |
| **Multi-projekt** | Každá služba = vlastní billing | 1 subscription = všechno |

### GCP shutdown postmortems (z `GCP/pitevni_kniha_v8`)

Klíčové fatální chyby, které pálily kredit:
1. `os.system("sudo shutdown -h now")` bez `import os` — VM nikdy nevypnulo
2. SSH hanging místo shutdownu
3. Cron nenajde `shutdown` kvůli `$PATH` — fix: `/sbin/shutdown`
4. Chybějící `@reboot` cron — VM startlá a běží idle
5. BigQuery API zapnuté bez workloadu = surprise-billing

**Závěr:** GCP vyžaduje příliš mnoho manuální hygiene. Azure free tier = Bicep IaC + 1 VM s docker-compose = žádné shutdown drama.

---

## 2. Multi-projekt Azure architektura

### 2.1 Cílový stav (1 subscription, $0/měsíc)

```
Azure Subscription ($200 kredit → pak free tier 12M)
│
├── Resource Group: rg-mcpjobs-prod (West Europe)
│
├── PostgreSQL Flexible Server B1ms (750h/měs free)
│   ├── Database: mcpjobs (187 ads, ~5 MB)
│   └── Database: vcf-parser (pokud bude potřeba)
│
├── VM B1s (750h/měs free, Ubuntu 24.04)
│   └── Docker Compose multi-app
│       ├── mcpjobs-dashboard (:8501) — Streamlit
│       ├── vcf-parser-demo (:8080) — Streamlit (Moodpasta B2B demo)
│       └── nginx (:80/443) — reverse proxy
│
├── Azure Functions (consumption, free forever)
│   └── meteo-hourly (timer trigger, 1M exec/měs free)
│
├── Blob Storage (5 GB free forever)
│   └── meteo-outputs/ (výstupy z meteo mineru)
│
└── NSG (Network Security Group)
    ├── AllowSSH (22) — tva IP
    ├── AllowHTTP (80) — Let's Encrypt
    ├── AllowHTTPS (443) — HTTPS
    └── AllowStreamlit (8501) — docasne
```

### 2.2 Free tier limity

| Sluzba | SKU | Limit free | Cena po limitu |
|--------|-----|------------|----------------|
| PostgreSQL | B1ms (1 vCore, 2 GB RAM) | 750h/měs, 32 GB storage | ~$12/měs |
| VM | B1s (1 vCPU, 1 GB RAM) | 750h/měs, 30 GB disk | ~$7.5/měs |
| Functions | Consumption | 1M req/měs, 400k GB-s | ~$0.20/1M |
| Container Apps | Consumption | 180k vCPU-s/měs free navždy | ~$0.000024/vCPU-s |
| Blob Storage | LRS | 5 GB navždy, 20k read/20k write | ~$0.02/GB |
| **Celkem** |  |  | **$0/měs (free tier)** |

### 2.3 Co se nesmí stát

- **Dva VM na free tier** — 750h = 1 VM 24/7. Druhá = platíš.
- **Dva PG servery** — 750h = 1 server. Druhý = platíš.
- **Zapomenuté GCP služby** — BigQuery API, Compute Engine zůstaly zapnuté → surprise billing.
- **VM bez docker-compose** — každý projekt zvlášť = port conflicts + duplicated resources.

---

## 3. Migrační kroky

### Fáze 0: Zastavení GCP (URGENTNÍ, 15 min)

```
1. Cloud Scheduler → PAUSE všechny jobs:
   - Jobs_Praha_mining (VM start 3×/den)
   - pipeline-meteo-hourly (720 invokací/měsíc)
   - cron-notebooky* (scraping crony)
   - material-tezba-cron (už paused, overit)

2. Artifact Registry → delete images (deregistrovat)

3. Compute Engine → STOP instance (ne delete — pro jistotu)

4. Overeni: az billing account list (nebo gcloud billing accounts list)
```

### Fáze 1: Infrastruktura (1-2 h)

```
1. Azure CLI: winget install Microsoft.AzureCLI
2. az login
3. Ziskej SSH klic + verejnou IP
4. Deploy: bash azure/deploy.sh --ssh-key "..." --client-ip "IP"
5. Vystup: VM_IP, PostgreSQL heslo, connection string
```

**Temp balíček:** `C:\Users\PC\AppData\Local\Temp\opencode\azure-mcpjobs\`

### Fáze 2: MCP-Jobs (30 min)

```
1. SSH na VM: ssh azureuser@VM_IP
2. Docker + app: bash azure/vm-setup.sh
3. Kopie zdrojaku z PC na VM
4. Sync dat: python scripts/sync_to_cloud.py --cloud-url $CLOUD_URL --init-schema
5. Overeni: curl http://VM_IP:8501/_stcore/health
```

### Fáze 3: VCF parser demo (20 min)

```
1. Kopie src/, dashboard.py, data/schema.sql na VM
2. Uprava: hardcoded heslo (moodpasta-demo-2026) → secret
3. Docker compose: 2. kontejner na stejne VM (:8080)
4. Overeni: curl http://VM_IP:8080/_stcore/health
```

### Fáze 4: Meteo cron (20 min)

```
1. Preneseni na Azure Functions timer trigger (1M exec/mesic free)
2. Vystup: Blob Storage misto GCS
3. Vypnuti GCP hourly scheduleru
```

### Fáze 5: Verifikace (10 min)

```
1. Healthcheck vsech sluzeb
2. Overeni $0 na Azure Cost Management
3. Budget alert na $0
4. DNS (volitelne): jobs.systeq.cz → VM_IP
```

---

## 4. Seznam repozitářů ovlivněných migrací

| Repo | Typ | Azure služba | Stav |
|------|-----|--------------|------|
| **MCP-Jobs** | Web dashboard + DB | VM + PostgreSQL | 🟡 Připraveno (temp balíček) |
| **vcf_parser_b2b** | B2B demo (Moodpasta) | VM (kontejner) | 🟡 Připraveno (deploy.ps1 existuje) |
| **Meteo_scraper_SQL** | Cron job | Functions timer | ⏳ Po deployi MCP-Jobs |
| **GCP** (PrahaScrapersV1) | Meta-repo | — | 🔴 Pauzovat schedulery |
| **linkedin-mcp-custom** | GH Actions cron | — | ✅ Bezměnné (GH Actions = zdarma) |
| **scrapers** | Batch pipeline | Volitelné | ⏳ Později (Nyx headed-login friction) |

---

## 5. Rizika a mitigace

| Riziko | Dopad | Mitigace |
|--------|-------|----------|
| Azure free tier konec (12M) | ~$21/měs | Přejít na Supabase/Neon (free navždy) nebo platit |
| VM selže (hardware) | Down time | Azure SLA 99.9% (Burstable tier), restart |
| PostgreSQL selže | Ztráta dat | Backup 7 dní (free tier), geo-redundant = platí |
| Hardcoded heslo (vcf_parser) | Bezpečnostní riziko | Přesun do Docker secrets / Azure Key Vault |
| Funkční GCP služby stále běží | Překvapivý billing | Pauznout VŠECHNY schedulery, overit billing |

---

## 6. Cesta dále

```
Azure migrace (tento dokument)
  ↓
AZ-900 certifikace (10-15 hod, Microsoft Learn)
  ↓
Azure Functions pro meteo cron
  ↓
Container Apps pro scale-to-zero (pokud 1 VM nestací)
  ↓
Dalsi Azure: Key Vault (secrets), DevOps (CI/CD deploy), Monitor (logging)
```

---

*Soubor je živý. Aktualizace po každém fázi migrace.*
