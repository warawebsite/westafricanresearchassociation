import csv
import html
import re
from pathlib import Path
from urllib.parse import urlparse, unquote

DOCS = Path("docs")
REPORTS = Path("migration/reports")
REPORTS.mkdir(parents=True, exist_ok=True)

pattern = re.compile(
    r'https?://[^\s"\'<>]+/wp-content/uploads/[^\s"\'<>]+',
    re.I
)

records = {}

for file in DOCS.rglob("index.html"):
    content = html.unescape(
        file.read_text(encoding="utf-8", errors="replace")
    )

    for raw in pattern.findall(content):
        url = raw.rstrip("),;")
        parsed = urlparse(url)
        path = unquote(parsed.path)

        marker = "/wp-content/uploads/"
        if marker not in path:
            continue

        relative = path.split(marker, 1)[1]

        if parsed.hostname in (
            "westafricanresearchassociation.org",
            "www.westafricanresearchassociation.org"
        ):
            category = "WARA"
        else:
            category = "EXTERNAL"

        key = (category, relative)

        if key not in records:
            records[key] = {
                "category": category,
                "relative_path": relative,
                "source_url": url,
                "referenced_by": set()
            }

        records[key]["referenced_by"].add(file.as_posix())

output = REPORTS / "media-manifest.csv"

with output.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([
        "category",
        "relative_path",
        "source_url",
        "referenced_by"
    ])

    for record in sorted(
        records.values(),
        key=lambda x: (x["category"], x["relative_path"])
    ):
        writer.writerow([
            record["category"],
            record["relative_path"],
            record["source_url"],
            "; ".join(sorted(record["referenced_by"]))
        ])

print("=== MEDIA RECOVERY MANIFEST ===")
print("Distinct media paths:", len(records))
print("WARA media:", sum(
    r["category"] == "WARA" for r in records.values()
))
print("External media:", sum(
    r["category"] == "EXTERNAL" for r in records.values()
))
print("Saved:", output)
