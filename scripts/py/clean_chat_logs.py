import os
import glob
import datetime
import subprocess
import shutil

CHAT_DIR = "/home/bestape/gemini/.chat/"
CLEANED_ORIGINAL_DIR = "/home/bestape/gemini/.chat/cleaned/original/"
CLEANED_CLEAN_DIR = "/home/bestape/gemini/.chat/cleaned/clean/"
PARSE_SCRIPT = "/home/bestape/gemini/scripts/py/parse_chat_log.py"
TIME_THRESHOLD_HOURS = 5

def clean_old_chat_logs():
    now = datetime.datetime.now()
    time_threshold = now - datetime.timedelta(hours=TIME_THRESHOLD_HOURS)

    all_txt_files = glob.glob(os.path.join(CHAT_DIR, "*.txt"))
    uncleaned_logs = []
    failed_files = []

    for file_path in all_txt_files:
        if file_path.endswith("_clean.txt"):
            continue

        # Check modification time
        file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        if file_mod_time > time_threshold:
            print(f"Skipping recently modified file: {file_path}")
            continue

        uncleaned_logs.append(file_path)

    print(f"Found {len(uncleaned_logs)} uncleaned logs to process.")

    os.makedirs(CLEANED_ORIGINAL_DIR, exist_ok=True)
    os.makedirs(CLEANED_CLEAN_DIR, exist_ok=True)

    for file_path in uncleaned_logs:
        if os.path.exists(file_path):
            print(f"Processing: {file_path}")
            base_name = os.path.basename(file_path)
            
            # Move original file
            try:
                shutil.move(file_path, os.path.join(CLEANED_ORIGINAL_DIR, base_name))
                print(f"Moved original log to: {os.path.join(CLEANED_ORIGINAL_DIR, base_name)}")
            except Exception as e:
                print(f"Error moving original file {file_path}: {e}")
                failed_files.append(file_path)
                continue

            # Run cleaning script
            try:
                original_file_path_in_cleaned_dir = os.path.join(CLEANED_ORIGINAL_DIR, base_name)
                result = subprocess.run(["python3", PARSE_SCRIPT, original_file_path_in_cleaned_dir], capture_output=True, text=True, check=True)
                
                cleaned_file_name = base_name.replace('.txt', '_clean.txt')
                cleaned_file_path = os.path.join(CHAT_DIR, cleaned_file_name)

                # Move cleaned file
                if os.path.exists(cleaned_file_path):
                    shutil.move(cleaned_file_path, os.path.join(CLEANED_CLEAN_DIR, cleaned_file_name))
                    print(f"Moved cleaned log to: {os.path.join(CLEANED_CLEAN_DIR, cleaned_file_name)}")
                else:
                    # if the parse script did not create a cleaned file, it might be because it output it to stdout
                    # let's write the stdout to the cleaned file
                    if result.stdout:
                        with open(os.path.join(CLEANED_CLEAN_DIR, cleaned_file_name), "w") as f:
                            f.write(result.stdout)
                        print(f"Wrote cleaned log to: {os.path.join(CLEANED_CLEAN_DIR, cleaned_file_name)}")
                    else:
                        print(f"Cleaned file not found for {file_path}")
                        failed_files.append(file_path)

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
        print("\n--- Failed to process the following files ---")
        for f in failed_files:
            print(f)
    else:
        print("\nAll eligible logs processed successfully.")

if __name__ == "__main__":
    clean_old_chat_logs()
