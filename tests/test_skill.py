"""The agent guide must be a valid skill and keep its non-negotiable rules."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skill/vaultwarden-recovery-deploy/SKILL.md").read_text(encoding="utf-8")


class SkillTests(unittest.TestCase):
    def test_frontmatter(self):
        m = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", SKILL)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "vaultwarden-recovery-deploy")

    def test_covers_both_platforms_and_the_rules(self):
        for needle in ("WSL2", "Linux", "never see", "Ask before", "loopback", "vw-init-passphrase.sh", "Definition of done"):
            self.assertIn(needle.lower(), SKILL.lower(), needle)

    def test_every_referenced_file_exists(self):
        for ref in set(re.findall(r"`((?:src|examples|docs|tests)/[A-Za-z0-9_./-]+)`", SKILL)):
            self.assertTrue((ROOT / ref).exists(), ref)

    def test_agents_file_points_to_the_skill(self):
        self.assertIn("skill/vaultwarden-recovery-deploy/SKILL.md", (ROOT / "AGENTS.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
