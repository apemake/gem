import os
import glob
import subprocess
import json
import sys
import shutil
from config_utils import (
    PROJECT_ROOT, PARSE_LOGS_SCRIPT, SUMMARIZE_LOGS_SCRIPT,
    CHAT_UNCLEAN_DIR, CHAT_PROCESSED_DIR, CHAT_PROCESSED_CLEAN_DIR, CHAT_PROCESSED_ORIGINAL_DIR,
    SUMMARY_BASE_DIR
)

def get_summarized_logs():
    """Reads the current daily, weekly, monthly, and quarterly summary files to get a list of already summarized logs."""
    summarized_logs = set()
    # Use SUMMARY_BASE_DIR from config_utils
    summary_base_dir = SUMMARY_BASE_DIR

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
                    pass
    return summarized_logs

def process_unsummarized_logs():
    os.makedirs(CHAT_PROCESSED_DIR, exist_ok=True)
    os.makedirs(CHAT_PROCESSED_CLEAN_DIR, exist_ok=True)
    os.makedirs(CHAT_PROCESSED_ORIGINAL_DIR, exist_ok=True)

    summarized_logs = get_summarized_logs()
    unclean_logs = glob.glob(os.path.join(CHAT_UNCLEAN_DIR, "*.txt"))

    # Load noise patterns from config
    config_path = os.path.join(PROJECT_ROOT, ".memory", "parsing_config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    noise_patterns = config.get("noise_patterns", [])
    noise_patterns_json = json.dumps(noise_patterns)

    processed_any_logs = False
    for log_file_path in unclean_logs:
        log_file_name = os.path.basename(log_file_path)
        if log_file_name in summarized_logs:
            print(f"Log {log_file_name} already summarized. Moving to processed.")
            shutil.move(log_file_path, os.path.join(CHAT_PROCESSED_ORIGINAL_DIR, log_file_name))
            continue
        
        print(f"Processing log: {log_file_name}")
        try:
            # 1. Clean the log file
            print(f"  - Cleaning log...")
            result = subprocess.run([sys.executable, PARSE_LOGS_SCRIPT, log_file_path, noise_patterns_json], capture_output=True, text=True, check=True)
            cleaned_log_content = result.stdout
            
            cleaned_file_name = log_file_name.replace('.txt', '_clean.txt')
            cleaned_file_path = os.path.join(CHAT_PROCESSED_CLEAN_DIR, cleaned_file_name)
            
            with open(cleaned_file_path, "w") as f:
                f.write(cleaned_log_content)
            print(f"  - Wrote cleaned log to: {cleaned_file_path}")

            # 2. Summarize the cleaned log
            print(f"  - Summarizing cleaned log...")
            subprocess.run([sys.executable, SUMMARIZE_LOGS_SCRIPT, cleaned_file_path], check=True)
            
            # 3. Move the original log to the processed directory
            shutil.move(log_file_path, os.path.join(CHAT_PROCESSED_ORIGINAL_DIR, log_file_name))
            processed_any_logs = True
            
        except subprocess.CalledProcessError as e:
            print(f"Error processing {log_file_name}: {e}", file=sys.stderr)
        except FileNotFoundError:
            print(f"Error: A script was not found.", file=sys.stderr)

    if not processed_any_logs:
        print("No new chat logs to summarize.")

if __name__ == "__main__":
    process_unsummarized_logs()

def get_summarized_logs():
    """Reads the current daily, weekly, monthly, and quarterly summary files to get a list of already summarized logs."""
    summarized_logs = set()
    summary_base_dir = os.path.join(".chat", "session_summaries")

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
                    pass
    return summarized_logs

def process_unsummarized_logs():
    os.makedirs(CHAT_PROCESSED_DIR, exist_ok=True)
    os.makedirs(CHAT_PROCESSED_CLEAN_DIR, exist_ok=True)
    os.makedirs(CHAT_PROCESSED_ORIGINAL_DIR, exist_ok=True)

    summarized_logs = get_summarized_logs()
    unclean_logs = glob.glob(os.path.join(CHAT_UNCLEAN_DIR, "*.txt"))

    # Load noise patterns from config
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '.memory', 'parsing_config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    noise_patterns = config.get("noise_patterns", [])
    noise_patterns_json = json.dumps(noise_patterns)

    processed_any_logs = False
    for log_file_path in unclean_logs:
        log_file_name = os.path.basename(log_file_path)
        if log_file_name in summarized_logs:
            print(f"Log {log_file_name} already summarized. Moving to processed.")
            shutil.move(log_file_path, os.path.join(CHAT_PROCESSED_ORIGINAL_DIR, log_file_name))
            continue
        
        print(f"Processing log: {log_file_name}")
        try:
            # 1. Clean the log file
            print(f"  - Cleaning log...")
            result = subprocess.run(["python3", PARSE_LOGS_SCRIPT, log_file_path, noise_patterns_json], capture_output=True, text=True, check=True)
            cleaned_log_content = result.stdout
            
            cleaned_file_name = log_file_name.replace('.txt', '_clean.txt')
            cleaned_file_path = os.path.join(CHAT_PROCESSED_CLEAN_DIR, cleaned_file_name)
            
            with open(cleaned_file_path, "w") as f:
                f.write(cleaned_log_content)
            print(f"  - Wrote cleaned log to: {cleaned_file_path}")

            # 2. Summarize the cleaned log
            print(f"  - Summarizing cleaned log...")
            subprocess.run([sys.executable, SUMMARIZE_LOGS_SCRIPT, cleaned_file_path], check=True)
            
            # 3. Move the original log to the processed directory
            shutil.move(log_file_path, os.path.join(CHAT_PROCESSED_ORIGINAL_DIR, log_file_name))
            processed_any_logs = True
            
        except subprocess.CalledProcessError as e:
            print(f"Error processing {log_file_name}: {e}", file=sys.stderr)
        except FileNotFoundError:
            print(f"Error: A script was not found.", file=sys.stderr)

    if not processed_any_logs:
        print("No new chat logs to summarize.")

if __name__ == "__main__":
    process_unsummarized_logs()
