---
name: "network-lab"
tags: ["advanced", "antigravity", "c:", "configuration", "core", "example", "frontend", "gemini", "governance", "lab", "layout", "<YOUR_USERNAME>", "maintenance", "nat", "network", "networking", "principles", "security", "setup", "slim"]
tier: 2
risk: "high"
estimated_tokens: 737
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.71
description: "Network security lab setup and virtual networking. Covers VirtualBox, VMware, and PNET/GNS3 lab design."
---
# Network Security Lab (v6.5.0-SLIM)

Design and build virtualized network environments for security testing and research.

## 1. Governance & Core Principles
- **Isolation (Host-Only):** No direct bridged connection to the internet from vulnerable machines.
- **NAT Network:** Shared internet access for updates with private IP range.
- **VLAN Isolation:** Separate "Attacker", "Middle", and "Victim" networks.

## 2. Virtual Networking Layout
- **Host:** Windows 11 / Linux (Debian/Ubuntu).
- **Hypervisor:** VirtualBox (Free) or VMware Workstation/Fusion.
- **Attacker VM:** Kali Linux / Parrot OS (Customized).
- **Victim VM:** Windows Server (AD Lab), Metasploitable (Linux), Ubuntu (Web).

### NAT Network Configuration (VBox Example)
```text
CIDR: 10.10.10.0/24
Gateway: 10.10.10.1
DHCP: Enabled
Port Forwarding: (Optional for Host-to-Guest access)
```

## 3. Advanced Lab Setup
- **PFsense / VyOS:** Dedicated virtual firewall for inter-VLAN routing and monitoring.
- **IDS/IPS (Snort/Suricata):** For testing NIDS evasion and signature matching.
- **SIEM (ELK/Wazuh):** Log centralization for forensic analysis and alert testing.

## 4. Lab Maintenance
- **Snapshots:** Always take a clean-state snapshot before running malware or destructive exploits.
- **Backups:** Export VMs (`.ova`) after stable configuration.
- **Updates:** Regularly update Kali/Victim OS for current CVE parity.

## Related Skills
`recon-scanning`, `web-security`, `linux-privesc`.
---
name: privesc-ad
description: Active Directory Privilege Escalation and Domain Domination methodology. Covers enumeration and lateral movement.
---

# Active Directory Privilege Escalation (v6.5.0-SLIM)

Methods for escalating privileges within a Windows Domain environment.

## 1. Domain Enumeration
- **Tools:** `Bloodhound (SharpHound)`, `PowerView`, `ADSearch`.
- **Targeting:** Domain Admins, Enterprise Admins, high-value SQL/Web accounts.
- **Logic:** Kerberoasting 🍖, AS-REP Roasting 🥓, GPP Password mining 🧀.

## 2. Lateral Movement
- **Relay Attacks:** NTLM Relay with `Responder` and `ntlmrelayx`.
- **PTH (Pass-The-Hash):** Using `Mimikatz` or `CrackMapExec` with NTLM hashes.
- **PTT (Pass-The-Ticket):** Kerberos ticket injection (`mimikatz kerberos::ptt`).

## 3. AD Misconfigurations
- **GPO Abuse:** Writable GPOs used to push malicious scheduled tasks.
- **ACL/ACE Abuse:** `GenericAll`, `WriteDacl`, `WriteOwner` privileges on Domain Admin groups.
- **Unconstrained Delegation:** Stealing Krbtgt tickets from domain controllers.

## 4. Persistence & Exfiltration
- **Golden Ticket:** Forged TGT for unrestricted domain access.
- **Silver Ticket:** Forged TGS for specific services.
- **DCShadow:** Mimicking a domain controller to push malicious changes to AD.

## Related Skills
`windows-privesc`, `recon-scanning`.
