# WARA GitHub Pages / Jekyll migration starter

This is a **working Jekyll starter**, not a verified full migration. It includes the homepage content from the supplied `Homepage(7).html`, the supplied About-page content, shared layouts, responsive navigation, and placeholder destinations for the existing menu. The placeholders link to the original WARA pages and must be replaced before cutover.

## GitHub Pages

1. Create a GitHub repository and upload the **contents** of this folder to its root.
2. Go to **Settings → Pages → Build and deployment** and choose **Deploy from a branch**, `main`, `/ (root)`.
3. For a project repository at `https://USERNAME.github.io/REPOSITORY/`, set `baseurl: "/REPOSITORY"` in `_config.yml`. For a root or custom-domain site, keep `baseurl: ""`.
4. Test the Pages URL before configuring the production domain.

## Edit content

- Homepage: `index.html`
- About: `about/index.html`
- Navigation: `_data/navigation.yml`
- Header and footer: `_includes/`
- Colors and layout: `assets/css/site.css`
- News cards: `index.html` and `news/index.html` (currently manually preserved from the uploaded HTML)
- Fellows: `_fellows/` (data staged; homepage cards currently static)

## Local preview

`bundle install` then `bundle exec jekyll serve`

## Critical outstanding work

See `MIGRATION_AUDIT.md`. In particular: original photographs and PDFs were not provided; some links remain on the existing WordPress site; membership, payment and newsletter functionality must be independently configured; and all content requires organizational review. No WordPress scripts, APIs, or runtime are needed to build this repository.
