#!/bin/bash

# Function to remove Python bytecode files, temporary files, and cache directories
cleanup_files() {
    echo "Cleaning up unnecessary files..."

    # Remove __pycache__ directories
    find . -type d -name '__pycache__' -exec rm -r {} +

    # Remove .DS_Store files
    find . -type f -name '.DS_Store' -exec rm -f {} +

    # Remove compiled Python files
    find . -type f -name '*.pyc' -delete
    find . -type f -name '*.pyo' -delete

    # Remove swap files and backup files
    find . -type f -name '*.swp' -delete
    find . -type f -name '*.swo' -delete
    find . -type f -name '*~' -delete

    # Remove editor-specific directories
    find . -type d -name '.vscode' -exec rm -r {} \;
    find . -type d -name '.idea' -exec rm -r {} \;
}

# Function to clear git cache
clear_git_cache() {
    echo "Clearing git cache..."

    # Remove files from the git index
    git rm -r --cached .

    # Commit the changes
    git commit -m "Cleanup before pushing"

    # Push the changes (force to overwrite)
    git push origin $(git rev-parse --abbrev-ref HEAD) --force
}

# Run cleanup functions
cleanup_files
clear_git_cache

echo "Cleanup complete. You are now ready to push to Git."


