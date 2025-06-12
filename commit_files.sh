#!/bin/bash

# Ensure we are in a Git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Error: Not inside a Git repository. Please initialize a repository first."
    exit 1
fi

# Function to add and commit a file with a message
commit_file() {
    local file=$1
    local message=$2
    if [ -f "$file" ] || [ -d "$file" ]; then
        git add "$file"
        git commit -m "$message" || echo "No changes to commit for $file"
    else
        echo "File or directory $file not found, skipping."
    fi
}

# Commit modified files
commit_file "diplomat_safes/settings.py" "Updated settings.py to suppress CKEditor warning and configure media/static paths for core app"
commit_file "diplomat_safes/urls.py" "Updated urls.py to include core app URLs and media serving configuration"
commit_file "templates/base.html" "Modified base.html to support core app template structure and styling"

# Commit untracked files (excluding .env and db.sqlite3 unless intentional)
commit_file "commit_files.sh" "Added commit_files.sh script to automate Git commits for core app changes"
commit_file "core/" "Added core/ directory with models.py, admin.py, views.py, and templates for TeamMember implementation"
commit_file "static/css/about_us.css" "Added about_us.css for styling the About Us page in core app"
commit_file "static/js/about_us.js" "Added about_us.js for interactive features on the About Us page in core app"
commit_file "store/migrations/0009_alter_safeproduct_category.py" "Added migration 0009 for safeproduct category update related to core integration"
commit_file "store/migrations/0010_alter_safeproduct_category.py" "Added migration 0010 for safeproduct category update related to core integration"
commit_file "templates/core/" "Added core/ templates directory with about_us.html for team member display"

# Exclude .env and db.sqlite3 by default (uncomment if you want to include them)
# commit_file ".env" "Added .env file with environment variables for core app configuration"
# commit_file "db.sqlite3" "Added db.sqlite3 with initial data for core and store apps"

echo "Git status:"
git status
echo "Commits created. Verify: 'git log --oneline'"
echo "Push with: 'git push origin core'"
