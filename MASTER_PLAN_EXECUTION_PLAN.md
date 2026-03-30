# 📋 MASTER PLAN EXECUTION - DETAILED PLANNING

> **Project:** Skills System Consolidation  
> **Version:** v6.3.0 → v6.4.0  
> **Estimated Time:** 8 hours  
> **Status:** 🔵 PLANNING PHASE

---

## 🎯 OBJECTIVE

Consolidate 250+ skills into unified system, reduce GEMINI.md from 25,167 lines to <300 lines, improve maintainability and token efficiency.

---

## 📊 PHASE OVERVIEW

| Phase | Duration | Status | Dependencies |
|-------|----------|--------|--------------|
| Phase 1: Analysis & Inventory | 30 min | ⏳ TODO | None |
| Phase 2: Directory Restructure | 1 hour | ⏳ TODO | Phase 1 |
| Phase 3: Create New Skills | 2 hours | ⏳ TODO | Phase 2 |
| Phase 4: Refactor GEMINI.md | 1 hour | ⏳ TODO | Phase 3 |
| Phase 5: Update Master Router | 1 hour | ⏳ TODO | Phase 4 |
| Phase 6: Cleanup & Optimize | 30 min | ⏳ TODO | Phase 5 |
| Phase 7: Testing & Validation | 1 hour | ⏳ TODO | Phase 6 |
| Phase 8: Documentation | 30 min | ⏳ TODO | Phase 7 |

**Total:** 8 hours

---

## 📝 PHASE 1: ANALYSIS & INVENTORY (30 minutes)

### Objective
Create complete inventory of all skills and identify duplicates.

### Tasks

#### Task 1.1: Scan antigravity/skills/ ⏳ TODO
**Time:** 10 minutes  
**Action:**
```bash
find antigravity/skills -name "*.md" -o -name "skill.md" > skills_antigravity.txt
```
**Output:** `skills_antigravity.txt`  
**Success Criteria:** File contains all skill paths

#### Task 1.2: Scan .ai-skills/ (if exists) ⏳ TODO
**Time:** 5 minutes  
**Action:**
```bash
find .ai-skills -name "*.md" > skills_ai.txt 2>/dev/null || echo "No .ai-skills directory"
```
**Output:** `skills_ai.txt` or confirmation no directory  
**Success Criteria:** Complete scan or confirmed absence

#### Task 1.3: Create SKILLS_INVENTORY.md ⏳ TODO
**Time:** 10 minutes  
**Action:** Analyze and categorize all found skills  
**Output:** `SKILLS_INVENTORY.md` with:
- Total count
- Category breakdown
- File paths
- Brief descriptions

**Success Criteria:**
- All skills listed
- Categories identified
- No missing files

#### Task 1.4: Identify Duplicates ⏳ TODO
**Time:** 5 minutes  
**Action:** Compare skills by name and content  
**Output:** `DUPLICATES_REPORT.md` with:
- Duplicate pairs
- Recommended merge strategy
- Priority order

**Success Criteria:**
- All duplicates identified
- Merge strategy clear

---

## 📦 PHASE 2: DIRECTORY RESTRUCTURE (1 hour)

### Objective
Create clean `.ai-skills/` structure and migrate existing skills.

### Tasks

#### Task 2.1: Create Directory Structure ⏳ TODO
**Time:** 10 minutes  
**Action:** Create all category directories  
**Directories to create:**
```
.ai-skills/
├── frontend/
├── backend/
├── security/
├── devops/
├── workflows/
├── data-engineering/
├── deep-tech/
├── specialized/
└── beyond/
```
**Success Criteria:** All 9 directories exist

#### Task 2.2: Create Master Files ⏳ TODO
**Time:** 15 minutes  
**Action:** Create index and router files  
**Files to create:**
- `.ai-skills/index-skills.md` (skeleton)
- `.ai-skills/MASTER_ROUTER.md` (copy from antigravity/skills/)

**Success Criteria:** Files created with basic structure

#### Task 2.3: Migrate Frontend Skills ⏳ TODO
**Time:** 10 minutes  
**Action:** Move/copy frontend skills to `.ai-skills/frontend/`  
**Skills:** React, CSS, Performance, Forms, PWA, etc.  
**Success Criteria:** All frontend skills in new location

#### Task 2.4: Migrate Backend Skills ⏳ TODO
**Time:** 10 minutes  
**Action:** Move/copy backend skills to `.ai-skills/backend/`  
**Skills:** API, Database, Auth, Validation, etc.  
**Success Criteria:** All backend skills in new location

#### Task 2.5: Migrate Remaining Categories ⏳ TODO
**Time:** 15 minutes  
**Action:** Move/copy all other category skills  
**Categories:** Security, DevOps, Workflows, Data, Deep Tech, Specialized, Beyond  
**Success Criteria:** All skills migrated, organized by category

---

