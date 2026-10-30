import re
from pathlib import Path
from urllib.parse import urlparse, unquote

DOCS = Path("docs")
MEDIA = DOCS / "assets/uploads"

pattern = re.compile(
    r'https?://(?:www\.)?westafricanresearchassociation\.org/wp-content/uploads/[^\s"\'<>]+',
    re.I
)

changed_files = 0
replacements = 0
missing = set()

for file in DOCS.rglob("index.html"):
    content = file.read_text(encoding="utf-8")

    def replace(match):
        global replacements

        original = match.group(0)
        parsed = urlparse(original)

        relative = unquote(
            parsed.path.split("/wp-content/uploads/", 1)[1]
        )

        local = MEDIA / relative

        if not local.is_file():
            missing.add(relative)
            return original

        replacements += 1

        return "{{ '/assets/uploads/" + relative + "' | relative_url }}"

    updated = pattern.sub(replace, content)

    if updated != content:
        file.write_text(updated, encoding="utf-8")
        changed_files += 1

print("=== MEDIA URL REWRITING ===")
print("Pages updated:", changed_files)
print("References replaced:", replacements)
print("Missing files:", len(missing))

for item in sorted(missing):
    print("MISSING:", item)
