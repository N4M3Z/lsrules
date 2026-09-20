#!/usr/bin/env python3
"""Exercise unsafe near misses in memory without changing package files."""

import unittest
from pathlib import Path
from unittest.mock import patch

import check


class ResourceChecks(unittest.TestCase):
    def setUp(self):
        self.root = check.ROOT
        self.skill = self.root / ".agents/skills/lsrules-audit/SKILL.md"
        self.source = self.skill.read_text()
        self.data, self.body = check.frontmatter(self.source)

    def resource_results_with_text(self, path, replacement):
        original = Path.read_text

        def read(candidate, *args, **kwargs):
            return replacement if candidate == path else original(candidate, *args, **kwargs)

        with patch.object(Path, "read_text", read):
            return dict(check.agent_checks(self.root))

    def test_current_agent_resources_pass(self):
        self.assertTrue(all(passed for _, passed in check.agent_checks(self.root)))

    def test_skill_name_cannot_disagree_with_directory(self):
        edited = self.source.replace("name: lsrules-audit", "name: unrelated-skill", 1)
        results = self.resource_results_with_text(self.skill, edited)
        self.assertFalse(results["lsrules-audit_canonical_frontmatter"])

    def test_skill_h1_cannot_disagree_with_name(self):
        self.assertFalse(check.skill_structure("lsrules-audit", self.body.replace("# lsrules-audit", "# unrelated-skill", 1)))

    def test_instructions_section_is_required(self):
        self.assertFalse(check.skill_structure("lsrules-audit", self.body.replace("## Instructions", "## Background", 1)))

    def test_section_order_matters(self):
        edited = self.body.replace("## Prerequisites", "## Temporary", 1)
        edited = edited.replace("## Constraints", "## Prerequisites", 1).replace("## Temporary", "## Constraints", 1)
        self.assertFalse(check.skill_structure("lsrules-audit", edited))

    def test_duplicate_frontmatter_keys_fail(self):
        with self.assertRaises(ValueError):
            check.frontmatter(self.source.replace("name: lsrules-audit", "name: lsrules-audit\nname: another", 1))

    def test_yaml_executable_tag_is_not_interpreted(self):
        with self.assertRaises(ValueError):
            check.scalar("!!python/object:example ignored")

    def test_multiline_frontmatter_is_outside_safe_subset(self):
        with self.assertRaises(ValueError):
            check.frontmatter("---\nname: safe\ndescription: |\n  hidden continuation\n---\n# safe\n")

    def test_unsafe_dynamic_context_fails(self):
        edited = self.source + "\n!`external-command`\n"
        results = self.resource_results_with_text(self.skill, edited)
        self.assertFalse(results["lsrules-audit_bounded_static_entrypoint"])

    def test_companion_cannot_escape_skill_tree(self):
        edited = self.source + "\n[Outside companion](../../../README.md)\n"
        results = self.resource_results_with_text(self.skill, edited)
        self.assertFalse(results["lsrules-audit_local_references"])

    def test_missing_companion_fails(self):
        edited = self.source + "\n[Missing companion](missing.md)\n"
        results = self.resource_results_with_text(self.skill, edited)
        self.assertFalse(results["lsrules-audit_local_references"])

    def test_daybreak_model_cannot_silently_change(self):
        path = self.root / ".codex/agents/daybreak-adversary.toml"
        edited = path.read_text().replace(check.DAYBREAK_MODEL, "different-model")
        results = self.resource_results_with_text(path, edited)
        self.assertFalse(results["codex_adapter_daybreak_read_only"])

    def test_daybreak_sandbox_cannot_gain_writes(self):
        path = self.root / ".codex/agents/daybreak-adversary.toml"
        edited = path.read_text().replace('sandbox_mode = "read-only"', 'sandbox_mode = "workspace-write"')
        results = self.resource_results_with_text(path, edited)
        self.assertFalse(results["codex_adapter_daybreak_read_only"])

    def test_adapter_cannot_add_an_unreviewed_capability(self):
        path = self.root / ".codex/agents/daybreak-adversary.toml"
        edited = 'web_search = "live"\n' + path.read_text()
        results = self.resource_results_with_text(path, edited)
        self.assertFalse(results["codex_adapter_fields_allowlisted"])

    def test_native_adapter_must_reference_canonical_contract(self):
        path = self.root / ".codex/agents/daybreak-adversary.toml"
        edited = path.read_text().replace(check.DAYBREAK_CONTRACT, ".agents/agents/missing.md")
        results = self.resource_results_with_text(path, edited)
        self.assertFalse(results["codex_adapter_canonical_contract_reference"])

    def test_ai_overlap_is_not_substring_matching(self):
        cases = [
            ("chatgpt.com", "chatgpt.com", True),
            ("proton.me", "lumo.proton.me", True),
            ("auth.openai.com", "openai.com", True),
            ("CHATGPT.COM.", "chatgpt.com", True),
            ("x.com", "x.ai", False),
            ("notopenai.com", "openai.com", False),
            ("openai.com.evil.example", "openai.com", False),
        ]
        for left, right, expected in cases:
            with self.subTest(left=left, right=right):
                self.assertEqual(check.domains_overlap(left, right), expected)


if __name__ == "__main__":
    unittest.main()
