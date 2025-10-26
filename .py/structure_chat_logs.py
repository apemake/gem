# Learning Summary:
# v1: Initial creation.


import os
import re
import json
import sys
from datetime import datetime
import strip_ansi

def strip_ansi_codes(line):
    """Removes all ANSI escape codes from a string."""
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

def parse_cleaned_log(file_path):
    """Parses a cleaned chat log file (in JSON format) and returns its content."""
    with open(file_path, 'r', errors='ignore') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def get_folder_paths(date_obj):
    """Generates the folder paths for a given date."""
    year = date_obj.strftime("%Y")
    quarter = f"Q{(date_obj.month - 1) // 3 + 1}"
    month = date_obj.strftime("%m-%B")
    week = f"W{date_obj.strftime('%U')}"
    return year, quarter, month, week

def structure_logs(chat_dir):
    """
    Structures all cleaned chat logs into a hierarchical folder structure.
    """
    for filename in os.listdir(chat_dir):
        if filename.endswith("_clean.txt"):
            file_path = os.path.join(chat_dir, filename)
            
            # Extract date from filename (assuming YYYYMMDD format)
            match = re.search(r'(\d{8})', filename)
            if not match:
                continue
            
            date_str = match.group(1)
            date_obj = datetime.strptime(date_str, "%Y%m%d")
            
            # Get folder paths
            year, quarter, month, week = get_folder_paths(date_obj)
            
            # Create folder structure
            day_folder = os.path.join(chat_dir, year, quarter, month, week)
            os.makedirs(day_folder, exist_ok=True)
            
            # Parse the log and create the structured JSON
            structured_log = parse_cleaned_log(file_path)
            
            # Save the structured log
            json_filename = f"{date_obj.strftime('%Y-%m-%d')}.json"
            json_path = os.path.join(day_folder, json_filename)
            with open(json_path, 'w') as f:
                json.dump(structured_log, f, indent=2)
            
            print(f"Structured log saved to: {json_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python structure_chat_logs.py <path_to_chat_directory>")
        sys.exit(1)
    
    chat_dir = sys.argv[1]
    structure_logs(chat_dir)
