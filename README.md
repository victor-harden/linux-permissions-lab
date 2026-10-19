# linux-permissions-lab

Learn Linux file permissions by doing: a calculator that converts between octal and
symbolic modes, explains every bit (including setuid, setgid and sticky), plus a
safe script that builds a practice tree in `/tmp`.

## Features

- `tools/permcalc.py`: `750` ↔ `rwxr-x---`, with `--explain` for a per-bit
  description and special bits (setuid `4`, setgid `2`, sticky `1`).
- `scripts/lab_setup.sh`: creates an isolated practice directory under
  `${TMPDIR:-/tmp}/perm-lab`, never touches system files.
- Tests for conversions, special bits and invalid input.

## Installation

```bash
git clone https://github.com/victor-harden/linux-permissions-lab.git
cd linux-permissions-lab
chmod +x scripts/*.sh
```

## Usage

```bash
python3 tools/permcalc.py 750
python3 tools/permcalc.py rwxr-x---
python3 tools/permcalc.py 4755 --explain

bash scripts/lab_setup.sh
ls -la "${TMPDIR:-/tmp}/perm-lab"
```

## Exercises

See [docs/exercises.md](docs/exercises.md) for eight graded exercises, from
reading a mode to explaining why a setuid binary is risky.

## Tests

```bash
python3 -m unittest discover -s tests -v   # calculator tests
bash tests/run_tests.sh                     # shell checks
```

## License

MIT — see [LICENSE](LICENSE).
