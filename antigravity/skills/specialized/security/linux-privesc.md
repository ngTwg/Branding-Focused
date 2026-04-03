---
name: "linux-privesc"
tags: ["antigravity", "binaries", "c:", "cron", "enumeration", "escalation", "exploits", "frontend", "gemini", "initial", "kernel", "<YOUR_USERNAME>", "linux", "misconfigurations", "privesc", "privilege", "scheduled", "security", "sgid", "slim"]
tier: 4
risk: "high"
estimated_tokens: 455
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
description: "Linux Privilege Escalation techniques and methodologies. Covers Kernel, Sudo, SUID, and Configuration exploits."
---
# Linux Privilege Escalation (v6.5.0-SLIM)

Methodology for escalating privileges from limited user to root on Linux systems.

## 1. Initial Enumeration
- **System Information:** `cat /etc/issue`, `uname -a`.
- **Environment:** `env`, `history`.
- **User Info:** `id`, `whoami`, `cat /etc/passwd`.
- **Network Info:** `ip a`, `ss -tulnp`, `arp -a`.
- **Automated Tools:** `LinPEAS`, `lse.sh`.

## 2. Kernel Exploits
- Check kernel version and cross-reference with exploit databases (e.g., DirtyCow, DirtyPipe, PwnKit).
- **Compilation:** Compile exploits on a separate system with identical architecture.

## 3. Sudo Misconfigurations
- **Check Sudo Privs:** `sudo -l`.
- **GTFOBins:** Check if any allowed command has an escape character/shell command capability.
- **LD_PRELOAD:** Exploiting environments where `LD_PRELOAD` is preserved to inject malicious `.so` files.

## 4. SUID/SGID Binaries
- **Find SUID:** `find / -perm -u=s -type f 2>/dev/null`.
- **Common vulnerable binaries:** `find`, `nmap`, `vim`, `bash`, `cp`, `mv`.

## 5. Scheduled Tasks (Cron)
- **List Cron Jobs:** `cat /etc/crontab`.
- **Exploitation:** Writable scripts, relative paths in scripts, or wildcards (`tar *`).

## 6. Writable Files & Directories
- **Writable /etc/passwd:** Add a new root user manually.
- **NFS Shares:** Check for `no_root_squash` in `/etc/exports`.
- **Sensitive files:** Read SSH keys, configuration files with passwords (`wp-config.php`, `.env`).

## 7. Operational Checklist
1. Enumeration (Manual + LinPEAS).
2. Check Sudo.
3. Check Kernel.
4. Check SUID.
5. Check Services/Tasks.
6. Check Environment/Files.

## Related Skills
`network-lab`, `web-security`.
