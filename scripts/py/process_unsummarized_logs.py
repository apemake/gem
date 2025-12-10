import os
import glob
import subprocess
import json
import sys

# Assume summarize_logs.py is in the same directory
SUMMARIZE_LOGS_SCRIPT = os.path.join(os.path.dirname(__file__), "summarize_logs.py")
CHAT_UNCLEAN_DIR = os.path.join(".chat", "unclean")
CHAT_PROCESSED_DIR = os.path.join(".chat", "processed")

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
    
    # Get a list of logs that have already been summarized
    summarized_logs = get_summarized_logs()

    # Find all chat logs in the unclean directory
    unclean_logs = glob.glob(os.path.join(CHAT_UNCLEAN_DIR, "*.txt"))

    processed_any_logs = False
    for log_file_path in unclean_logs:
        log_file_name = os.path.basename(log_file_path)
        if log_file_name not in summarized_logs:
            print(f"Summarizing log: {log_file_name}")
            try:
                # Call summarize_logs.py
                subprocess.run([sys.executable, SUMMARIZE_LOGS_SCRIPT, log_file_path], check=True)
                
                # Move the log to the processed directory
                os.rename(log_file_path, os.path.join(CHAT_PROCESSED_DIR, log_file_name))
                processed_any_logs = True
            except subprocess.CalledProcessError as e:
                print(f"Error summarizing {log_file_name}: {e}", file=sys.stderr)
            except FileNotFoundError:
                print(f"Error: {SUMMARIZE_LOGS_SCRIPT} not found.", file=sys.stderr)
        else:
            print(f"Log {log_file_name} already summarized. Moving to processed.")
            os.rename(log_file_path, os.path.join(CHAT_PROCESSED_DIR, log_file_name))
            processed_any_logs = True
            
    if not processed_any_logs:
        print("No new chat logs to summarize.")

if __name__ == "__main__":
    process_unsummarized_logs()
