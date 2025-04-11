# Git Guide for NLP Data Pipeline

This guide provides detailed instructions for using Git with the NLP Data Pipeline project.

## Table of Contents
- [Initial Setup](#initial-setup)
- [Basic Git Operations](#basic-git-operations)
- [Branching Strategy](#branching-strategy)
- [Best Practices](#best-practices)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)

## Initial Setup

### First-Time Git Configuration
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

### Project Setup
```bash
# Clone the repository
git clone https://github.com/your-username/nlp-data-pipeline.git
cd nlp-data-pipeline

# Create and switch to a new feature branch
git checkout -b feature/your-feature-name
```

## Basic Git Operations

### Daily Git Commands
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

### Viewing Changes
```bash
# View changes in staged files
git diff --staged

# View changes in unstaged files
git diff

# View commit history
git log
git log --oneline --graph --decorate  # Compact view
```

## Branching Strategy

### Main Branches
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `hotfix/*` - Emergency fixes
- `release/*` - Release preparation

### Branch Operations
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

## Best Practices

### Commit Messages
- Use clear, descriptive commit messages
- Format: `<type>: <description>`
- Types: feat, fix, docs, style, refactor, test, chore

Example:
```bash
git commit -m "feat: add news API integration"
git commit -m "fix: resolve data parsing issue"
git commit -m "docs: update installation guide"
```

### Git Ignore
The project's `.gitignore` file handles:
- Python artifacts (`__pycache__`, `.pyc`)
- Virtual environments
- Environment variables
- IDE files
- System files
- Data files

### Code Review Process
1. Create feature branch
2. Make changes and commit
3. Push to remote
4. Create Pull Request
5. Address review comments
6. Merge after approval

## Common Workflows

### Feature Development
```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# Work on feature
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature

# Create Pull Request through GitHub
```

### Hotfix Process
```bash
# Create hotfix branch
git checkout main
git checkout -b hotfix/issue-fix

# Fix issue
git add .
git commit -m "fix: critical issue"
git push origin hotfix/issue-fix

# Merge to main and develop after review
```

## Troubleshooting

### Common Issues and Solutions

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

### Git Help
```bash
# Get help for any command
git help <command>
git <command> --help
```

## Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

## Project-Specific Guidelines

1. **Branch Naming Convention**
   - Features: `feature/descriptive-name`
   - Fixes: `fix/issue-description`
   - Docs: `docs/document-name`

2. **Code Review Checklist**
   - Code follows project style guide
   - Tests are included
   - Documentation is updated
   - No sensitive data in commits
   - Commit messages are clear

3. **Release Process**
   - Version bumping
   - Changelog updates
   - Tag creation
   - Deployment steps 