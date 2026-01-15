# Learn
To keep all learning docs 

## Table of Contents

1. [Quiz File Analysis](#quiz-file-analysis)
2. [GitHub Operations Guide](#github-operations-guide)
   - [Combining README Files from Multiple Repositories](#1-combining-readme-files-from-multiple-repositories)
   - [Using GitHub API to Extract Changes Between Releases](#2-using-github-api-to-extract-changes-between-releases)

---

## Quiz File Analysis

The repository contains a comprehensive quiz file (`quiz-format.csv`) with 298 questions covering multiple topics and languages.

### 📊 Quiz Statistics

- **Total Questions**: 298
- **Topics**: 12 different categories
- **Languages**: Kannada, Hindi, and English
- **Format**: CSV with 7 fields (question, option_a, option_b, option_c, option_d, correct_answer, topic)

### ⚠️ Important Finding: Answer Distribution Bias

Analysis of the quiz file has revealed a **critical issue** with the distribution of correct answers:

| Correct Answer | Count | Percentage | Status |
|---------------|-------|------------|--------|
| A | 14 | 4.7% | ⚠️ Too Low |
| **B** | **161** | **54.0%** | ❌ Too High |
| C | 110 | 36.9% | ⚠️ High |
| D | 13 | 4.4% | ⚠️ Too Low |

**Problem**: 54% of all questions have "B" as the correct answer, which is more than double the ideal distribution (25% per option). This creates a significant bias where test-takers could achieve better scores by predominantly guessing "B".

### 📝 Topics with Highest Bias

Some topics show particularly severe bias:
- **Hindi Fill Blanks**: 89.7% of answers are B
- **Mahabharata**: 70.0% of answers are B
- **Kannada Fill Blanks**: 65.5% of answers are B
- **English Vocabulary**: 65.0% of answers are C
- **Science Environment**: 65.0% of answers are B

### 🔧 Tools Available

#### 1. Analysis Tool
Run the analysis script to see detailed statistics:
```bash
python3 analyze_quiz.py
```

This tool provides:
- Detailed answer distribution statistics
- Topic-wise bias analysis
- Quality checks (duplicates, short questions)
- Overall health assessment

#### 2. Rebalancing Tool
Automatically fix the answer distribution by shuffling options:
```bash
# Dry run (preview changes without modifying files)
python3 rebalance_quiz.py

# Apply changes (creates quiz-format-balanced.csv)
python3 rebalance_quiz.py --apply
```

This tool:
- Changes 123 questions to achieve balanced distribution
- Creates a new file (doesn't modify original)
- Maintains question quality while fixing statistical bias
- Achieves target: ~25% per option (A, B, C, D)

### 📚 Documentation

- [QUIZ_ANALYSIS.md](QUIZ_ANALYSIS.md) - Comprehensive analysis report
- [QUIZ_IMPROVEMENT_SUGGESTIONS.md](QUIZ_IMPROVEMENT_SUGGESTIONS.md) - Detailed improvement strategies

### 💡 Recommendations

1. **Review and Rebalance**: Questions should be reviewed to distribute correct answers more evenly across all options
2. **Target Distribution**: Aim for ~25% (75 questions) per option for a balanced quiz
3. **Quality Assurance**: Implement automated checks to prevent such biases in future quiz creation

### ✅ Positive Aspects

- All questions have complete data (no missing fields)
- All correct answers are valid (A, B, C, or D)
- Good variety of topics covered
- Multiple languages supported
- Consistent CSV format throughout
- No duplicate questions detected

---

## GitHub Operations Guide

This section provides comprehensive guides for common GitHub operations, including combining README files and extracting changes between releases.

### 1. Combining README Files from Multiple Repositories

This guide demonstrates how to retrieve and combine README.md files from multiple GitHub repositories into a single consolidated document.

#### 1.1 Prerequisites

- Python 3.6 or higher
- `requests` library: `pip install requests`
- GitHub Personal Access Token (for private repositories or higher rate limits)

#### 1.2 Methods to Retrieve README Files

##### Method A: Using GitHub API (Recommended)

Create a Python script to fetch README files:

```python
#!/usr/bin/env python3
"""
combine_readmes.py - Combine README files from multiple GitHub repositories
"""

import requests
import base64
import sys
from datetime import datetime

def get_readme(owner, repo, token=None):
    """
    Fetch README.md content from a GitHub repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        token: GitHub Personal Access Token (optional)
    
    Returns:
        Dictionary with repo info and README content, or None if not found
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Decode base64 content
            content = base64.b64decode(data['content']).decode('utf-8')
            
            return {
                'owner': owner,
                'repo': repo,
                'url': f"https://github.com/{owner}/{repo}",
                'content': content,
                'path': data['path']
            }
        elif response.status_code == 404:
            print(f"Warning: No README found for {owner}/{repo}")
            return None
        else:
            print(f"Error fetching {owner}/{repo}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception fetching {owner}/{repo}: {e}")
        return None

def combine_readmes(repositories, output_file='COMBINED_README.md', token=None):
    """
    Combine README files from multiple repositories.
    
    Args:
        repositories: List of tuples (owner, repo)
        output_file: Output filename
        token: GitHub Personal Access Token (optional)
    """
    readmes = []
    
    print(f"Fetching README files from {len(repositories)} repositories...")
    
    for owner, repo in repositories:
        print(f"  - Fetching {owner}/{repo}...", end=" ")
        readme = get_readme(owner, repo, token)
        if readme:
            readmes.append(readme)
            print("✓")
        else:
            print("✗")
    
    print(f"\nSuccessfully fetched {len(readmes)} README files.")
    
    # Generate combined README
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("# Combined README Documentation\n\n")
        f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("This document combines README files from multiple repositories.\n\n")
        
        # Write table of contents
        f.write("## Table of Contents\n\n")
        for i, readme in enumerate(readmes, 1):
            repo_name = f"{readme['owner']}/{readme['repo']}"
            anchor = repo_name.lower().replace('/', '-')
            f.write(f"{i}. [{repo_name}](#{anchor})\n")
        f.write("\n---\n\n")
        
        # Write each README
        for readme in readmes:
            repo_name = f"{readme['owner']}/{readme['repo']}"
            
            # Section header with attribution
            f.write(f"## {repo_name}\n\n")
            f.write(f"**Repository:** [{readme['url']}]({readme['url']})\n\n")
            f.write(f"**Source:** `{readme['path']}`\n\n")
            
            # Write content (remove the first # heading if it exists to avoid duplication)
            content = readme['content']
            lines = content.split('\n')
            
            # Skip the first heading if it's an H1
            if lines and lines[0].startswith('# '):
                content = '\n'.join(lines[1:]).lstrip()
            
            f.write(content)
            f.write("\n\n---\n\n")
    
    print(f"✓ Combined README written to: {output_file}")

if __name__ == "__main__":
    # Example: Combine README files from multiple repositories
    
    # Define repositories to combine (owner, repo)
    REPOSITORIES = [
        ('octocat', 'Hello-World'),
        ('torvalds', 'linux'),
        ('microsoft', 'vscode'),
    ]
    
    # Optional: Set your GitHub token for higher rate limits
    # You can also pass it as an environment variable
    import os
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', None)
    
    # Combine READMEs
    combine_readmes(REPOSITORIES, token=GITHUB_TOKEN)
```

##### Method B: Using Git and Shell Commands

```bash
#!/bin/bash
# combine_readmes.sh - Combine README files using git clone

OUTPUT_FILE="COMBINED_README.md"
TEMP_DIR="/tmp/readme_combine"

# Create temporary directory
mkdir -p "$TEMP_DIR"

# Array of repositories (format: owner/repo)
REPOS=(
    "octocat/Hello-World"
    "microsoft/vscode"
    "torvalds/linux"
)

# Initialize output file
cat > "$OUTPUT_FILE" << EOF
# Combined README Documentation

*Generated on: $(date '+%Y-%m-%d %H:%M:%S')*

This document combines README files from multiple repositories.

## Table of Contents

EOF

# Fetch and combine READMEs
for REPO in "${REPOS[@]}"; do
    OWNER=$(echo "$REPO" | cut -d'/' -f1)
    REPO_NAME=$(echo "$REPO" | cut -d'/' -f2)
    
    echo "Fetching $REPO..."
    
    # Clone repository (shallow clone for speed)
    if git clone --depth 1 "https://github.com/$REPO.git" "$TEMP_DIR/$REPO_NAME" 2>&1 | grep -v '^Cloning'; then
        :
    else
        echo "  Warning: Failed to clone $REPO" >&2
    fi
    
    if [ -f "$TEMP_DIR/$REPO_NAME/README.md" ]; then
        echo "## $REPO" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "**Repository:** https://github.com/$REPO" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$TEMP_DIR/$REPO_NAME/README.md" >> "$OUTPUT_FILE"
        echo -e "\n\n---\n" >> "$OUTPUT_FILE"
    fi
done

# Cleanup
rm -rf "$TEMP_DIR"

echo "✓ Combined README written to: $OUTPUT_FILE"
```

#### 1.3 Usage Instructions

##### Using the Python Script:

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Set up GitHub token (optional but recommended):**
   ```bash
   export GITHUB_TOKEN="your_personal_access_token_here"
   ```

3. **Edit the script to specify your repositories:**
   ```python
   REPOSITORIES = [
       ('owner1', 'repo1'),
       ('owner2', 'repo2'),
       ('owner3', 'repo3'),
   ]
   ```

4. **Run the script:**
   ```bash
   python3 combine_readmes.py
   ```

5. **Output:** A file named `COMBINED_README.md` will be created with all README contents.

##### Using the Shell Script:

1. **Edit the script to specify your repositories:**
   ```bash
   REPOS=(
       "owner1/repo1"
       "owner2/repo2"
   )
   ```

2. **Make the script executable:**
   ```bash
   chmod +x combine_readmes.sh
   ```

3. **Run the script:**
   ```bash
   ./combine_readmes.sh
   ```

#### 1.4 Structure of Combined README

The combined README will have the following structure:

```markdown
# Combined README Documentation

*Generated on: YYYY-MM-DD HH:MM:SS*

## Table of Contents

1. [owner1/repo1](#owner1-repo1)
2. [owner2/repo2](#owner2-repo2)
...

---

## owner1/repo1

**Repository:** https://github.com/owner1/repo1

**Source:** `README.md`

[Content of repo1's README]

---

## owner2/repo2

**Repository:** https://github.com/owner2/repo2

**Source:** `README.md`

[Content of repo2's README]

---
```

#### 1.5 Best Practices

- **Attribution:** Always include repository URLs and source file paths
- **Table of Contents:** Generate a TOC for easy navigation
- **Timestamp:** Include generation timestamp for reference
- **Formatting:** Maintain consistent formatting and section separators
- **License Compliance:** Ensure you have rights to combine and redistribute content
- **Error Handling:** Handle missing READMEs gracefully
- **Rate Limits:** Use authentication to avoid GitHub API rate limits (60 requests/hour unauthenticated, 5000/hour authenticated)

---

### 2. Using GitHub API to Extract Changes Between Releases

This guide demonstrates how to extract and document changes between two releases using the GitHub API.

#### 2.1 Prerequisites

- Python 3.6 or higher
- `requests` library: `pip install requests`
- GitHub Personal Access Token (recommended for higher rate limits)

#### 2.2 Complete Python Script

Create a file named `github_release_changelog.py`:

```python
#!/usr/bin/env python3
"""
github_release_changelog.py - Extract changes between GitHub releases

This script fetches commits and pull requests between two releases
and generates a formatted changelog.
"""

import requests
import sys
import os
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlparse

class GitHubReleaseChangelog:
    """Extract and format changes between GitHub releases."""
    
    def __init__(self, owner: str, repo: str, token: Optional[str] = None):
        """
        Initialize the changelog generator.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            token: GitHub Personal Access Token (optional but recommended)
        """
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to the GitHub API."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: API returned status {response.status_code}")
                print(f"Message: {response.json().get('message', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"Exception making request: {e}")
            return None
    
    def get_release_by_tag(self, tag: str) -> Optional[Dict]:
        """
        Get release information by tag name.
        
        Args:
            tag: Tag name (e.g., 'v1.0.0')
        
        Returns:
            Release data or None if not found
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/releases/tags/{tag}"
        return self._make_request(endpoint)
    
    def get_commit_sha_for_tag(self, tag: str) -> Optional[str]:
        """
        Get commit SHA for a tag.
        
        Args:
            tag: Tag name
        
        Returns:
            Commit SHA or None if not found
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/git/refs/tags/{tag}"
        data = self._make_request(endpoint)
        
        if data:
            # Handle annotated tags vs lightweight tags
            if data['object']['type'] == 'tag':
                # Annotated tag - need to fetch the tag object
                tag_url = data['object']['url']
                parsed_url = urlparse(tag_url)
                endpoint = parsed_url.path
                tag_data = self._make_request(endpoint)
                return tag_data['object']['sha'] if tag_data else None
            else:
                # Lightweight tag - directly points to commit
                return data['object']['sha']
        return None
    
    def compare_commits(self, base: str, head: str) -> Optional[Dict]:
        """
        Compare two commits/tags.
        
        Args:
            base: Base tag or commit SHA
            head: Head tag or commit SHA
        
        Returns:
            Comparison data including commits
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/compare/{base}...{head}"
        return self._make_request(endpoint)
    
    def get_pull_requests_for_commits(self, commits: List[Dict]) -> List[Dict]:
        """
        Get pull request information for commits.
        
        Args:
            commits: List of commit objects
        
        Returns:
            List of pull requests with details
        """
        prs = []
        seen_pr_numbers = set()
        
        for commit in commits:
            commit_sha = commit['sha']
            
            # Search for PRs that include this commit
            endpoint = f"/repos/{self.owner}/{self.repo}/commits/{commit_sha}/pulls"
            pr_data = self._make_request(endpoint)
            
            if pr_data:
                for pr in pr_data:
                    if pr['number'] not in seen_pr_numbers:
                        prs.append({
                            'number': pr['number'],
                            'title': pr['title'],
                            'url': pr['html_url'],
                            'author': pr['user']['login'],
                            'merged_at': pr.get('merged_at'),
                            'labels': [label['name'] for label in pr.get('labels', [])]
                        })
                        seen_pr_numbers.add(pr['number'])
        
        return prs
    
    def generate_changelog(self, from_tag: str, to_tag: str, 
                          include_prs: bool = True,
                          output_file: Optional[str] = None) -> str:
        """
        Generate a changelog between two releases.
        
        Args:
            from_tag: Starting tag (older release)
            to_tag: Ending tag (newer release)
            include_prs: Whether to include pull request information
            output_file: Optional file to write changelog to
        
        Returns:
            Formatted changelog string
        """
        print(f"Generating changelog: {from_tag} → {to_tag}")
        print(f"Repository: {self.owner}/{self.repo}\n")
        
        # Get release information
        print("Fetching release information...")
        from_release = self.get_release_by_tag(from_tag)
        to_release = self.get_release_by_tag(to_tag)
        
        # Compare commits
        print("Comparing commits...")
        comparison = self.compare_commits(from_tag, to_tag)
        
        if not comparison:
            print("Error: Could not compare tags")
            return ""
        
        commits = comparison.get('commits', [])
        print(f"Found {len(commits)} commits")
        
        # Get pull requests if requested
        prs = []
        if include_prs:
            print("Fetching pull request information...")
            prs = self.get_pull_requests_for_commits(commits)
            print(f"Found {len(prs)} pull requests")
        
        # Generate changelog content
        changelog = self._format_changelog(from_tag, to_tag, commits, prs,
                                          from_release, to_release)
        
        # Write to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(changelog)
            print(f"\n✓ Changelog written to: {output_file}")
        
        return changelog
    
    def _format_changelog(self, from_tag: str, to_tag: str,
                         commits: List[Dict], prs: List[Dict],
                         from_release: Optional[Dict],
                         to_release: Optional[Dict]) -> str:
        """Format the changelog content."""
        
        lines = []
        
        # Header
        lines.append(f"# Changelog: {from_tag} → {to_tag}\n")
        lines.append(f"**Repository:** {self.owner}/{self.repo}\n")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Release information
        if to_release:
            lines.append(f"**Release Date:** {to_release.get('published_at', 'N/A')}\n")
            if to_release.get('name'):
                lines.append(f"**Release Name:** {to_release['name']}\n")
        
        lines.append(f"**Commits:** {len(commits)}\n")
        lines.append(f"**Pull Requests:** {len(prs)}\n")
        lines.append("\n---\n")
        
        # Pull Requests section
        if prs:
            lines.append("\n## Pull Requests\n")
            
            # Group PRs by label if available
            labeled_prs = {}
            unlabeled_prs = []
            
            for pr in prs:
                if pr['labels']:
                    for label in pr['labels']:
                        if label not in labeled_prs:
                            labeled_prs[label] = []
                        labeled_prs[label].append(pr)
                else:
                    unlabeled_prs.append(pr)
            
            # Write labeled PRs
            for label in sorted(labeled_prs.keys()):
                formatted_label = label.replace('-', ' ').replace('_', ' ').title()
                lines.append(f"\n### {formatted_label}\n")
                for pr in labeled_prs[label]:
                    lines.append(f"- #{pr['number']}: {pr['title']} (@{pr['author']}) - {pr['url']}\n")
            
            # Write unlabeled PRs
            if unlabeled_prs:
                lines.append("\n### Other Changes\n")
                for pr in unlabeled_prs:
                    lines.append(f"- #{pr['number']}: {pr['title']} (@{pr['author']}) - {pr['url']}\n")
        
        # Commits section
        lines.append("\n## Commits\n")
        
        for commit in commits:
            sha_short = commit['sha'][:7]
            message = commit['commit']['message'].split('\n')[0]  # First line only
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']
            
            lines.append(f"- `{sha_short}` {message} - {author} ({date})\n")
        
        # Release notes section
        if to_release and to_release.get('body'):
            lines.append("\n## Release Notes\n")
            lines.append(f"{to_release['body']}\n")
        
        return ''.join(lines)

def main():
    """Main entry point."""
    
    # Example usage
    if len(sys.argv) < 5:
        print("Usage: python3 github_release_changelog.py <owner> <repo> <from_tag> <to_tag>")
        print("\nExample:")
        print("  python3 github_release_changelog.py microsoft vscode v1.75.0 v1.76.0")
        print("\nEnvironment variables:")
        print("  GITHUB_TOKEN - GitHub Personal Access Token (optional)")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    from_tag = sys.argv[3]
    to_tag = sys.argv[4]
    
    # Get GitHub token from environment
    token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print("Warning: No GITHUB_TOKEN found. API rate limits will be lower (60 requests/hour).")
        print("Set GITHUB_TOKEN environment variable for higher limits (5000 requests/hour).\n")
    
    # Create changelog generator
    changelog_gen = GitHubReleaseChangelog(owner, repo, token)
    
    # Generate changelog
    output_file = f"CHANGELOG_{from_tag}_to_{to_tag}.md"
    changelog = changelog_gen.generate_changelog(from_tag, to_tag, 
                                                 include_prs=True,
                                                 output_file=output_file)
    
    # Print to console as well
    print("\n" + "="*80)
    print(changelog)

if __name__ == "__main__":
    main()
```

#### 2.3 Usage Instructions

##### Setting up Authentication:

1. **Create a GitHub Personal Access Token:**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Click "Generate new token"
   - Select scopes: `repo` (for private repos) or `public_repo` (for public repos only)
   - Copy the generated token

2. **Set the token as an environment variable:**
   ```bash
   export GITHUB_TOKEN="your_personal_access_token_here"
   ```

##### Running the Script:

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Make the script executable:**
   ```bash
   chmod +x github_release_changelog.py
   ```

3. **Run the script:**
   ```bash
   python3 github_release_changelog.py <owner> <repo> <from_tag> <to_tag>
   ```

   **Example:**
   ```bash
   python3 github_release_changelog.py microsoft vscode v1.75.0 v1.76.0
   ```

4. **Output:**
   - Changelog printed to console
   - Saved to file: `CHANGELOG_<from_tag>_to_<to_tag>.md`

#### 2.4 CLI Commands Alternative

You can also use GitHub CLI (`gh`) for simpler operations:

##### Install GitHub CLI:

```bash
# macOS
brew install gh

# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
```

##### Extract commits between tags:

```bash
# Compare two tags
gh api repos/{owner}/{repo}/compare/{base}...{head}

# Example
gh api repos/microsoft/vscode/compare/v1.75.0...v1.76.0 | jq '.commits[] | {sha: .sha, message: .commit.message}'
```

##### List pull requests merged between dates:

```bash
# List merged PRs in a date range
gh pr list --repo {owner}/{repo} --state merged --search "merged:2023-01-01..2023-12-31"

# Example
gh pr list --repo microsoft/vscode --state merged --search "merged:2023-01-01..2023-01-31" --json number,title,url
```

##### Generate release notes:

```bash
# Generate release notes between tags
gh api repos/{owner}/{repo}/releases/generate-notes \
  -f tag_name=v2.0.0 \
  -f target_commitish=main \
  -f previous_tag_name=v1.0.0

# Example
gh api repos/microsoft/vscode/releases/generate-notes \
  -f tag_name=v1.76.0 \
  -f previous_tag_name=v1.75.0
```

#### 2.5 Example Output

The script generates a changelog in the following format:

```markdown
# Changelog: v1.0.0 → v2.0.0

**Repository:** owner/repo
**Generated:** 2024-01-15 10:30:00
**Release Date:** 2024-01-15T09:00:00Z
**Release Name:** Version 2.0.0
**Commits:** 127
**Pull Requests:** 45

---

## Pull Requests

### Bug Fixes

- #123: Fix memory leak in cache handler (@developer1) - https://github.com/owner/repo/pull/123
- #145: Resolve race condition in async operations (@developer2) - https://github.com/owner/repo/pull/145

### Features

- #134: Add support for new API endpoints (@developer3) - https://github.com/owner/repo/pull/134
- #156: Implement dark mode support (@developer4) - https://github.com/owner/repo/pull/156

### Other Changes

- #167: Update dependencies (@dependabot) - https://github.com/owner/repo/pull/167

## Commits

- `abc1234` Fix memory leak in cache handler - Developer One (2024-01-10T14:23:00Z)
- `def5678` Add support for new API endpoints - Developer Two (2024-01-11T09:15:00Z)
- `ghi9012` Update documentation - Developer Three (2024-01-12T16:45:00Z)
...

## Release Notes

This release includes major improvements to performance and new features...
```

#### 2.6 Best Practices

- **Authentication:** Always use a GitHub token to avoid rate limits
- **Error Handling:** Handle cases where releases or tags don't exist
- **Categorization:** Group changes by type (features, bug fixes, etc.)
- **Attribution:** Include contributor information
- **Links:** Provide links to commits and pull requests
- **Formatting:** Use consistent markdown formatting
- **Automation:** Consider integrating into CI/CD pipelines
- **Rate Limits:** Be mindful of API rate limits (5000 requests/hour with authentication)

#### 2.7 Troubleshooting

**Issue:** API rate limit exceeded
- **Solution:** Use authentication token and implement rate limiting in your script

**Issue:** Tag not found
- **Solution:** Verify tag names with `gh api repos/{owner}/{repo}/tags` or check repository releases

**Issue:** Large number of commits
- **Solution:** Paginate results or filter commits by date range

**Issue:** Missing pull request information
- **Solution:** Ensure the repository uses pull requests (not direct commits) and PR numbers are in commit messages

---

## Additional Resources

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub API Rate Limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [Creating Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

