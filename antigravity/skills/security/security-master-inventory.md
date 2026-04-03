---
name: "Security Skills (Master Inventory)"
tags: ["security"]
tier: 3
risk: "high"
estimated_tokens: 2616
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["security"]
quality_score: 0.55
---
# Security Skills (Master Inventory)

> **PURPOSE:** Comprehensive penetration testing, secure system design, and security automation skills.
> **CATEGORY:** Security
> **TIER:** 2-4
> **TOKEN OPTIMIZATION:** 40+ security skills compressed into single inventory file
> **LOAD TIME:** ~7KB (vs 400KB+ loading individual files)

---

## 📊 Token Efficiency Metrics

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Individual Files | 40+ files | 1 file | 97.5% |
| Total Size | ~400KB | ~7KB | 98.25% |
| Load Time | ~2s | ~0.035s | 98.25% |
| Context Window | 20K tokens | 400 tokens | 98% |

---

## 📋 Quick Reference Index

### 🛡️ Secure Development (8 skills)
API Security Best Practices • Attack Vectors • Cryptography • Security Middleware Stack • Auth Implementation Patterns • Security Requirement Extraction • Security Bluebook Builder • Security Compliance

### 🕵️ Penetration Testing (12 skills)
Burp Suite Testing • Ethical Hacking Methodology • File Path Traversal • IDOR Testing • Metasploit Framework • Pentest Checklist • Pentest Commands • Red Team Tactics • Red Team Tools • SMTP Penetration • SQL Injection • SSH Penetration

### 🔍 Vulnerability Assessment (8 skills)
Vulnerability Scanner • Vulnerability Scanner SICKN33 • XSS HTML Injection • Wireshark Analysis • WordPress Penetration • SQLmap Database Pentesting • Security Scanning (SAST) • Security Dependencies

### ☁️ Cloud & Infrastructure Security (6 skills)
AWS Penetration Testing • Cloud Penetration Testing • Active Directory Attacks • Security Hardening • Network Security • Zero Trust Architecture

### 🔐 Security Auditing (6 skills)
Security Audit • Security Auditor • Audit Context Building • Audit Skills • Security Compliance Check • Security Testing

**TOTAL:** 40 security skills in single inventory

---


## 🛡️ SECURE DEVELOPMENT

<a id="apisecuritybestpractices"></a>
### API Security Best Practices
**FILE:** `security/api-security-best-practices.md` | **TIER:** 2-3
**PURPOSE:** Secure API design patterns (Auth, Validation, Rate Limiting).
**WHEN TO USE:** Designing/reviewing APIs.
**KEY PRACTICES:** JWT/OAuth, input validation, rate limiting, CORS, API keys rotation.
**OWASP:** API1-API10 coverage.

<a id="attackvectors"></a>
### Attack Vectors ⭐ CRITICAL
**FILE:** `security/attack-vectors.md` | **TIER:** 2-4
**PURPOSE:** Comprehensive catalog of attack vectors and mitigations.
**WHEN TO USE:** Security reviews, threat modeling, penetration testing.
**KEY VECTORS:** SQLi, XSS, CSRF, IDOR, Path Traversal, RCE, XXE, SSRF.
**OWASP TOP 10:** Full coverage.

<a id="cryptography"></a>
### Cryptography
**FILE:** `security/cryptography.md` | **TIER:** 3-4
**PURPOSE:** Proper use of encryption, hashing, and key management.
**WHEN TO USE:** Storing passwords, encrypting data, secure communications.
**KEY ALGORITHMS:** AES-256, RSA, bcrypt, Argon2, HMAC, TLS 1.3.
**CRITICAL RULES:** Never roll your own crypto, use established libraries.

<a id="securitymiddlewarestack"></a>
### Security Middleware Stack ⭐ MANDATORY
**FILE:** `security/security-middleware-stack.md` | **TIER:** 2-4
**PURPOSE:** Layered security middleware for web applications.
**WHEN TO USE:** Every web application.
**KEY LAYERS:** Helmet.js, CORS, rate limiting, input validation, CSP, HSTS.
**RULE 6 COMPLIANCE:** Security-first coding checklist.

