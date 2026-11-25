"""World-news atlas of 24 November 2026 — 36 verified stories.

The atlas image is committed alongside this program as ``entry.png``.
This program is standard-library only (nothing is installed before the
entry runs on the grader), so it simply copies the committed image
byte-for-byte into the output directory, then verifies the copy by
comparing both file size and SHA-256 hash against the original.
"""

import hashlib
import os
import shutil

IMAGE_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, IMAGE_NAME)

    shutil.copyfile(source, destination)

    # Verify the copy is complete: same size and same bytes.
    source_size = os.path.getsize(source)
    copied_size = os.path.getsize(destination)
    if copied_size != source_size:
        raise RuntimeError(
            "Incomplete copy of %s: %d bytes copied, expected %d"
            % (IMAGE_NAME, copied_size, source_size)
        )

    def _sha256(path):
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    if _sha256(source) != _sha256(destination):
        raise RuntimeError("Copied %s differs from the committed image" % IMAGE_NAME)


if __name__ == "__main__":
    main()
