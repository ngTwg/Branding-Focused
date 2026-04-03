# Community + Packaging Roadmap (30 Days)

Date: 2026-04-01
Version Context: v6.5.0-SLIM
Scope: Productize Antigravity beyond architecture strength into distribution, discoverability, and community adoption.

---

## 1) Strategic Intent

Current strength is system depth (router, governance, memory, autonomous loop). The 30-day goal is to remove adoption friction and make the system easier to install, trust, and evaluate publicly.

Primary outcomes:
- Better onboarding conversion for first-time users
- Higher trust via security and benchmark transparency
- Better discoverability through packaging and docs UX
- Better contributor inflow via standard OSS surface

---

## 2) Keep / Drop / Add Matrix

| Action | Item | Why |
|---|---|---|
| KEEP | MASTER_ROUTER + tier-based routing | Core differentiator and system identity |
| KEEP | Governance chain (constitution checks, overlap resolution, PII scrubbing) | Strong trust foundation for enterprise-like usage |
| KEEP | Hybrid model (primary + external skill bridge) | Breadth advantage across niche domains |
| DROP | Version drift across docs | Reduces external trust and onboarding confidence |
| DROP | Implicit assumptions on underspecified requests | Increases wrong execution risk and user friction |
| DROP | Hard-to-browse inventory-only discoverability | Prevents newcomers from finding relevant skills quickly |
| ADD | Packaging layer (install/convert for multi-agent tools) | Matches top-repo usability expectations |
| ADD | Security gate for external skills (PASS/WARN/FAIL) | Required for safe bridge-based ingestion |
| ADD | Persona bundles (solo-founder, startup-cto, secure-saas, etc.) | Compresses complexity for new users |
| ADD | Public benchmark suite + release cadence | Converts claims into visible proof |

---

## 3) 30-Day Sprint Plan

## Week 1 (Days 1-7): Packaging Foundation

Deliverables:
- `tools/skillpack/` CLI scaffold for convert/install commands
- Standard output templates per target tool (Cursor, Claude, Copilot, Cline, Continue, Kiro, Roo)
- Unified metadata schema draft: `name`, `tags`, `tier`, `risk`, `estimated_tokens`, `tools_needed`, `applies_to_agents`, `industry`, `quality_score`
- `RELEASE_NOTES_TEMPLATE.md` and release checklist

Acceptance:
- At least 3 working install targets and 1 conversion flow validated end-to-end

## Week 2 (Days 8-14): Security + Persona Layer

Deliverables:
- `antigravity/scripts/skill_security_auditor.py` (or equivalent module)
- Security gate report format: PASS/WARN/FAIL with reason codes
- Detection rules: shell injection markers, risky command patterns, suspicious network exfiltration cues, prompt injection signatures
- First 6 persona bundles:
  - solo-founder
  - startup-cto
  - frontend-brand-builder
  - seo-launch
  - secure-saas
  - mcp-builder

Acceptance:
- Every external skill import path passes through security audit
- Persona bundles are installable and documented with sample prompts

## Week 3 (Days 15-21): Discoverability + Marketplace UX

Deliverables:
- Filterable docs catalog MVP with dimensions:
  - domain
  - agent/tool compatibility
  - tier
  - risk
  - token budget
- Skill detail card template with "when to use" and example prompt
- Searchable catalog index generation script

Acceptance:
- New users can locate a relevant skill path within 2 minutes without reading full router tree

## Week 4 (Days 22-30): Evidence + Distribution + Community

Deliverables:
- Public benchmark pack:
  - build landing page
  - fix checkout crash
  - generate MCP server
  - healthtech compliance checklist
- Release cadence setup:
  - semantic tags
  - changelog discipline
  - monthly release notes
- OSS contributor surface hardening:
  - CONTRIBUTING.md refresh
  - issue templates
  - PR template
  - repository topics/description update

Acceptance:
- Benchmark results published and reproducible
- First formal release with changelog and installation matrix published

---

## 4) KPI Targets (30 Days)

- Installation targets: from ad-hoc to >= 7 stable targets
- Security-audited external imports: 100% coverage
- Persona bundles published: >= 6
- Benchmark scenarios public: >= 4 with reproducible steps
- Docs discoverability:
  - catalog page online
  - metadata coverage >= 80% of high-traffic skills
- Community traction:
  - contributors: +3 net new
  - stars: measurable positive trend week-over-week

---

## 5) Risk Controls

- Prevent feature sprawl by shipping minimum useful packaging first
- Keep governance strict during scaling (do not bypass audit gate)
- Avoid docs-only progress without runnable installer/benchmark artifacts
- Track all roadmap items with binary acceptance checks

---

## 6) Immediate Next Actions (Start This Week)

1. Ship metadata schema v1 and validate on top 100 skills.
2. Build installer/converter MVP for 3 tool targets.
3. Implement security auditor baseline with PASS/WARN/FAIL report.
4. Publish first two persona bundles with example prompts.
5. Open first public benchmark scenario and baseline score.
