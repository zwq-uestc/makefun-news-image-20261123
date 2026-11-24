#!/usr/bin/env python3
"""Write the 23 November 2026 news image to the output directory.

The entry image is drawn by generate_image.py in this repository
(PIL, Noto Serif/Sans) from news checked on 24 November 2026. This
program only copies that image, using the standard library, with no
network access. It refuses to write anything unless entry.png is a
complete 1024 by 1024 PNG, and it writes through a temporary file so
a failed run never leaves a half-written image behind. Run it twice
and the output bytes are identical.
"""
import hashlib
import os
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def main():
    root = Path(__file__).resolve().parent
    image = root / "entry.png"
    if not image.is_file():
        fail("entry.png is missing")
    payload = image.read_bytes()
    if len(payload) == 0:
        fail("entry.png is empty")
    if payload[:8] != PNG_MAGIC:
        fail("entry.png is not a PNG")
    width = int.from_bytes(payload[16:20], "big")
    height = int.from_bytes(payload[20:24], "big")
    if width != EXPECTED_WIDTH or height != EXPECTED_WIDTH:
        fail(f"entry.png is {width}x{height}, not 1024x1024")

    destination_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    staging = destination_dir / "entry.png.tmp"
    staging.write_bytes(payload)
    staging.replace(destination_dir / "entry.png")
    digest = hashlib.sha256(payload).hexdigest()[:12]
    print(f"wrote entry.png ({len(payload)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
