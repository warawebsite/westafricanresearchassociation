import csv
import re
from pathlib import Path
from collections import Counter

DOCS = Path("docs")
REPORTS = Path("migration/reports")
REPORTS.mkdir(parents=True, exist_ok=True)

checks = {
    "wordpress_shortcode": r"\[[a-zA-Z][\w-]*(?:\s[^\]]*)?\]",
    "wordpress_media": r"wp-content/uploads/",
    "wordpress_admin": r"wp-admin|admin-ajax\.php|wp-json",
    "embedded_form": r"<form\b",
    "embedded_script": r"<script\b",
    "iframe": r"<iframe\b",
    "external_wara_link": r"https?://(?:www\.)?westafricanresearchassociation\.org",
    "placeholder": r"placeholder|content coming soon|read original"
}

rows = []

for file in sorted(DOCS.rglob("index.html")):
    content = file.read_text(encoding="utf-8", errors="replace")

    for category, pattern in checks.items():
        count = len(re.findall(pattern, content, re.I))
        if count:
            rows.append({
                "file": file.as_posix(),
                "issue": category,
                "count": count
            })

output = REPORTS / "content-audit.csv"

with output.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f, fieldnames=["file", "issue", "count"]
    )
    writer.writeheader()
    writer.writerows(rows)

print("=== CONTENT AUDIT ===")
print("Pages inspected:", len(list(DOCS.rglob("index.html"))))

for issue, count in Counter(r["issue"] for r in rows).items():
    print(f"{issue}: {count} affected files")

print("Report:", output)
