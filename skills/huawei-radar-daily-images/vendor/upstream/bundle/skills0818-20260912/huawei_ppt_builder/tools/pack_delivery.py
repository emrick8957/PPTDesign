#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys


def main(delivery_dir: str, output_zip: str | None = None) -> int:
    base = Path(delivery_dir)
    if not base.exists():
        print(f"Delivery directory not found: {base}")
        return 1
    output = Path(output_zip) if output_zip else base.with_suffix("")
    zip_path = shutil.make_archive(str(output), "zip", base)
    print(zip_path)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
