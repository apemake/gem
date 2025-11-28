import os
import json
import re
import sys
import datetime

def get_week_of_month(date):
    first_day_of_month = date.replace(day=1)
    adjusted_date = date.day + first_day_of_month.weekday()
    return (adjusted_date - 1) // 7 + 1

def strip_ansi_codes(line):
    """Removes all ANSI escape codes from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\-_]|[[\[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', line)

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
    summary_file_path = os.path.join(summary_dir, f"{day}.json")

    hourly_conversations = {}

    with open(file_path, 'r', errors='ignore') as f:
        for line in f:
            cleaned_line = strip_ansi_codes(line).strip()
            
            if "User:" not in cleaned_line and "Gemini:" not in cleaned_line:
                continue

            timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', cleaned_line)
            timestamp = timestamp_match.group(1) if timestamp_match else None

            if "User:" in cleaned_line:
                speaker = "user"
                utterance = cleaned_line.split("User:", 1)[1].strip()
            else:
                speaker = "gemini"
                utterance = cleaned_line.split("Gemini:", 1)[1].strip()

            if timestamp:
                hour_key = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:00")
                
                if hour_key not in hourly_conversations:
                    hourly_conversations[hour_key] = []
                
                hourly_conversations[hour_key].append({
                    "speaker": speaker,
                    "utterance": utterance,
                    "timestamp": timestamp
                })

    if not hourly_conversations:
        print(f"No conversations found in {file_path}")
        return

    if os.path.exists(summary_file_path):
        try:
            with open(summary_file_path, "r") as f:
                summary_data = json.load(f)
        except json.JSONDecodeError:
            summary_data = None
    else:
        summary_data = None

    if not summary_data:
        summary_data = {
            "summary_template": {
                "name": "Hierarchical Hourly Summary",
                "description": "A template for generating a hierarchical summary of chat logs, with an hourly breakdown of conversations.",
                "structure": { "year": { year: { "quarter": { quarter: { "month": { month: { "week": { week: { "day": { day: { "hourly_summary": [] }}}}}}}}}}}
            }
        }
    
    try:
        hourly_summary_list = summary_data["summary_template"]["structure"]["year"][year]["quarter"][quarter]["month"][month]["week"][week]["day"][day]["hourly_summary"]
    except KeyError:
        summary_data["summary_template"]["structure"]["year"][year] = {"quarter": {quarter: {"month": {month: {"week": {week: {"day": {day: {"hourly_summary": [] }}}}}}}}}
        hourly_summary_list = summary_data["summary_template"]["structure"]["year"][year]["quarter"][quarter]["month"][month]["week"][week]["day"][day]["hourly_summary"]


    for hour, conversation in hourly_conversations.items():
        existing_hour = next((item for item in hourly_summary_list if item["hour"] == hour), None)
        if existing_hour:
            existing_hour["conversation"].extend(conversation)
        else:
            hourly_summary_list.append({
                "hour": hour,
                "conversation": conversation
            })

    with open(summary_file_path, "w") as f:
        json.dump(summary_data, f, indent=2)

    print(f"Successfully summarized {file_path} into {summary_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python summarize_logs.py <path_to_log_file>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    summarize_log(file_path)