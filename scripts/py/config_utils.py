import os
import subprocess

PROJECT_ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True).stdout.strip()

# Define paths to other scripts
PARSE_LOGS_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "parse_chat_log.py")
SUMMARIZE_LOGS_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "summarize_logs.py")
PROCESS_UNSUMMARIZED_LOGS_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "process_unsummarized_logs.py")
GENERATE_SUMMARY_MANIFEST_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "generate_summary_manifest.py")
VERIFY_ENVIRONMENT_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "verify_environment.py")
SEND_MESSAGE_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "send_swarm_message.py")
READ_MESSAGE_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "read_swarm_messages.py")
GENERATE_PROJECT_STRUCTURE_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "generate_clean_project_structure.py")
VALIDATE_PROJECT_STRUCTURE_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "validate_project_structure.py")

# Define other common paths
COMMS_DIR = os.path.join(PROJECT_ROOT, ".chat", "comms")
PROCESSED_MESSAGES_FILE = os.path.join(PROJECT_ROOT, ".chat", "comms", "processed_messages.txt")
RULES_FILE = os.path.join(PROJECT_ROOT, ".memory", "rules.json")
SUMMARY_BASE_DIR = os.path.join(PROJECT_ROOT, ".chat", "session_summaries")

# Processed log directories
CHAT_UNCLEAN_DIR = os.path.join(PROJECT_ROOT, ".chat", "unclean")
CHAT_PROCESSED_DIR = os.path.join(PROJECT_ROOT, ".chat", "processed")
CHAT_PROCESSED_CLEAN_DIR = os.path.join(PROJECT_ROOT, ".chat", "processed", "clean")
CHAT_PROCESSED_ORIGINAL_DIR = os.path.join(PROJECT_ROOT, ".chat", "processed", "original")

