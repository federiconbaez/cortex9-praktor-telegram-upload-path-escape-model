import ast
import unittest
from unittest import mock
import subprocess

from c9praktor import cases, paths

ROOT = cases.ROOT

# Table taken from Go's path.Base / path.Join (see LIMITATIONS.md).
GO_BASE = {
    "../../../NOTES.md": "NOTES.md",
    "foo/bar": "bar",
    "..": "..",
    ".": ".",
    "": ".",
    "/": "/",
    "foo/": "foo",
    "foo//bar": "bar",
    r"..\..\NOTES.md": r"..\..\NOTES.md",
}
GO_JOIN = {
    ("/vol", "uploads/123_../../../NOTES.md"): "/vol/NOTES.md",
    ("/vol", "uploads/123_../../../../NOTES.md"): "/NOTES.md",
    ("/vol", "ok/a.txt"): "/vol/ok/a.txt",
    ("/vol", "../etc/x"): "/etc/x",
    ("/vol", "foo/../../x"): "/x",
    ("/vol", "uploads/123_ok.txt"): "/vol/uploads/123_ok.txt",
    ("/vol", "."): "/vol",
    ("/vol", "uploads/123_.."): "/vol/uploads/123_..",
    ("/vol", "uploads/123_../etc/x"): "/vol/uploads/123_../etc/x",
    ("/vol", "uploads/123_foo/../../x"): "/vol/x",
    ("/vol", ""): "/vol",
}


class Adversarial(unittest.TestCase):
    def test_src_never_calls_popen_or_system(self):
        for f in sorted((ROOT / "src/c9praktor").glob("*.py")):
            tree = ast.parse(f.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    fn = node.func
                    name = fn.attr if isinstance(fn, ast.Attribute) else getattr(
                        fn, "id", "")
                    self.assertNotIn(name, {"Popen", "run", "call", "system",
                                            "check_output", "getoutput",
                                            "open", "urlopen"})

    def test_running_cases_never_touches_subprocess(self):
        boom = mock.Mock(side_effect=AssertionError("subprocess used"))
        with mock.patch.object(subprocess, "Popen", boom), \
                mock.patch.object(subprocess, "run", boom):
            for c in cases.load():
                for v in paths.VERSIONS:
                    cases.run(c, v)
        boom.assert_not_called()

    def test_go_path_base_table(self):
        for inp, out in GO_BASE.items():
            self.assertEqual(paths.go_path_base(inp), out, inp)

    def test_go_path_join_table(self):
        for (a, b), out in GO_JOIN.items():
            self.assertEqual(paths.go_path_join(a, b), out, (a, b))

    def test_post_base_then_prefix_on_three_dotdot(self):
        r = paths.analyze("post", "../../../NOTES.md")
        self.assertEqual(r["outcome"], "IN_UPLOADS")
        self.assertEqual(r["volume_path"], "uploads/123_NOTES.md")
        self.assertEqual(r["landing"], "/vol/uploads/123_NOTES.md")

    def test_pre_three_dotdot_lands_at_volume_root(self):
        r = paths.analyze("pre", "../../../NOTES.md")
        self.assertEqual(r["outcome"], "IN_VOLUME")
        self.assertEqual(r["landing"], "/vol/NOTES.md")

    def test_unknown_version(self):
        with self.assertRaises(ValueError):
            paths.analyze("v9", "ok.txt")

    def test_deterministic(self):
        a = [cases.run(c, "pre")["outcome"] for c in cases.load()]
        b = [cases.run(c, "pre")["outcome"] for c in cases.load()]
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
