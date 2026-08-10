import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "skill_toggle.py"
SPEC = importlib.util.spec_from_file_location("skill_toggle", MODULE_PATH)
skill_toggle = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = skill_toggle
SPEC.loader.exec_module(skill_toggle)


def make_skill(root: Path, name: str, *, claude=None, codex=None) -> Path:
    directory = root / skill_toggle.SKILLS_SUBDIR / name
    directory.mkdir(parents=True)
    claude_line = (
        "" if claude is None else f"disable-model-invocation: {str(claude).lower()}\n"
    )
    (directory / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        f"description: Use {name} for tests.\n"
        f"{claude_line}"
        "---\n\n"
        f"# {name}\n",
        encoding="utf-8",
    )
    if codex is not None:
        agents = directory / "agents"
        agents.mkdir()
        (agents / "openai.yaml").write_text(
            "interface:\n"
            f'  display_name: "{name}"\n'
            '  short_description: "A test skill used by the selector."\n'
            f'  default_prompt: "Use ${name} for this task."\n'
            "\n"
            "policy:\n"
            "  products:\n"
            "  - codex\n"
            f"  allow_implicit_invocation: {str(codex).lower()}  # preserve me\n",
            encoding="utf-8",
        )
    return directory


class SkillToggleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_disable_updates_claude_and_creates_valid_codex_metadata(self):
        directory = make_skill(self.root, "alpha")

        skill_toggle.set_skill_enabled(
            skill_toggle.load_skill(directory), enabled=False
        )

        skill_text = (directory / "SKILL.md").read_text(encoding="utf-8")
        openai_text = (directory / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("disable-model-invocation: true", skill_text)
        self.assertIn("interface:\n", openai_text)
        self.assertIn("allow_implicit_invocation: false", openai_text)
        self.assertEqual(
            skill_toggle.load_skill(directory).state,
            skill_toggle.InvocationState.DISABLED,
        )

    def test_enable_preserves_existing_codex_metadata_and_comment(self):
        directory = make_skill(self.root, "beta", claude=True, codex=False)

        skill_toggle.set_skill_enabled(skill_toggle.load_skill(directory), enabled=True)

        skill_text = (directory / "SKILL.md").read_text(encoding="utf-8")
        openai_text = (directory / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("disable-model-invocation: false", skill_text)
        self.assertIn("  - codex", openai_text)
        self.assertIn("allow_implicit_invocation: true  # preserve me", openai_text)
        self.assertEqual(
            skill_toggle.load_skill(directory).state,
            skill_toggle.InvocationState.ENABLED,
        )

    def test_mixed_state_toggles_to_enabled(self):
        directory = make_skill(self.root, "gamma", claude=False, codex=False)
        skill = skill_toggle.load_skill(directory)
        self.assertEqual(skill.state, skill_toggle.InvocationState.MIXED)

        skill_toggle.toggle_skill(skill)

        self.assertEqual(
            skill_toggle.load_skill(directory).state,
            skill_toggle.InvocationState.ENABLED,
        )

    def test_products_can_be_changed_independently(self):
        directory = make_skill(self.root, "individual")

        claude_changed = skill_toggle.set_skill_product_states(
            skill_toggle.load_skill(directory), claude_enabled=False
        )
        self.assertEqual(claude_changed.claude_enabled, False)
        self.assertEqual(claude_changed.codex_enabled, True)
        self.assertFalse((directory / "agents/openai.yaml").exists())

        codex_changed = skill_toggle.set_skill_product_states(
            claude_changed, codex_enabled=False
        )
        self.assertEqual(codex_changed.state, skill_toggle.InvocationState.DISABLED)

    def test_discovery_excludes_hidden_and_external_symlinked_skills(self):
        make_skill(self.root, "visible")
        make_skill(self.root / ".hidden", "nested")
        make_skill(self.root, "gstack-transient")
        with tempfile.TemporaryDirectory() as external:
            external_skill = make_skill(Path(external), "outside")
            try:
                os.symlink(external_skill, self.root / "linked")
            except OSError:
                self.skipTest("symlinks are unavailable")

            names = [skill.key for skill in skill_toggle.discover_skills(self.root)]

        self.assertEqual(names, ["visible"])

    def test_discovery_reads_categories_from_wrapper_frontmatter(self):
        make_skill(self.root, "categorized")
        (self.root / "categorized.md").write_text(
            "---\ntitle: categorized\ndomain: single-cell-omics\n---\n",
            encoding="utf-8",
        )

        skills = skill_toggle.discover_skills(self.root)

        self.assertEqual(skills[0].category, "single-cell-omics")

    def test_cli_disable_and_list(self):
        directory = make_skill(self.root, "delta")
        result = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "--root",
                str(self.root),
                "disable",
                "delta",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("disabled\tdelta", result.stdout)

        listed = subprocess.run(
            [sys.executable, str(MODULE_PATH), "--root", str(self.root), "list"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertIn(
            "disabled\tdelta\tuncategorized\tUse delta for tests.", listed.stdout
        )
        self.assertTrue((directory / "agents/openai.yaml").exists())

    def test_cli_changes_multiple_skills_in_one_command(self):
        alpha = make_skill(self.root, "alpha")
        beta = make_skill(self.root, "beta")
        result = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "--root",
                str(self.root),
                "disable",
                "--product",
                "codex",
                "alpha",
                "beta",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(skill_toggle.load_skill(alpha).codex_enabled)
        self.assertFalse(skill_toggle.load_skill(beta).codex_enabled)

    def test_snapshot_round_trip_restores_both_products(self):
        directory = make_skill(self.root, "snapshot")
        snapshot = skill_toggle.save_snapshot(self.root)
        skill_toggle.set_skill_enabled(
            skill_toggle.load_skill(directory), enabled=False
        )

        loaded, changed = skill_toggle.load_snapshot(self.root)

        self.assertEqual(loaded, snapshot)
        self.assertEqual(changed, 1)
        self.assertEqual(
            skill_toggle.load_skill(directory).state,
            skill_toggle.InvocationState.ENABLED,
        )

    def test_pre_commit_reset_saves_state_and_restores_only_head_metadata(self):
        directory = make_skill(self.root, "committed")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "add", f"{skill_toggle.SKILLS_SUBDIR}/committed/SKILL.md"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Skill Toggle Test",
                "-c",
                "user.email=skill-toggle@example.test",
                "commit",
                "-qm",
                "fixture",
            ],
            cwd=self.root,
            check=True,
        )
        skill_toggle.set_skill_enabled(
            skill_toggle.load_skill(directory), enabled=False
        )
        skill_path = directory / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8") + "\nUnrelated working edit.\n",
            encoding="utf-8",
        )

        snapshot, changed = skill_toggle.pre_commit_reset(self.root)

        skill_text = skill_path.read_text(encoding="utf-8")
        self.assertGreaterEqual(changed, 2)
        self.assertTrue(snapshot.exists())
        self.assertNotIn("disable-model-invocation", skill_text)
        self.assertIn("Unrelated working edit.", skill_text)
        self.assertFalse((directory / "agents/openai.yaml").exists())
        self.assertEqual(
            skill_toggle.load_skill(directory).state,
            skill_toggle.InvocationState.ENABLED,
        )

    def test_pre_commit_reset_restores_tracked_openai_yaml_exactly(self):
        directory = make_skill(self.root, "tracked-openai")
        openai_path = directory / "agents" / "openai.yaml"
        openai_path.parent.mkdir()
        original = (
            "interface:\n"
            '  display_name: "Tracked OpenAI"\n'
            '  short_description: "Preserve exact formatting."\n'
        )
        openai_path.write_text(original, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Skill Toggle Test",
                "-c",
                "user.email=skill-toggle@example.test",
                "commit",
                "-qm",
                "fixture",
            ],
            cwd=self.root,
            check=True,
        )
        skill_toggle.set_skill_product_states(
            skill_toggle.load_skill(directory), codex_enabled=False
        )

        skill_toggle.pre_commit_reset(self.root)

        self.assertEqual(openai_path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
