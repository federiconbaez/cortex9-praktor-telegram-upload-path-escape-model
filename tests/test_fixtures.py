import unittest
from c9praktor import cases, paths

DATA = cases.load()
EXPECTED = {}
for line in (cases.ROOT / "fixtures/expected.tsv").read_text(
        encoding="utf-8").splitlines()[1:]:
    cid, ver, outcome = line.split("\t")
    EXPECTED[(cid, ver)] = outcome
VERSIONS = paths.VERSIONS


class Fixtures(unittest.TestCase):
    def test_expected_covers_everything(self):
        self.assertEqual(len(EXPECTED), len(DATA) * len(VERSIONS))

    def test_model_derivation_and_hand_labels_agree(self):
        for c in DATA:
            for v in VERSIONS:
                with self.subTest(case=c["id"], version=v):
                    got = cases.run(c, v)["outcome"]
                    self.assertEqual(got, EXPECTED[(c["id"], v)])
                    self.assertEqual(got, c["expected"][v])

    def test_acceptance_pos_telegram_flip(self):
        for c in DATA:
            if c["class"] != "pos" or c.get("site") != "telegram":
                continue
            pre, post = cases.run(c, "pre"), cases.run(c, "post")
            self.assertIn(pre["outcome"], {"IN_VOLUME", "ESCAPES_VOLUME"}, c["id"])
            self.assertEqual(post["outcome"], "IN_UPLOADS", c["id"])

    def test_acceptance_pos_write_flip(self):
        for c in DATA:
            if c["class"] != "pos" or c.get("site") != "write":
                continue
            self.assertEqual(cases.run(c, "pre")["outcome"], "ESCAPES_VOLUME", c["id"])
            self.assertEqual(cases.run(c, "post")["outcome"], "REJECTED", c["id"])

    def test_acceptance_negatives_identical(self):
        for c in DATA:
            if c["class"] != "neg":
                continue
            self.assertEqual(cases.run(c, "pre")["outcome"], "IN_UPLOADS", c["id"])
            self.assertEqual(cases.run(c, "post")["outcome"], "IN_UPLOADS", c["id"])


if __name__ == "__main__":
    unittest.main()