## 📝 PHASE 3: CREATE NEW SKILLS (2 hours)

### Objective
Create missing skills from MASTER_PLAN specification.

### Tasks

#### Task 3.1: Beyond Horizon Skills (12 skills) ⏳ TODO
**Time:** 1 hour  
**Skills to create:**

- ⏳ spatial-os-xr.md
- ⏳ meta-rules-agentic.md
- ⏳ astrodynamics.md
- ⏳ fully-homomorphic-encryption.md
- ⏳ neuromorphic-snn.md
- ⏳ compiler-mlir.md
- ⏳ zero-knowledge-proofs.md
- ⏳ stochastic-superoptimization.md
- ⏳ photonic-computing.md
- ⏳ materials-informatics.md
- ⏳ plasma-fusion.md
- ⏳ planetary-geoengineering.md

**Success Criteria:** All 12 skills created with proper format

#### Task 3.2: Specialized Domain Skills (15 skills) ⏳ TODO
**Time:** 1 hour  
**Skills to create:**
- ⏳ legaltech.md
- ⏳ proptech.md
- ⏳ retail-supply-chain.md
- ⏳ govtech.md
- ⏳ humanitarian-tech.md
- ⏳ autonomous-logistics.md
- ⏳ algorithmic-economics.md
- ⏳ generative-media.md
- ⏳ neuro-symbolic-ai.md
- ⏳ macro-economics-cbdc.md
- ⏳ deep-space-networking.md
- ⏳ cognitive-security.md
- ⏳ topological-data-analysis.md
- ⏳ quantum-computing.md
- ⏳ bioinformatics.md

**Success Criteria:** All 15 skills created with proper format

---

## 🔄 PHASE 4: REFACTOR GEMINI.md (1 hour)

### Objective
Reduce GEMINI.md from 25,167 lines to <300 lines.

### Tasks

#### Task 4.1: Backup Current GEMINI.md ⏳ TODO
**Time:** 2 minutes  
**Action:** `cp GEMINI.md GEMINI_v6.3_BACKUP.md`  
**Success Criteria:** Backup file created

#### Task 4.2: Create New GEMINI.md Structure ⏳ TODO
**Time:** 20 minutes  
**Action:** Write new compact GEMINI.md with:
- Core rules (5 rules)
- Master Router reference
- Skills system overview
- Links to detailed docs

**Target:** <300 lines  
**Success Criteria:** New structure complete, all essential rules included

#### Task 4.3: Extract Content to Separate Files ⏳ TODO
**Time:** 30 minutes  
**Action:** Move detailed content to:
- `.ai-skills/DETAILED_RULES.md` (technical details)
- `.ai-skills/EXAMPLES.md` (code examples)
- `.ai-skills/ADVANCED_TOPICS.md` (advanced features)

**Success Criteria:** Content organized, no duplication

#### Task 4.4: Verify All References ⏳ TODO
**Time:** 8 minutes  
**Action:** Check all links and references work  
**Success Criteria:** No broken links, all paths correct

---

## 🎨 PHASE 5: UPDATE MASTER ROUTER (1 hour)

### Objective
Update Master Router with all new skills and improved routing logic.

### Tasks

#### Task 5.1: Update Skill Mappings ⏳ TODO
**Time:** 30 minutes  
**Action:** Add all 27 new skills to routing table  
**Success Criteria:** All skills mapped with correct tags and tiers

#### Task 5.2: Update Decision Tree ⏳ TODO
**Time:** 20 minutes  
**Action:** Refine routing logic for new categories  
**Success Criteria:** Decision tree covers all scenarios

#### Task 5.3: Add Examples ⏳ TODO
**Time:** 10 minutes  
**Action:** Add routing examples for each category  
**Success Criteria:** Clear examples for all 9 categories

---

## 🧹 PHASE 6: CLEANUP & OPTIMIZE (30 minutes)

### Objective
Remove duplicates, fix references, optimize structure.

### Tasks

#### Task 6.1: Remove Duplicate Skills ⏳ TODO
**Time:** 10 minutes  
**Action:** Delete or merge duplicate skills identified in Phase 1  
**Success Criteria:** No duplicates remain

#### Task 6.2: Update All References ⏳ TODO
**Time:** 10 minutes  
**Action:** Find and replace old paths with new paths  
**Success Criteria:** All references updated

#### Task 6.3: Optimize File Sizes ⏳ TODO
**Time:** 10 minutes  
**Action:** Compress verbose content, remove redundancy  
**Success Criteria:** Average skill file <500 lines

---

## ✅ PHASE 7: TESTING & VALIDATION (1 hour)

### Objective
Verify system works correctly with new structure.

### Tasks

#### Task 7.1: Test Master Router ⏳ TODO
**Time:** 20 minutes  
**Test Cases:**
- "Tạo app quản lý sách" → Load correct skills?
- "Fix bug trong checkout" → Load debug skills first?
- "Tạo firmware máy bơm insulin" → Tier 4, ask FDA?