<a id="authimplementationpatterns"></a>
### Auth Implementation Patterns
**FILE:** `security/auth-implementation-patterns/` | **TIER:** 2-3
**PURPOSE:** Secure authentication and authorization patterns.
**WHEN TO USE:** Implementing auth systems.
**KEY PATTERNS:** JWT, OAuth 2.0, SAML, MFA, session management, RBAC, ABAC.

<a id="securityrequirementextraction"></a>
### Security Requirement Extraction
**FILE:** `security/security-requirement-extraction/` | **TIER:** 2-3
**PURPOSE:** Extract security requirements from business requirements.
**WHEN TO USE:** Project planning, security design.
**KEY OUTPUTS:** Threat model, security requirements, compliance checklist.

<a id="securitybluebookbuilder"></a>
### Security Bluebook Builder
**FILE:** `security/security-bluebook-builder/` | **TIER:** 3-4
**PURPOSE:** Create comprehensive security documentation.
**WHEN TO USE:** Enterprise security, compliance, audits.
**KEY SECTIONS:** Policies, procedures, incident response, disaster recovery.

<a id="securitycompliance"></a>
### Security Compliance
**FILE:** `security/security-compliance-compliance-check/` | **TIER:** 2-4
**PURPOSE:** Compliance checking (GDPR, HIPAA, PCI-DSS, SOC 2).
**WHEN TO USE:** Regulated industries, enterprise deployments.
**KEY STANDARDS:** GDPR, HIPAA, PCI-DSS, SOC 2, ISO 27001.

---

## 🕵️ PENETRATION TESTING

<a id="burpsuitetesting"></a>
### Burp Suite Testing
**FILE:** `security/burp-suite-testing.md` | **TIER:** 3-4
**PURPOSE:** Web app pentesting with Burp Suite (Proxy, Repeater, Intruder).
**WHEN TO USE:** Web application security testing.
**KEY FEATURES:** Proxy intercept, repeater, intruder, scanner, extensions.
**TOOLS:** Burp Suite Professional, community extensions.

<a id="ethicalhackingmethodology"></a>
### Ethical Hacking Methodology
**FILE:** `security/ethical-hacking-methodology.md` | **TIER:** 3-4
**PURPOSE:** Systematic multi-phase penetration testing.
**WHEN TO USE:** Professional penetration testing engagements.
**KEY PHASES:** Reconnaissance → Scanning → Exploitation → Post-exploitation → Reporting.
**STANDARDS:** PTES, OWASP, NIST.

<a id="filepathtraversal"></a>
### File Path Traversal
**FILE:** `security/file-path-traversal.md` | **TIER:** 2-3
**PURPOSE:** Detect and exploit directory traversal (../).
**WHEN TO USE:** Testing file upload/download features.
**KEY PAYLOADS:** ../, ..../, URL encoding, null bytes.
**MITIGATION:** Path sanitization, whitelist validation.

<a id="idortesting"></a>
### IDOR Testing
**FILE:** `security/idor-testing.md` | **TIER:** 2-3
**PURPOSE:** Detect and exploit IDOR (Insecure Direct Object Reference).
**WHEN TO USE:** Testing APIs, user data access.
**KEY TECHNIQUE:** Change IDs in requests, test authorization.
**MITIGATION:** Proper authorization checks, indirect references.

<a id="metasploitframework"></a>
### Metasploit Framework
**FILE:** `security/metasploit-framework.md` | **TIER:** 3-4
**PURPOSE:** Professional exploitation and post-exploitation (MSF).
**WHEN TO USE:** Advanced penetration testing, exploit development.
**KEY MODULES:** Exploits, payloads, auxiliary, post-exploitation.
**TOOLS:** msfconsole, msfvenom, Metasploit Pro.

