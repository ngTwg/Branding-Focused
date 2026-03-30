# SKILL MIGRATION EXECUTION PLAN

## PHASES
- Phase 1: Preparation & Structure ⏳ TODO
- Phase 2: Skill Consolidation (Migration) ⏳ TODO
- Phase 3: Reference Updates (MASTER_ROUTER & GEMINI) ⏳ TODO
- Phase 4: Final Cleanup & Validation ⏳ TODO

## DETAILED TASKS
### Phase 1: Preparation
- [x] Create project structure (antigravity/skills/) ✅ DONE
- [x] Initialize `antigravity/skills/MASTER_ROUTER.md` ✅ DONE
- [x] Initialize `antigravity/skills/index-skills.md` ✅ DONE

### Phase 2: Consolidation
- [x] Copy `antigravity/skills/*` to `antigravity/skills/` (excluding duplicates) ✅ DONE
- [x] Verify category mapping (Frontend, Backend, etc.) ✅ DONE

### Phase 3: Reference Updates
- [x] Update documentation path references (README.md, GEMINI.md, MASTER_PLAN.md) ✅ DONE
- [x] Update `GEMINI.md` Rule 1 path to `antigravity/skills/MASTER_ROUTER.md` ✅ DONE
- [x] Update `antigravity/skills/MASTER_ROUTER.md` to point to internal skills using relative or `antigravity/skills/` absolute paths ✅ DONE
- [x] Update any agent-specific rules (CLAUDE.md, CURSOR.md) if they use hardcoded paths ✅ DONE

### Phase 4: Validation & Cleanup
- [x] Bulk update agent folders (AGENT_Claude, AGENT_Cursor, etc.) ✅ DONE
- [x] Verify internal skill references within `antigravity/skills/` ✅ DONE
- [x] Run grep search to ensure no old `antigravity/skills` references remain in root rules ✅ DONE
- [x] Test Master Router by simulating a task ✅ DONE
- [x] Delete legacy `antigravity/skills/` folder ✅ DONE
- [x] Final verification with global grep ✅ DONE

## PROGRESS TRACKING
- Overall: 0/11 tasks (0%)
- Phase 1: 0/3 tasks
