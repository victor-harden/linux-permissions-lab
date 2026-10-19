#!/usr/bin/env python3
"""Convert and explain Linux file permission modes."""
from __future__ import annotations

import argparse
import sys

SPECIAL = {"4": "setuid", "2": "setgid", "1": "sticky"}


def octal_to_symbolic(mode: str) -> str:
    mode = mode.strip()
    if len(mode) == 3:
        mode = "0" + mode
    if len(mode) != 4 or not all(c in "01234567" for c in mode):
        raise ValueError(f"invalid octal mode: {mode!r}")

    special_digit = int(mode[0])
    out = []
    for idx, digit in enumerate(mode[1:], start=0):
        value = int(digit)
        out.append("r" if value & 4 else "-")
        out.append("w" if value & 2 else "-")
        if idx == 0 and special_digit & 4:
            out.append("s" if value & 1 else "S")
        elif idx == 1 and special_digit & 2:
            out.append("s" if value & 1 else "S")
        elif idx == 2 and special_digit & 1:
            out.append("t" if value & 1 else "T")
        else:
            out.append("x" if value & 1 else "-")
    return "".join(out)


def symbolic_to_octal(symbolic: str) -> str:
    symbolic = symbolic.strip()
    if len(symbolic) != 9:
        raise ValueError(f"symbolic mode must be 9 characters: {symbolic!r}")
    special = 0
    digits = []
    for i in range(3):
        chunk = symbolic[i * 3:(i + 1) * 3]
        value = 0
        if chunk[0] == "r":
            value += 4
        if chunk[1] == "w":
            value += 2
        third = chunk[2]
        if third in "xst":
            value += 1
        if i == 0 and third in "sS":
            special += 4
        if i == 1 and third in "sS":
            special += 2
        if i == 2 and third in "tT":
            special += 1
        digits.append(str(value))
    return f"{special}{''.join(digits)}" if special else "".join(digits)


def explain(mode: str):
    mode = mode if len(mode) == 4 else "0" + mode
    lines = []
    special_digit = int(mode[0])
    for flag, label in SPECIAL.items():
        if special_digit & int(flag):
            lines.append(f"special: {label} bit is set")
    owners = ("user", "group", "other")
    for idx, owner in enumerate(owners, start=1):
        value = int(mode[idx])
        parts = []
        if value & 4:
            parts.append("read")
        if value & 2:
            parts.append("write")
        if value & 1:
            parts.append("execute")
        lines.append(f"{owner}: {', '.join(parts) if parts else 'no permissions'}")
    return lines


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Linux permission calculator")
    parser.add_argument("mode", help="octal (750, 4755) or symbolic (rwxr-x---)")
    parser.add_argument("--explain", action="store_true", help="describe each bit")
    args = parser.parse_args(argv)

    mode = args.mode.strip()
    try:
        if mode.isdigit():
            symbolic = octal_to_symbolic(mode)
            print(f"{mode} -> {symbolic}")
            octal = mode if len(mode) == 4 else "0" + mode
        else:
            octal = symbolic_to_octal(mode)
            print(f"{mode} -> {octal}")
            symbolic = mode
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    if args.explain:
        for line in explain(octal):
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
