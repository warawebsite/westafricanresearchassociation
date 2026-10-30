from pathlib import Path
from html import escape
import re
import shutil
import sys

ROOT = Path.cwd()
DOCS = ROOT / "docs"
BACKUP = ROOT / "migration" / "gallery-backup"
UPLOADS = Path.home() / "Downloads/wp-admin/wp-content/uploads/2018/07"

FILES = {
    "218": "DSC_0528.jpg",
    "443": "337482_291257707604200_1247579323_o.jpg",
}

GALLERIES = {
    "announcements/evenements-au-warc/index.html":
        ["464", "465"],
    "announcements/in-their-own-words/index.html":
        ["233", "221", "218", "239", "251"],
    "announcements/join-us-for-africa-awareness-week-at-bsu/index.html":
        ["444", "443", "451", "452"],
    "announcements/warc-ceremonie-de-dedicace-de-prof-ousmane-oumar-kane-harvard-university/index.html":
        ["261", "262"],
}

GALLERY_PATTERN = re.compile(
    r'\[gallery\b[^\]]*\]',
    re.IGNORECASE
)

YOUTUBE_PATTERN = re.compile(
    r'\[youtube\s+https?://(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]+)\s*\]',
    re.IGNORECASE
)

CAPTION_PATTERN = re.compile(
    r'\[caption\b[^\]]*\](.*?)\[/caption\]',
    re.IGNORECASE | re.DOTALL
)

def save_page(path, content):
    original = path.read_text(encoding="utf-8")

    if original == content:
        return False

    backup_path = BACKUP / path.relative_to(DOCS)
    backup_path.parent.mkdir(parents=True, exist_ok=True)

    if not backup_path.exists():
        shutil.copy2(path, backup_path)

    path.write_text(content, encoding="utf-8")
    return True

def build_gallery(ids):
    cards = []
    missing = []

    for image_id in ids:
        filename = FILES.get(image_id)

        if filename:
            source = UPLOADS / filename

            if source.is_file():
                target = DOCS / "assets/uploads/2018/07" / filename
                target.parent.mkdir(parents=True, exist_ok=True)

                if not target.exists():
                    shutil.copy2(source, target)

                url = (
                    "{{ '/assets/uploads/2018/07/"
                    + filename
                    + "' | relative_url }}"
                )

                cards.append(
                    '<figure class="wara-gallery-item">'
                    '<a href="' + url + '" target="_blank" rel="noopener">'
                    '<img src="' + url + '" loading="lazy" '
                    'alt="Historical WARA event photograph">'
                    '</a>'
                    '</figure>'
                )
                continue

        missing.append(image_id)

    result = []

    if cards:
        result.append(
            '<div class="wara-gallery" aria-label="Historical event photographs">'
            + "\n".join(cards)
            + '</div>'
        )

    if missing:
        result.append(
            '<p class="wara-gallery-archive-note">'
            'Additional photographs from this historical gallery '
            'have not yet been recovered from the available archive.'
            '</p>'
        )

    return "\n".join(result)

def replace_youtube(match):
    video_id = match.group(1)

    return (
        '<div class="wara-video">'
        '<iframe '
        'src="https://www.youtube-nocookie.com/embed/'
        + video_id
        + '" '
        'title="WARA historical lecture recording" '
        'loading="lazy" '
        'referrerpolicy="strict-origin-when-cross-origin" '
        'allow="accelerometer; autoplay; clipboard-write; '
        'encrypted-media; gyroscope; picture-in-picture; web-share" '
        'allowfullscreen>'
        '</iframe>'
        '</div>'
    )

def replace_caption(match):
    inner = match.group(1).strip()

    image_match = re.search(
        r'<img\b[^>]*>',
        inner,
        re.IGNORECASE | re.DOTALL
    )

    if not image_match:
        return match.group(0)

    image = image_match.group(0)
    caption = (
        inner[:image_match.start()]
        + inner[image_match.end():]
    ).strip()

    if caption:
        return (
            '<figure class="wara-figure">'
            + image
            + '<figcaption>'
            + caption
            + '</figcaption></figure>'
        )

    return '<figure class="wara-figure">' + image + '</figure>'

def main():
    if not DOCS.exists():
        sys.exit("ERROR: Run this script from the repository root.")

    print("=== RESTORING WARA HISTORICAL GALLERIES ===")

    for relative, ids in GALLERIES.items():
        path = DOCS / relative

        if not path.exists():
            print("SKIPPED, page missing:", relative)
            continue

        content = path.read_text(encoding="utf-8")
        matches = list(GALLERY_PATTERN.finditer(content))

        if not matches:
            print("SKIPPED, no gallery shortcode:", relative)
            continue

        gallery = build_gallery(ids)

        content = GALLERY_PATTERN.sub(
            lambda _: gallery,
            content,
            count=1
        )

        if save_page(path, content):
            print("UPDATED:", relative)

    for path in DOCS.rglob("*.html"):
        content = path.read_text(encoding="utf-8")

        updated = YOUTUBE_PATTERN.sub(replace_youtube, content)
        updated = CAPTION_PATTERN.sub(replace_caption, updated)

        if save_page(path, updated):
            print("SHORTCODES UPDATED:", path.relative_to(DOCS))

    print("\nMigration complete.")
    print("Original page backups:", BACKUP)

if __name__ == "__main__":
    main()
