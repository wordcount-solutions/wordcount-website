"""Exercise staging safeguards at domain and project-site URL prefixes.

Create small real HTML trees with the pages required by the site checker.
Confirm missing banners and indexing metadata reject staging artifacts.
Keep production pages and immediate Zola redirects valid without banners.
Use temporary files so these checks need no network or service mocks.
The Makefile runs these regressions alongside real Zola build validation.
"""

import tempfile
import unittest
from pathlib import Path

from scripts.check_site import check


class StagingPolicyTests(unittest.TestCase):
    def test_staging_policy_for_each_url_layout(self) -> None:
        for suffix in ("/staging", "/wordcount-website/staging/"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                base = "https://example.com" + suffix
                noindex = '<meta name="robots" content="noindex, nofollow">'
                banner = '<aside id="staging-banner">STAGING</aside>'
                for name in ("index.html", "about/index.html", "contact/index.html", "team-page/index.html", "404.html"):
                    page = root / name
                    page.parent.mkdir(parents=True, exist_ok=True)
                    page.write_text(noindex + banner)
                (root / "robots.txt").write_text("User-agent: *\n")
                (root / "redirect.html").write_text(noindex + '<title>Redirect</title>')
                check(root, base)
                (root / "index.html").write_text(noindex)
                with self.assertRaisesRegex(ValueError, "missing its banner"):
                    check(root, base)
                (root / "index.html").write_text(banner)
                with self.assertRaisesRegex(ValueError, "indexable"):
                    check(root, base)
                for page in root.rglob("*.html"):
                    page.write_text("<p>Production</p>")
                check(root, "https://example.com/wordcount-website")
