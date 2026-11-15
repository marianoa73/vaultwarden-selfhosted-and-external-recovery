"""Spanish and English versions must stay in sync: same sections and same code blocks."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ("why", "architecture", "install", "security", "backup", "recovery", "emergency-access", "limitations")
PAIRS = [("README.es.md", "README.md")] + [(f"docs/{n}.md", f"docs/{n}.en.md") for n in GUIDES]


def shape(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    headings = [len(m.group(1)) for m in re.finditer(r"^(#{1,6}) ", text, re.M)]
    blocks = re.findall(r"^\s*```.*?^\s*```", text, re.M | re.S)
    return headings, len(blocks), text


class BilingualDocs(unittest.TestCase):
    def test_pairs_exist_and_match(self):
        for es, en in PAIRS:
            with self.subTest(pair=(es, en)):
                h_es, b_es, t_es = shape(es)
                h_en, b_en, t_en = shape(en)
                self.assertEqual(h_es, h_en, "different heading structure")
                self.assertEqual(b_es, b_en, "different number of code blocks")
                self.assertIn(Path(en).name, t_es)
                self.assertIn(Path(es).name, t_en)

    def test_both_diagram_languages_exist(self):
        for n in ("01-overview", "02-encryption", "03-backup", "04-contingency", "05-keys", "06-emergency", "banner"):
            for lang in ("en", "es"):
                for ext in ("svg", "png"):
                    self.assertTrue((ROOT / f"docs/assets/{n}.{lang}.{ext}").is_file(), f"{n}.{lang}.{ext}")

    def test_language_buttons_in_readmes(self):
        self.assertIn("btn-es.svg", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("btn-en.svg", (ROOT / "README.es.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
