# Atomic Skill Templates

> **Purpose:** Standardized templates for creating token-efficient atomic skills  
> **Version:** 1.0.0 (v6.5.0-SLIM)  
> **Created:** 2024-03-26

---

## Overview

This directory contains templates and guides for creating atomic skills that are optimized for token efficiency and ease of use. All atomic skills should follow these templates to ensure consistency across the Antigravity skills system.

---

## Files in This Directory

### 1. `atomic-skill-template.md` (3.01KB)
**Purpose:** Base template for creating new atomic skills

**Use this when:**
- Creating a new atomic skill from scratch
- Splitting a large skill into smaller atomic skills
- Standardizing an existing skill

**Key features:**
- Pre-formatted header with Tier, Tags, When to use
- 10 rule slots with example formatting
- Quick Reference section with common patterns
- Metadata section for tracking relationships

**How to use:**
1. Copy `atomic-skill-template.md` to your target location
2. Rename to `[skill-name].md`
3. Fill in all sections following the guidelines
4. Verify file size < 20KB
5. Add to relevant master inventory

---

### 2. `ATOMIC_SKILL_GUIDE.md` (14.95KB)
**Purpose:** Comprehensive guide for creating and maintaining atomic skills

**Use this when:**
- Learning how to create atomic skills
- Understanding the atomization process
- Troubleshooting skill creation issues
- Updating existing skills

**Key sections:**
- Template structure explanation
- Size optimization techniques
- Atomization process (when and how to split)
- Quality checklist
- Common mistakes to avoid
- Master inventory integration
- Versioning and updates

**How to use:**
1. Read before creating your first atomic skill
2. Reference during skill creation
3. Use quality checklist before finalizing
4. Consult when splitting large skills

---

### 3. `atomic-skill-example.md` (6.74KB)
**Purpose:** Filled-in example demonstrating best practices

**Use this when:**
- Need a concrete example of a well-structured skill
- Want to see how to format rules and quick reference
- Looking for inspiration on structure

**Key features:**
- Complete API Design Patterns skill
- 10 well-formatted rules with examples
- Comprehensive Quick Reference with tables
- Proper use of code blocks and formatting

**How to use:**
1. Study the structure and formatting
2. Use as reference when creating similar skills
3. Copy patterns (tables, decision trees) as needed

---

## Quick Start

### Creating Your First Atomic Skill

1. **Copy the template:**
   ```bash
   cp atomic-skill-template.md ../[category]/[skill-name].md
   ```

2. **Fill in the header:**
   - Choose appropriate Tier (1-4)
   - Add 3-5 relevant tags
   - Write one-sentence "When to use"

3. **Write the Overview:**
   - 2-3 sentences
   - Explain what, why, and key capabilities

4. **Create 5-10 Rules:**
   - Action-oriented titles
   - Include WHY, not just WHAT
   - Add ❌/✅ examples
   - Order by importance

5. **Build Quick Reference:**
   - 3-4 subsections
   - Use tables, checklists, or decision trees
   - Focus on scannable content

6. **Complete Metadata:**
   - List related skills
   - Note dependencies (if any)
   - Set version to 1.0.0
   - Add current date

7. **Verify Quality:**
   - Check file size < 20KB
   - Run through quality checklist
   - Test readability

8. **Integrate:**
   - Add to master inventory
   - Update routing logic
   - Cross-reference related skills

---

## Size Requirements

| File Type | Target Size | Maximum Size | Notes |
|-----------|-------------|--------------|-------|
| Template | < 5KB | 5KB | Keep minimal for easy copying |
| Atomic Skill | 15-18KB | 20KB | Leave room for future additions |
| Master Inventory | 5-10KB | 15KB | Lightweight index only |
| Guide/Documentation | 10-20KB | 30KB | Comprehensive but focused |

---

## Quality Standards

### All atomic skills must:
- ✅ Be < 20KB in size
- ✅ Have 5-10 rules (not more, not less)
- ✅ Include Quick Reference section
- ✅ Use consistent formatting
- ✅ Have complete metadata
- ✅ Be self-contained (no required dependencies)
- ✅ Include concrete examples
- ✅ Use ❌/✅ for anti-patterns and best practices

### All atomic skills should:
- ✅ Be scannable in < 30 seconds
- ✅ Have actionable rules (not just informational)
- ✅ Include tables or checklists in Quick Reference
- ✅ Cross-reference related skills
- ✅ Be focused on a single domain
- ✅ Have clear, descriptive names
- ✅ Use consistent terminology

---

## Atomization Success Metrics

### Token Efficiency
- **Target:** 60% reduction in tokens for single-skill loads
- **Measurement:** Compare loading full file vs. atomic skill
- **Example:** Marketing skills achieved 60% savings

### Load Time
- **Target:** 40% faster load time
- **Measurement:** Time to load and parse skill
- **Benefit:** Faster routing and execution

### Cache Hit Rate
- **Target:** 70% cache hit rate
- **Measurement:** Percentage of skills loaded from cache
- **Benefit:** Reduced redundant loading

### Usability
- **Target:** < 30 seconds to scan and understand
- **Measurement:** User testing and feedback
- **Benefit:** Faster task execution

---

## Examples of Successful Atomization

### Marketing Skills (Task 30.2)
**Original:** `specialized-marketing.md` (229.77KB)

