---
name: "Analytics & Tracking"
tags: ["analytics", "antigravity", "c:", "framework", "frontend", "gemini", "key", "<YOUR_USERNAME>", "marketing", "metrics", "overview", "quick", "reference", "rules", "specialized", "testing", "tracking", "users"]
tier: 3
risk: "medium"
estimated_tokens: 1555
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.80
---
# Analytics & Tracking

> **Tier:** 2  
> **Tags:** `[analytics, tracking, metrics, optimization, data-driven, roi]`  
> **When to use:** Marketing analytics, performance tracking, ROI measurement, optimization

---

## Overview

Comprehensive analytics and tracking strategies for marketing campaigns including metrics frameworks, attribution models, testing methodologies, and optimization tactics.

---

## Rules

**RULE-001: Track North Star Metric**
Identify the one metric that best represents value delivery. All other metrics should ladder up to this.

```markdown
Examples:
- SaaS: Weekly Active Users (WAU)
- E-commerce: Revenue per Visitor
- Marketplace: Gross Merchandise Value (GMV)
- Media: Time Spent / Engagement
```

**RULE-002: Pirate Metrics Framework (AARRR)**
Track the full funnel:
- **Acquisition:** How do people find you?
- **Activation:** Do they have a great first experience?
- **Retention:** Do they come back?
- **Revenue:** Do they pay?
- **Referral:** Do they tell others?

**RULE-003: Attribution Model Selection**
Choose attribution model based on business:
- **Last-click:** Simple, biased toward bottom-funnel
- **First-click:** Credits discovery, ignores nurture
- **Linear:** Equal credit, oversimplifies
- **Time-decay:** Recent touchpoints weighted more
- **Data-driven:** ML-based, most accurate but complex

**RULE-004: UTM Parameter Standards**
Consistent UTM tagging for all campaigns:
```
utm_source: Where traffic comes from (google, facebook, newsletter)
utm_medium: Marketing medium (cpc, email, social)
utm_campaign: Specific campaign name (spring_sale_2024)
utm_content: Variant identifier (banner_a, cta_blue)
utm_term: Paid keyword (optional)
```

**RULE-005: Event Tracking Hierarchy**
Track events in order of importance:
1. Critical conversions (signup, purchase, trial start)
2. Micro-conversions (add to cart, video watch, download)
3. Engagement events (scroll depth, time on page, clicks)
4. Diagnostic events (errors, load times, feature usage)

**RULE-006: Cohort Analysis**
Analyze user behavior by cohort (signup date, acquisition channel, plan type). Track retention, LTV, and engagement over time.

**RULE-007: Statistical Significance**
Don't call test winners prematurely:
- Minimum 95% confidence level
- Minimum 100 conversions per variant
- Run for at least one full business cycle
- Watch for novelty effects

**RULE-008: Segment Everything**
Analyze metrics by:
- Traffic source (organic, paid, referral, direct)
- Device type (mobile, desktop, tablet)
- User type (new, returning, customer)
- Geography (country, region, city)
- Time period (day, week, month, season)

**RULE-009: Real-Time Monitoring**
Set up alerts for:
- Traffic drops > 20%
- Conversion rate drops > 15%
- Error rate spikes
- Page load time increases
- Campaign budget depletion

**RULE-010: Privacy-First Tracking**
- Comply with GDPR, CCPA regulations
- Implement consent management
- Anonymize IP addresses
- Provide opt-out mechanisms
- Document data retention policies

---

## Quick Reference

### Key Marketing Metrics

**Acquisition Metrics:**
- Traffic (sessions, users, pageviews)
- Traffic sources (organic, paid, referral, direct)
- Cost per Click (CPC)
- Cost per Acquisition (CPA)
- Customer Acquisition Cost (CAC)

**Engagement Metrics:**
- Bounce rate (% single-page sessions)
- Pages per session
- Average session duration
- Scroll depth
- Video completion rate

**Conversion Metrics:**
- Conversion rate (% visitors who convert)
- Micro-conversion rate (% who take intermediate action)
- Form completion rate
- Cart abandonment rate
- Checkout completion rate

**Retention Metrics:**
- Return visitor rate
- Day 1, 7, 30 retention
- Churn rate
- Customer lifetime (months/years)
- Net Promoter Score (NPS)

**Revenue Metrics:**
- Revenue per Visitor (RPV)
- Average Order Value (AOV)
- Customer Lifetime Value (LTV)
- LTV:CAC ratio (target: 3:1 or higher)
- Payback period (months to recover CAC)

### Testing Framework

**A/B Test Checklist:**
- [ ] Clear hypothesis ("Changing X will increase Y because Z")
- [ ] One variable changed
- [ ] Sufficient sample size calculated
- [ ] Random traffic split
- [ ] Tracking implemented correctly
- [ ] Run duration planned (minimum 1 week)
- [ ] Success criteria defined
- [ ] Statistical significance threshold set (95%)

**What to Test:**
- Headlines and value propositions
- CTA copy and button color
- Page layout and structure
- Images and videos
- Form length and fields
- Pricing display
- Social proof placement
- Navigation structure

**Testing Prioritization (PIE Framework):**
- **P**otential: How much improvement is possible?
- **I**mportance: How valuable is the traffic?
- **E**ase: How easy is it to implement?

Score each 1-10, multiply, prioritize highest scores.

### Analytics Tools Stack

**Core Analytics:**
- Google Analytics 4 (GA4) - Free, comprehensive
- Mixpanel - Product analytics, event-based
- Amplitude - User behavior, cohort analysis
- Heap - Auto-capture, retroactive analysis

**Heatmaps & Session Recording:**
- Hotjar - Heatmaps, recordings, surveys
- FullStory - Session replay, error tracking
- Crazy Egg - Heatmaps, A/B testing
- Microsoft Clarity - Free heatmaps and recordings

**A/B Testing:**
- Google Optimize (sunset 2023, use alternatives)
- Optimizely - Enterprise testing platform
- VWO - Visual editor, multivariate testing
- AB Tasty - Testing and personalization

**Attribution:**
- Google Analytics 4 - Multi-touch attribution
- HubSpot - Marketing attribution
- Segment - Customer data platform
- Ruler Analytics - Call tracking attribution

### Dashboard Structure

**Executive Dashboard:**
- North Star Metric (trend)
- Revenue (actual vs. target)
- New customers
- CAC and LTV
- Top 3 channels by ROI

**Marketing Dashboard:**
- Traffic by source
- Conversion rate by channel
- Campaign performance
- Content performance
- Lead quality metrics

**Product Dashboard:**
- Active users (DAU, WAU, MAU)
- Feature adoption
- User retention cohorts
- Engagement metrics
- Churn indicators

---

## Metadata

- **Related Skills:** seo-optimization.md, email-campaigns.md, social-media.md
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
