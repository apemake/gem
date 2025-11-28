import os
import json
import subprocess

def get_git_files():
    """Get a list of all files tracked by git."""
    try:
        result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, check=True)
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
    git_files = get_git_files()
    project_structure = build_tree(git_files)
    
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    output_path = os.path.join(project_path, '.memory', 'project_structure.json')

    with open(output_path, 'w') as f:
        json.dump({"project_structure": project_structure}, f, indent=2)

    print(f"Project structure written to {output_path}")
