import json
import os
import argparse
import subprocess
import glob

PROJECT_ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True).stdout.strip()
PROCESSED_MESSAGES_FILE = os.path.join(PROJECT_ROOT, ".chat", "comms", "processed_messages.txt")
SEND_MESSAGE_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "py", "send_swarm_message.py")
RULES_FILE = os.path.join(PROJECT_ROOT, ".memory", "rules.json")

def get_current_agent_name():
    with open(RULES_FILE, 'r') as f:
        rules = json.load(f)
        for rule_set in rules.get("rules", []):
            if rule_set.get("name") == "user_preferences":
                for preference in rule_set.get("preferences", []):
                    if preference.get("id") == "agent_id":
                        return preference.get("value")
    return "UnknownAgent" # Fallback

def get_processed_messages():
    if not os.path.exists(PROCESSED_MESSAGES_FILE):
        return set()
    with open(PROCESSED_MESSAGES_FILE, "r") as f:
        return set(f.read().splitlines())

def add_processed_message(message_filename):
    with open(PROCESSED_MESSAGES_FILE, "a") as f:
        f.write(message_filename + "\n")

def send_acknowledgment(sender_name, recipient_name, acknowledged_message_filename):
    print(f"Sending acknowledgment to {recipient_name} for message {acknowledged_message_filename}...")
    try:
        subprocess.run(
            [
                "python3", SEND_MESSAGE_SCRIPT,
                "--sender", sender_name,
                "--recipient", recipient_name,
                "--message_type", "acknowledgment",
                "--content", f"Message '{acknowledged_message_filename}' received.",
                "--other_relevant_info", json.dumps({"acknowledged_message": acknowledged_message_filename})
            ],
            check=True,
            capture_output=True,
            text=True
        )
        print("Acknowledgment sent successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to send acknowledgment: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print(f"Error: {SEND_MESSAGE_SCRIPT} not found. Acknowledgment failed.")

def read_swarm_messages():
    current_agent_name = get_current_agent_name()
    comms_dir = os.path.join(".chat", "comms")
    if not os.path.exists(comms_dir):
        print(f"Communication directory '{comms_dir}' does not exist.")
        return

    processed_messages = get_processed_messages()
    
    new_messages = []
    
    # Optimized file filtering: look for messages specifically for this agent or the swarm
    search_patterns = [
        os.path.join(comms_dir, f"*_to_{current_agent_name}_*.json"),
        os.path.join(comms_dir, f"*_to_swarm_*.json")
    ]
    
    candidate_files = []
    for pattern in search_patterns:
        candidate_files.extend(glob.glob(pattern))

    for file_path in candidate_files:
        filename = os.path.basename(file_path)
        
        # Skip directories and the processed_messages.txt file
        if not os.path.isfile(file_path) or filename == os.path.basename(PROCESSED_MESSAGES_FILE):
            continue

        if filename not in processed_messages:
            try:
                with open(file_path, "r") as f:
                    message = json.load(f)
                    # Filter out messages sent by the current agent (redundant with filename filter but good as a sanity check)
                    if message.get('sender') != current_agent_name:
                        new_messages.append((filename, message))
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {filename}")
    
    if not new_messages:
        print("No new messages.")
        return

    for filename, message in new_messages:
        print(f"--- New Message from {message.get('sender', 'Unknown')} ---")
        print(f"  Recipient: {message.get('recipient', 'Unknown')}")
        print(f"  Timestamp: {message.get('timestamp', 'Unknown')}")
        print(f"  Type: {message.get('message_type', 'Unknown')}")
        print(f"  Content: {message.get('content', 'No Content')}")
        
        context = message.get('context', {})
        if context:
            if context.get('file_paths'):
                print(f"  Context - File Paths: {', '.join(context['file_paths'])}")
            if context.get('commit_hashes'):
                print(f"  Context - Commit Hashes: {', '.join(context['commit_hashes'])}")
            if context.get('other_relevant_info'):
                print(f"  Context - Other Info: {json.dumps(context['other_relevant_info'])}")
        print("------------------------------------")
        
        add_processed_message(filename)
        # Send acknowledgment if the message was not an acknowledgment itself
        if message.get('message_type') != 'acknowledgment':
            send_acknowledgment(current_agent_name, message.get('sender', 'swarm'), filename)


if __name__ == "__main__":
    read_swarm_messages()
