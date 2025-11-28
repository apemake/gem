import os
import json
import re
import sys
import datetime
from collections import defaultdict

def get_week_of_month(date):
    first_day_of_month = date.replace(day=1)
    adjusted_date = date.day + first_day_of_month.weekday()
    return (adjusted_date - 1) // 7 + 1

def append_to_summary(summary_file_path, new_conversations):
    if os.path.exists(summary_file_path):
        with open(summary_file_path, 'r+') as f:
            try:
                summary_data = json.load(f)
                summary_data = defaultdict(list, summary_data) # Convert to defaultdict
            except json.JSONDecodeError:
                summary_data = defaultdict(list)
            
            for hour, conversation in new_conversations.items():
                summary_data[hour].extend(conversation)
            
            f.seek(0)
            json.dump(summary_data, f, indent=2)
            f.truncate()
    else:
        with open(summary_file_path, 'w') as f:
            json.dump(new_conversations, f, indent=2)


def summarize_log(file_path):
    base_name = os.path.basename(file_path)
    date_str = base_name.split('_')[0]
    
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y%m%d-%H%M%S")
    except ValueError:
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            print(f"Could not parse date from filename: {base_name}")
            return

    year = date_obj.strftime("%Y")
    quarter = f"Q{(date_obj.month - 1) // 3 + 1}"
    month = date_obj.strftime("%m-%B")
    week = f"W{get_week_of_month(date_obj)}"
    day = date_obj.strftime("%Y-%m-%d")

    summary_dir = os.path.join(".chat", "session_summaries", year, quarter, month, week)
    os.makedirs(summary_dir, exist_ok=True)
    
    daily_summary_file_path = os.path.join(summary_dir, f"{day}.json")
    weekly_summary_file_path = os.path.join(summary_dir, "WEEK.json")
    monthly_summary_file_path = os.path.join(os.path.dirname(summary_dir), "MONTH.json")
    quarterly_summary_file_path = os.path.join(os.path.dirname(os.path.dirname(summary_dir)), "QUARTER.json")

    hourly_conversations = defaultdict(list)

    with open(file_path, 'r', errors='ignore') as f:
        current_speaker = None
        current_utterance_lines = []
        last_known_timestamp = None

        for line in f:
            cleaned_line = line.strip() # No ANSI stripping, as it's already done
            
            if not cleaned_line:
                continue

            timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', cleaned_line)
            if timestamp_match:
                last_known_timestamp = timestamp_match.group(1)
                cleaned_line = cleaned_line.replace(timestamp_match.group(0), '').strip()


            if cleaned_line.startswith('> '): # User input
                if current_speaker == "gemini" and current_utterance_lines:
                    if last_known_timestamp:
                        hour_key = datetime.datetime.strptime(last_known_timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:00")
                        hourly_conversations[hour_key].append({
                            "speaker": "gemini",
                            "utterance": " ".join(current_utterance_lines).strip(),
                            "timestamp": last_known_timestamp
                        })
                    current_utterance_lines = []
                
                current_speaker = "user"
                current_utterance_lines.append(cleaned_line[2:]) # Remove '> '
            else: # Likely Gemini's response
                if current_speaker == "user" and current_utterance_lines:
                    if last_known_timestamp:
                        hour_key = datetime.datetime.strptime(last_known_timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:00")
                        hourly_conversations[hour_key].append({
                            "speaker": "user",
                            "utterance": " ".join(current_utterance_lines).strip(),
                            "timestamp": last_known_timestamp
                        })
                    current_utterance_lines = []
                
                current_speaker = "gemini"
                current_utterance_lines.append(cleaned_line)

        # Append any remaining turn after the loop
        if current_utterance_lines and current_speaker and last_known_timestamp:
            hour_key = datetime.datetime.strptime(last_known_timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:00")
            hourly_conversations[hour_key].append({
                "speaker": current_speaker,
                "utterance": " ".join(current_utterance_lines).strip(),
                "timestamp": last_known_timestamp
            })


    if not hourly_conversations:
        print(f"No conversations found in {file_path}")
        return

    # Append to daily, weekly, monthly, and quarterly summaries
    append_to_summary(daily_summary_file_path, hourly_conversations)
    append_to_summary(weekly_summary_file_path, hourly_conversations)
    append_to_summary(monthly_summary_file_path, hourly_conversations)
    append_to_summary(quarterly_summary_file_path, hourly_conversations)
    
    print(f"Successfully summarized {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize_logs.py <path_to_log_file1> <path_to_log_file2> ...", file=sys.stderr)
        sys.exit(1)

    for file_path in sys.argv[1:]:
        summarize_log(file_path)