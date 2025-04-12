# Git Guide for NLP Data Pipeline

## Getting Started

### 1. Initial Setup (First Time Only)

#### 1.1 Install Git
```bash
# For macOS (using Homebrew)
brew install git

# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install git

# For Windows
# Download and install from https://git-scm.com/download/windows
```

#### 1.2 Configure Git (First Time Only)
```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Configure line ending handling
git config --global core.autocrlf input  # For Mac/Linux
# git config --global core.autocrlf true # For Windows
```

### 2. Getting the Repository

#### 2.1 Clone the Repository
1. Go to the repository page on GitHub
2. Click the green "Code" button
3. Copy the HTTPS URL (e.g., `https://github.com/username/nlp-data-pipeline.git`)

```bash
# Navigate to where you want to store the project
cd ~/Documents/Projects  # or your preferred directory

# Clone the repository
git clone https://github.com/username/nlp-data-pipeline.git

# Enter the project directory
cd nlp-data-pipeline
```

#### 2.2 Set Up the Project
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Mac/Linux:
source venv/bin/activate
# For Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your actual values
```

### 3. Basic Git Operations

#### 3.1 Daily Git Commands
```bash
# Check repository status
git status

# Stage changes
git add <filename>      # Stage specific file
git add .              # Stage all changes

# Commit changes
git commit -m "Description of changes"

# Push changes
git push origin <branch-name>

# Pull latest changes
git pull origin <branch-name>
```

#### 3.2 Viewing Changes
```bash
# View changes in staged files
git diff --staged

# View changes in unstaged files
git diff

# View commit history
git log
git log --oneline --graph --decorate  # Compact view
```

### 4. Branching Strategy

#### 4.1 Main Branches
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `hotfix/*` - Emergency fixes
- `release/*` - Release preparation

#### 4.2 Branch Operations
```bash
# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout <branch-name>

# List branches
git branch  # Local branches
git branch -a  # All branches including remote

# Delete branch
git branch -d <branch-name>  # Local delete
git push origin --delete <branch-name>  # Remote delete
```

### 5. Best Practices

#### 5.1 Commit Messages
- Use clear, descriptive commit messages
- Format: `<type>: <description>`
- Types: feat, fix, docs, style, refactor, test, chore

Example:
```bash
git commit -m "feat: add news API integration"
git commit -m "fix: resolve data parsing issue"
git commit -m "docs: update installation guide"
```

#### 5.2 Protecting Sensitive Data
- Never commit `.env` files
- Never commit API keys or credentials
- Use `.gitignore` to exclude sensitive files
- If you accidentally commit sensitive data:
  ```bash
  # Remove sensitive file from git history
  git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive-file" \
  --prune-empty --tag-name-filter cat -- --all
  ```

### 6. Common Workflows

#### 6.1 Starting New Work
```bash
# Get latest changes
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/your-feature
```

#### 6.2 Updating Your Branch
```bash
# Get latest changes from main
git checkout main
git pull origin main

# Update your feature branch
git checkout feature/your-feature
git merge main
```

### 7. Troubleshooting

#### 7.1 Common Issues
1. **Merge Conflicts**
```bash
# When encountering merge conflicts
git status  # Check conflicting files
# Resolve conflicts in editor
git add <resolved-files>
git commit -m "resolve merge conflicts"
```

2. **Undo Last Commit**
```bash
# Undo commit but keep changes staged
git reset --soft HEAD^

# Undo commit and unstage changes
git reset HEAD^
```

3. **Stashing Changes**
```bash
# Stash changes temporarily
git stash save "work in progress"

# List stashes
git stash list

# Apply stashed changes
git stash pop
```

### 8. Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

### 9. Project-Specific Guidelines

#### 9.1 Branch Naming Convention
- Features: `feature/descriptive-name`
- Fixes: `fix/issue-description`
- Docs: `docs/document-name`

#### 9.2 Code Review Checklist
- Code follows project style guide
- Tests are included
- Documentation is updated
- No sensitive data in commits
- Commit messages are clear

#### 9.3 Release Process
- Version bumping
- Changelog updates
- Tag creation
- Deployment steps 