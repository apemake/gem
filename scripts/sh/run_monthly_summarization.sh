#!/bin/bash
# This script is used to run the summarization process on all unclean chat logs.
# It is intended to be run monthly or as needed to keep the chat summaries up to date.

# Find all unclean chat log files and process them
for file in .chat/cleaned/clean/*.txt
do
  echo "Summarizing $file"
  python3 scripts/py/summarize_logs.py "$file"
done
