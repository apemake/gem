import json
import os
import argparse
import subprocess

PROCESSED_MESSAGES_FILE = os.path.join(".chat", "comms", "processed_messages.txt")
SEND_MESSAGE_SCRIPT = os.path.join("scripts", "py", "send_swarm_message.py")

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

def read_swarm_messages(current_agent_name):
    comms_dir = os.path.join(".chat", "comms")
    if not os.path.exists(comms_dir):
        print(f"Communication directory '{comms_dir}' does not exist.")
        return

    processed_messages = get_processed_messages()
    
    new_messages = []
    for filename in os.listdir(comms_dir):
        file_path = os.path.join(comms_dir, filename)
        
        # Skip directories, non-JSON files, and the processed_messages.txt file
        if not os.path.isfile(file_path) or not filename.endswith(".json") or filename == os.path.basename(PROCESSED_MESSAGES_FILE):
            continue

        if filename not in processed_messages:
            try:
                with open(file_path, "r") as f:
                    message = json.load(f)
                    # Filter out messages sent by the current agent
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
    parser = argparse.ArgumentParser(description="Read and process incoming messages from the swarm.")
    parser.add_argument("--agent_name", required=True, help="The name of the current agent (e.g., Vesper).")
    args = parser.parse_args()
    
    read_swarm_messages(args.agent_name)
