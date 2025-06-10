#!/bin/bash

# File: commit_each.sh
# Usage: ./commit_each.sh

# Verify we're in a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Error: Not in a Git repository"
    exit 1
fi

# Define sensitive files/directories to ignore (regex patterns)
declare -a ignore_patterns=(
    "d-safe/.*"                # Virtual environment
    ".*\.pyc$"                 # Python compiled files
    "__pycache__"              # Python cache
    ".*/\.env$"                # Environment files
    ".*\.secret$"              # Secret files
    ".*\.key$"                 # Key files
    ".*/node_modules/.*"       # Node modules
    ".*\.log$"                 # Log files
)

# Get all changed files (modified + untracked)
files=$(git status --porcelain | awk '{print $2}')

for file in $files; do
    # Skip directories
    if [ -d "$file" ]; then
        continue
    fi
    
    # Check against ignore patterns
    skip=0
    for pattern in "${ignore_patterns[@]}"; do
        if [[ $file =~ $pattern ]]; then
            echo "Skipping sensitive file: $file"
            skip=1
            break
        fi
    done
    
    if [ $skip -eq 1 ]; then
        continue
    fi
    
    # Commit individual file
    git add "$file"
    git commit -m "Update $file" >/dev/null
    
    if [ $? -eq 0 ]; then
        echo "Committed: $file"
    else
        echo "Failed to commit: $file (may be empty/unchanged)"
        git reset --quiet HEAD^
    fi
done

echo "Commit process completed"