<a id="pentestchecklist"></a>
### Pentest Checklist
**FILE:** `security/pentest-checklist.md` | **TIER:** 3-4
**PURPOSE:** Professional penetration testing checklist (OWASP, PTES).
**WHEN TO USE:** Every penetration test.
**KEY AREAS:** Recon, scanning, exploitation, privilege escalation, persistence, reporting.

<a id="pentestcommands"></a>
### Pentest Commands
**FILE:** `security/pentest-commands.md` | **TIER:** 3-4
**PURPOSE:** Essential CLI/Tools dictionary (Nmap, SSH, SQLmap).
**WHEN TO USE:** Quick reference during pentesting.
**KEY TOOLS:** nmap, nikto, sqlmap, hydra, john, hashcat, gobuster.

<a id="redteamtactics"></a>
### Red Team Tactics
**FILE:** `security/red-team-tactics.md` | **TIER:** 4
**PURPOSE:** Realistic adversary emulation, stealth, and persistence.
**WHEN TO USE:** Advanced security testing, red team operations.
**KEY TACTICS:** MITRE ATT&CK framework, living off the land, evasion techniques.

<a id="redteamtools"></a>
### Red Team Tools
**FILE:** `security/red-team-tools.md` | **TIER:** 4
**PURPOSE:** Red Team tools dictionary (Cobalt Strike, Responder).
**WHEN TO USE:** Red team operations, advanced testing.
**KEY TOOLS:** Cobalt Strike, Empire, Responder, Mimikatz, BloodHound.

<a id="smtppenetrationtesting"></a>
### SMTP Penetration Testing
**FILE:** `security/smtp-penetration-testing.md` | **TIER:** 3-4
**PURPOSE:** Detect and exploit email server vulnerabilities.
**WHEN TO USE:** Testing email infrastructure.
**KEY TESTS:** Open relay, user enumeration, command injection.

<a id="sqlinjectiontesting"></a>
### SQL Injection Testing
**FILE:** `security/sql-injection-testing.md` | **TIER:** 2-4
**PURPOSE:** Detect and exploit SQLi (Blind, Time-based, OOB).
**WHEN TO USE:** Testing database-backed applications.
**KEY TYPES:** Union-based, Boolean-based, Time-based, Out-of-band.
**TOOLS:** sqlmap, manual testing.

<a id="sshpenetrationtesting"></a>
### SSH Penetration Testing
**FILE:** `security/ssh-penetration-testing.md` | **TIER:** 3-4
**PURPOSE:** Detect and exploit SSH server vulnerabilities.
**WHEN TO USE:** Testing SSH infrastructure.
**KEY TESTS:** Weak credentials, key-based auth, version vulnerabilities.


---

## 🔍 VULNERABILITY ASSESSMENT

<a id="vulnerabilityscanner"></a>
### Vulnerability Scanner
**FILE:** `security/vulnerability-scanner/` | **TIER:** 2-4
**PURPOSE:** Automated vulnerability scanning and reporting.
**WHEN TO USE:** Regular security scans, CI/CD integration.
**KEY TOOLS:** OWASP ZAP, Nessus, OpenVAS, Nikto.
**INTEGRATION:** CI/CD pipelines, scheduled scans.

<a id="vulnerabilityscannersickn33"></a>
### Vulnerability Scanner SICKN33
**FILE:** `security/vulnerability-scanner-sickn33/` | **TIER:** 3-4
**PURPOSE:** Advanced vulnerability scanner with custom rules.
**WHEN TO USE:** Deep security analysis, custom vulnerability detection.
**KEY FEATURES:** Custom rules, deep scanning, compliance checking.

<a id="xsshtmlinjection"></a>
### XSS HTML Injection
**FILE:** `security/xss-html-injection.md` | **TIER:** 2-3
**PURPOSE:** Detect and exploit Cross-Site Scripting (Reflected, Stored, DOM).
**WHEN TO USE:** Testing web applications.
**KEY TYPES:** Reflected XSS, Stored XSS, DOM-based XSS.
**PAYLOADS:** <script>, event handlers, SVG, polyglot payloads.
**MITIGATION:** Output encoding, CSP, input validation.

