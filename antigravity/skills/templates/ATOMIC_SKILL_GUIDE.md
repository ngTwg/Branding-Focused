---
name: "Atomic Skill Creation Guide"
tags: ["antigravity", "atomic", "c:", "creation", "frontend", "gemini", "guide", "header", "<YOUR_USERNAME>", "name", "optimization", "overview", "required", "section", "seo", "skill", "structure", "template", "templates", "users"]
tier: 4
risk: "medium"
estimated_tokens: 3662
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# Atomic Skill Creation Guide

> **Purpose:** Guide for creating token-efficient atomic skills  
> **Target Size:** < 20KB per skill  
> **Version:** 1.0.0 (v6.5.0-SLIM)

---

## Overview

This guide explains how to create atomic skills that are:
- **Token-efficient:** < 20KB per file (typically 15-20KB)
- **Self-contained:** Can be loaded independently
- **Actionable:** Focused on practical rules and quick reference
- **Scannable:** Easy to navigate and find information quickly

---

## Template Structure

### 1. Header Section (Required)

```markdown
# [Skill Name]

> **Tier:** [1-4]  
> **Tags:** `[tag1, tag2, tag3, tag4, tag5]`  
> **When to use:** [Brief description]
```

**Guidelines:**
- **Skill Name:** Clear, descriptive, 2-4 words max
- **Tier:** 1=Simple, 2=Standard, 3=Advanced, 4=Critical/Life-Critical
- **Tags:** 3-5 relevant tags for routing (lowercase, hyphenated)
- **When to use:** One sentence describing trigger conditions

**Examples:**
```markdown
# SEO Optimization
> **Tier:** 2  
> **Tags:** `[seo, search-optimization, programmatic-seo, seo-audit]`  
> **When to use:** SEO strategy, programmatic SEO, SEO audits, search optimization
```

---

### 2. Overview Section (Required)

**Purpose:** Provide context and scope in 2-3 sentences.

**Guidelines:**
- Explain WHAT the skill covers
- Explain WHY it matters
- Mention key capabilities or frameworks
- Keep it under 100 words

**Example:**
```markdown
## Overview

Expert guidance for SEO optimization including programmatic SEO at scale, 
comprehensive SEO audits, and search optimization strategies. Covers both 
technical and content SEO with actionable frameworks.
```

---

### 3. Rules Section (Required)

**Purpose:** Core actionable rules (5-10 rules maximum).

**Guidelines:**
- **Rule Limit:** 5-10 rules (if you need more, split into multiple skills)
- **Format:** `**RULE-XXX: [Action-Oriented Title]**`
- **Content:** 
  - Explain WHY the rule matters
  - Provide context and edge cases
  - Include code/text examples
  - Use ❌/✅ for anti-patterns and best practices
- **Ordering:** Most important/frequent rules first

**Example:**
```markdown
**RULE-001: Clarity Over Cleverness**
If you have to choose between clear and creative, choose clear. Every 
sentence should have one job. Remove words that don't add meaning.

**RULE-002: Benefits Over Features**
Always connect features to outcomes. Features = what it does. Benefits = 
what that means for the customer.

```markdown
❌ "Our platform uses AI-powered analytics"
✅ "Our AI-powered analytics surface insights you'd miss manually—so you 
   can make better decisions in half the time"
```
```

