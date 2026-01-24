# Git Commands Reference

A quick reference guide for common Git workflows.

---

## 1. Create a Branch

### Create and switch to a new branch (recommended)

```bash
git checkout -b <branch-name>

# Example:
git checkout -b feature/user-authentication
```

### Alternative: Using modern Git syntax (Git 2.23+)

```bash
git switch -c <branch-name>
```

### Branch Naming Conventions

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New features | `feature/user-login` |
| `bugfix/` | Bug fixes | `bugfix/header-alignment` |
| `hotfix/` | Urgent production fixes | `hotfix/security-patch` |
| `release/` | Release preparation | `release/v1.0.0` |
| `docs/` | Documentation updates | `docs/api-guide` |

---

## 2. Add Files

### Add specific files

```bash
git add <file-name>

# Example:
git add index.html
git add src/app.js
```

### Add multiple files

```bash
git add <file1> <file2> <file3>

# Example:
git add index.html style.css app.js
```

### Add all changes in current directory

```bash
git add .
```

### Add all changes in entire repository

```bash
git add -A
```

### Add files interactively (choose which changes to stage)

```bash
git add -p
```

### Check what's staged vs unstaged

```bash
git status
```

---

## 3. Commit Changes

### Commit with a message

```bash
git commit -m "Your commit message"

# Example:
git commit -m "Add user authentication feature"
```

### Commit with multi-line message

```bash
git commit -m "Short summary" -m "Detailed description of changes"
```

### Add and commit in one step (only for tracked files)

```bash
git commit -am "Your commit message"
```

### Amend the last commit (fix message or add forgotten files)

```bash
# First, stage any additional files if needed
git add <forgotten-file>

# Then amend the commit
git commit --amend -m "Updated commit message"
```

### Commit Message Best Practices

| Type | Format | Example |
|------|--------|---------|
| Feature | `feat: description` | `feat: add login functionality` |
| Bug Fix | `fix: description` | `fix: resolve header overlap` |
| Docs | `docs: description` | `docs: update API documentation` |
| Refactor | `refactor: description` | `refactor: simplify auth logic` |
| Style | `style: description` | `style: format code with prettier` |
| Test | `test: description` | `test: add unit tests for auth` |

---

## 4. Push to GitHub

### Push branch to remote

```bash
git push -u origin <branch-name>

# Example:
git push -u origin feature/user-authentication
```

### Push subsequent commits (after initial push)

```bash
git push
```

### Force push (use with caution!)

```bash
git push --force
```

---

## 5. Common Workflow Example

```bash
# 1. Create and switch to a new branch
git checkout -b feature/new-feature

# 2. Make your changes to files...

# 3. Check status to see changed files
git status

# 4. Add files to staging
git add .

# 5. Commit your changes
git commit -m "feat: add new feature"

# 6. Push to GitHub
git push -u origin feature/new-feature
```

---

## 6. Useful Commands

### View commit history

```bash
git log --oneline
```

### View all branches

```bash
git branch -a
```

### Switch between branches

```bash
git checkout <branch-name>
# or
git switch <branch-name>
```

### Discard changes in a file

```bash
git checkout -- <file-name>
```

### Unstage a file

```bash
git reset HEAD <file-name>
```
