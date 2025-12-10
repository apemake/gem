import os
import json
from collections import defaultdict
import re
import sys
import shutil

def aggregate_summaries(source_files):
    """
    Aggregates a list of summary files into a single in-memory dictionary.
    """
    aggregated_data = defaultdict(list)
    for source_file in source_files:
        if os.path.exists(source_file):
            with open(source_file, 'r') as f:
                try:
                    data = json.load(f)
                    if "summary_template" in data:
                        # It's a daily summary
                        for year_data in data.get("summary_template", {}).get("structure", {}).get("year", {}).values():
                            for quarter_data in year_data.get("quarter", {}).values():
                                for month_data in quarter_data.get("month", {}).values():
                                    for week_data in month_data.get("week", {}).values():
                                        for day_summary in week_data.get("day", {}).values():
                                            for hourly_summary in day_summary.get("hourly_summary", []):
                                                aggregated_data[hourly_summary["hour"]].extend(hourly_summary["conversation"])
                    else:
                        # It's already a higher-level summary (e.g., WEEK.json)
                        for hour, conversation in data.items():
                            aggregated_data[hour].extend(conversation)
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    print(f"Skipping file due to error: {source_file} - {e}")
    return aggregated_data

def create_higher_level_summaries(summary_dir):
    # Process weeks
    all_daily_files = [os.path.join(root, file) for root, _, files in os.walk(summary_dir) for file in files if re.match(r'\d{4}-\d{2}-\d{2}\.json', file)]
    weekly_groups = defaultdict(list)
    for daily_file in all_daily_files:
        week_dir = os.path.dirname(daily_file)
        weekly_groups[week_dir].append(daily_file)
    
    for week_dir, daily_files in weekly_groups.items():
        weekly_summary_file = os.path.join(week_dir, "WEEK.json")
        weekly_summary = aggregate_summaries(daily_files)
        if weekly_summary:
            with open(weekly_summary_file, 'w') as f:
                json.dump(weekly_summary, f, indent=2)
            print(f"Processed weekly summary: {weekly_summary_file}")

    # Process months
    all_weekly_files = [os.path.join(root, file) for root, _, files in os.walk(summary_dir) for file in files if file == "WEEK.json"]
    monthly_groups = defaultdict(list)
    for weekly_file in all_weekly_files:
        month_dir = os.path.dirname(os.path.dirname(weekly_file))
        monthly_groups[month_dir].append(weekly_file)
        
    for month_dir, weekly_files in monthly_groups.items():
        monthly_summary_dir = os.path.join(month_dir, "monthly_summaries")
        os.makedirs(monthly_summary_dir, exist_ok=True)
        for weekly_file in weekly_files:
            week_name = os.path.basename(os.path.dirname(weekly_file)) # e.g., "W1"
            shutil.copy(weekly_file, os.path.join(monthly_summary_dir, f"{week_name}.json"))
        print(f"Processed monthly summaries for: {month_dir}")

    # Process quarters
    all_month_dirs = [os.path.join(root, d) for root, dirs, _ in os.walk(summary_dir) for d in dirs if re.match(r'\d{2}-', d)]
    quarterly_groups = defaultdict(list)
    for month_dir in all_month_dirs:
        quarter_dir = os.path.dirname(os.path.dirname(month_dir))
        quarterly_groups[quarter_dir].append(month_dir)

    for quarter_dir, month_dirs in quarterly_groups.items():
        quarterly_summary_dir = os.path.join(quarter_dir, "quarterly_summaries")
        os.makedirs(quarterly_summary_dir, exist_ok=True)
        for month_dir in month_dirs:
            month_name = os.path.basename(month_dir)
            monthly_summary_manifest = {
                "month": month_name,
                "weekly_summaries": [os.path.join(month_dir, "monthly_summaries", f) for f in os.listdir(os.path.join(month_dir, "monthly_summaries"))]
            }
            manifest_path = os.path.join(quarterly_summary_dir, f"{month_name}.json")
            with open(manifest_path, 'w') as f:
                json.dump(monthly_summary_manifest, f, indent=2)
        print(f"Processed quarterly summaries for: {quarter_dir}")


if __name__ == "__main__":
    summary_dir = os.path.join(".chat", "session_summaries")
    create_higher_level_summaries(summary_dir)