import os
import glob
import subprocess
import json
import sys
import shutil # Import shutil for moving files

# Import the cleaning function
from clean_chat_logs import clean_old_chat_logs 

# Assume summarize_logs.py is in the same directory
SUMMARIZE_LOGS_SCRIPT = os.path.join(os.path.dirname(__file__), "summarize_logs.py")
CHAT_UNCLEAN_DIR = os.path.join(".chat", "unclean")
CHAT_PROCESSED_DIR = os.path.join(".chat", "processed")
CHAT_PROCESSED_CLEAN_DIR = os.path.join(".chat", "processed", "clean") # New directory for processed clean logs
CLEANED_CLEAN_DIR = os.path.join(".chat", "cleaned", "clean") # Directory where cleaned logs are stored by clean_chat_logs.py
CLEANED_ORIGINAL_DIR = os.path.join(".chat", ".chat", "cleaned", "original") # Directory where original logs are moved by clean_chat_logs.py


def get_summarized_logs():
    """Reads the current daily, weekly, monthly, and quarterly summary files to get a list of already summarized logs."""
    summarized_logs = set()
    summary_base_dir = os.path.join(".chat", "session_summaries")

    # Iterate through all summary JSON files
    for root, _, files in os.walk(summary_base_dir):
        for file in files:
            if file.endswith(".json"):
                summary_file_path = os.path.join(root, file)
                try:
                    with open(summary_file_path, 'r') as f:
                        summary_data = json.load(f)
                        for hour_data in summary_data.values():
                            for entry in hour_data:
                                if "source_log" in entry:
                                    summarized_logs.add(os.path.basename(entry["source_log"]))
                except (json.JSONDecodeError, KeyError):
                    # Ignore corrupted or incomplete summary files
                    pass
    return summarized_logs

def process_unsummarized_logs():
    os.makedirs(CHAT_PROCESSED_DIR, exist_ok=True)
    os.makedirs(CHAT_PROCESSED_CLEAN_DIR, exist_ok=True) # Create new directory

    # First, run the cleaning process. This will move files from CHAT_UNCLEAN_DIR
    # to CLEANED_ORIGINAL_DIR and their cleaned versions to CLEANED_CLEAN_DIR.
    print("Running chat log cleaning process...")
    clean_old_chat_logs()
    print("Chat log cleaning process complete.")

    # Get a list of logs that have already been summarized
    summarized_logs = get_summarized_logs()

    # Now, find all *cleaned* chat logs to summarize
    cleaned_logs_for_summarization = glob.glob(os.path.join(CLEANED_CLEAN_DIR, "*.txt"))

    processed_any_logs = False
    for cleaned_log_file_path in cleaned_logs_for_summarization:
        # The base name of the cleaned log is original_log_name_clean.txt
        # We need the original log name to check against summarized_logs
        original_log_file_name = os.path.basename(cleaned_log_file_path).replace('_clean.txt', '.txt')

        if original_log_file_name not in summarized_logs:
            print(f"Summarizing cleaned log: {os.path.basename(cleaned_log_file_path)}")
            try:
                # Call summarize_logs.py with the cleaned log file
                subprocess.run([sys.executable, SUMMARIZE_LOGS_SCRIPT, cleaned_log_file_path], check=True)
                
                # Move the *original* log from CLEANED_ORIGINAL_DIR to CHAT_PROCESSED_DIR
                original_uncleaned_path = os.path.join(CLEANED_ORIGINAL_DIR, original_log_file_name)
                if os.path.exists(original_uncleaned_path):
                    shutil.move(original_uncleaned_path, os.path.join(CHAT_PROCESSED_DIR, original_log_file_name))
                
                # Move the *cleaned* log from CLEANED_CLEAN_DIR to CHAT_PROCESSED_CLEAN_DIR
                shutil.move(cleaned_log_file_path, os.path.join(CHAT_PROCESSED_CLEAN_DIR, os.path.basename(cleaned_log_file_path)))
                
                processed_any_logs = True
            except subprocess.CalledProcessError as e:
                print(f"Error summarizing {os.path.basename(cleaned_log_file_path)}: {e}", file=sys.stderr)
            except FileNotFoundError:
                print(f"Error: {SUMMARIZE_LOGS_SCRIPT} not found.", file=sys.stderr)
        else:
            print(f"Log {original_log_file_name} already summarized. Moving associated files to processed.")
            # Move the *original* log from CLEANED_ORIGINAL_DIR to CHAT_PROCESSED_DIR
            original_uncleaned_path = os.path.join(CLEANED_ORIGINAL_DIR, original_log_file_name)
            if os.path.exists(original_uncleaned_path):
                shutil.move(original_uncleaned_path, os.path.join(CHAT_PROCESSED_DIR, original_log_file_name))
            
            # Move the *cleaned* log from CLEANED_CLEAN_DIR to CHAT_PROCESSED_CLEAN_DIR
            shutil.move(cleaned_log_file_path, os.path.join(CHAT_PROCESSED_CLEAN_DIR, os.path.basename(cleaned_log_file_path)))
            processed_any_logs = True
            
    if not processed_any_logs:
        print("No new chat logs to summarize.")

if __name__ == "__main__":
    process_unsummarized_logs()
