import os
import json
import subprocess
from config_utils import PROJECT_ROOT

def get_git_files(project_path): # Pass project_path as argument
    """Get a list of all files tracked by git."""
    try:
        # cd to project_path before running git command
        result = subprocess.run(['git', 'ls-files'], cwd=project_path, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error getting git files: {e}")
        return []

def build_tree(files):
    """Build a tree structure from a list of files."""
    tree = {}
    for file in files:
        parts = file.split('/')
        node = tree
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                node[part] = 'file'
            else:
                if part + '/' not in node:
                    node[part + '/'] = {}
                node = node[part + '/']
    return tree

if __name__ == '__main__':
    project_path = PROJECT_ROOT # Use PROJECT_ROOT from config_utils

    git_files = get_git_files(project_path) # Pass project_path
    project_structure = build_tree(git_files)
    
    output_path = os.path.join(project_path, '.memory', 'project_structure.json')

    with open(output_path, 'w') as f:
        json.dump({"project_structure": project_structure}, f, indent=2)

    print(f"Project structure written to {output_path}")
