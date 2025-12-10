import os
import json
from collections import defaultdict
import gc # Import garbage collector
import re
import sys

def process_level(source_level_files, target_summary_file):
    """
    Generic function to create a higher-level summary from a list of lower-level summary files.
    """
    summary_data = defaultdict(list)
    for source_file in source_level_files:
        if os.path.exists(source_file):
            with open(source_file, 'r') as f:
                try:
                    data = json.load(f)
                    # The structure of WEEK.json, MONTH.json, etc. is just a dict of hourly conversations
                    # The daily summaries have the nested structure
                    if "summary_template" in data:
                        # It's a daily summary
                        for year_data in data.get("summary_template", {}).get("structure", {}).get("year", {}).values():
                            for quarter_data in year_data.get("quarter", {}).values():
                                for month_data in quarter_data.get("month", {}).values():
                                    for week_data in month_data.get("week", {}).values():
                                        for day_summary in week_data.get("day", {}).values():
                                            for hourly_summary in day_summary.get("hourly_summary", []):
                                                summary_data[hourly_summary["hour"]].extend(hourly_summary["conversation"])
                    else:
                        # It's already a higher-level summary (e.g., WEEK.json)
                        for hour, conversation in data.items():
                            summary_data[hour].extend(conversation)

                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    print(f"Skipping file due to error: {source_file} - {e}")
            gc.collect() # Force garbage collection after processing each file

    if summary_data:
        with open(target_summary_file, 'w') as f:
            json.dump(summary_data, f, indent=2)
        print(f"Created/updated summary: {target_summary_file}")


def create_higher_level_summaries(summary_dir):
    # Get all daily summary files
    all_daily_files = [os.path.join(root, file) for root, _, files in os.walk(summary_dir) for file in files if re.match(r'\d{4}-\d{2}-\d{2}\.json', file)]

    # Group daily files by week
    weekly_groups = defaultdict(list)
    for daily_file in all_daily_files:
        week_dir = os.path.dirname(daily_file)
        weekly_groups[week_dir].append(daily_file)
    
    # Process weeks
    for week_dir, daily_files in weekly_groups.items():
        weekly_summary_file = os.path.join(week_dir, "WEEK.json")
        process_level(daily_files, weekly_summary_file)
        
    # Group weekly files by month
    all_weekly_files = [os.path.join(root, file) for root, _, files in os.walk(summary_dir) for file in files if file == "WEEK.json"]
    monthly_groups = defaultdict(list)
    for weekly_file in all_weekly_files:
        month_dir = os.path.dirname(os.path.dirname(weekly_file)) # Go up two levels
        monthly_groups[month_dir].append(weekly_file)
        
    # Process months
    for month_dir, weekly_files in monthly_groups.items():
        monthly_summary_file = os.path.join(month_dir, "MONTH.json")
        process_level(weekly_files, monthly_summary_file)

    # Group monthly files by quarter
    all_monthly_files = [os.path.join(root, file) for root, _, files in os.walk(summary_dir) for file in files if file == "MONTH.json"]
    quarterly_groups = defaultdict(list)
    for monthly_file in all_monthly_files:
        quarter_dir = os.path.dirname(os.path.dirname(monthly_file)) # Go up two levels
        quarterly_groups[quarter_dir].append(monthly_file)
        
    # Process quarters
    for quarter_dir, monthly_files in quarterly_groups.items():
        quarterly_summary_file = os.path.join(quarter_dir, "QUARTER.json")
        process_level(monthly_files, quarterly_summary_file)


if __name__ == "__main__":
    summary_dir = os.path.join(".chat", "session_summaries")
    create_higher_level_summaries(summary_dir)