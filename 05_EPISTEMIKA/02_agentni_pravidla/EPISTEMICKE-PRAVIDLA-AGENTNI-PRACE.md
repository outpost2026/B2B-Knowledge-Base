# Epistemická pravidla pro agentní vývojovou práci

> **Platnost:** Od 17.06.2026
> **Autor:** PC / vývojové prostředí Windows 11 Pro
> **Kontext:** Práce s agentními LLM (opencode, DeepSeek V4, Gemini CLI, Codex)
> **Důvod vzniku:** Incident z 16.06.2026 – agent smazal systémové soubory při "trimming" úkolu

---

## Shrnutí incidentu (pro kontext)

Při práci s agentním systémem (DeepSeek V4 Flash, Build mód) došlo ke zničení nainstalovaných programů a profilů prohlížečů. Agent dostal úkol přesunout trackované repozitáře a "trimmout" netrackovaný vývojový adresář. Během přesunu souborů přes temp adresáře agent pravděpodobně spustil destruktivní příkazy (`Remove-Item -Recurse`, `rm -rf`) na cestách zahrnujících i systémové složky. Výsledek: smazané programy, prázdné ikony v liště, prohlížeče jako po čisté instalaci.

**Příčina:** Agent nemá skutečné porozumění rozsahu svých akcí, nemá guardrail pro destruktivní operace a neověřuje výsledky svých příkazů.

---

## 1. Souborový systém – absolutní hranice

### 1.1 Zakázané cesty (nikdy, za žádných okolností)

Agent **nesmí** číst, modifikovat, přesouvat ani mazat soubory v těchto adresářích:

```
C:\Program Files\
C:\Program Files (x86)\
C:\Users\PC\AppData\Local\
C:\Users\PC\AppData\Roaming\
C:\Users\PC\AppData\LocalLow\
C:\Windows\
C:\ProgramData\
C:\Recovery\
C:\$Recycle.Bin\
C:\System Volume Information\
```

### 1.2 Povolené cesty (jen v rámci projektu)

Agent smí pracovat **výhradně** v těchto adresářích:

```
C:\Users\PC\Documents\Repozitar_Dev\_github\
C:\Users\PC\Desktop\  (jen pro installery a dočasné soubory)
```

### 1.3 Pravidlo chdir

Před jakoukoli operací agent **povinně** provede:

```powershell
# Ověř, že jsi v správném adresáři
Get-Location
# Pokud nejsi v projektu, NIKDY nepokračuj
```

Agent **nikdy** nepoužívá absolutní cesty mimo projekt. Pokud potřebuje pracovat s jiným adresářem, **musí** získat explicitní potvrzení uživatele.

---

## 2. Git – pravidla bezpečnosti

### 2.1 Před úkolem (povinný check-in)

```powershell
# 1. Zálohuj aktuální stav
git stash push -m "Pred agentnim ukolem: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

# 2. Nebo proveď commit
git add -A
git commit -m "checkpoint: pred agentnim ukolem"

# 3. Ověř, že je vše uloženo
git status
git log --oneline -3
```

### 2.2 Během úkolu

- Agent **nikdy** nepoužívá `git reset --hard` bez potvrzení
- Agent **nikdy** nepoužívá `git clean -fd` bez potvrzení
- Agent **nikdy** nemění historii (rebase, amend) bez potvrzení
- Před `git push` = vždy ověř `git diff` a `git log`

### 2.3 Po úkolu (povinný review)

```powershell
# Ověř, že nedošlo k nechtěným změnám
git status
git diff --stat
git log --oneline -5
```

---

## 3. Ochrana API klíčů

### 3.1 Pravidla pro API klíče

| Služba | Umístění klíče | Přístup agenta |
|--------|----------------|----------------|
| DeepSeek V4 | `.env` nebo env proměnná | **ZAKÁZÁN** |
| MiniMax M3 | `.env` nebo env proměnná | **ZAKÁZÁN** |
| Gemini | `.env` nebo env proměnná | **ZAKÁZÁN** |
| OpenCode config | `~/.config/opencode/` | **ZAKÁZÁN** |

### 3.2 Struktura .env souboru

```bash
# .env ( nikdy necommitovat! )
DEEPSEEK_API_KEY=sk-xxxxx
MINIMAX_API_KEY=xxxxx
GEMINI_API_KEY=xxxxx
```

### 3.3 .gitignore (povinný)

```gitignore
# API keys
.env
.env.local
.env.*.local

# Konfigurace s klíči
config/secrets.*
*.key
*.pem
```

### 3.4 Co agent nesmí

