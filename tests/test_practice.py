"""Answers to PRACTICE.md."""
import unittest
from pathlib import Path
from c9praktor import paths


class Practice(unittest.TestCase):
    def test_level_1_plain(self):
        self.assertEqual(
            paths.analyze("pre", "ok.txt")["outcome"], "IN_UPLOADS")

    def test_level_2_three_dotdot(self):
        r = paths.analyze("pre", "../../../NOTES.md")
        self.assertEqual(r["outcome"], "IN_VOLUME")
        self.assertEqual(r["landing"], "/vol/NOTES.md")

    def test_level_3_post_base(self):
        r = paths.analyze("post", "../../../NOTES.md")
        self.assertEqual(r["outcome"], "IN_UPLOADS")

    def test_level_4_volume_escape(self):
        r = paths.analyze("pre", "../../../../NOTES.md")
        self.assertEqual(r["outcome"], "ESCAPES_VOLUME")

    def test_level_5_write_gate(self):
        pre = paths.analyze("pre", "../etc/x", site="write")
        post = paths.analyze("post", "../etc/x", site="write")
        self.assertEqual(pre["outcome"], "ESCAPES_VOLUME")
        self.assertEqual(post["outcome"], "REJECTED")

    def test_level_6_observation(self):
        text = Path("LIMITATIONS.md").read_text(encoding="utf-8")
        self.assertIn("o01", text)
        self.assertEqual(
            paths.analyze("pre", "../etc/x")["outcome"], "IN_UPLOADS")


if __name__ == "__main__":
    unittest.main()
