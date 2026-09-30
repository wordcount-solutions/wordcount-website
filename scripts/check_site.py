"""Validate rendered sites before publishing the combined Pages artifact.

Resolve internal links and CSS assets within each build's own URL prefix.
Recognize staging beneath both custom domains and GitHub project paths.
Require noindex metadata and a visible banner on staging content pages.
Allow Zola's immediate redirects to omit the content-page banner.
Run through Makefile checks for local builds and deployment artifacts.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.urls.extend(value for key, value in attrs if key in ("href", "src") and value)


def check(root: Path, base: str) -> None:
    root = root.resolve()
    base_parts = urlsplit(base)
    prefix = base_parts.path.rstrip("/") + "/"
    staging = prefix.endswith("/staging/")
    for relative in ("index.html", "about/index.html", "contact/index.html", "team-page/index.html", "404.html"):
        if not (root / relative).is_file():
            raise ValueError(f"Missing page: {root / relative}")
    if staging and not (root / "robots.txt").is_file():
        raise ValueError("Staging static assets are incomplete")
    for document in root.rglob("*.html"):
        html = document.read_text(encoding="utf-8")
        if staging and 'content="noindex, nofollow"' not in html:
            raise ValueError(f"Staging page is indexable: {document}")
        if staging and '<title>Redirect</title>' not in html and 'id="staging-banner"' not in html:
            raise ValueError(f"Staging page is missing its banner: {document}")
        parser = Links()
        parser.feed(html)
        document_url = base.rstrip("/") + "/" + document.relative_to(root).as_posix()
        for link in parser.urls:
            target = urlsplit(urljoin(document_url, link))
            if target.netloc != base_parts.netloc or target.scheme not in ("http", "https"):
                continue
            target_path = target.path or "/"
            if target_path == prefix.rstrip("/"):
                target_path += "/"
            if not target_path.startswith(prefix):
                raise ValueError(f"Link escapes {prefix}: {document}: {link}")
            local = root / unquote(target_path.removeprefix(prefix))
            if local.is_dir():
                local /= "index.html"
            if not local.is_file():
                raise ValueError(f"Broken link: {document}: {link}")
    for css in root.rglob("*.css"):
        for raw in re.findall(r"url\(([^)]+)\)", css.read_text(encoding="utf-8")):
            link = raw.strip("\"' ")
            if not link or link.startswith(("data:", "https:", "http:")):
                continue
            target = (css.parent / unquote(urlsplit(link).path)).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                raise ValueError(f"Missing CSS asset: {css}: {link}")
    print(f"Verified pages, links, assets, and staging policy: {base}")


def check_redirect(root: Path) -> None:
    html = (root / "index.html").read_text(encoding="utf-8")
    for required in ('content="noindex, nofollow"', 'content="0; url=../staging/"', 'href="../staging/"'):
        if required not in html:
            raise ValueError(f"Invalid /stage/ redirect: missing {required}")


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[3] == "--redirect":
        check_redirect(Path(sys.argv[1]))
    else:
        check(Path(sys.argv[1]), sys.argv[2])