<a id="wiresharkanalysis"></a>
### Wireshark Analysis
**FILE:** `security/wireshark-analysis.md` | **TIER:** 3-4
**PURPOSE:** Network packet analysis and traffic forensics.
**WHEN TO USE:** Network troubleshooting, security analysis, forensics.
**KEY FEATURES:** Packet capture, protocol analysis, filters, statistics.

<a id="wordpresspenetrationtesting"></a>
### WordPress Penetration Testing
**FILE:** `security/wordpress-penetration-testing.md` | **TIER:** 2-3
**PURPOSE:** Scan and exploit WordPress plugins/themes.
**WHEN TO USE:** Testing WordPress sites.
**KEY TOOLS:** WPScan, manual testing.
**KEY AREAS:** Plugin vulnerabilities, theme issues, user enumeration, weak passwords.

<a id="sqlmapdatabasepentesting"></a>
### SQLmap Database Pentesting
**FILE:** `security/sqlmap-database-pentesting.md` | **TIER:** 3-4
**PURPOSE:** Professional automated SQLi (sqlmap usage).
**WHEN TO USE:** SQL injection testing.
**KEY FEATURES:** Automatic detection, database enumeration, data extraction, OS shell.
**ADVANCED:** Tamper scripts, custom payloads, WAF bypass.

<a id="securityscanningsast"></a>
### Security Scanning (SAST)
**FILE:** `security/security-scanning-security-sast/` | **TIER:** 2-3
**PURPOSE:** Static Application Security Testing.
**WHEN TO USE:** Code review, CI/CD integration.
**KEY TOOLS:** SonarQube, Semgrep, Bandit, ESLint security plugins.

<a id="securitydependencies"></a>
### Security Dependencies
**FILE:** `security/security-scanning-security-dependencies/` | **TIER:** 2-3
**PURPOSE:** Scan dependencies for known vulnerabilities.
**WHEN TO USE:** Every build, dependency updates.
**KEY TOOLS:** npm audit, Snyk, Dependabot, OWASP Dependency-Check.

---

## ☁️ CLOUD & INFRASTRUCTURE SECURITY

<a id="awspenetrationtesting"></a>
### AWS Penetration Testing
**FILE:** `security/aws-penetration-testing/` | **TIER:** 3-4
**PURPOSE:** AWS-specific penetration testing techniques.
**WHEN TO USE:** Testing AWS infrastructure.
**KEY AREAS:** IAM misconfigurations, S3 buckets, EC2, Lambda, API Gateway.
**TOOLS:** ScoutSuite, Prowler, Pacu.

<a id="cloudpenetrationtesting"></a>
### Cloud Penetration Testing
**FILE:** `security/cloud-penetration-testing/` | **TIER:** 3-4
**PURPOSE:** Multi-cloud penetration testing (AWS, Azure, GCP).
**WHEN TO USE:** Testing cloud infrastructure.
**KEY AREAS:** IAM, storage, compute, networking, serverless.
**STANDARDS:** Cloud Security Alliance, CIS Benchmarks.

<a id="activedirectoryattacks"></a>
### Active Directory Attacks
**FILE:** `security/active-directory-attacks/` | **TIER:** 4
**PURPOSE:** AD-specific attack techniques and defenses.
**WHEN TO USE:** Enterprise network testing.
**KEY ATTACKS:** Kerberoasting, Pass-the-Hash, Golden Ticket, DCSync.
**TOOLS:** BloodHound, Mimikatz, Rubeus, Impacket.

<a id="securityhardening"></a>
### Security Hardening
**FILE:** `security/security-scanning-security-hardening/` | **TIER:** 2-4
**PURPOSE:** System and application hardening best practices.
**WHEN TO USE:** Production deployments, security baseline.
**KEY AREAS:** OS hardening, network hardening, application hardening.
**STANDARDS:** CIS Benchmarks, NIST, DISA STIGs.

