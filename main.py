#!/usr/bin/env python3
"""news-image-20261124: sum up 24 November 2026's world news in one image.

The entry image is the atlas infographic stored beside this file as
``entry.png``. This program copies it to the output directory unchanged, so
every run writes identical bytes: no timestamps, no randomness, no network.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or ".")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    # Confirm the copy is complete: a truncated write must fail loudly
    # instead of shipping a corrupt image to the gate.
    if target.stat().st_size != source.stat().st_size:
        raise RuntimeError("entry.png copy incomplete")


if __name__ == "__main__":
    main()
