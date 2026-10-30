import csv
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path.home() / "Documents/GitHub"
BACKUP = ROOT / "WARA-private-backup"
REPORTS = ROOT / "westafricanresearchassociation/migration/reports"

REPORTS.mkdir(parents=True, exist_ok=True)

xml_file = BACKUP / (
    "westafricanresearchassociationwara."
    "WordPress.2026-10-30.xml"
)

ns = {
    "wp": "http://wordpress.org/export/1.2/"
}

tree = ET.parse(xml_file)
rows = []

for item in tree.findall(".//channel/item"):
    def value(path):
        return item.findtext(path, default="", namespaces=ns)

    rows.append({
        "title": value("title"),
        "url": value("link"),
        "type": value("wp:post_type"),
        "status": value("wp:status"),
        "date": value("wp:post_date"),
        "slug": value("wp:post_name"),
        "id": value("wp:post_id")
    })

output = REPORTS / "wordpress-inventory.csv"

with output.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "title", "url", "type", "status",
        "date", "slug", "id"
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Records found: {len(rows)}")
print(f"Inventory saved: {output}")

from collections import Counter

for kind, count in Counter(r["type"] for r in rows).items():
    print(f"{kind}: {count}")