**Atomized into:**
- `marketing-master-inventory.md` (7.57KB) - Index
- `marketing/seo-optimization.md` (19.8KB)
- `marketing/content-strategy.md` (18.2KB)
- `marketing/social-media.md` (17.5KB)
- `marketing/email-campaigns.md` (19.1KB)
- `marketing/analytics-tracking.md` (18.9KB)

**Results:**
- ✅ 60% token savings for single-skill loads
- ✅ All atomic skills < 20KB
- ✅ Maintained backward compatibility
- ✅ Improved routing precision

---

## Common Use Cases

### Use Case 1: Creating a New Skill
1. Copy `atomic-skill-template.md`
2. Follow structure in `ATOMIC_SKILL_GUIDE.md`
3. Reference `atomic-skill-example.md` for formatting
4. Verify against quality checklist

### Use Case 2: Splitting a Large Skill
1. Read "Atomization Process" in guide
2. Identify natural boundaries (5-10 rules per skill)
3. Create atomic skills using template
4. Create master inventory
5. Update routing logic

### Use Case 3: Updating an Existing Skill
1. Check current version in metadata
2. Make changes following template structure
3. Increment version number
4. Update "Last Updated" date
5. Update master inventory if needed

### Use Case 4: Reviewing Skill Quality
1. Use quality checklist in guide
2. Check file size < 20KB
3. Verify 5-10 rules
4. Test scannability (< 30 seconds)
5. Validate examples and formatting

---

## Integration with Antigravity System

### Routing Integration
Atomic skills integrate with `MASTER_ROUTER.md`:

```markdown
User mentions "[keyword]" → Load [atomic-skill].md
```

### Master Inventory Integration
Each category has a master inventory that indexes atomic skills:

```markdown
# [Category] Master Inventory

## Atomic Skills (Core - Always Load)

### 1. [Skill Name]
**File:** `[category]/[skill-name].md` ([size]KB)
**Tags:** `[tags]`
**Use when:** [conditions]
```

### Cache Integration (Future - Task 30.4)
Atomic skills will be cached using LRU cache:
- 20 skill slots
- Automatic eviction
- Hit rate tracking

---

## Maintenance

### Regular Updates
- **Quarterly:** Review and update examples
- **Annually:** Major version updates if domain changes
- **As needed:** Patch updates for typos and clarifications

### Deprecation Process
1. Mark skill as deprecated in header
2. Add deprecation notice in Overview
3. Reference replacement skill
4. Keep for 2 versions (backward compatibility)
5. Remove after 2 versions

### Version Control
- Use semantic versioning (major.minor.patch)
- Document changes in skill metadata
- Update master inventory when versions change

---

## Troubleshooting

### Problem: Skill is too large (> 20KB)
**Solutions:**
- Remove redundant content
- Convert prose to tables
- Split into multiple atomic skills
- Move extended content to separate skill

### Problem: Too many rules (> 10)
**Solutions:**
- Split into multiple atomic skills
- Combine related rules
- Move less important rules to extended skill

### Problem: Skill is too generic
**Solutions:**
- Narrow the scope
- Focus on specific use cases
- Add concrete examples
- Split into domain-specific skills

### Problem: Skill has many dependencies
**Solutions:**
- Make skill more self-contained
- Include essential information inline
- Use cross-references instead of dependencies

---

## Resources

### Templates
- `atomic-skill-template.md` - Base template
- `atomic-skill-example.md` - Filled example

### Documentation
- `ATOMIC_SKILL_GUIDE.md` - Comprehensive guide
- `README.md` - This file

### Related Files
- `../MASTER_ROUTER.md` - Routing logic
- `../specialized/marketing-master-inventory.md` - Example inventory
- `../../docs/V62_RESILIENCE_UPGRADE_COMPLETE.md` - Context

### Tools (Future)
- `scripts/check_skill_size.py` - Validate sizes
- `scripts/atomize_skill.py` - Split large skills
- `scripts/update_master_inventory.py` - Auto-update inventories

---

## Success Criteria (Task 30.3)

- [x] Template file created at `atomic-skill-template.md`
- [x] Template size < 5KB (actual: 3.01KB) ✅
- [x] Clear documentation on how to use template (ATOMIC_SKILL_GUIDE.md)
- [x] Example filled-in template (atomic-skill-example.md)
- [x] Easy to copy and adapt
- [x] Includes metadata (tags, tier, dependencies)
- [x] Max 10 rules structure
- [x] Quick Reference section included
- [x] All files < 20KB ✅

---

## Next Steps

### Immediate (Task 30.3 Complete)
- ✅ Template created and documented
- ✅ Example provided
- ✅ Quality standards defined

### Next Task (30.4)
- [ ] Implement `skill_cache.py` with LRU cache
- [ ] 20 slot capacity
- [ ] Hit rate tracking
- [ ] Integration with HybridRetriever

### Future Tasks (30.5+)
- [ ] Batch atomization of remaining large skills
- [ ] Automated validation scripts
- [ ] Performance benchmarking
- [ ] Cache optimization

---

**Maintained by:** Antigravity Skills System v6.5.0-SLIM  
**Task:** 30.3 - Create skill atom template  
**Status:** COMPLETE ✅  
**Next:** Task 30.4 - Implement skill_cache.py

