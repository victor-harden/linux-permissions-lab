import contextlib
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import permcalc


class PermcalcTests(unittest.TestCase):
    def test_octal_to_symbolic(self):
        self.assertEqual(permcalc.octal_to_symbolic("750"), "rwxr-x---")
        self.assertEqual(permcalc.octal_to_symbolic("644"), "rw-r--r--")
        self.assertEqual(permcalc.octal_to_symbolic("600"), "rw-------")

    def test_symbolic_to_octal(self):
        self.assertEqual(permcalc.symbolic_to_octal("rwxr-x---"), "750")
        self.assertEqual(permcalc.symbolic_to_octal("rw-r--r--"), "644")

    def test_roundtrip(self):
        for mode in ("600", "640", "755", "777", "700"):
            self.assertEqual(permcalc.symbolic_to_octal(permcalc.octal_to_symbolic(mode)), mode)

    def test_setuid(self):
        self.assertEqual(permcalc.octal_to_symbolic("4755"), "rwsr-xr-x")
        self.assertEqual(permcalc.symbolic_to_octal("rwsr-xr-x"), "4755")

    def test_sticky(self):
        self.assertEqual(permcalc.octal_to_symbolic("1777"), "rwxrwxrwt")

    def test_explain(self):
        lines = permcalc.explain("4755")
        self.assertTrue(any("setuid" in line for line in lines))
        self.assertTrue(any("user: read, write, execute" in line for line in lines))

    def test_invalid_mode(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(permcalc.main(["999"]), 2)

    def test_cli_symbolic(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(permcalc.main(["rwxr-x---"]), 0)
        self.assertIn("750", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
