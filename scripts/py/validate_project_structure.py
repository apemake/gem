import os
import json
import pathspec
import subprocess

def build_actual_structure(project_path, spec):
    actual_structure = {}
    for root, dirs, files in os.walk(project_path, topdown=True):
        # filter out ignored directories
        dirs[:] = [d for d in dirs if not spec.match_file(os.path.relpath(os.path.join(root, d), project_path))]
        
        # add files to structure
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_path)
            if not spec.match_file(relative_path):
                parts = relative_path.split(os.sep)
                node = actual_structure
                for i, part in enumerate(parts):
                    if i == len(parts) - 1:
                        node[part] = 'file'
                    else:
                        if part + '/' not in node:
                            node[part + '/'] = {}
                        node = node[part + '/']
    return actual_structure

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
    gitignore_path = os.path.join(project_path, '.gitignore')

    with open(structure_file_path, 'r') as f:
        expected = json.load(f).get("project_structure", {})

    gitignore_patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_patterns = f.read().splitlines()
    
    spec = pathspec.PathSpec.from_lines('gitwildmatch', gitignore_patterns)

    actual_structure = build_actual_structure(project_path, spec)
    
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