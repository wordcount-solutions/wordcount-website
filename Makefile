.DEFAULT_GOAL := build
ZOLA ?= zola
PYTHON ?= python3
SITE_URL ?= https://wordcount-solutions.github.io/wordcount-website
BASE_URL ?= $(SITE_URL)
OUTPUT_DIR ?= public
PORT ?= 1111
PRODUCTION_SOURCE ?= .
STAGING_SOURCE ?= .
# DreamHost URL and rsync destination; RSYNC_RSH supplies SSH options in Actions.
# DREAMHOST_SSH_PRIVATE_KEY is an Actions secret, written under RUNNER_TEMP there.
RSYNC ?= rsync
DREAMHOST_URL ?= https://wordcount.solutions
DREAMHOST_DEST ?= dh_wordcount@wordcount.solutions:wordcount.solutions/
RSYNC_FLAGS = --archive --compress --delete-after --exclude=/.htaccess --exclude=/.well-known/

.PHONY: build staging check test assemble verify-artifact sync-dreamhost preview serve clean pub

build:
	$(ZOLA) build --base-url "$(BASE_URL)" --output-dir "$(OUTPUT_DIR)" --force
	$(PYTHON) scripts/noindex_redirects.py "$(OUTPUT_DIR)" "$(BASE_URL)"

staging:
	$(MAKE) build BASE_URL="$(SITE_URL)/staging" OUTPUT_DIR=.tmp/staging

check:
	$(ZOLA) check --skip-external-links
	$(MAKE) build OUTPUT_DIR=.tmp/production
	$(MAKE) staging
	$(PYTHON) scripts/check_site.py .tmp/production "$(SITE_URL)"
	$(PYTHON) scripts/check_site.py .tmp/staging "$(SITE_URL)/staging"

test: check
	$(PYTHON) -m unittest discover -s tests

# Each source may be a separate branch checkout in GitHub Actions.
assemble: OUTPUT_DIR = .tmp/pages
assemble:
	$(MAKE) -C "$(PRODUCTION_SOURCE)" build SITE_URL="$(SITE_URL)" BASE_URL="$(SITE_URL)" OUTPUT_DIR=public
	$(MAKE) -C "$(STAGING_SOURCE)" build SITE_URL="$(SITE_URL)" BASE_URL="$(SITE_URL)/staging" OUTPUT_DIR=.tmp/staging
	$(PYTHON) scripts/assemble.py "$(PRODUCTION_SOURCE)/public" "$(STAGING_SOURCE)/.tmp/staging" "$(OUTPUT_DIR)"

verify-artifact: OUTPUT_DIR = .tmp/pages
verify-artifact:
	$(PYTHON) scripts/check_site.py "$(OUTPUT_DIR)" "$(SITE_URL)"
	$(PYTHON) scripts/check_site.py "$(OUTPUT_DIR)/staging" "$(SITE_URL)/staging"
	$(PYTHON) scripts/check_site.py "$(OUTPUT_DIR)/stage" "$(SITE_URL)/stage" --redirect

# Upload both branch snapshots together, only after validating the whole artifact.
sync-dreamhost:
	$(MAKE) verify-artifact SITE_URL="$(DREAMHOST_URL)" OUTPUT_DIR="$(OUTPUT_DIR)"
	$(RSYNC) $(RSYNC_FLAGS) "$(OUTPUT_DIR)/" "$(DREAMHOST_DEST)"

preview:
	$(MAKE) build BASE_URL=http://127.0.0.1:$(PORT) OUTPUT_DIR=.tmp/preview-production
	$(MAKE) build BASE_URL=http://127.0.0.1:$(PORT)/staging OUTPUT_DIR=.tmp/preview-staging
	$(PYTHON) scripts/assemble.py .tmp/preview-production .tmp/preview-staging .tmp/preview-combined
	$(PYTHON) -m http.server $(PORT) --bind 127.0.0.1 --directory .tmp/preview-combined

serve:
	$(ZOLA) serve --interface 127.0.0.1 --port $(PORT)

clean:
	rm -rf public .tmp/production .tmp/staging .tmp/pages .tmp/preview-production .tmp/preview-staging .tmp/preview-combined

# Manual production upload preserves staging and server-managed configuration.
pub:
	$(MAKE) build BASE_URL="$(DREAMHOST_URL)"
	$(RSYNC) $(RSYNC_FLAGS) --exclude=/staging/ --exclude=/stage/ public/ "$(DREAMHOST_DEST)"
