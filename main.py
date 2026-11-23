#!/usr/bin/env python3
"""make.fun entry: Sum up 23 November's world news in one image.

The image is rendered by draw.py (PIL + DejaVu, run locally by the agent)
and stored as entry.png in this repository. This program only copies it to
the grader's output directory using the standard library, so it runs in the
no-network sandbox. Deterministic: the same bytes on every run.

Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
The grader runs it with /output as the output directory.
"""

import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    assert os.path.getsize(src) <= 1048576, "image over 1 MiB"
    with open(src, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
