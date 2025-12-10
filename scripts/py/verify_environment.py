import os
import sys
import subprocess
import json

def verify_environment():
    print("--- Verifying Environment and Pre-commit ---")

    # 1. Check for active virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✔ Virtual environment is active.")
        venv_active = True
    else:
        print("❌ No virtual environment detected. Please activate your virtual environment (e.g., 'source .venv/bin/activate').")
        venv_active = False

    # 2. Check if pre-commit is installed in the active environment
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", "pre-commit"], capture_output=True, check=True)
        print("✔ 'pre-commit' is installed in the active environment.")
        pre_commit_installed = True
    except subprocess.CalledProcessError:
        print("❌ 'pre-commit' is not installed in the active environment. Please install it (e.g., 'pip install pre-commit').")
        pre_commit_installed = False

    # 3. Check if pre-commit hooks are installed
    pre_commit_config_path = ".pre-commit-config.yaml"
    if os.path.exists(pre_commit_config_path):
        try:
            # Run pre-commit install --check to see if hooks are installed and up-to-date
            # This command returns 0 if hooks are installed and up-to-date, 1 if not.
            result = subprocess.run([sys.executable, "-m", "pre_commit", "install", "--check"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✔ Pre-commit hooks are installed and up-to-date.")
                hooks_installed = True
            else:
                print(f"❌ Pre-commit hooks are not installed or are not up-to-date. Please install them by running: '{sys.executable} -m pre_commit install'.")
                hooks_installed = False
        except FileNotFoundError:
            print("❌ 'pre-commit' executable not found. Make sure it's installed and in your PATH within the virtual environment.")
            hooks_installed = False
    else:
        print(f"❌ No .pre-commit-config.yaml found in the project root. Please ensure this file exists.")
        hooks_installed = False

    print("--- Environment Verification Complete ---")

    return venv_active and pre_commit_installed and hooks_installed

if __name__ == '__main__':
    if not verify_environment():
        sys.exit(1)
