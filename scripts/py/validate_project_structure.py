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

def validate_structure(expected_structure, actual_structure):
    inconsistencies = []

    # Check for missing files/directories
    for item, value in expected_structure.items():
        if item not in actual_structure:
            inconsistencies.append(f"Missing: {item}")
        elif isinstance(value, dict):
            inconsistencies.extend(validate_structure(value, actual_structure.get(item, {})))

    # Check for extra files/directories
    for item in actual_structure.keys():
        if item not in expected_structure:
            inconsistencies.append(f"Extra: {item}")

    return inconsistencies

if __name__ == '__main__':
    try:
        project_path = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting project root: {e}")
        exit(1)

    structure_file_path = os.path.join(project_path, '.memory', 'project_structure.json')

    with open(structure_file_path, 'r') as f:
        expected = json.load(f).get("project_structure", {})

    git_files = get_git_files()
    actual_structure = build_tree(git_files)
    
    # Exclude the project_structure.json file from the validation
    if '.memory/' in actual_structure and 'project_structure.json' in actual_structure['.memory/']:
        del actual_structure['.memory/']['project_structure.json']

    inconsistencies = validate_structure(expected, actual_structure)

    if inconsistencies:
        print("Project validation found inconsistencies:")
        for issue in inconsistencies:
            print(f"- {issue}")
    else:
        print("Project structure is valid.")