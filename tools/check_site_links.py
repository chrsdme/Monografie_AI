#!/usr/bin/env python3
"""Check generated MkDocs HTML for broken local targets and fragments.

MkDocs --strict does not rewrite/validate links written directly in HTML.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Targets(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        args = dict(attrs)
        anchor_id = args.get("id") or (args.get("name") if tag == "a" else None)
        if anchor_id:
            self.ids.add(anchor_id)
        uri = args.get("href") if tag in ("a", "link") else (
            args.get("src") if tag in ("img", "script") else None
        )
        if uri:
            self.links.append((tag, uri))


def audit(site: Path, site_prefix="/Monografie_AI/"):
    site = site.resolve()
    htmls = sorted(site.rglob("*.html"))
    if not htmls:
        raise ValueError("No generated HTML files found")
    parsed = {}
    for page in htmls:
        target = Targets()
        target.feed(page.read_text(encoding="utf-8"))
        parsed[page.resolve()] = target

    errors = []
    checked = 0
    for page, doc in parsed.items():
        for tag, uri in doc.links:
            parts = urlsplit(uri)
            if parts.scheme or parts.netloc:
                continue
            path = unquote(parts.path)
            fragment = unquote(parts.fragment)
            if path.startswith(site_prefix):
                destination = site / path[len(site_prefix):]
            elif path.startswith("/"):
                continue
            else:
                destination = page.parent / path if path else page
            destination = destination.resolve()
            checked += 1
            if not destination.is_relative_to(site):
                errors.append((page.relative_to(site).as_posix(), uri, "outside site root"))
                continue
            if destination.is_dir():
                destination = destination / "index.html"
            if not destination.exists() and not destination.suffix:
                alternatives = (destination / "index.html", destination.with_suffix(".html"))
                destination = next((item for item in alternatives if item.exists()), destination)
            if not destination.exists():
                errors.append((page.relative_to(site).as_posix(), uri, "missing target"))
                continue
            if destination.suffix == ".html" and fragment and destination in parsed:
                if fragment not in parsed[destination].ids:
                    errors.append((page.relative_to(site).as_posix(), uri, "missing fragment"))
    return len(htmls), checked, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", default="site")
    args = parser.parse_args()
    pages, checked, errors = audit(Path(args.site))
    for page, uri, reason in errors:
        print(f"ERROR: {page}: {uri}: {reason}")
    print(f"HTML LINK AUDIT: {pages} pages; {checked} local links/assets; {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
