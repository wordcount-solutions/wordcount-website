# WordCount Solutions Website

This is the source code for the WordCount Solutions website, built with [Zola](https://www.getzola.org/), a static site generator written in Rust.

Production is hosted on DreamHost at `https://wordcount.solutions/`, with staging at `https://wordcount.solutions/staging/`. GitHub Actions publishes both branch snapshots to DreamHost and GitHub Pages:

| Branch | GitHub Pages URL |
| --- | --- |
| `production` | https://wordcount-solutions.github.io/wordcount-website/ |
| `main` | https://wordcount-solutions.github.io/wordcount-website/staging/ |

Within the Pages site, `/stage/` redirects to `/staging/`. Both paths are public; staging pages display an amber **STAGING** banner and ask search engines not to index them.

## Project Structure

```
wordcount-website/
├── config.toml              # Main Zola configuration
├── content/                 # Content files (markdown)
│   ├── _index.md           # Homepage content
│   ├── team/               # Team member profiles
│   │   ├── _index.md       # Team section index
│   │   └── *.md            # Individual team member files
│   ├── testimonials/       # Client testimonials
│   ├── posts/              # Blog posts
│   └── projects/           # Project portfolio
├── static/                 # Static assets (copied to public/ during build)
│   └── images/
│       └── team/           # Team member photos
│           └── *.jpeg      # Team photos (Firstname-Lastname.jpeg format)
├── templates/              # Custom templates (override theme templates)
│   ├── index.html          # Homepage template
│   └── components/         # Custom component templates
│       ├── index.html      # Component router
│       └── team-section.html # Team section component
├── themes/                 # Zola theme
│   └── vonge/              # Vonge theme files
└── public/                 # Generated site (output directory - do not edit)
```

## Prerequisites

You need to have [Zola](https://www.getzola.org/) installed on your system.

### Installing Zola

**macOS (using Homebrew):**
```bash
brew install zola
```

**Linux:**
```bash
# Download from https://github.com/getzola/zola/releases
# Or use your distribution's package manager
```

**Windows:**
Download the executable from [Zola releases](https://github.com/getzola/zola/releases)

## Building and Serving the Site

### Serve Locally (Development)
```bash
make serve
```

This will start a local development server at `http://127.0.0.1:1111` that auto-reloads when you make changes.

### Build for Production
```bash
make build
```

This generates the static site in the `public/` directory.

Run `make test` to check both URL layouts and the deployment assembly. Run `make assemble` followed by `make verify-artifact` to build and check the combined Pages artifact in `.tmp/pages/`. `make preview` serves the combined root and staging layout locally at `http://127.0.0.1:1111/`.

## Editing Content

### Homepage

**File**: `content/_index.md`

The homepage content is configured in `content/_index.md` under `[[extra.content_blocks]]`. These blocks take precedence over the legacy fallback in `config.toml`, so direct edits to the homepage file are rendered by the next build. The main hero section includes:
- **Title**: The main homepage heading
- **Description**: The main tagline/description
- **Team Section**: Displays team members from `content/team/`

To modify the homepage content, edit the `[[extra.content_blocks]]` sections in `content/_index.md`. Each block has different properties:
- `block = "hero"`: Main hero section with title, description, and image
- `block = "team-section"`: Team member carousel section

### Team Page

**File**: `content/team-page.md`

The Team page displays all team members in a dedicated page. To edit:
1. Open `content/team-page.md`
2. Modify the `title` and `description` in the `page-heading` block
3. The team members are automatically loaded from `content/team/` directory

The page uses content blocks:
- `page-heading`: Page title and description
- `team-section`: Displays all team members
- `newsletter`: Newsletter subscription form

### Philosophy Page

**File**: `content/philosophy.md`

The Philosophy page (formerly Elements) contains your company philosophy and values. To edit:
1. Open `content/philosophy.md`
2. Modify the `title` in the front matter (currently "Philosophy")
3. Edit the `content_html` field in the `content` block to change the page content
4. You can use HTML tags in the `content_html` field for formatting

**Content Block Structure:**
- `page-heading`: Page title
- `page-image`: Optional header image
- `content`: Main page content (HTML)
- `newsletter`: Newsletter subscription form

### About Page

**File**: `content/about.md`

The About page contains information about WordCount Solutions. To edit:
1. Open `content/about.md`
2. Modify the `title` in the `page-image` block
3. Edit the `content_html` field in the `content` block
4. Optionally change the `page-image` block to use a different header image

The `page-image` block supports `overlay_title = true` to place its `title` over the image. Set `overlay_title = false` to show the title above the image. `title_color` accepts a CSS color such as `"white"`, `"black"`, `"red"`, or `"#17183b"`. `image_fade` is the opacity of a white layer over the photo: `0` leaves it unchanged and `1` makes it fully white. The About page currently uses `image_fade = 0.65` and a dark title. These settings are optional on other `page-image` blocks; existing images without a title render as before.

**Content Block Structure:**
- `page-image`: Header image and optional overlaid title
- `content`: Main page content (HTML)
- `newsletter`: Newsletter subscription form

### Team Members

Team members are displayed in a dedicated "WordCount Team" section on the homepage. Each team member requires:

1. **Photo**: Place team member photos in `static/images/team/` with the naming format:
   - `Firstname-Lastname.jpeg` (e.g., `John-Smith.jpeg`)
   - Use capital letters for the first letter of each name
   - Use hyphens to separate first and last names

2. **Content File**: Create a markdown file in `content/team/` with the same naming pattern:
   - `content/team/Firstname-Lastname.md`

3. **File Structure**: Each team member file should follow this format:

```toml
+++
[extra]
name = "Firstname Lastname"
position = "One sentence description of what they do"
image = "/images/team/Firstname-Lastname.jpeg"
blurb = ""
+++
```

**Fields:**
- `name`: Full name as it should appear on the website
- `position`: One sentence description of their role/responsibilities (appears under the photo)
- `image`: Path to the photo (must match the filename in `static/images/team/`)
- `blurb`: Leave empty (reserved for longer quotes/testimonials)

**Example:**
```toml
+++
[extra]
name = "John Smith"
position = "Senior Technical Writer specializing in API documentation"
image = "/images/team/John-Smith.jpeg"
blurb = ""
+++
```

### Adding a New Team Member

1. Add the photo to `static/images/team/Firstname-Lastname.jpeg`
2. Create `content/team/Firstname-Lastname.md` with the structure above
3. Fill in the `name` and `position` fields
4. The site will automatically rebuild and display the new team member

### Testimonials

Client testimonials are stored in `content/testimonials/`. Each testimonial file follows a similar structure to team members but includes a `blurb` field for the testimonial text.

**Testimonial File Format:**
```toml
+++
[extra]
name = "Client Name"
position = "Client Title/Company"
image = "/images/client-X.jpg"
blurb = "The testimonial text goes here."
+++
```

### Navigation

**File**: `config.toml`

The site navigation is configured in `config.toml` under `[extra.navigation]`. The current navigation includes:
- **Home**: Links to the homepage
- **Team**: Links to the team page (`/team-page`)
- **Pages** (dropdown):
  - **About**: Links to the about page
  - **Philosophy**: Links to the philosophy page

To modify navigation, edit the `navigation` array in `config.toml`. Each item can have:
- `url`: The page URL (use `$BASE_URL` for the site's base URL)
- `title`: The link text
- `submenu`: Optional array of submenu items

**Note**: Projects, Blog, and Tags sections are hidden from navigation but can be enabled by setting `show_projects = true`, `show_blog = true`, or `show_tags = true` in `config.toml` and adding them back to the navigation array.

## Static Assets

All files in `static/` are copied directly to `public/` during the build process, preserving the directory structure.

- **Team Photos**: `static/images/team/` → `public/images/team/`
- **Other Images**: `static/images/` → `public/images/`
- **CSS/JS**: Place in `static/css/` or `static/js/` as needed

## Configuration

### Main Configuration (`config.toml`)

The main site configuration is in `config.toml` at the root. Key sections:

- `[[extra.content_blocks]]`: Legacy homepage fallback when `content/_index.md` has no content blocks
- `[extra.navigation]`: Site navigation menu configuration
- `[extra.newsletter]`: Newsletter subscription configuration
- `social_media_share_image`: Default image used in Open Graph and Twitter link previews; page-specific SEO or image metadata can override it
- `show_projects`, `show_blog`, `show_tags`: Boolean flags to control section visibility (currently all set to `false`)
- `title`, `description`, `base_url`: Site metadata

### Theme

This site uses the **Vonge** theme (located in `themes/vonge/`) as its base. The theme provides:
- Homepage layout with content blocks
- Team/testimonials display components
- Blog and project templates
- Responsive design

**Note**: Do not modify files in `themes/vonge/` directly. Instead, override them by creating files in `templates/` at the root level.

## Custom Templates

Custom templates that override the theme are in `templates/`:

- `templates/index.html`: Homepage template
- `templates/components/team-section.html`: Custom team section component
- `templates/components/index.html`: Component router (adds team-section support)

## Troubleshooting

### Images Not Appearing
- Ensure images are in `static/images/team/` (not `public/`)
- Check that image paths in markdown files match the actual filenames
- Verify filenames match exactly (case-sensitive)
- Hard refresh browser: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows/Linux)

### Changes Not Showing
- Restart `make serve` if it's running
- Clear browser cache
- Check for build errors in the terminal

### Build Errors
- Verify TOML syntax in `config.toml` and content files
- Check that all referenced images exist
- Ensure markdown front matter is properly formatted

## Deployment

GitHub Pages is hosted from `wordcount-solutions/wordcount-website`. The production-branch preview is at `https://wordcount-solutions.github.io/wordcount-website/`, staging is at `https://wordcount-solutions.github.io/wordcount-website/staging/`, and `/stage/` redirects to `/staging/`. One Pages artifact contains the `production` branch at the project root and the `main` branch under `/staging/`. Every push to `main`, including direct commits from GitHub's website editor, rebuilds and publishes staging. `main` is intentionally unprotected; no PR is required. Pushes to `production` publish the root preview. An unmerged PR validates both builds and the combined artifact without deploying. Promote a reviewed staging version with a PR from `main` into `production`.

Staging is identified by the build base URL ending in `/staging` (with an optional trailing slash). The shared layout shows the banner on every staging content page, including the 404 page. Validation rejects missing staging banners or indexing exclusions, including under the GitHub project prefix; immediate pagination redirects only require indexing exclusions.

The workflow checks out both branches after acquiring one deployment lock. It builds and verifies two combined artifacts: one with GitHub Pages URLs and another with WordCount Solutions URLs. It deploys Pages, then rsyncs the DreamHost artifact to `dh_wordcount@wordcount.solutions:wordcount.solutions/`. Each artifact contains `production` at `/`, `main` at `/staging/`, and the `/stage/` redirect. A staging push never promotes content into `/`. Both snapshots are uploaded together, so production uploads retain staging. Deleted generated files disappear on the next deployment; DreamHost's root `.htaccess` and `.well-known/` are preserved.

Both branches must keep the `make build` interface and the updated `.github/workflows/pages.yml` for push-triggered deployments. Install the deployment changes on `main` first, then copy the workflow to `production` without promoting website content. Later website promotion remains a separate PR from `main` to `production`. An Actions run reads the workflow from its triggering branch, so updating only `main` is insufficient for production pushes.

### Initial GitHub setup

1. Give `@simsong-codex` write access and repository administration rights needed for Pages setup. Keep GitHub writes under that identity.
2. Use the **public** `wordcount-solutions/wordcount-website` repository. Keep `wordcount.solutions` DNS pointing to DreamHost and leave the Pages custom-domain field empty.
3. Push the initial `production` and `main` branches **before enabling the new workflow**. Keep the old single-branch Pages workflow absent or disabled during these initial pushes.
4. Add `.github/workflows/pages.yml` to both branches, then select **GitHub Actions** in **Settings → Pages**. Permit `main` and `production` in the `github-pages` environment. Run **Publish production and staging** if no push occurs after Pages is enabled.
5. Verify the production, staging, and redirect URLs on both hosts.

The workflow uses `SITE_URL=https://wordcount-solutions.github.io/wordcount-website` for Pages and `DREAMHOST_URL=https://wordcount.solutions` for DreamHost. Keep these separate so each build's navigation, assets, canonical URLs, and sitemap point to the correct host. A `CNAME` file is not needed for the Actions-published Pages site.

### DreamHost authentication

Store the deployment private key in the repository Actions secret `DREAMHOST_SSH_PRIVATE_KEY`, and install its public key in the DreamHost account's `~/.ssh/authorized_keys`. The workflow expects a key without a passphrase, writes it to a temporary file readable only by the runner user, validates it without printing it, and removes it in an always-run cleanup step. PR validation never receives this secret or deploys.

SSH uses `scripts/dreamhost_known_hosts` with strict host-key checking. Its public host key was verified through the existing trusted DreamHost connection and against the local known-hosts entry. Verify any future host-key replacement through a trusted channel before updating the file.

| Variable | Purpose |
| --- | --- |
| `SITE_URL` | GitHub Pages base URL; overridable with the repository Actions variable of the same name or a Make argument. |
| `DREAMHOST_URL` | DreamHost public base URL for the separate artifact; defaults to `https://wordcount.solutions`. |
| `DREAMHOST_DEST` | Make variable for the rsync destination; defaults to `dh_wordcount@wordcount.solutions:wordcount.solutions/`. |
| `DREAMHOST_SSH_PRIVATE_KEY` | Actions secret used only by the SSH setup step. |
| `RSYNC_RSH` | SSH command and options used by rsync; Actions selects the temporary key and pinned host-key file. |
| `RSYNC` | Optional Make override for the rsync executable. |
| `RUNNER_TEMP`, `GITHUB_WORKSPACE` | GitHub-provided directories for temporary artifacts/key files and checked-out branch sources. |

`make test` includes a real local rsync regression for stale-file removal, staging isolation, preservation of server configuration, and rejection of incomplete artifacts. `make assemble verify-artifact SITE_URL=https://wordcount.solutions OUTPUT_DIR=.tmp/dreamhost` checks the DreamHost layout without uploading. After building the intended branch snapshots, `make sync-dreamhost OUTPUT_DIR=.tmp/dreamhost` verifies and uploads that combined artifact. A failed second-host upload leaves the already successful Pages deployment intact; rerun the workflow to retry.

### Manual DreamHost deployment

The `make pub` target builds for `DREAMHOST_URL` and uploads `public/` to `DREAMHOST_DEST` over SSH. It publishes the current checkout and removes obsolete generated files while preserving `/staging/`, `/stage/`, root `.htaccess`, and `.well-known/`. Run it explicitly from the intended release checkout; GitHub Actions uses the combined-artifact target instead.

## Quick Reference

| Task | Location |
|------|----------|
| Edit homepage content | `content/_index.md` |
| Edit Team page | `content/team-page.md` |
| Edit Philosophy page | `content/philosophy.md` |
| Edit About page | `content/about.md` |
| Add team member | `content/team/Firstname-Lastname.md` + `static/images/team/Firstname-Lastname.jpeg` |
| Add testimonial | `content/testimonials/Client-Name.md` |
| Modify navigation | `config.toml` → `[extra.navigation]` |
| Team photos | `static/images/team/` |
| Other images | `static/images/` |

## Support

For Zola documentation, visit: https://www.getzola.org/documentation/

For theme-specific questions, see: `themes/vonge/README.md`
