import os
import json
import re
import sys
import datetime

def generate_summary_manifest(summary_dir):
    """
    Generates a JSON manifest of all daily summary files.
    """
    all_daily_files = [os.path.join(root, file) for root, _, files in os.walk(summary_dir) for file in files if re.match(r'\d{4}-\d{2}-\d{2}\.json', file)]
    all_daily_files.sort()

    manifest = {
        "manifest_creation_timestamp": datetime.datetime.utcnow().isoformat(),
        "daily_summary_files": all_daily_files
    }

    manifest_path = os.path.join(summary_dir, "summary_manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"Summary manifest created at: {manifest_path}")

if __name__ == "__main__":
    summary_dir = os.path.join(".chat", "session_summaries")
    generate_summary_manifest(summary_dir)