- Číst soubory `.env`, `.env.*`, `*.key`, `*.pem`
- Logovat, printovat nebo jinak zobrazovat API klíče
- Ukládat klíče do git historie, logů nebo dočasných souborů
- Předávat klíče v URL parametrech

---

## 4. Ověřování (read-after-write principle)

### 4.1 Zlaté pravidlo

**Po KAŽDÉ operaci, která mění souborový systém, agent OKAMŽITĚ ověří výsledek.**

### 4.2 Povinné ověřovací kroky

| Operace | Povinné ověření |
|---------|-----------------|
| `mkdir` | `Test-Path` nebo `ls` – adresář existuje? |
| `Move-Item` | `Test-Path` – soubor na novém místě? Staré místo prázdné? |
| `Remove-Item` | `Test-Path` – soubor NEEXISTUJE? |
| `Set-Content` | `Get-Content` – obsah sedí? |
| `git commit` | `git log --oneline -1` – commit je tam? |
| `git push` | `git status` – žádné unmatched commits? |

### 4.3 Vzor ověření

```powershell
# PŘED: Ověř, že zdroj existuje
Test-LiteralPath "zdrojovy_soubor.txt"

# PROVEĎ operaci
Move-Item -LiteralPath "zdrojovy_soubor.txt" -Destination "cilovy adresar\"

# PO: Ověř výsledek
Test-LiteralPath "zdrojovy_soubor.txt"           # mělo by být $false
Test-LiteralPath "cilovy adresar\soubor.txt"     # mělo by být $true
```

### 4.4 Při selhání

Pokud ověření selže, agent **OKAMŽITĚ přestane** a oznámí chybu. **Nikdy nepokračuje** v dalších krocích.

---

## 5. Destruktivní operace – zákaz a povolení

### 5.1 Absolutní zákaz (bez výjimky)

Tyto příkazy agent **nikdy** nesmí spustit:

```powershell
# PowerShell
Remove-Item -Recurse -Force C:\*
Remove-Item -Recurse -Force ~\
Remove-Item -Recurse -Force $env:USERPROFILE
Remove-Item -Recurse -Force "C:\Users\PC\AppData"
Remove-Item -Recurse -Force "C:\Program Files"

# Bash (pokud je dostupný)
rm -rf /
rm -rf ~
rm -rf /*
rm -rf ~/AppData
find / -delete
find ~ -delete
```

### 5.2 Povoleno jen s potvrzením

Tyto příkazy vyžadují **explicitní potvrzení uživatele** před provedením:

```powershell
# Mazání v rámci projektu
Remove-Item -Recurse -Force "C:\Users\PC\Documents\Repozitar_Dev\_github\*"

# Git operace
git reset --hard
git clean -fd
git branch -D

# Systémové operace
sfc /scannow
DISM /Online /Cleanup-Image
```

### 5.3 Bez potvrzení (jen v rámci projektu)

```powershell
# Čtení
Get-Content
Get-ChildItem
Select-String
git status
git log
git diff

# Zápis v rámci projektu
Set-Content (jen v projektu)
New-Item (jen v projektu)
git add
git commit
```

---

## 6. Práce s agentními nástroji

### 6.1 opencode – konfigurace

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "bash": {
      "git status": "allow",
      "git log*": "allow",
      "git diff*": "allow",
      "git stash*": "allow",
      "git add*": "ask",
      "git commit*": "ask",
      "git push*": "ask",
      "git reset*": "deny",
      "git clean*": "deny",
      "Remove-Item*": "ask",
      "rm *": "ask",
      "del *": "ask",
      "*": "ask"
    },
    "external_directory": {
      "C:\\Users\\PC\\Documents\\Repozitar_Dev\\_github\\**": "allow",
      "C:\\Users\\PC\\AppData\\**": "deny",
      "C:\\Program Files\\**": "deny",
      "C:\\Windows\\**": "deny",
      "*": "deny"
    }
  }
}
```

### 6.2 Build mód – pravidla

- Build mód = agent může spouštět příkazy, ale **nesmí měnit soubory mimo projekt**
- Pokud agent potřebuje editovat soubor mimo projekt, **musí** získat potvrzení
- Žádné `--dangerously-skip-permissions`

### 6.3 PreToolUse hook (doporučení)

```bash
#!/bin/bash
# ~/.opencode/hooks/destructive-guard.sh
# Blokuje destruktivní příkazy před provedením

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
[ -z "$COMMAND" ] && exit 0