**Rule Writing Tips:**
- Start with action verbs: "Use", "Avoid", "Always", "Never"
- Be specific: "< 3 seconds" not "fast"
- Include rationale: "...because X causes Y"
- One concept per rule
- Self-contained (don't require reading other rules)

---

### 4. Quick Reference Section (Required)

**Purpose:** Scannable reference material for quick lookup during execution.

**Guidelines:**
- Use tables, checklists, or structured lists
- 3-4 subsections maximum
- Focus on patterns, templates, and troubleshooting
- Keep each subsection under 15 lines

**Common Subsection Types:**

#### A. Checklists
```markdown
### Technical SEO Checklist

- [ ] Site crawlable and indexable
- [ ] XML sitemap present and submitted
- [ ] Robots.txt configured correctly
- [ ] HTTPS implemented
- [ ] Page speed < 3 seconds
```

#### B. Pattern Tables
```markdown
### Common Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Templates | "[Type] template" searches | Resume templates |
| Comparisons | "[X] vs [Y]" pages | Notion vs Airtable |
```

#### C. Problem-Solution Tables
```markdown
### Common Problems & Fixes

| Problem | Fix |
|---------|-----|
| Wall of Features | Add "which means..." after each feature |
| Corporate Speak | Ask "How would a human say this?" |
```

#### D. Decision Trees
```markdown
### Routing Logic

```
User mentions "SEO" → Load seo-optimization.md
User mentions "copy" → Load content-strategy.md
User mentions "social" → Load social-media.md
```
```

---

### 5. Metadata Section (Required)

**Purpose:** Track relationships and versioning.

**Format:**
```markdown
## Metadata

- **Related Skills:** [skill1.md], [skill2.md], [skill3.md]
- **Dependencies:** [None | List required skills]
- **Version:** 1.0.0
- **Last Updated:** [YYYY-MM-DD]
```

**Guidelines:**
- **Related Skills:** Skills that are often used together
- **Dependencies:** Skills that MUST be loaded first (rare)
- **Version:** Semantic versioning (major.minor.patch)
- **Last Updated:** ISO date format

---

## Size Optimization Techniques

### Target: < 20KB per file

**Techniques to stay under 20KB:**

1. **Limit Rules to 10 Maximum**
   - If you need more, split into multiple atomic skills
   - Example: Split "Marketing" into "SEO", "Content", "Social", "Email"

2. **Use Tables Over Prose**
   - Tables are more scannable and token-efficient
   - Convert long paragraphs into structured tables

3. **Remove Redundancy**
   - Don't repeat information across sections
   - Reference other skills instead of duplicating content

4. **Focus on Actionable Content**
   - Remove theory and background
   - Keep only practical, executable guidance

5. **Use Code Blocks Sparingly**
   - Only include essential examples
   - Keep code snippets under 10 lines

6. **Compress Quick Reference**
   - Use abbreviations in tables
   - Combine related items
   - Remove obvious information

**Size Checking:**
```bash
# Check file size
ls -lh atomic-skill.md

# Target: < 20KB (20,480 bytes)
# Ideal: 15-18KB for future additions
```

---

## Atomization Process

### When to Split a Large Skill

**Indicators a skill should be split:**
- File size > 100KB
- More than 15 rules
- Covers multiple distinct domains
- Takes > 30 seconds to scan
- Multiple unrelated "Quick Reference" sections

**Splitting Strategy:**

1. **Identify Natural Boundaries**
   - Look for distinct topics or domains
   - Group related rules together
   - Aim for 5-10 rules per atomic skill

2. **Create Master Inventory**
   - Keep a lightweight index file
   - List all atomic skills with brief descriptions
   - Include routing logic

3. **Maintain Backward Compatibility**
   - Keep original file as navigation layer
   - Reference atomic skills
   - Document migration in metadata

**Example: Marketing Skill Split**

```
Original: specialized-marketing.md (229KB)
    ↓
Split into:
├── marketing-master-inventory.md (7.5KB) - Index
├── marketing/seo-optimization.md (19.8KB)
├── marketing/content-strategy.md (18.2KB)
├── marketing/social-media.md (17.5KB)
├── marketing/email-campaigns.md (19.1KB)
└── marketing/analytics-tracking.md (18.9KB)

Token savings: 60% for single-skill loads
```

---

## Quality Checklist

Before finalizing an atomic skill, verify:

### Content Quality
- [ ] All rules are actionable (not just informational)
- [ ] Examples are concrete and realistic
- [ ] Anti-patterns (❌) and best practices (✅) included
- [ ] No redundant information
- [ ] No broken references to other skills

### Structure Quality
- [ ] Header section complete (Tier, Tags, When to use)
- [ ] Overview is 2-3 sentences
- [ ] 5-10 rules maximum
- [ ] Quick Reference has 3-4 subsections
- [ ] Metadata section complete

### Size & Efficiency
- [ ] File size < 20KB
- [ ] Ideally 15-18KB (room for future additions)
- [ ] No unnecessary prose
- [ ] Tables used where appropriate
- [ ] Code examples are minimal

### Usability
- [ ] Can be understood without reading other skills
- [ ] Quick Reference is scannable in < 10 seconds
- [ ] Rules are ordered by importance
- [ ] Tags are accurate for routing

### Integration
- [ ] Added to relevant master inventory
- [ ] Routing logic updated in MASTER_ROUTER.md
- [ ] Related skills cross-referenced
- [ ] Version and date updated

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Too Much Theory
**Problem:** Long explanations of concepts without actionable guidance.

**Fix:** Focus on "how to" not "what is". Move theory to separate documentation.

### ❌ Mistake 2: Too Many Rules
**Problem:** 20+ rules make the skill hard to scan and remember.

**Fix:** Split into multiple atomic skills. Aim for 5-10 rules per skill.

### ❌ Mistake 3: Duplicate Content
**Problem:** Repeating information from other skills.

**Fix:** Reference other skills instead. Use "See [skill.md] for details."

### ❌ Mistake 4: Vague Examples
**Problem:** Generic examples that don't illustrate the point.

**Fix:** Use specific, realistic examples from actual use cases.

### ❌ Mistake 5: Poor Organization
**Problem:** Rules in random order, no logical flow.

**Fix:** Order by importance/frequency. Group related rules together.

### ❌ Mistake 6: Missing Quick Reference
**Problem:** No scannable reference material.

**Fix:** Always include tables, checklists, or decision trees.

### ❌ Mistake 7: Broken Dependencies
**Problem:** References to skills that don't exist or are renamed.

**Fix:** Verify all skill references. Update when skills are refactored.

---

## Examples of Good Atomic Skills

### Example 1: SEO Optimization (19.8KB)
**Why it's good:**
- Clear scope (SEO only, not all marketing)
- 10 focused rules
- Comprehensive Quick Reference (4 subsections)
- Actionable checklists
- Specific examples

### Example 2: Content Strategy (18.2KB)
**Why it's good:**
- Single domain (copywriting/editing)
- Seven Sweeps framework clearly explained
- Problem-solution tables
- Page structure templates
- Under 20KB with room to grow

### Example 3: Email Campaigns (19.1KB)
**Why it's good:**
- Focused on email marketing only
- Sequence templates included
- Personalization hierarchy
- Deliverability fundamentals
- Practical examples

---

## Master Inventory Integration

After creating atomic skills, update the master inventory:

### Master Inventory Structure

```markdown
# [Category] Master Inventory

## Atomic Skills (Core - Always Load)

### 1. [Skill Name]
**File:** `[category]/[skill-name].md` ([size]KB)  
**Tags:** `[tags]`  
**Use when:** [trigger conditions]

**Key capabilities:**
- [Capability 1]
- [Capability 2]
- [Capability 3]

**Quick access:** [When to load this skill]

---

### 2. [Next Skill]
[Same format]

---

## Extended Skills (Load on Demand)

### [Extended Skill 1]
**Topics:** [Brief list]
**Use when:** [Conditions]

---

## Usage Guidelines

### Token Efficiency Strategy

**Tier 1 Tasks:** Load 1-2 atomic skills
**Tier 2 Tasks:** Load 2-3 atomic skills
**Tier 3 Tasks:** Load 3-4 atomic skills
**Tier 4 Tasks:** Load 4-5 atomic skills + extended

### Routing Logic

```
User mentions "[keyword]" → Load [skill].md
User mentions "[keyword]" → Load [skill].md
```
```

---

## Versioning & Updates

### Version Numbering

- **Major (X.0.0):** Breaking changes, complete restructure
- **Minor (1.X.0):** New rules added, significant content additions
- **Patch (1.0.X):** Typo fixes, minor clarifications, example updates

### Update Process

1. Make changes to atomic skill
2. Update "Last Updated" date
3. Increment version number
4. Update master inventory if needed
5. Test routing logic
6. Commit with descriptive message

### Deprecation

When deprecating a skill:
1. Mark as deprecated in header
2. Add deprecation notice in Overview
3. Reference replacement skill
4. Keep file for 2 versions (backward compatibility)
5. Remove after 2 versions

---

## Testing Your Atomic Skill

### Manual Testing

1. **Size Check:**
   ```bash
   ls -lh [skill-name].md
   # Should be < 20KB
   ```

2. **Readability Check:**
   - Can you scan Quick Reference in < 10 seconds?
   - Are rules clear without reading other skills?
   - Are examples concrete and realistic?

3. **Routing Check:**
   - Test with sample queries
   - Verify correct skill is loaded
   - Check for conflicts with other skills

4. **Integration Check:**
   - Load with related skills
   - Verify no duplicate content
   - Check cross-references work

### Automated Testing (Future)

```python
# Future: Automated skill validation
def validate_atomic_skill(file_path):
    # Check file size < 20KB
    # Verify required sections present
    # Count rules (should be 5-10)
    # Validate metadata format
    # Check for broken references
    pass
```

---

## FAQ

### Q: How do I decide if a skill should be atomic or extended?

**A:** Atomic skills are:
- Frequently used (loaded in > 20% of tasks)
- Self-contained (don't require other skills)
- Actionable (have clear rules and examples)
- Focused (single domain or framework)

Extended skills are:
- Rarely used (loaded in < 20% of tasks)
- Supplementary (add depth to atomic skills)
- Informational (more reference than rules)

### Q: What if my skill needs more than 10 rules?

**A:** Split it into multiple atomic skills. Example:
- "Frontend Development" → "React Patterns", "CSS Styling", "Performance"
- "Security" → "Attack Vectors", "Cryptography", "Compliance"

### Q: How do I handle dependencies between skills?

**A:** 
1. **Prefer self-contained skills** (no dependencies)
2. **Use cross-references** for related content
3. **Document dependencies** in metadata
4. **Load dependencies automatically** in routing logic

### Q: Can I include code examples?

**A:** Yes, but keep them minimal:
- Max 10 lines per example
- Only essential examples
- Use comments to explain
- Prefer pseudo-code over full implementations

### Q: How often should I update atomic skills?

**A:** 
- **Patch updates:** As needed (typos, clarifications)
- **Minor updates:** Quarterly (new rules, examples)
- **Major updates:** Annually or when domain changes significantly

---

## Resources

### Templates
- `atomic-skill-template.md` - Base template for new skills
- `master-inventory-template.md` - Template for category inventories

### Examples
- `marketing/seo-optimization.md` - SEO skill example
- `marketing/content-strategy.md` - Content skill example
- `marketing-master-inventory.md` - Master inventory example

### Tools
- `scripts/check_skill_size.py` - Validate skill file sizes
- `scripts/atomize_skill.py` - Helper for splitting large skills
- `scripts/update_master_inventory.py` - Auto-update inventories

---

## Changelog

### Version 1.0.0 (2024-03-26)
- Initial atomic skill guide
- Template structure defined
- Size optimization techniques documented
- Quality checklist created
- Examples from marketing atomization

---

**Maintained by:** Antigravity Skills System v6.5.0-SLIM  
**Related:** Task 30.3 - Create skill atom template  
**Next:** Task 30.4 - Implement skill_cache.py

