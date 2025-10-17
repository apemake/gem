
import os
import re
import json
import sys
from datetime import datetime
import strip_ansi

def strip_ansi_codes(line):
    """Removes all ANSI escape codes from a string."""
    return strip_ansi.strip_ansi(line)

def parse_cleaned_log(file_path):
    """Parses a cleaned chat log file and returns a structured representation."""
    with open(file_path, 'r', errors='ignore') as f:
        lines = f.readlines()

    conversation = []
    current_speaker = None
    current_utterance = []

    for line in lines:
        cleaned_line = strip_ansi_codes(line).strip()

        if not cleaned_line:
            continue

        if cleaned_line.startswith("User:"):
            if current_speaker:
                conversation.append({
                    "speaker": current_speaker,
                    "utterance": "\n".join(current_utterance).strip(),
                    "context": {}
                })
            current_speaker = "user"
            current_utterance = [cleaned_line.replace("User:", "").strip()]
        elif cleaned_line.startswith("Gemini:"):
            if current_speaker:
                conversation.append({
                    "speaker": current_speaker,
                    "utterance": "\n".join(current_utterance).strip(),
                    "context": {}
                })
            current_speaker = "gemini"
            current_utterance = [cleaned_line.replace("Gemini:", "").strip()]
        elif current_speaker:
            current_utterance.append(cleaned_line)

    if current_speaker:
        conversation.append({
            "speaker": current_speaker,
            "utterance": "\n".join(current_utterance).strip(),
            "context": {}
        })

    # This is a placeholder for session metadata extraction
    session_id = "unknown"
    start_time = "unknown"
    end_time = "unknown"

    return {
        "session_id": session_id,
        "start_time": start_time,
        "end_time": end_time,
        "conversation": conversation
    }

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
