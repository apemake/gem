import os
import json
from collections import defaultdict

def create_higher_level_summaries(summary_dir):
    # Process weeks
    for year_dir in os.listdir(summary_dir):
        year_path = os.path.join(summary_dir, year_dir)
        if not os.path.isdir(year_path):
            continue

        for quarter_dir in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter_dir)
            if not os.path.isdir(quarter_path):
                continue

            for month_dir in os.listdir(quarter_path):
                month_path = os.path.join(quarter_path, month_dir)
                if not os.path.isdir(month_path):
                    continue

                for week_dir in os.listdir(month_path):
                    week_path = os.path.join(month_path, week_dir)
                    if not os.path.isdir(week_path):
                        continue
                    
                    weekly_summary_file_path = os.path.join(week_path, "WEEK.json")
                    
                    with open(weekly_summary_file_path, 'w') as weekly_f:
                        weekly_summary = defaultdict(list)
                        for day_file in os.listdir(week_path):
                            if day_file.endswith(".json") and day_file != "WEEK.json":
                                day_path = os.path.join(week_path, day_file)
                                with open(day_path, 'r') as f:
                                    try:
                                        day_data = json.load(f)
                                        for year, year_data in day_data.get("summary_template", {}).get("structure", {}).get("year", {}).items():
                                            for quarter, quarter_data in year_data.get("quarter", {}).items():
                                                for month, month_data in quarter_data.get("month", {}).items():
                                                    for week, week_data in month_data.get("week", {}).items():
                                                        for day, day_summary in week_data.get("day", {}).items():
                                                            for hourly_summary in day_summary.get("hourly_summary", []):
                                                                weekly_summary[hourly_summary["hour"]].extend(hourly_summary["conversation"])
                                    except (json.JSONDecodeError, KeyError, IndexError) as e:
                                        print(f"Skipping file due to error: {day_path} - {e}")
                        
                        if weekly_summary:
                            json.dump(weekly_summary, weekly_f, indent=2)
                            print(f"Created weekly summary: {weekly_summary_file_path}")

    # Process months
    for year_dir in os.listdir(summary_dir):
        year_path = os.path.join(summary_dir, year_dir)
        if not os.path.isdir(year_path):
            continue

        for quarter_dir in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter_dir)
            if not os.path.isdir(quarter_path):
                continue

            for month_dir in os.listdir(quarter_path):
                month_path = os.path.join(quarter_path, month_dir)
                if not os.path.isdir(month_path):
                    continue

                monthly_summary_file_path = os.path.join(month_path, "MONTH.json")

                with open(monthly_summary_file_path, 'w') as monthly_f:
                    monthly_summary = defaultdict(list)
                    for week_dir in os.listdir(month_path):
                        week_path = os.path.join(month_path, week_dir)
                        if not os.path.isdir(week_path):
                            continue
                        
                        weekly_summary_file_path = os.path.join(week_path, "WEEK.json")
                        if os.path.exists(weekly_summary_file_path):
                            with open(weekly_summary_file_path, 'r') as f:
                                try:
                                    weekly_data = json.load(f)
                                    for hour, conversation in weekly_data.items():
                                        monthly_summary[hour].extend(conversation)
                                except json.JSONDecodeError as e:
                                    print(f"Skipping file due to error: {weekly_summary_file_path} - {e}")
                    
                    if monthly_summary:
                        json.dump(monthly_summary, monthly_f, indent=2)
                        print(f"Created monthly summary: {monthly_summary_file_path}")


    # Process quarters
    for year_dir in os.listdir(summary_dir):
        year_path = os.path.join(summary_dir, year_dir)
        if not os.path.isdir(year_path):
            continue

        for quarter_dir in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter_dir)
            if not os.path.isdir(quarter_path):
                continue

            quarterly_summary_file_path = os.path.join(quarter_path, "QUARTER.json")
            with open(quarterly_summary_file_path, 'w') as quarterly_f:
                quarterly_summary = defaultdict(list)
                for month_dir in os.listdir(quarter_path):
                    month_path = os.path.join(quarter_path, month_dir)
                    if not os.path.isdir(month_path):
                        continue

                    monthly_summary_file_path = os.path.join(month_path, "MONTH.json")
                    if os.path.exists(monthly_summary_file_path):
                        with open(monthly_summary_file_path, 'r') as f:
                            try:
                                monthly_data = json.load(f)
                                for hour, conversation in monthly_data.items():
                                    quarterly_summary[hour].extend(conversation)
                            except json.JSONDecodeError as e:
                                print(f"Skipping file due to error: {monthly_summary_file_path} - {e}")
                
                if quarterly_summary:
                    json.dump(quarterly_summary, quarterly_f, indent=2)
                    print(f"Created quarterly summary: {quarterly_summary_file_path}")


if __name__ == "__main__":
    summary_dir = os.path.join(".chat", "session_summaries")
    create_higher_level_summaries(summary_dir)