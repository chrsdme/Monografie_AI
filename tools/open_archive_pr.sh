#!/usr/bin/env bash
# Persist generated PDF through a reviewed PR instead of a direct push to main.
set -euo pipefail
name="Monografie_AI_De_la_Chat_la_Sisteme_Agentice"
version=$(python -c 'import pathlib,re; s=pathlib.Path("Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md").read_text(); print(re.search(r"^edition: \"([^\"]+)\"",s,re.M).group(1))')
# Re-read main: another archive PR may have merged since this job started.
# A duplicate is harmless, but a same-version/different-PDF race is not.
git fetch --quiet --no-tags origin main
if python tools/archive_pr_guard.py --repo . --check-open-prs; then
  :
else
  guard_status=$?
  if [ "$guard_status" -eq 10 ]; then
    echo "ARCHIVE: identical edition already persisted on main; no PR needed"
    exit 0
  fi
  exit "$guard_status"
fi
id=$(git rev-parse --short=10 HEAD)
branch="auto/archive-${version}-${id}"
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git checkout -b "$branch"
git add -- "${name}.md" docs/README.md docs/.publication.json \
  "docs/${name}.pdf" "docs/${name}_${version}.pdf"
git add -- wiki/index.md wiki/introducere.md
git add -- ':(glob)wiki/partea-*/*.md' ':(glob)wiki/anexe/*.md'
if [ -f content/book/manifest.json ]; then
  git add -- content/book/manifest.json ':(glob)content/book/fragments/*.md'
fi
if git diff --cached --quiet; then
  echo "ARCHIVE: no files to persist"
  exit 0
fi
git commit -m "chore(archive): edition ${version} PDF and publication metadata"
if git ls-remote --exit-code origin "refs/heads/${branch}" >/dev/null 2>&1; then
  echo "::warning::Archive branch already exists: ${branch}"
  exit 0
fi
git push origin "HEAD:refs/heads/${branch}"
if ! gh pr create \
    --base main \
    --head "$branch" \
    --title "Archive edition ${version} PDF and metadata" \
    --body "This PR adds the generated manuscript and canonical Studio fragments/manifest (when present), the immutable PDF, current PDF copy and publication metadata for edition ${version}. It requires owner review under Wiki_Rules; no direct push to main was performed."; then
  echo "::error::Enable GitHub Actions permission to create pull requests or open a PR manually from branch ${branch}."
  exit 1
fi
