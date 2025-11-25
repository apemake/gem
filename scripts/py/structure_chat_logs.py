# Learning Summary:
# v1: Initial creation.


import os
import re
import json
import sys
from datetime import datetime, timedelta
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

def is_last_day_of_week(date_obj):
    return date_obj.weekday() == 6  # Sunday

def is_last_day_of_month(date_obj):
    next_day = date_obj + timedelta(days=1)
    return next_day.month != date_obj.month

def is_last_day_of_quarter(date_obj):
    return is_last_day_of_month(date_obj) and date_obj.month in [3, 6, 9, 12]

def is_last_day_of_year(date_obj):
    return is_last_day_of_month(date_obj) and date_obj.month == 12

def generate_summary(summary_files, output_path):
    """
    Generates a summary from a list of daily summary files.
    """
    conversations = []
    for summary_file in summary_files:
        with open(summary_file, 'r') as f:
            data = json.load(f)
            conversations.extend(data.get('conversation', []))

    summary_data = {
        "conversation": conversations
    }

    with open(output_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    print(f"Generated summary: {output_path}")


def structure_logs(chat_dir):
    """
    Structures all cleaned chat logs into a hierarchical folder structure.
    """
    processed_dates = set()
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
            conversation = parse_cleaned_log(file_path)
            
            # Group by hour
            hourly_summary = {}
            for turn in conversation:
                if turn['timestamp']:
                    hour = datetime.strptime(turn['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%H:00')
                    if hour not in hourly_summary:
                        hourly_summary[hour] = []
                    hourly_summary[hour].append(turn)

            # Save the structured log
            json_filename = f"{date_obj.strftime('%Y-%m-%d')}.json"
            json_path = os.path.join(day_folder, json_filename)
            with open(json_path, 'w') as f:
                json.dump({"hourly_summary": hourly_summary}, f, indent=2)
            
            print(f"Structured log saved to: {json_path}")

            if date_obj not in processed_dates:
                processed_dates.add(date_obj)

                if is_last_day_of_week(date_obj):
                    week_folder = os.path.dirname(day_folder)
                    daily_summaries = []
                    for root, _, files in os.walk(week_folder):
                        for file in files:
                            if file.endswith('.json') and not file.startswith('weekly_summary'):
                                daily_summaries.append(os.path.join(root, file))
                    weekly_summary_path = os.path.join(week_folder, f"weekly_summary_{week}.json")
                    generate_summary(daily_summaries, weekly_summary_path)

                if is_last_day_of_month(date_obj):
                    month_folder = os.path.dirname(os.path.dirname(day_folder))
                    daily_summaries = []
                    for root, _, files in os.walk(month_folder):
                        for file in files:
                            if file.endswith('.json') and not file.startswith('monthly_summary'):
                                daily_summaries.append(os.path.join(root, file))
                    monthly_summary_path = os.path.join(month_folder, f"monthly_summary_{month}.json")
                    generate_summary(daily_summaries, monthly_summary_path)

                if is_last_day_of_quarter(date_obj):
                    quarter_folder = os.path.dirname(os.path.dirname(os.path.dirname(day_folder)))
                    daily_summaries = []
                    for root, _, files in os.walk(quarter_folder):
                        for file in files:
                            if file.endswith('.json') and not file.startswith('quarterly_summary'):
                                daily_summaries.append(os.path.join(root, file))
                    quarterly_summary_path = os.path.join(quarter_folder, f"quarterly_summary_{quarter}.json")
                    generate_summary(daily_summaries, quarterly_summary_path)

                if is_last_day_of_year(date_obj):
                    year_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(day_folder))))
                    daily_summaries = []
                    for root, _, files in os.walk(year_folder):
                        for file in files:
                            if file.endswith('.json') and not file.startswith('yearly_summary'):
                                daily_summaries.append(os.path.join(root, file))
                    yearly_summary_path = os.path.join(year_folder, f"yearly_summary_{year}.json")
                    generate_summary(daily_summaries, yearly_summary_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python structure_chat_logs.py <path_to_chat_directory>")
        sys.exit(1)
    
    chat_dir = sys.argv[1]
    structure_logs(chat_dir)