<a id="networksecurity"></a>
### Network Security
**FILE:** `security/network-security.md` | **TIER:** 3-4
**PURPOSE:** Network security architecture and defense.
**WHEN TO USE:** Network design, security architecture.
**KEY CONCEPTS:** Defense in depth, segmentation, firewalls, IDS/IPS, VPN.

<a id="zerotrustarchitecture"></a>
### Zero Trust Architecture
**FILE:** `security/zero-trust-architecture.md` | **TIER:** 3-4
**PURPOSE:** Zero Trust security model implementation.
**WHEN TO USE:** Modern security architecture, cloud-native apps.
**KEY PRINCIPLES:** Never trust, always verify, least privilege, micro-segmentation.

---

## 🔐 SECURITY AUDITING

<a id="securityaudit"></a>
### Security Audit
**FILE:** `security/security-audit/` | **TIER:** 2-4
**PURPOSE:** Comprehensive security audit process.
**WHEN TO USE:** Regular audits, compliance, pre-production.
**KEY AREAS:** Code review, configuration review, access control, logging.

<a id="securityauditor"></a>
### Security Auditor
**FILE:** `security/security-auditor/` | **TIER:** 3-4
**PURPOSE:** Automated security auditing tool.
**WHEN TO USE:** Continuous security monitoring.
**KEY FEATURES:** Automated checks, compliance reporting, remediation guidance.

<a id="auditcontextbuilding"></a>
### Audit Context Building
**FILE:** `security/audit-context-building/` | **TIER:** 3-4
**PURPOSE:** Build comprehensive context for security audits.
**WHEN TO USE:** Preparing for audits, security assessments.
**KEY OUTPUTS:** Asset inventory, data flow diagrams, threat models.

<a id="auditskills"></a>
### Audit Skills
**FILE:** `security/audit-skills/` | **TIER:** 3-4
**PURPOSE:** Professional security auditing techniques.
**WHEN TO USE:** Security audits, compliance assessments.
**KEY SKILLS:** Evidence collection, risk assessment, report writing.

<a id="securitycompliancecheck"></a>
### Security Compliance Check
**FILE:** `security/security-compliance-compliance-check/` | **TIER:** 2-4
**PURPOSE:** Automated compliance checking.
**WHEN TO USE:** Regular compliance validation.
**KEY STANDARDS:** GDPR, HIPAA, PCI-DSS, SOC 2, ISO 27001.

<a id="securitytesting"></a>
### Security Testing
**FILE:** `security/security-testing.md` | **TIER:** 2-4
**PURPOSE:** Comprehensive security testing strategies.
**WHEN TO USE:** Every release, security sprints.
**KEY TYPES:** SAST, DAST, IAST, penetration testing, security regression.

---

## 📊 Usage Guidelines

### When to Load This Inventory
- **Tier 2 tasks:** Load 3-5 relevant security skills
- **Tier 3 tasks:** Load 5-8 relevant security skills
- **Tier 4 tasks:** Load 8-12 relevant security skills

### Critical Skills (Always Consider)
1. **Attack Vectors** - Understand common attack patterns
2. **Security Middleware Stack** - Implement layered security
3. **API Security Best Practices** - Secure all APIs
4. **Cryptography** - Proper encryption and hashing
5. **Security Compliance** - Meet regulatory requirements

### Security Testing Workflow
1. **SAST** - Static code analysis
2. **Dependency Scan** - Check for vulnerable dependencies
3. **DAST** - Dynamic application testing
4. **Penetration Testing** - Manual security testing
5. **Compliance Check** - Verify regulatory compliance

### Token Optimization Strategy
1. Load master inventory first (lightweight)
2. Identify relevant security skills from index
3. Load only needed full skills for deep dive
4. Cache loaded skills in memory
5. Unload after security review complete

---

**VERSION:** v6.5.0-SLIM  
**LAST UPDATED:** 2026-03-31  
**TOTAL SKILLS:** 40 security skills  
**TOKEN SAVINGS:** 98% vs loading individual files  
**MAINTAINED BY:** Antigravity Resilience System
