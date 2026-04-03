---
name: "Paid Ads Setup & Audit Checklists"
tags: ["ads", "antigravity", "audit", "backend", "c:", "checklist", "checklists", "creative", "drops", "facebook", "gemini", "google", "instagram", "<YOUR_USERNAME>", "linkedin", "meta", "paid", "performance", "setup", "specialized"]
tier: 2
risk: "medium"
estimated_tokens: 632
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.67
---
# Paid Ads Setup & Audit Checklists

Use these checklists to ensure your campaigns are set up for success and to identify areas for optimization.

---

## Meta Ads (Facebook/Instagram) Setup Checklist

- [ ] Meta Pixel/API Conversion Gateway installed and verified
- [ ] Events (Lead, Purchase, View Content) firing correctly
- [ ] Domain verified in Business Manager
- [ ] CAPI (Conversions API) implemented (to mitigate iOS14+ tracking issues)
- [ ] Lookalike Audiences (LAL) created (1%, 1-3%) from customer/visitor data
- [ ] Automated Rules set up (e.g., pause ad set if CPA > 1.5x target)
- [ ] Ad Creative: Multi-format (Static, Carousels, Video/Reels)
- [ ] Headlines: At least 3 variations per ad set
- [ ] Broad Audience trial (Age/Gender/Location only) to see if algorithm out-targets manual interests

---

## Google Ads Setup Checklist

- [ ] Conversion Value/Action tracking set up in Google Tag Manager
- [ ] Remarketing audiences created in Google Analytics 4 (GA4)
- [ ] Negative Keyword List applied (e.g., free, jobs, careers, review)
- [ ] Broad Match vs Phrasal vs Exact match strategy defined
- [ ] Performance Max (PMax) campaign configured if using E-commerce
- [ ] Dynamic Search Ads (DSA) to catch long-tail intent
- [ ] Ad Extensions (Sitelinks, Callouts, Structured Snippets) fully populated
- [ ] Budget sufficient for at least 10x target CPA per day

---

## LinkedIn Ads Setup Checklist

- [ ] Insight Tag installed on all pages
- [ ] Matched Audiences (Account lists/Contact lists) uploaded
- [ ] Document Ads (PDFs/E-books) for lead generation without leaving platform
- [ ] Targeting: Job Title + Seniority + Years of Experience (narrow enough, but not too narrow)
- [ ] Conversions: Multi-step tracking (e.g., Download → Contact)
- [ ] Budget realistic for CPMs (LinkedIn is expensive, don't spread too thin)

---

## Ad Audit Checklist (When performance drops)

### Creative
- [ ] Is frequency too high (>3)? Refresh creative.
- [ ] Is CTR < 1%? Hook isn't working/audience mismatch.
- [ ] Is CPC high? Image/Video not stopping the scroll.

### Targeting
- [ ] Are ad sets overlapping? Use Meta's Inspect tool.
- [ ] Is the audience too small? Audience may be fatigued.
- [ ] Am I excluding converters? Don't pay to show ads to existing customers.

### Bottom Line
- [ ] Is ROAS > Break-even? If not, check landing page conversion rate first.
- [ ] Is the algorithm in "Learning Phase"? Stop making changes until it exits.
- [ ] Is attribution window correct (e.g., 7-day click, 1-day view)?
