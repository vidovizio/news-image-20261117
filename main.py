from pathlib import Path
import os
import shutil


def main() -> None:
    source = Path(__file__).resolve().with_name("entry.png")
    if not source.is_file():
        raise FileNotFoundError("entry.png must be beside main.py")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
