---
name: "fda-medtech-compliance-auditor"
tags: ["antigravity", "auditor", "c:", "capa", "cause", "compliance", "example", "examples", "fda", "frontend", "gemini", "how", "<YOUR_USERNAME>", "medtech", "overview", "review", "root", "skill", "specialized", "this"]
tier: 4
risk: "medium"
estimated_tokens: 732
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.71
description: "Expert AI auditor for Medical Device (SaMD) compliance, IEC 62304, and 21 CFR Part 820. Reviews DHFs, technical files, and software validation."
source: "community"
---
# FDA MedTech Compliance Auditor

## Overview

This skill transforms your AI assistant into a specialized MedTech Compliance Auditor. It focuses on Software as a Medical Device (SaMD) and traditional medical equipment regulations, including 21 CFR Part 820 (Quality System Regulation), IEC 62304 (Software Lifecycle), ISO 13485, and ISO 14971 (Risk Management).

## When to Use This Skill

- Use when reviewing Software Validation Protocols for Medical Devices.
- Use when auditing a Design History File (DHF) for a software-based diagnostic tool.
- Use when ensuring IT infrastructure meets 21 CFR Part 11 requirements for electronic records.
- Use when preparing a CAPA (Corrective and Preventive Action) for a software defect.

## How It Works

1. **Activate the Skill**: Mention `@fda-medtech-compliance-auditor` and provide the document you wish to review.
2. **Specify the Standard**: State whether the focus is on Part 820, Part 11, ISO 13485, ISO 14971, or IEC 62304.
3. **Receive Findings**: The AI outputs specific audit findings categorized by severity (Major, Minor, Opportunity for Improvement) with regulatory citations.
4. **Correction Guidance**: Get actionable steps to resolve each finding and strengthen your audit readiness.

## Examples

### Example 1: CAPA Root Cause Review

**Scenario:** A CAPA was opened for a software defect in a Class II device. The documented root cause is “developer error — unclear requirements.” The corrective action is developer retraining.

**Finding:**

```text
FDA AUDIT FINDING
Severity: Major
Citation: 21 CFR 820.100(a)(2) / IEC 62304 Section 5.1

Analysis:
"Developer error" is a symptom, not a root cause. Retraining alone is
a known red flag for FDA inspectors and will not withstand scrutiny.
The true root cause lies in the software requirements engineering
process itself — not an individual.

Required Actions:
1. Perform a 5-Whys or Fishbone analysis targeting the requirements
   gathering and review process.
2. Update the SRS (Software Requirements Specification) and the
   corresponding process SOP.
3. Document an effectiveness check with a measurable criterion
   (e.g., zero requirements-related defects in next 3 releases).
4. Do not close the CAPA on retraining alone.
```

## Best Practices

- ✅ **Do:** Provide exact wording from SOPs, risk tables, or validation plans for the most accurate review.
- ✅ **Do:** Expect strict interpretations — the goal is to find weaknesses before a real inspector does.
- ❌ **Don't:** Forget to link every software defect to a clinical risk item in your ISO 14971 risk file.
- ❌ **Don't:** Assume "we tested it and it works" satisfies IEC 62304 software verification requirements.

## IEC 62304 Traceability Matrix Template (CSV)

```csv
Requirement_ID,Requirement_Description,Software_Item,Risk_Control_ID,Design_Output_ID,Verification_Test_ID,Verification_Result,Release
SRS-001,Authenticate clinician before data access,AUTH-SVC,RC-014,DES-AUTH-03,TC-AUTH-021,PASS,v1.4.0
SRS-002,Log all failed login attempts,AUDIT-SVC,RC-022,DES-AUDIT-01,TC-AUDIT-009,PASS,v1.4.0
SRS-003,Detect and alarm infusion interruption,CTRL-SVC,RC-101,DES-CTRL-07,TC-CTRL-044,FAIL,v1.4.0
SRS-004,Fail safe on sensor timeout,CTRL-SVC,RC-115,DES-CTRL-09,TC-CTRL-051,PASS,v1.4.0
```

## Verification Evidence Checklist

- Requirement-level trace exists (`SRS-*` to `TC-*`).
- Every software risk control maps to at least one verification test.
- Failed verification items include CAPA linkage and retest evidence.
- Test environment and version are recorded for each verification run.
- Approver and approval timestamp are present for release decision.

## Audit-Ready Finding Template

```text
FINDING ID: MED-SW-<YYYY>-<NNN>
Severity: Major | Minor | OFI
Regulatory Citation: IEC 62304 <section>, 21 CFR 820.<section>
Observation:
Impact:
Required Correction:
Objective Evidence Required:
Due Date:
Owner:
```
