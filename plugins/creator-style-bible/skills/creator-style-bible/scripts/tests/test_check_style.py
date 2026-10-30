"""Tests for check_style.py and check_no_consecutive_repeat.py.

Run: python3 -m unittest discover -s scripts/tests -v
"""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "demo"


def run_checker(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_style.py"), *args],
        capture_output=True, text=True, check=False,
    )


class TestCheckStyle(unittest.TestCase):
    def test_demo_fails_on_banned_phrase_and_repeat(self):
        result = run_checker(
            "--bible", str(DEMO / "demo-style-bible.yaml"),
            "--script", str(DEMO / "demo-script.txt"),
            "--timeline", str(DEMO / "demo-timeline.txt"),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Banned phrase", result.stdout)
        self.assertIn("Topic already used", result.stdout)
        self.assertIn("Title already used", result.stdout)
        self.assertIn("back-to-back", result.stdout)

    def test_json_output_and_numbers_warning(self):
        result = run_checker(
            "--bible", str(DEMO / "demo-style-bible.yaml"),
            "--script", str(DEMO / "demo-script.txt"),
            "--json",
        )
        self.assertEqual(result.returncode, 1)
        import json
        data = json.loads(result.stdout)
        self.assertEqual(data["result"], "FAIL")
        self.assertTrue(any("66" in w for w in data["warnings"]))

    def test_clean_script_passes(self):
        script = DEMO / "clean-script.txt"
        script.write_text("A New Topic Nobody Covered\nThis video gives one specific fact about ocean currents.\n", encoding="utf-8")
        try:
            result = run_checker(
                "--bible", str(DEMO / "demo-style-bible.yaml"),
                "--script", str(script),
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("PASS", result.stdout)
        finally:
            script.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
