import os
import glob
import datetime
import subprocess
import shutil
import json

PROJECT_ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True).stdout.strip()
CHAT_DIR = os.path.join(PROJECT_ROOT, ".chat", "unclean")
CLEANED_ORIGINAL_DIR = os.path.join(PROJECT_ROOT, ".chat", "cleaned", "original")
CLEANED_CLEAN_DIR = os.path.join(PROJECT_ROOT, ".chat", "cleaned", "clean")
PARSE_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "parse_chat_log.py")

def clean_old_chat_logs():
    all_txt_files = [f for f in glob.glob(os.path.join(CHAT_DIR, "*.txt")) if not f.endswith("_clean.txt")]
    uncleaned_logs = []
    failed_files = []

    # Load noise patterns from config
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '.memory', 'parsing_config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    noise_patterns = config.get("noise_patterns", [])
    noise_patterns_json = json.dumps(noise_patterns)

    # Get active chat logs from environment variable
    active_chat_logs_json = os.environ.get("ACTIVE_CHAT_LOGS", "[]")
    active_chat_logs = json.loads(active_chat_logs_json)

    # Get already cleaned files
    cleaned_files_basenames = set()
    for cleaned_file_path in glob.glob(os.path.join(CLEANED_CLEAN_DIR, "*.txt")):
        cleaned_files_basenames.add(os.path.basename(cleaned_file_path).replace('_clean.txt', '.txt'))

    for file_path in all_txt_files:
        base_name = os.path.basename(file_path)
        if base_name in cleaned_files_basenames:
            continue

        if file_path in active_chat_logs:
            continue

        uncleaned_logs.append(file_path)

    print(f"Found {len(uncleaned_logs)} uncleaned logs to process.")

    os.makedirs(CLEANED_ORIGINAL_DIR, exist_ok=True)
    os.makedirs(CLEANED_CLEAN_DIR, exist_ok=True)

    for i, file_path in enumerate(uncleaned_logs):
        print(f"\nProcessing file {i+1}/{len(uncleaned_logs)}: {file_path}")
        if os.path.exists(file_path):
            base_name = os.path.basename(file_path)
            
            # Move original file to 'cleaned/original' as a backup
            try:
                destination_path = os.path.join(CLEANED_ORIGINAL_DIR, base_name)
                shutil.move(file_path, destination_path)
                print(f"  - Moved original log to: {destination_path}")
            except Exception as e:
                print(f"  - Error moving original file {file_path}: {e}")
                failed_files.append(file_path)
                continue

            # Run cleaning script
            try:
                print(f"  - Running cleaning script...")
                result = subprocess.run(["python3", PARSE_SCRIPT, destination_path, noise_patterns_json], capture_output=True, text=True, check=True)
                print(f"  - Cleaning script finished.")
                
                cleaned_file_name = base_name.replace('.txt', '_clean.txt')
                
                # The parse script now prints the cleaned content to stdout
                if result.stdout:
                    cleaned_file_path = os.path.join(CLEANED_CLEAN_DIR, cleaned_file_name)
                    with open(cleaned_file_path, "w") as f:
                        f.write(result.stdout)
                    print(f"  - Wrote cleaned log to: {cleaned_file_path}")
                else:
                    print(f"  - Cleaned file not found for {file_path} (no stdout from parser).")
                    failed_files.append(destination_path)

                if result.stderr:
                    print(f"  - Stderr for {file_path}:")
                    print(result.stderr)

            except subprocess.CalledProcessError as e:
                print(f"  - Failed to clean {destination_path}: {e}")
                print(f"  - Stdout: {e.stdout}")
                print(f"  - Stderr: {e.stderr}")
                failed_files.append(destination_path)
            except FileNotFoundError:
                print(f"  - Error: {PARSE_SCRIPT} not found. Summarization failed for {destination_path}.")
                failed_files.append(destination_path)
        else:
            print(f"Skipping non-existent file: {file_path}")

    if failed_files:
        print("\n--- Failed to process the following files ---")
        for f in failed_files:
            print(f)
    else:
        print("\nAll eligible logs processed successfully.")

if __name__ == "__main__":
    clean_old_chat_logs()