import os
import sys
import glob
import json

CHAT_PROCESSED_CLEAN_DIR = os.path.join(".chat", "processed", "clean")

def show_recent_chats(chat_dir, num_files, tail_lines=None):
    """
    Shows the content of the most recent chat log chunks in a readable format.
    """
    search_pattern = os.path.join(chat_dir, '*.txt')

    try:
        chunk_files = glob.glob(search_pattern)

        if not chunk_files:
            print(f"No chat chunks found in: {chat_dir}")
            return

        chunk_files.sort(key=os.path.getmtime, reverse=True)
        files_to_show = chunk_files[:num_files]

        print(f"--- Showing content of the {len(files_to_show)} most recent chat(s) ---")

        for file_path in reversed(files_to_show):
            print(f"\n--- Chat from {os.path.basename(file_path)} ---\n")
            with open(file_path, 'r', errors='ignore') as f:
                try:
                    chat_data = json.load(f)
                    
                    if tail_lines:
                        chat_data = chat_data[-tail_lines:]

                    for turn in chat_data:
                        speaker = turn.get("speaker", "unknown")
                        utterance = turn.get("utterance", "")
                        timestamp = turn.get("timestamp", "")
                        print(f"[{timestamp}] {speaker.capitalize()}: {utterance}")
                        
                except json.JSONDecodeError:
                    print("Could not parse JSON from chat log.")
                    # Fallback to printing raw content if not valid JSON
                    f.seek(0)
                    print(f.read())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    num_to_show = 1
    tail = None

    if len(sys.argv) > 1:
        try:
            num_to_show = int(sys.argv[1])
        except ValueError:
            print("Error: num_files must be an integer.")
            sys.exit(1)

    if len(sys.argv) > 2:
        try:
            tail = int(sys.argv[2])
        except ValueError:
            print("Error: tail must be an integer.")
            sys.exit(1)

    show_recent_chats(CHAT_PROCESSED_CLEAN_DIR, num_to_show, tail)
