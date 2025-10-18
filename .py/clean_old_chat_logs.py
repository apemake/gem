# Learning Summary:
# v1: SyntaxError: unterminated f-string literal. Fix: Separated stderr print statement.

import os
import glob
import datetime
import subprocess
import shutil

CHAT_DIR = "/home/bestape/gemini/.chat/"
PARSE_SCRIPT = "/home/bestape/gemini/.py/parse_chat_log.py"

def clean_old_chat_logs():
    all_txt_files = glob.glob(os.path.join(CHAT_DIR, "*.txt"))
    uncleaned_logs = []
    failed_files = []

    for file_path in all_txt_files:
        if file_path.endswith("_clean.txt"):
            continue

        # Check if a cleaned version already exists in cleaned_logs
        base_name = os.path.basename(file_path)
        cleaned_file_name = base_name.replace('.txt', '_clean.txt')
        cleaned_file_path_in_cleaned_dir = os.path.join(CHAT_DIR, "cleaned_logs", cleaned_file_name)
        
        if os.path.exists(cleaned_file_path_in_cleaned_dir):
            # If cleaned version exists, move the original to cleaned_logs
            try:
                cleaned_dir = os.path.join(CHAT_DIR, "cleaned_logs")
                os.makedirs(cleaned_dir, exist_ok=True)
                shutil.move(file_path, cleaned_dir)
                print(f"Original log file moved to: {os.path.join(cleaned_dir, os.path.basename(file_path))}")
            except Exception as e:
                print(f"Error moving original file {file_path}: {e}")
            continue

        # Extract timestamp from filename (e.g., 20251017-170612_gemini_chat.txt)
        try:
            timestamp_str = base_name.split('_')[0]
            log_date = datetime.datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
        except ValueError:
            # Handle files with different naming conventions or no timestamp
            # For now, we'll treat them as old enough to be cleaned
            log_date = datetime.datetime.min # Effectively always old enough

        # Only clean logs older than one day
        if (datetime.datetime.now() - log_date).days >= 1:
            uncleaned_logs.append(file_path)

    print(f"Found {len(uncleaned_logs)} uncleaned logs older than one day.")

    for file_path in uncleaned_logs:
        if os.path.exists(file_path):
            print(f"Attempting to clean: {file_path}")
            try:
                result = subprocess.run(["python3", PARSE_SCRIPT, file_path], capture_output=True, text=True, check=True)
                print(result.stdout)
                if result.stderr:
                    print(f"Stderr for {file_path}:")
                    print(result.stderr)
            except subprocess.CalledProcessError as e:
                print(f"Failed to clean {file_path}: {e}")
                print(f"Stdout: {e.stdout}")
                print(f"Stderr: {e.stderr}")
                failed_files.append(file_path)
            except FileNotFoundError:
                print(f"Skipping non-existent file (already handled): {file_path}")
        else:
            print(f"Skipping non-existent file: {file_path}")

    if failed_files:
        print("\n--- Failed to clean the following files ---")
        for f in failed_files:
            print(f)
    else:
        print("\nAll eligible logs cleaned successfully.")

if __name__ == "__main__":
    clean_old_chat_logs()
