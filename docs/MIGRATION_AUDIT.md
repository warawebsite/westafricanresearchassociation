# Migration audit / remaining work

## Implemented
- Jekyll structure and GitHub Pages configuration
- Shared responsive navigation, footer and page layout
- Homepage: original mission, featured fellow, and news-card text from the supplied saved HTML
- About: content extracted from the supplied saved HTML
- Fellowship, program, WARC, membership, donation, news and involvement landing pages
- Navigable submenu destinations with explicit original-site links where the complete content is not yet migrated

## Not complete
- Many submenu pages are **clearly marked placeholders**, not full content migrations.
- News article cards link to their original site; full articles/comments have not been migrated.
- Original images are not present in the supplied HTML file; download or upload approved originals to `assets/images/` and update the references.
- Annual report and bylaws PDFs have not been migrated. Existing About links may still refer to the original site.
- Existing donation, membership, application, newsletter, and forms need external-service integration and testing.
- SEO redirects, canonical URL checks, content audits, accessibility audits and production-domain cutover remain outstanding.

## Missing homepage assets (as referenced in supplied HTML)
- `./Homepage_files/29809032-book-shelf-in-form-of-head-on-gray-backgrounds.jpg`
- `./Homepage_files/10410217_800862919972273_1104417780587733614_n-1.jpg`
- `./Homepage_files/world-1303628_960_720.png`
- `./Homepage_files/IMG_6529-1.jpg`
- `./Homepage_files/IMG-20210513-WA0042-1.jpg`
- `./Homepage_files/Susan-and-Aisha-cropped-1.png`
- `./Homepage_files/IMG_20210625_162506_143-1.jpg`

## Launch rule
Do not switch the production domain until all pages and assets have been reviewed and external services tested.
