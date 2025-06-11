#!/bin/bash

# Ensure we are in a Git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Error: Not inside a Git repository. Please initialize a repository first."
    exit 1
fi

# List of files to commit with their paths and descriptive messages
declare -A files=(
    [".gitignore"]="Added .gitignore to exclude virtual environment and irrelevant files"
    ["static/css/cart.css"]="Updated cart.css with fixed comment and styling"
    ["static/js/base.js"]="Fixed base.js to resolve cart synchronization issues"
    ["static/js/cart.js"]="Updated cart.js for quantity updates and item removal"
    ["store/urls.py"]="Reordered URLs to fix product detail routing"
    ["store/views.py"]="Enhanced cart_view and update_cart for session handling"
    ["templates/store/cart.html"]="Added cart.html with Ksh currency and CSRF token"
    ["store/migrations/0008_order_cartitem_orderitem_wishlistitem.py"]="Added migration for Order, CartItem, OrderItem, WishlistItem models"
    ["store/templatetags/"]="Added custom template tags directory"
)

# List of deleted files to commit
declare -A deleted_files=(
    ["commit_each.sh"]="Removed obsolete commit_each.sh script"
    ["templates/store/cart.htm"]="Removed cart.htm, replaced with cart.html"
)

# Stage and commit .gitignore first
if [ -f ".gitignore" ]; then
    git add .gitignore
    git commit -m "${files[.gitignore]}" || echo "No changes to commit for .gitignore"
else
    echo "Creating .gitignore..."
    cat <<EOL > .gitignore
# Virtual environment
d-safe/

# Python cache and bytecode
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Django-specific
*.log
debug.log
staticfiles/
media/

# Python package metadata
*.egg-info/
dist/
build/

# IDE and editor files
.idea/
.vscode/
*.swp
*.swo

# macOS
.DS_Store

# Other
*.bak
*.backup
EOL
    git add .gitignore
    git commit -m "${files[.gitignore]}"
fi

# Remove debug.log from Git index if tracked
if git ls-files --error-unmatch debug.log > /dev/null 2>&1; then
    git rm --cached debug.log
    git commit -m "Stopped tracking debug.log"
fi

# Stage and commit modified and untracked files
for file in "${!files[@]}"; do
    if [ "$file" != ".gitignore" ] && [ -e "$file" ]; then
        git add "$file"
        git commit -m "${files[$file]}" || echo "No changes to commit for $file"
    else
        [ "$file" != ".gitignore" ] && echo "File $file does not exist, skipping..."
    fi
done

# Stage and commit deleted files
for file in "${!deleted_files[@]}"; do
    if git ls-files --deleted | grep -Fx "$file" > /dev/null; then
        git rm "$file"
        git commit -m "${deleted_files[$file]}" || echo "No changes to commit for $file"
    else
        echo "Deleted file $file not found in Git index, skipping..."
    fi
done

# Remove untracked commit_files.sh if it exists
if [ -f "commit_files.sh" ]; then
    git add commit_files.sh
    git commit -m "Added commit_files.sh for previous commit operations"
fi

echo "All files have been processed. Check Git status for confirmation:"
git status

echo "Commits created. Verify with 'git log --oneline' and push with 'git push origin Cart'"
