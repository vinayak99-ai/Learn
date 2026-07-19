---
name: release-summary
description: Generate a release summary between two git tags for a tracked repo, then update the product features file and changelog. Use when a release manager runs a release and asks things like "run release summary for <repo> from <old-tag> to <new-tag>", "update the changelog for this release", "generate product feature diff for the release", or "prepare release notes for <repo>". Requires the gh CLI authenticated locally.
---

# Release Summary

Turns two release tags into (1) a release summary, (2) an updated product
features file, and (3) an updated changelog entry — driven entirely from
the release manager's local terminal via `gh` and `git`. No CI, no
webhooks, no background state. Full design rationale: `plans/release-summary.md`.

## Before you start

Confirm with the user (don't guess):
- **Which repo** (must be in the tracked list below, or explicitly added for
  this run).
- **Old tag** and **new tag** to compare.

Check `gh auth status`. If not authenticated, stop and tell the user to run
`gh auth login` first — don't attempt to work around missing auth.

## Tracked repos

Read from `release-tracking/repos.yaml` (create it from the template below
on first use if missing). Only operate on repos listed here unless the user
explicitly names one outside the list for a one-off run.

```yaml
repos:
  - owner: vinayak99-ai
    repo: quiz
  - owner: vinayak99-ai
    repo: learn
```

## Step 1 — Gather the raw release data

Run, in order, stopping at the first that returns usable content:

```bash
# Preferred: GitHub's native categorized release notes
gh api repos/OWNER/REPO/releases/generate-notes \
  -f tag_name="NEW_TAG" \
  -f previous_tag_name="OLD_TAG" \
  --jq '.body'
```

If that returns empty or the repo has no `.github/release.yml` grouping
worth trusting, fall back to:

```bash
git -C <local-clone-path> fetch --tags
git -C <local-clone-path> log OLD_TAG..NEW_TAG --pretty=format:'- %s (%h) by %an'
```

Cross-check against merged PRs when commit messages look squashed/unclear:

```bash
gh pr list --repo OWNER/REPO --state merged \
  --search "merged:$(git -C <local-clone-path> log -1 --format=%aI OLD_TAG)..$(git -C <local-clone-path> log -1 --format=%aI NEW_TAG)" \
  --json number,title,labels,author
```

## Step 2 — Classify each entry

Sort every entry from Step 1 into exactly one bucket:

- **Product feature added/removed** — user-visible capability or behavior
  change.
- **Technical/internal** — refactors, dependency bumps, CI/build changes,
  internal-only fixes.

Use PR labels or Conventional Commit prefixes (`feat:`, `fix:`, `chore:`)
when present — they're close to ground truth. When absent, infer from the
diff/PR description, and say so if a classification is a guess rather than
a clear signal, so the release manager can correct it during review.

## Step 3 — Update `release-tracking/product-features.md`

Replace **only this repo's section**, fully, using this exact structure —
stability here is what keeps Step 4's diff clean:

```markdown
## <repo>

<!-- last updated: <NEW_TAG> (<today's date>) -->

- <feature bullet>
- <feature bullet>
- ~~<removed feature>~~ (removed)
```

Do not touch other repos' sections. Do not append — overwrite the section
between its `## <repo>` heading and the next `## ` heading (or end of file).
If the file doesn't exist yet, create it with a one-line header (`# Product
Features`) followed by each tracked repo's section.

## Step 4 — Update `CHANGELOG.md`

After Step 3's file is written (but before committing), diff it to build
the changelog entry:

```bash
git -C /workspace/learn diff -- release-tracking/product-features.md
```

Turn that diff into a new dated section, prepended under the top-level
heading (newest first):

```markdown
## <today's date> — <repo> <NEW_TAG>

### Added
- <feature bullet>

### Removed
- <feature bullet>
```

Skip a subsection (`### Added` / `### Removed`) entirely if it has no
entries — don't emit empty headers.

## Step 5 — Show the diff, then commit only on confirmation

Show the release manager the full diff of both files
(`git diff -- release-tracking/product-features.md CHANGELOG.md`) before
committing anything. Once they confirm:

```bash
git add release-tracking/product-features.md CHANGELOG.md
git commit -m "release summary: <repo> <OLD_TAG> -> <NEW_TAG>"
git push
```

Never push without an explicit go-ahead in that turn, even if a previous
run was approved — each release gets its own confirmation.

## Guardrails

- Never invent a tag, repo, or version — ask if any input is missing.
- Never fabricate release content if `gh api`/`git log` return nothing;
  report the empty result instead of guessing what changed.
- Keep `product-features.md` sections in the same order as
  `release-tracking/repos.yaml` so diffs stay predictable across runs.
