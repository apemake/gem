import os
import json

def validate_structure(expected_structure, actual_path):
    inconsistencies = []
    
    # Check for missing files/directories
    for item in expected_structure.keys():
        item_path = os.path.join(actual_path, item.rstrip('/'))
        if not os.path.exists(item_path):
            inconsistencies.append(f"Missing: {item_path}")

    # Check for extra files/directories
    if os.path.exists(actual_path):
        for item in os.listdir(actual_path):
            item_path = os.path.join(actual_path, item)
            # Ignore git files
            if '.git' in item_path:
                continue

            if os.path.isdir(item_path):
                item_key = item + '/'
            else:
                item_key = item

            if item_key not in expected_structure:
                inconsistencies.append(f"Extra: {item_path}")
            elif isinstance(expected_structure[item_key], dict):
                inconsistencies.extend(validate_structure(expected_structure[item_key], item_path))

    return inconsistencies

if __name__ == '__main__':
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    structure_file_path = os.path.join(project_path, '.memory', 'project_structure.json')

    with open(structure_file_path, 'r') as f:
        expected = json.load(f)

    inconsistencies = validate_structure(expected.get("project_structure", {}), project_path)

    if inconsistencies:
        print("Project structure inconsistencies found:")
        for issue in inconsistencies:
            print(f"- {issue}")
    else:
        print("Project structure is valid.")
