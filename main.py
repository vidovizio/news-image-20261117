"""Copy the finished, deterministic news image into the competition output."""

import os
from pathlib import Path
import shutil


def main() -> None:
    source = Path(__file__).with_name("entry.png")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