**Success Criteria:** All test cases pass

#### Task 7.2: Validate Structure ⏳ TODO
**Time:** 20 minutes  
**Checks:**
- All skills have correct format
- All links work
- No duplicates
- Categories complete

**Success Criteria:** All checks pass

#### Task 7.3: Test with AI Agent ⏳ TODO
**Time:** 20 minutes  
**Action:** Load new GEMINI.md and test with sample tasks  
**Success Criteria:** AI loads correct skills, follows routing logic

---

## 📚 PHASE 8: DOCUMENTATION (30 minutes)

### Objective
Document changes and create migration guide.

### Tasks

#### Task 8.1: Update README Files ⏳ TODO
**Time:** 10 minutes  
**Files to update:**
- Project root README.md
- .ai-skills/README.md
- Each category README.md

**Success Criteria:** All READMEs current

#### Task 8.2: Create CHANGELOG Entry ⏳ TODO
**Time:** 10 minutes  
**Action:** Document v6.4.0 changes  
**Success Criteria:** Complete changelog entry

#### Task 8.3: Create MIGRATION_GUIDE.md ⏳ TODO
**Time:** 10 minutes  
**Content:**
- For Users: How to use new system
- For AI Agents: How to load skills
- Breaking changes
- Migration steps

**Success Criteria:** Clear migration guide

---

## 🎯 SUCCESS CRITERIA (Overall)

### Must Have (P0)
- ✅ All skills consolidated into `.ai-skills/`
- ✅ GEMINI.md <300 lines
- ✅ Master Router updated with all skills
- ✅ No duplicates
- ✅ All tests pass

### Should Have (P1)
- ✅ 27 new skills created
- ✅ Documentation complete
- ✅ Migration guide available
- ✅ All references updated

### Nice to Have (P2)
- ✅ Examples for each category
- ✅ Performance optimizations
- ✅ Visual skill browser (future)

---

## 📊 PROGRESS TRACKING

### Phase Completion
- [ ] Phase 1: Analysis & Inventory (0/4 tasks)
- [ ] Phase 2: Directory Restructure (0/5 tasks)
- [ ] Phase 3: Create New Skills (0/2 tasks)
- [ ] Phase 4: Refactor GEMINI.md (0/4 tasks)
- [ ] Phase 5: Update Master Router (0/3 tasks)
- [ ] Phase 6: Cleanup & Optimize (0/3 tasks)
- [ ] Phase 7: Testing & Validation (0/3 tasks)
- [ ] Phase 8: Documentation (0/3 tasks)

**Overall Progress:** 0/27 tasks (0%)

### Time Tracking
- Estimated: 8 hours
- Actual: 0 hours
- Remaining: 8 hours

---

## 🚨 RISKS & MITIGATION

### Risk 1: Skills Scattered Across Multiple Locations
**Impact:** High  
**Probability:** High  
**Mitigation:** Thorough inventory in Phase 1

### Risk 2: Breaking Existing References
**Impact:** High  
**Probability:** Medium  
**Mitigation:** Comprehensive testing in Phase 7

### Risk 3: GEMINI.md Too Complex to Reduce
**Impact:** Medium  
**Probability:** Low  
**Mitigation:** Extract to separate files in Phase 4

### Risk 4: Time Overrun
**Impact:** Low  
**Probability:** Medium  
**Mitigation:** Focus on P0 tasks first, defer P2 if needed

---

## 📝 NOTES & DECISIONS

### Decision Log
- **2026-03-27:** Created detailed execution plan
- **Pending:** Start Phase 1 after user approval

### Open Questions
- Should we delete old skills or keep as archive?
- Merge duplicates or keep separate with deprecation notice?
- Create automated migration script?

### Assumptions
- Current skills are in `antigravity/skills/`
- Target location is `.ai-skills/`
- GEMINI.md can be reduced to <300 lines
- All skills follow similar format

---

## 🎯 NEXT ACTIONS

### Immediate (After Approval)
1. Start Phase 1: Run inventory scripts
2. Create SKILLS_INVENTORY.md
3. Identify duplicates

### This Session
- Complete Phase 1-2 (1.5 hours)
- Start Phase 3 (create 5-10 skills)

### Next Session
- Complete Phase 3-4 (3 hours)
- Start Phase 5-6 (1.5 hours)

### Final Session
- Complete Phase 7-8 (1.5 hours)
- Final review and deployment

---

**Created:** 2026-03-27  
**Status:** 🔵 PLANNING COMPLETE - AWAITING APPROVAL  
**Estimated Completion:** 2026-03-28 (if 8 hours continuous)  
**Next Step:** User approval to begin Phase 1

**Planning Principle:** "Plan the work, work the plan, track the progress." 📋✅
