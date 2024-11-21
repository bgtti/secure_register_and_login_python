"""
**ABOUT THIS FILE**

Run this script to generate a tree.text file that excludes cache and other automatically generated directories.

*Ps: this script has been tested in a windows terminal. Might need adjustments if you plan to run it from other operating systems.*

##Usage:
You can run this file from the root directory with:
```bash
python utils/tree_file_generator.py
```

The `tree.txt` file in the root directory will be updated to show the current structure of this project.
"""
import os

# Specify the directory to start from (e.g., current directory)
start_dir = "."
output_file = "tree.txt"

# Directories and file extensions to exclude
excluded_dirs = {"__pycache__", ".pytest_cache", ".env", "env", "instance"}
excluded_extensions = {".pyc"}

def generate_tree(dir_path, prefix=""):
    tree_lines = []
    
    # Filter out files and directories based on exclusions
    entries = [e for e in os.listdir(dir_path) if e not in excluded_dirs]
    entries = sorted(entries, key=lambda s: s.lower())  # Sort for consistency
    entries_count = len(entries)

    for i, entry in enumerate(entries):
        path = os.path.join(dir_path, entry)
        connector = "├── " if i < entries_count - 1 else "└── "
        
        # Exclude files with unwanted extensions
        if os.path.isfile(path) and any(entry.endswith(ext) for ext in excluded_extensions):
            continue
        
        # Add directory or file to the tree
        if os.path.basename(path) == "system_logs":
            tree_lines.append(f"{prefix}{connector}system_logs")
            tree_lines.append(f"{prefix}    └── ...")  # Indicate that files are hidden
            continue

        tree_lines.append(f"{prefix}{connector}{entry}")
        
        # If it's a directory, recursively add its contents
        if os.path.isdir(path) and os.path.basename(path) != "system_logs":
            new_prefix = prefix + ("│   " if i < entries_count - 1 else "    ")
            tree_lines.extend(generate_tree(path, new_prefix))

    return tree_lines

# Generate the directory tree and write to output file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"{start_dir}\n")
    f.write("\n".join(generate_tree(start_dir)))

print(f"Tree structure saved to {output_file}")
