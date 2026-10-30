import csv
import re
import html
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path.cwd()
DOCS = ROOT / "docs"
REPORTS = ROOT / "migration/reports"

SOURCE = (
    ROOT.parent / "WARA-private-backup" /
    "westafricanresearchassociationwara.WordPress.2026-10-30.xml"
)

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/"
}

tree = ET.parse(SOURCE)
items = tree.findall(".//channel/item")

REPORTS.mkdir(parents=True, exist_ok=True)

records = []
created = 0
skipped = 0

def get(item, path):
    return item.findtext(path, default="", namespaces=NS)

def frontmatter(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'

for item in items:
    status = get(item, "wp:status")
    kind = get(item, "wp:post_type")

    if status != "publish" or kind not in ("page", "post"):
        continue

    title = get(item, "title")
    url = get(item, "link")
    body = get(item, "content:encoded")

    parsed = urlparse(url)

    # Accept only content from the original WARA domain
    if parsed.hostname not in (
        "westafricanresearchassociation.org",
        "www.westafricanresearchassociation.org"
    ):
        continue

    path = parsed.path.strip("/")

    if not path:
        destination = DOCS / "index.html"
    else:
        parts = Path(path).parts
        if any(p in (".", "..") or p.startswith(".") for p in parts):
            continue
        destination = DOCS.joinpath(*parts) / "index.html"

    result = "skipped_existing"

    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)

        # Preserve WordPress HTML for later review.
        # WordPress shortcodes and forms still require conversion.
        content = f"""---
layout: page
title: {frontmatter(title)}
permalink: /{path + '/' if path else ''}
---

{body}
"""

        destination.write_text(content, encoding="utf-8")
        result = "created"
        created += 1
    else:
        skipped += 1

    records.append({
        "title": title,
        "type": kind,
        "url": url,
        "destination": str(destination.relative_to(ROOT)),
        "result": result,
        "body_characters": len(body)
    })

with (REPORTS / "conversion-report.csv").open(
    "w", newline="", encoding="utf-8-sig"
) as f:
    writer = csv.DictWriter(f, fieldnames=[
        "title", "type", "url",
        "destination", "result", "body_characters"
    ])
    writer.writeheader()
    writer.writerows(records)

print("=== WORDPRESS CONVERSION ===")
print("Published records processed:", len(records))
print("New pages created:", created)
print("Existing pages preserved:", skipped)
print("Report: migration/reports/conversion-report.csv")
