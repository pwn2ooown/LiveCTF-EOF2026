#!/usr/bin/env python3
import re
import sys

# Match lines like:
# if ((flag[313] ^ 0xBC) != 0x8F) goto fail;
PAT = re.compile(
    r"""if\s*\(\s*\(\s*flag\[(\d+)\]\s*\^\s*(0x[0-9a-fA-F]+|\d+)\s*\)\s*!=\s*(0x[0-9a-fA-F]+|\d+)\s*\)\s*goto\s+fail\s*;""",
    re.IGNORECASE,
)

def parse_int(s: str) -> int:
    s = s.strip()
    return int(s, 0)  # handles 0x.. and decimal

def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input.c_or_txt>", file=sys.stderr)
        return 2

    data = open(sys.argv[1], "r", encoding="utf-8", errors="ignore").read()

    assigns = {}  # idx -> byte value
    conflicts = []

    for m in PAT.finditer(data):
        idx = int(m.group(1))
        a = parse_int(m.group(2)) & 0xFF
        b = parse_int(m.group(3)) & 0xFF
        val = (a ^ b) & 0xFF  # flag[idx] must satisfy flag[idx]^a == b

        if idx in assigns and assigns[idx] != val:
            conflicts.append((idx, assigns[idx], val))
        assigns[idx] = val

    if not assigns:
        print("No matching constraints found.", file=sys.stderr)
        return 1

    if conflicts:
        print("Conflicts found for some indices:", file=sys.stderr)
        for idx, old, new in conflicts:
            print(f"  flag[{idx}] old=0x{old:02x} new=0x{new:02x}", file=sys.stderr)

    max_i = max(assigns)
    flag = bytearray(b"?" * (max_i + 1))
    for i, v in assigns.items():
        flag[i] = v

    # Print recovered bytes
    print(f"Recovered {len(assigns)} bytes, max index = {max_i}")
    print("Assignments:")
    for i in sorted(assigns):
        print(f"flag[{i}] = 0x{assigns[i]:02x}")

    # Print a best-effort ASCII view
    print("\nASCII (unknown as '?'):")
    try:
        print(flag.decode("latin-1"))
    except Exception:
        print(bytes(flag))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

