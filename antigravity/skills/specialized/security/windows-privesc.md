---
name: "windows-privesc"
tags: ["antigravity", "attacks", "c:", "credential", "enumeration", "escalation", "exploitable", "exploitation", "frontend", "gemini", "harvesting", "impersonation", "initial", "kernel", "<YOUR_USERNAME>", "potato", "privesc", "privilege", "security", "slim"]
tier: 4
risk: "high"
estimated_tokens: 857
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.69
description: "Windows Privilege Escalation techniques and methodology. Covers enumeration, service abuse, and impersonation."
---
# Windows Privilege Escalation (v6.5.0-SLIM)

Methods for escalating privileges from limited user to SYSTEM on Windows environments.

## 1. Initial Enumeration
- **System Information:** `systeminfo`, `wmic os get /all`.
- **Environment:** `whoami /all`, `net user`, `net localgroup`.
- **Network Info:** `ipconfig`, `netstat -ano`, `arp -a`, `net share`.
- **Automated Tools:** `WinPEAS`, `PowerUp.ps1`.

## 2. Exploitable Vulnerabilities
- **Misconfigured Services:** Writable binary paths, unquoted service paths.
- **AlwaysInstallElevated:** Registry flag that executes `.msi` installations as SYSTEM.
- **Insecure File Permissions:** Find writable directories (`C:\Windows\Temp`) or configuration files with passwords.

## 3. Token Impersonation (Potato Attacks)
- **Privileges:** Check `whoami /priv` for `SeImpersonatePrivilege` or `SeAssignPrimaryTokenPrivilege`.
- **JuicyPotato (v2019 and below):** CLSID abuse for local SYSTEM elevation.
- **PrintSpoofer (v2019+ and Win10):** Spooler service pipe impersonation.
- **RoguePotato/GodPotato:** Modern alternatives for hardened systems.

## 4. Credential Harvesting
- **SAM/SYSTEM:** Extract and crack local password hashes.
- **Stored Creds:** Check `cmdkey /list`, browser profiles, PuTTY, and VNC registry keys.
- **Unattend/Sysprep:** Search for cleartext passwords in configuration files.

## 5. Kernel Exploitation
- **Exploit Suggester:** Use `wes.py` on `systeminfo` output to find missing KB patches.
- **EternalBlue (MS17-010):** Common for legacy environments.
- **Win32k:** Various CVEs for memory corruption/elevation.

## 6. Operational Checklist
1. Enumeration (Manual + WinPEAS).
2. Check Privileges.
3. Check Services.
4. Check Credentials.
5. Check Kernel Patches.

## Related Skills
`linux-privesc`, `web-security`.
---
name: recon-scanning
description: Reconnaissance and Network Scanning methodology. Covers Nmap, Masscan, and Shodan reconnaissance.
---

# Reconnaissance & Scanning (v6.5.0-SLIM)

Framework for discovering, identifying, and mapping network assets and vulnerabilities.

## 1. Strategic Methodology
- **Passive Recon:** No direct interaction (Shodan, WHOIS, DNSDumpster).
- **Active Recon:** Direct interaction (Nmap, Masscan, Ping sweep).
- **Phasing:** Port Scanning → Service Identification → Version Detection → Vulnerability Audit.

## 2. Mass Scanning (Speed)
- **Masscan:** Best for full-range internet scans.
- **Nmap (-T4/-T5):** Aggressive scanning for smaller ranges.

## 3. Service Identification (Depth)
- **Nmap (-sV):** Detailed version detection.
- **Banner Grabbing:** Use `nc`, `curl`, or Nmap's `banner.nse`.
- **Default Scripts:** Use `nmap -sC` for common configuration checks.

## 4. Shodan Reconnaissance
Use Shodan for external asset mapping (cloud, IoT, exposed databases).
- **Filters:** `org:"TargetName"`, `port:443`, `product:"Microsoft IIS"`, `os:"Linux"`, `net:"1.2.3.4/24"`.
- **API Automation:** Integrate Shodan into discovery pipelines for real-time monitoring.

## 5. Security & Evasion
- **Fragmentation:** `-f` to split packets and evade simple IDSs.
- **Source Ports:** `-g 53` or `-g 88` for DNS/DHCP bypass.
- **Timing:** Use `-T2` (Polite) to evade rate limit sensors.

## Related Skills
`web-security`, `linux-privesc`, `windows-privesc`.
