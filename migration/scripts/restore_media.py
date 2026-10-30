import csv
import shutil
from pathlib import Path

ROOT = Path.cwd()
SOURCE = Path.home() / "Downloads/wp-admin/wp-content/uploads"
DEST = ROOT / "docs/assets/uploads"
MANIFEST = ROOT / "migration/reports/media-manifest.csv"

copied = 0
existing = 0
missing = []

with MANIFEST.open(encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        if row["category"] != "WARA":
            continue

        relative = Path(row["relative_path"])

        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe media path: {relative}")

        source = SOURCE / relative
        target = DEST / relative

        if not source.is_file():
            missing.append(str(relative))
            continue

        target.parent.mkdir(parents=True, exist_ok=True)

        if target.exists():
            existing += 1
            continue

        shutil.copy2(source, target)
        copied += 1

print("=== MEDIA RESTORATION ===")
print("Files copied:", copied)
print("Already present:", existing)
print("Missing:", len(missing))

for item in missing:
    print("MISSING:", item)
