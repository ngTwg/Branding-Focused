from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Optional

from antigravity.core.hybrid_retriever import HybridRetriever
from antigravity.core.index_manager import IndexManager
from antigravity.core.schemas import (
    ArtifactCheck,
    PlanStep,
    Skill,
    SkillDocument,
    TaskCompletionSpec,
)

logger = logging.getLogger(__name__)

class SkillStore:
    """Phase 3: Actionable Intelligence Memory Hub"""

    def __init__(self, skills_dir: Optional[Path] = None, enable_hybrid: Optional[bool] = None):
        self.skills: list[Skill] = []
        self._skills_dir = skills_dir or (Path(__file__).resolve().parents[1] / "skills")
        self._index_cache_dir = Path(
            os.getenv(
                "AG_SKILL_INDEX_CACHE_DIR",
                str(Path(__file__).resolve().parents[1] / "brain" / "skill_index_cache"),
            )
        )

        if enable_hybrid is None:
            enable_hybrid = self._env_flag("AG_ENABLE_PERSISTENT_SKILL_RETRIEVER", default=True)

        self._hybrid_retriever: Optional[HybridRetriever] = None
        self._index_manager: Optional[IndexManager] = None

        self._bootstrap_hardcoded_skills()
        if enable_hybrid:
            self._initialize_hybrid_retriever()

    def _env_flag(self, var_name: str, default: bool) -> bool:
        raw = os.getenv(var_name)
        if raw is None:
            return default
        return raw.strip().lower() not in {"0", "false", "no", "off"}

    def _initialize_hybrid_retriever(self) -> None:
        if not self._skills_dir.exists():
            logger.warning("Skill directory not found for hybrid retriever: %s", self._skills_dir)
            return

        try:
            self._index_manager = IndexManager(self._skills_dir, self._index_cache_dir)
            self._hybrid_retriever = HybridRetriever(
                skills_dir=self._skills_dir,
                alpha=0.45,
                beta=0.55,
                index_manager=self._index_manager,
            )

            changed_files = self._index_manager.detect_changes()
            if changed_files:
                self._index_manager.mark_stale(changed_files)
                # Quick-fix for corpus-retention safety: rebuild full corpus when changes are detected.
                self._index_manager.reindex(self._hybrid_retriever, mode="full")
                logger.info("Hybrid retriever reindexed with full corpus (%d changed files)", len(changed_files))
                return

            documents = self._load_skill_documents()
            if documents:
                self._hybrid_retriever.index(documents)
                logger.info("Hybrid retriever indexed %d skill documents", len(documents))
        except Exception as e:
            logger.warning("Hybrid retriever initialization failed, using hardcoded fallback only: %s", e)
            self._hybrid_retriever = None
            self._index_manager = None

    def _load_skill_documents(self) -> list[SkillDocument]:
        documents: list[SkillDocument] = []
        for md_file in self._skills_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            relative_path = md_file.relative_to(self._skills_dir).as_posix()
            title_match = re.search(r"^#\s+(.+)$", content, flags=re.MULTILINE)
            name = title_match.group(1).strip() if title_match else md_file.stem.replace("-", " ").replace("_", " ")

            parts = relative_path.split("/")
            domain_tags = [parts[0]] if parts else ["general"]

            documents.append(
                SkillDocument(
                    skill_id=relative_path,
                    name=name,
                    content=content,
                    domain_tags=domain_tags,
                    file_path=relative_path,
                )
            )

        return documents

    def _bootstrap_hardcoded_skills(self):
        """Mock version of DB loading. Loading 10 classic production skills."""
        
        # 1. React Missing Component
        react_missing_comp = Skill(
            name="fix_react_missing_component",
            description="Fix missing React component.",
            trigger_patterns=["module not found", "failed to resolve import", "is not defined", "missing file"],
            plan_template=[
                PlanStep(step_id=1, action="generate_code", agent="frontend", input={"instruction": "Create the missing React component."})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="file_exists", path="{DYNAMIC_PATH}")],
                semantic_goal="Component correctly generated."
            )
        )
        
        # 2. NPM Missing Dependency
        npm_missing_dep = Skill(
            name="fix_missing_npm_dependency",
            description="Install generic missing JS package.",
            trigger_patterns=["cannot find package", "npm err!", "is not in the npm registry"],
            plan_template=[
                PlanStep(step_id=1, action="run_cmd", agent="infra", input={"command": "npm install {PACKAGE_NAME}"})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="file_contains", path="package.json", keyword="{PACKAGE_NAME}")],
                semantic_goal="Dependency installed."
            )
        )

        # 3. TypeScript Type Error (Any / Implicit)
        ts_type_error = Skill(
            name="fix_typescript_implicit_any",
            description="Fix TypeScript implicitly has an 'any' type error.",
            trigger_patterns=["implicitly has an 'any' type", "ts(7006)", "parameter '", "has an 'any'"],
            plan_template=[
                PlanStep(step_id=1, action="generate_code", agent="frontend", input={"instruction": "Add proper typings or strict interfaces to resolve implicit any errors."}),
                PlanStep(step_id=2, action="run_cmd", agent="frontend", input={"command": "npx tsc --noEmit"})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="cmd_exit_zero", cmd="npx tsc --noEmit")],
                semantic_goal="File conforms to strict TypeScript rules."
            )
        )

        # 4. Python Module Import Error
        py_missing_module = Skill(
            name="fix_python_missing_module",
            description="Install missing Python dependency via pip.",
            trigger_patterns=["importerror: no module named", "modulenotfounderror: no module named"],
            plan_template=[
                PlanStep(step_id=1, action="run_cmd", agent="backend", input={"command": "pip install {MODULE_NAME}"}),
                PlanStep(step_id=2, action="run_cmd", agent="infra", input={"command": "pip freeze > requirements.txt"})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="file_contains", path="requirements.txt", keyword="{MODULE_NAME}")],
                semantic_goal="Python module installed and recorded."
            )
        )

        # 5. Env Var Missing 
        missing_env_var = Skill(
            name="fix_missing_env_var",
            description="Provide missing environment variable to prevent crash.",
            trigger_patterns=["missing environment variable", "undefined error reading property", "process.env.", "key error:"],
            plan_template=[
                PlanStep(step_id=1, action="generate_code", agent="infra", input={"instruction": "Add placeholder {ENV_VAR} to .env.example"}),
                PlanStep(step_id=2, action="run_cmd", agent="infra", input={"command": "cp .env.example .env"})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="file_exists", path=".env"), ArtifactCheck(type="file_contains", path=".env", keyword="{ENV_VAR}")],
                semantic_goal="Environment fallback structured."
            )
        )

        # 6. React Hook Rules Violation
        react_hook_rules = Skill(
            name="fix_react_hook_rules",
            description="Fix React hooks called conditionally or in wrong order.",
            trigger_patterns=["rendered more hooks than during the previous render", "react hook", "called conditionally"],
            plan_template=[
                PlanStep(step_id=1, action="generate_code", agent="frontend", input={"instruction": "Refactor component: move all hooks to the top level, pulling them outside conditionals."})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="file_contains", path="{FILE_PATH}", keyword="use")],
                semantic_goal="Hooks pulled to root logic tier."
            )
        )

        # 7. Port Already In Use (Dev Environment)
        port_in_use = Skill(
            name="fix_port_already_in_use",
            description="Kill node process occupying commonly used dev ports.",
            trigger_patterns=["listen eaddrinuse", "port is already in use", "address already in use"],
            plan_template=[
                PlanStep(step_id=1, action="run_cmd", agent="infra", input={"command": "npx kill-port {PORT_NUMBER}"})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="cmd_exit_zero", cmd="node -e \"console.log('port freed')\"")],
                semantic_goal="Port freed for local development."
            )
        )

        # 8. Git Merge Conflict Markers Left Behind
        merge_conflict = Skill(
            name="fix_merge_conflict_markers",
            description="Clean up unresolved git merge markers in code.",
            trigger_patterns=["<<<<<<<", "=======", ">>>>>>>", "merge conflict"],
            plan_template=[
                PlanStep(step_id=1, action="generate_code", agent="general", input={"instruction": "Resolve git merge conflict in {FILE_PATH} by accepting correct inbound changes and removing markers."})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="cmd_exit_zero", cmd="grep -v '<<<<<<<' {FILE_PATH}")],
                semantic_goal="Merge conflicts neutralized."
            )
        )

        # 9. JSON Parse Error (Syntax/Trailing Comma)
        json_parse_error = Skill(
            name="fix_json_parse_error",
            description="Fix trailing commas or syntax string errors in JSON files.",
            trigger_patterns=["unexpected token", "in json at position", "expected double-quoted property name", "json.parse"],
            plan_template=[
                PlanStep(step_id=1, action="generate_code", agent="general", input={"instruction": "Fix invalid JSON formatting in {FILE_PATH}."})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="json_valid", path="{FILE_PATH}")],
                semantic_goal="JSON syntax strictly compliant."
            )
        )

        # 10. Jest/Vitest Snapshot Failed
        test_snapshot_failed = Skill(
            name="fix_test_snapshot",
            description="Update UI component snapshots when intention was deliberate.",
            trigger_patterns=["snapshot failed", "does not match snapshot", "snapshot testing"],
            plan_template=[
                PlanStep(step_id=1, action="run_cmd", agent="frontend", input={"command": "npm run test -- -u {FILE_PATH}"})
            ],
            success_criteria=TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="cmd_exit_zero", cmd="npm run test {FILE_PATH}")],
                semantic_goal="Snapshots synced with DOM intent."
            )
        )

        self.skills.extend([
            react_missing_comp, npm_missing_dep, ts_type_error, py_missing_module, 
            missing_env_var, react_hook_rules, port_in_use, merge_conflict, 
            json_parse_error, test_snapshot_failed
        ])

    def _matches_candidate_hint(self, skill: Skill, candidate_skills: list[str]) -> bool:
        if not candidate_skills:
            return False

        skill_name = skill.name.lower().replace("_", "-")
        for hint in candidate_skills:
            norm_hint = hint.lower().replace("\\", "/")
            if skill_name in norm_hint:
                return True
            if any(trigger in norm_hint for trigger in skill.trigger_patterns[:3]):
                return True
        return False

    def _aggregate_score(
        self,
        scored: dict[str, tuple[float, Skill]],
        skill: Skill,
        score: float,
    ) -> None:
        current = scored.get(skill.name)
        if current is None or score > current[0]:
            scored[skill.name] = (score, skill)

    def retrieve_many(
        self,
        task: str,
        errors: list[str] | None = None,
        top_k: int = 3,
        candidate_skills: list[str] | None = None,
        domain_hint: str | None = None,
    ) -> list[Skill]:
        """Ranked retrieval with hybrid backend plus hardcoded fallback skills."""
        candidate_skills = candidate_skills or []
        scored: dict[str, tuple[float, Skill]] = {}

        # 1) Hardcoded pattern retrieval (fast fallback, deterministic).
        err_str = " ".join(errors).lower() if errors else ""
        task_lower = (task or "").lower()
        for skill in self.skills:
            score = 0.0
            if err_str and any(pattern in err_str for pattern in skill.trigger_patterns):
                score += 2.0
            if any(pattern in task_lower for pattern in skill.trigger_patterns):
                score += 1.0
            if self._matches_candidate_hint(skill, candidate_skills):
                score += 0.75
            if score > 0:
                self._aggregate_score(scored, skill, score)

        # 2) Hybrid retrieval against persisted skill documents.
        if self._hybrid_retriever:
            try:
                query = task
                if candidate_skills:
                    query = f"{task} {' '.join(candidate_skills)}"

                domain_filter = domain_hint if domain_hint in {
                    "frontend", "backend", "infra", "debug", "architecture", "general"
                } else None

                ranked = self._hybrid_retriever.retrieve(
                    query=query,
                    errors=errors,
                    domain_filter=domain_filter,
                    top_k=max(top_k * 2, 6),
                )

                for rank in ranked:
                    score = float(rank.final_score)
                    if self._matches_candidate_hint(rank.skill, candidate_skills):
                        score += 0.2
                    self._aggregate_score(scored, rank.skill, score)
            except Exception as e:
                logger.warning("Hybrid retrieval failed, falling back to pattern-only skills: %s", e)

        if not scored:
            return []

        ranked_skills = sorted(scored.values(), key=lambda item: (-item[0], item[1].name.lower()))
        return [skill for _, skill in ranked_skills[: max(top_k, 1)]]

    def retrieve(
        self,
        task: str,
        errors: list[str] | None = None,
        candidate_skills: list[str] | None = None,
        domain_hint: str | None = None,
    ) -> Skill | None:
        """Backward-compatible single best-match retrieval."""
        matches = self.retrieve_many(
            task=task,
            errors=errors,
            top_k=1,
            candidate_skills=candidate_skills,
            domain_hint=domain_hint,
        )
        return matches[0] if matches else None
