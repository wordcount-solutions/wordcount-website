"""Exercise DreamHost publishing against a real local rsync destination.

Build small valid production and staging trees, then assemble one artifact.
Run the same Makefile sync target used by Actions without SSH or secrets.
Verify stale files disappear while server configuration survives uploads.
Check that staging and production retain independent content on updates.
Reject incomplete artifacts before rsync can change the destination.
"""

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.assemble import assemble


class DreamHostSyncTests(unittest.TestCase):
    def test_sync_preserves_host_files_and_branch_isolation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            production, staging, artifact, remote = (root / name for name in ("prod", "staging", "artifact", "remote"))
            for source in (production, staging):
                for name in ("index.html", "about/index.html", "contact/index.html", "team-page/index.html", "404.html"):
                    page = source / name
                    page.parent.mkdir(parents=True, exist_ok=True)
                    markup = "<p>Production</p>"
                    if source == staging:
                        markup = '<meta name="robots" content="noindex, nofollow"><aside id="staging-banner">Staging v1</aside>'
                    page.write_text(markup)
                (source / "robots.txt").write_text("User-agent: *\n")
            (remote / ".well-known").mkdir(parents=True)
            (remote / ".well-known" / "challenge").write_text("certificate validation")
            (remote / ".htaccess").write_text("server configuration")
            (remote / "staging").mkdir()
            for target in (remote, remote / "staging"):
                (target / "obsolete.html").write_text("old file")
            # Even an artifact-provided file must not replace host configuration.
            (production / ".htaccess").write_text("unwanted override")
            assemble(production, staging, artifact)
            command = ["make", "sync-dreamhost", f"OUTPUT_DIR={artifact}", f"DREAMHOST_DEST={remote}/"]
            subprocess.run(command, check=True, capture_output=True, text=True)
            self.assertEqual((remote / "index.html").read_text(), "<p>Production</p>")
            self.assertIn("Staging v1", (remote / "staging/index.html").read_text())
            for target in (remote, remote / "staging"):
                self.assertFalse((target / "obsolete.html").exists())
            page = staging / "index.html"
            page.write_text(page.read_text().replace("v1", "version two"))
            assemble(production, staging, artifact)
            subprocess.run(command, check=True, capture_output=True, text=True)
            self.assertEqual((remote / "index.html").read_text(), "<p>Production</p>")
            self.assertIn("version two", (remote / "staging/index.html").read_text())
            self.assertEqual((remote / ".htaccess").read_text(), "server configuration")
            self.assertEqual((remote / ".well-known/challenge").read_text(), "certificate validation")
            (artifact / "staging/index.html").unlink()
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("version two", (remote / "staging/index.html").read_text())
