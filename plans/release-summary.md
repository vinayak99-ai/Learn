# Release Summary: Local GitHub CLI Workflow

How a release manager generates a release summary from two release tags, entirely
from a local terminal using `gh` + `git`, and uses it to update the product
features file and the changelog. The whole process is driven by one
`SKILL.md` — no CI, no servers, no state files beyond the two markdown files
being maintained.

## Prerequisites

- `gh` CLI installed and authenticated: `gh auth login` (needs `repo` read scope
  for every tracked repo, including private ones).
- `git` installed.
- Each tracked repo either cloned locally, or reachable via `gh api` (no clone
  needed — the commands below work against the GitHub API directly).
- `jq` optional, only used for readability in a couple of examples below.

## Step 1 — Define which repos to connect to

Kept as a plain list inside the skill (or a small `repos.yaml` next to it) —
this is the only piece of "config" the process needs:

```yaml
# release-tracking/repos.yaml
repos:
  - owner: vinayak99-ai
    repo: quiz
  - owner: vinayak99-ai
    repo: learn
```

## Step 2 — Get the release summary for one repo, given two tags

The release manager supplies the two tags being compared (old → new), e.g.
`v1.2.0` and `v1.3.0`. Two ways to gather what changed:

**Option A — GitHub's native generated notes (preferred).** This uses the
same engine as GitHub's "Generate release notes" button, grouping PRs by
label if `.github/release.yml` exists, and crediting authors automatically:

```bash
gh api repos/OWNER/REPO/releases/generate-notes \
  -f tag_name="v1.3.0" \
  -f previous_tag_name="v1.2.0" \
  --jq '.body' > /tmp/OWNER-REPO-v1.3.0-notes.md
```

**Option B — Raw commit diff (fallback for repos without clean PR/label
hygiene).** Works even without releases configured:

```bash
git fetch --tags
git log v1.2.0..v1.3.0 --pretty=format:'- %s (%h) by %an' > /tmp/OWNER-REPO-v1.3.0-raw.md
```

**Cross-check with merged PRs directly** (useful when commits are squashed
and Option A's grouping needs verifying):

```bash
gh pr list --repo OWNER/REPO --state merged \
  --search "merged:$(git log -1 --format=%aI v1.2.0)..$(git log -1 --format=%aI v1.3.0)" \
  --json number,title,labels,author \
  --jq '.[] | "- #\(.number) \(.title) (\(.author.login))"'
```

Run Step 2 once per repo in the tracked list, for that repo's own two tags
(tags don't need to line up across repos — each repo has its own version
history).

## Step 3 — Classify: product feature vs. technical

This is the step the skill's instructions (not a script) do: read each
repo's generated notes/diff and sort every entry into one of two buckets:

- **Product features added/removed** — anything a user of the product would
  notice (new capability, removed capability, behavior change).
- **Technical/internal** — refactors, dependency bumps, CI changes, internal
  fixes with no user-visible effect.

Classification quality depends on input quality: PR labels or Conventional
Commit prefixes (`feat:`, `fix:`, `chore:`) make this close to mechanical;
terse/unlabeled commits make it inference from the diff, so spot-check the
first few runs.

## Step 4 — Update the main product features file

File: `release-tracking/product-features.md`. **Regenerate the section for
this repo fully, in a fixed template, every run** — don't hand-edit or
append in place. This matters: if the structure (heading order, one bullet
per feature) isn't stable across runs, later diffing this file for the
changelog produces noise instead of a clean set of adds/removes.

```markdown
## quiz

<!-- last updated: v1.3.0 (2026-07-19) -->

- Timed quiz mode with configurable countdown
- CSV import for question banks
- ~~Legacy XML question format~~ (removed)
```

Replace the whole `## quiz` section each time this repo is processed; leave
every other repo's section untouched.

## Step 5 — Update the changelog

File: `CHANGELOG.md`. Two ways to produce it, pick one and stay consistent:

- **Diff-based (recommended, least manual work):** after Step 4 updates
  `product-features.md` and it's committed, the changelog entry is just
  `git diff` of that file between this commit and the previous one:
  ```bash
  git diff HEAD~1 -- release-tracking/product-features.md
  ```
  The skill turns that diff into a dated changelog entry automatically —
  git history *is* the version tracking, no separate state file needed.

- **Append-based (simpler to read, slightly more manual):** the skill
  appends a new dated section directly, sourced from Step 3's classified
  list:
  ```markdown
  ## 2026-07-19 — quiz v1.3.0

  ### Added
  - Timed quiz mode with configurable countdown
  - CSV import for question banks

  ### Removed
  - Legacy XML question format
  ```

## Step 6 — Commit

```bash
git add release-tracking/product-features.md CHANGELOG.md
git commit -m "release summary: quiz v1.2.0 -> v1.3.0"
git push
```

## How this maps to SKILL.md

The whole workflow above is one skill. Its `SKILL.md` holds:

1. **The repo list** (Step 1) — which repos it's allowed to touch.
2. **Inputs it asks for at invocation time** — repo name, old tag, new tag
   (release manager supplies these; the skill doesn't guess versions).
3. **The exact `gh`/`git` commands from Step 2** it runs to gather data.
4. **The classification instructions from Step 3.**
5. **The fixed templates from Steps 4 and 5**, so output stays diff-stable
   across runs.
6. **The commit step**, left as a proposed command for the release manager
   to review before it runs — never auto-pushed without a look.

Nothing here needs a scheduled job, a webhook, or a state file: the release
manager runs the skill from their own terminal each time a release happens,
supplies the two tags, and reviews the diff before pushing.