# Blokovat nebezpečné vzory
if echo "$COMMAND" | grep -qE 'rm\s+(-[a-z]*r[a-z]*f|--recursive\s+--force)'; then
  echo "BLOKOVÁNO: rm -rf je trvale zakázán bezpečnostním hookem." >&2
  exit 2
fi

if echo "$COMMAND" | grep -qE 'Remove-Item\s+-Recurse\s+-Force'; then
  echo "BLOKOVÁNO: Remove-Item -Recurse -Force vyžaduje potvrzení." >&2
  exit 2
fi

if echo "$COMMAND" | grep -qE 'find\s+/\s+.*-delete|find\s+.*-delete'; then
  echo "BLOKOVÁNO: find -delete je zakázán." >&2
  exit 2
fi

if echo "$COMMAND" | grep -qE 'git\s+(reset\s+--hard|clean\s+-fd)'; then
  echo "BLOKOVÁNO: $COMMAND vyžaduje potvrzení." >&2
  exit 2
fi

exit 0
```

---

## 7. Backup a obnova

### 7.1 Pravidla zálohování

| Co | Jak často | Jak |
|----|-----------|-----|
| Celý projekt | Před každým úkolem | `git stash` / commit |
| API klíče | Týdně | Kopie do šifrovaného úložiště |
| System Restore | Před většími změnami | Windows Body obnovení |
| Důležitá data | Denně | Git push na remote |

### 7.2 System Restore – povinný před:

- Přeinstalací ovladačů
- Velkými aktualizacemi systému
- Úkoly, které mění systémové soubory
- Práce agenta s možným přístupem mimo projekt

### 7.3 Nouzový postup při selhání

```
1. OKAMŽITĚ přeruš agenta (Escape / Ctrl+C)
2. NERESTARTUJ počítač
3. Ověř stav: git status, ls klíčových adresářů
4. Pokud jsou soubory pryč: nepiš na disk (vypni PC)
5. Použij live USB a nástroje na obnovu (Recuva, TestDisk)
6. Obnov z bodu obnovení
```

---

## 8. Kontrolní seznam před úkolem

Před KAŽDÝM úkolem s agentem:

- [ ] Jsem v správném adresáři? (`Get-Location`)
- [ ] Je projekt commitnutý? (`git status` čistý)
- [ ] Vytvořil jsem stash/commit? (`git stash list`)
- [ ] Je System Restore aktivní? (`Get-ComputerRestorePoint`)
- [ ] Nemá agent přístup mimo projekt? (opencode permission)
- [ ] Jsou API klíče v bezpečí? (`.env` v `.gitignore`)
- [ ] Vím, co agent smí a nesmí? (tento dokument)

---

## 9. Poučení z incidentů

### 9.1 Gemini CLI – phantom directory (červenec 2025)
- Agent vytvořil adresář, který selhal, ale zpracoval to jako úspěch
- `move` na neexistující cíl = přejmenování místo přesunu
- **Poučení:** Ověřuj KAŽDOU operaci. Nikdy nepokračuj bez ověření.

### 9.2 PocketOS – 9 sekund (duben 2026)
- Agent našel API token s plným přístupem
- Sám se rozhodl "opravit" problém = smazal produkční DB + zálohy
- **Poučení:** API klíče s minimálními oprávněními. Nikdy nedávej agentovi plný přístup.

### 9.3 Claude Code – rm -rf / (říjen 2025)
- Agent spustil `rm -rf` z root `/`
- Systémové soubory přežily díky oprávněním
- **Poučení:** Používej sandbox. Nikdy nepoužívej `--dangerously-skip-permissions`.

### 9.4 Claude Code + NTFS junctions (únor 2026)
- `Remove-Item -Recurse -Force` na `node_modules` sledoval NTFS junctions
- Smazal Documents, Downloads, Music, Pictures
- **Poučení:** PowerShell na Windows sleduje junctions. Používej `cmd.exe /c rmdir /S /Q` pro bezpečné mazání.

---

## 10. Contact a eskalace

Pokud agent provedl nechtěnou operaci:

1. **Zastav** – Escape / Ctrl+C / zavři terminál
2. **Nepokračuj** – nedůvěřuj "hotovo" bez ověření
3. **Ověř** – `git status`, kontrola souborů
4. **Obnov** – System Restore / git reset
5. **Nahlas** – zapiš co se stalo pro budoucí poučení

---

## Revize

| Datum | Změna | Autor |
|-------|-------|-------|
| 17.06.2026 | Vytvoření dokumentu | PC |

---

*Tento dokument je živý. Aktualizuj ho po každém incidentu nebo novém poučení.*
