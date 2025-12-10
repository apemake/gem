import os
import json
from collections import defaultdict
import re
import sys

def append_to_summary(target_file, source_file):
    """
    Appends data from a source_file to a target_file.
    """
    if not os.path.exists(source_file):
        return

    # Load new data
    with open(source_file, 'r') as f:
        try:
            new_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Skipping corrupted file: {source_file}")
            return
            
    # Load existing summary data or initialize if not present
    if os.path.exists(target_file):
        with open(target_file, 'r+') as f:
            try:
                summary_data = json.load(f)
                summary_data = defaultdict(list, summary_data)
            except json.JSONDecodeError:
                summary_data = defaultdict(list)
    else:
        summary_data = defaultdict(list)

    if "summary_template" in new_data:
        # It's a daily summary
        for year_data in new_data.get("summary_template", {}).get("structure", {}).get("year", {}).values():
            for quarter_data in year_data.get("quarter", {}).values():
                for month_data in quarter_data.get("month", {}).values():
                    for week_data in month_data.get("week", {}).values():
                        for day_summary in week_data.get("day", {}).values():
                            for hourly_summary in day_summary.get("hourly_summary", []):
                                summary_data[hourly_summary["hour"]].extend(hourly_summary["conversation"])
    else:
        # It's already a higher-level summary (e.g., WEEK.json)
        for hour, conversation in new_data.items():
            summary_data[hour].extend(conversation)
            
    # Write the updated summary back to the file
    with open(target_file, 'w') as f:
        json.dump(summary_data, f, indent=2)

def create_higher_level_summaries(summary_dir):
    # Process weeks
    all_daily_files = [os.path.join(root, file) for root, _, files in os.walk(summary_dir) for file in files if re.match(r'\d{4}-\d{2}-\d{2}\.json', file)]
    weekly_groups = defaultdict(list)
    for daily_file in all_daily_files:
        week_dir = os.path.dirname(daily_file)
        weekly_groups[week_dir].append(daily_file)
    
    for week_dir, daily_files in weekly_groups.items():
        weekly_summary_file = os.path.join(week_dir, "WEEK.json")
        # Clear the weekly summary file before processing
        if os.path.exists(weekly_summary_file):
            os.remove(weekly_summary_file)
        for daily_file in daily_files:
            append_to_summary(weekly_summary_file, daily_file)
        print(f"Processed weekly summary: {weekly_summary_file}")

    # Process months
    all_weekly_files = [os.path.join(root, file) for root, _, files in os.walk(summary_dir) for file in files if file == "WEEK.json"]
    monthly_groups = defaultdict(list)
    for weekly_file in all_weekly_files:
        month_dir = os.path.dirname(os.path.dirname(weekly_file))
        monthly_groups[month_dir].append(weekly_file)
        
    for month_dir, weekly_files in monthly_groups.items():
        monthly_summary_file = os.path.join(month_dir, "MONTH.json")
        if os.path.exists(monthly_summary_file):
            os.remove(monthly_summary_file)
        for weekly_file in weekly_files:
            append_to_summary(monthly_summary_file, weekly_file)
        print(f"Processed monthly summary: {monthly_summary_file}")

    # Process quarters
    all_monthly_files = [os.path.join(root, file) for root, _, files in os.walk(summary_dir) for file in files if file == "MONTH.json"]
    quarterly_groups = defaultdict(list)
    for monthly_file in all_monthly_files:
        quarter_dir = os.path.dirname(os.path.dirname(monthly_file))
        quarterly_groups[quarter_dir].append(monthly_file)
        
    for quarter_dir, monthly_files in quarterly_groups.items():
        quarterly_summary_file = os.path.join(quarter_dir, "QUARTER.json")
        if os.path.exists(quarterly_summary_file):
            os.remove(quarterly_summary_file)
        for monthly_file in monthly_files:
            append_to_summary(quarterly_summary_file, monthly_file)
        print(f"Processed quarterly summary: {quarterly_summary_file}")


if __name__ == "__main__":
    summary_dir = os.path.join(".chat", "session_summaries")
    create_higher_level_summaries(summary_dir)