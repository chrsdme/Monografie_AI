# Gate A verification

Date: 2026-10-22
Branch: `studio-test`

## Existing fragment set

- `content/book/manifest.json` lists 242 fragments (`BOOK-0001` through `BOOK-0242`) in explicit assembly order.
- Declared source and generated SHA256: `1e12008817bd34dcf161b4aa4f59cae94689fba04dd68c632ba2b5ae253b70ed`.
- The manifest and fragment directory were inspected read-only. No migration was run and no fragment was changed.
- Windows `.venv` command `python tools/studio.py assemble` passed byte-for-byte with the same SHA256.
- Windows `.venv` command `python -m unittest discover -s tests -p test_studio.py -v` passed all 6 tests.

## Gate A blocker

Gate A is not activated. `tools/release.py` edits only the monolithic Markdown file. `tools/studio.py build` subsequently assembles the file from fragments and can overwrite those release edits with the fragment contents. The GitHub publication workflow also invokes release and `tools/ci-build.sh` against the monolithic file; it does not validate the fragment manifest or preserve release metadata in fragments. Therefore an edition/date/changelog update could diverge or be lost, and the canonical-source handoff is not safe yet.

The required repair is to make release transformations update the canonical fragment set and regenerate the monolithic build input from it, then have CI assert manifest integrity and round-trip parity before wiki/PDF generation and archiving. Until that change is implemented and tested, no full build, PDF generation, release operation, or destination implementation was run.

## Scope not verified

Fragment-level hash validation, bibliography/glossary/link integrity, MkDocs strict build, PDF generation, published-link checks, and the wiki/book/resource destination matrix remain unverified.
