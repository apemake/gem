# Learning Summary:
# v1: re.error: incomplete escape. Fix: Escaped backslashes in regex for unicode.
# v2: re.error: unbalanced parenthesis. Fix: Corrected regex for strip_ansi_codes.
# v3: re.error: unbalanced parenthesis. Fix: Corrected regex for is_noise.
# v4: SyntaxError: unterminated string literal. Fix: Escaped special characters in is_noise.
# v5: SyntaxError: (unicode error). Fix: Properly escaped backslashes in JSON summary.
# v6: SyntaxError: unterminated triple-quoted string literal. Fix: Simplified learning summary to single-line comments.
# v7: re.error: unbalanced parenthesis. Fix: Correctly escaped parentheses in is_noise.
# v8: re.error: unterminated character set. Fix: Simplified strip_ansi_codes regex.
# v9: re.error: unterminated character set. Fix: Removed regex for braille characters and will check for them directly.
# v10: re.error: unbalanced parenthesis. Fix: Simplified is_noise and strip_ansi_codes.

import re
import json
import sys
import os
import shutil

def strip_ansi_codes(line):
    """Removes ANSI escape codes from a string."""
    return re.sub(r'\x1b\[[0-9;]*[mK]', '', line)

def is_noise(line):
    """Checks if a line is considered noise and should be filtered out."""
    # Common noise patterns observed in the logs
    noise_patterns = [
        r"Script started on",
        r"Loaded cached credentials.",
        r"Tips for getting started:",
        r"Ask questions, edit files, or run commands.",
        r"Be specific for the best results.",
        r"/help for more information.",
        r"Using: \d+ GEMINI.md files",
        r"Press 'i' for INSERT mode and 'Esc' for NORMAL mode.",
        r"Waiting for auth...",
        r"Summoning the code gremlins...",
        r"Acknowledging and Logging Updates",
        r"Analyzing Confidentiality Clauses",
        r"Concluding the Review",
        r"Dissecting the Copyright Details",
        r"Deconstructing the Contract",
        r"╭", r"─", r"╮", r"│", r"╰", # Box drawing characters
        r"\[NORMAL\]", r"\[INSERT\]", # Terminal prompts
        r"Error: \(none\)", # Corrected
        r"███", r"░░░", # ASCII art
        r"\(stage\*\)", # Corrected
        r"/docs\)", # Corrected
        r"left\)", # Corrected
        r"details\)", # Corrected
        r"Pre-heating the servers...", # Added: terminal status
        r"Checking for syntax errors in the universe...", # Added: terminal status
        r"Polishing the algorithms...", # Added: terminal status
        r"Garbage collecting...", # Added: terminal status
        r"Giving Cloudy a pat on the head...", # Added: terminal status
    ]
    for pattern in noise_patterns:
        if re.search(pattern, line):
            return True
    return False

def parse_chat_log(file_path):
    chat_turns = []
    current_user_input = []
    current_gemini_response = []
    
    # State: 0 = looking for user input, 1 = collecting user input, 2 = collecting gemini response
    state = 0 

    with open(file_path, 'r', errors='ignore') as f:
        for line in f:
            cleaned_line = strip_ansi_codes(line).strip()

            if not cleaned_line or is_noise(cleaned_line):
                continue

            # Check for user input pattern
            if re.match(r'^[| ]*> ', cleaned_line):
                # If we were collecting a Gemini response, save it
                if state == 2 and current_gemini_response:
                    chat_turns.append({
                        "user": "\n".join(current_user_input).strip(),
                        "gemini": "\n".join(current_gemini_response).strip()
                    })
                    current_user_input = []
                    current_gemini_response = []
                
                # Start collecting new user input
                current_user_input.append(re.sub(r'^[| ]*> ', '', cleaned_line))
                state = 1
            elif state == 1:
                # Continue collecting user input if the line is not empty and doesn't look like a response
                # This is a heuristic: if the line doesn't start with a common response indicator, assume it's part of multi-line user input
                if not re.match(r'^[a-zA-Z0-9]', cleaned_line) and not cleaned_line.startswith("```"):
                     current_user_input.append(cleaned_line)
                else:
                    # Transition to collecting Gemini response
                    state = 2
                    current_gemini_response.append(cleaned_line)
            elif state == 2:
                # Continue collecting Gemini response
                current_gemini_response.append(cleaned_line)
            else: # state == 0, initial state, looking for first user input
                # If we encounter content before the first user input, treat it as part of the first Gemini response
                # This handles cases where Gemini might start the conversation or there's initial output
                current_gemini_response.append(cleaned_line)
                state = 2 # Transition to collecting Gemini response

    # Add any remaining turn after the loop
    if current_user_input or current_gemini_response:
        chat_turns.append({
            "user": "\n".join(current_user_input).strip(),
            "gemini": "\n".join(current_gemini_response).strip()
        })

    return chat_turns

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_chat_log.py <path_to_chat_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    parsed_data = parse_chat_log(file_path)

    # Create the cleaned_logs directory if it doesn't exist
    cleaned_dir = os.path.join(os.path.dirname(file_path), "cleaned_logs")
    os.makedirs(cleaned_dir, exist_ok=True)

    # Create the new filename in the cleaned_logs directory
    base_name = os.path.basename(file_path)
    new_file_name = base_name.replace('.txt', '_clean.txt')
    new_file_path = os.path.join(cleaned_dir, new_file_name)

    with open(new_file_path, 'w') as f:
        for turn in parsed_data:
            f.write(f"User: {turn['user']}\n\n")
            f.write(f"Gemini: {turn['gemini']}\n\n")

    print(f"Cleaned chat log saved to: {new_file_path}")
    # Move the original file to the cleaned_logs directory
    try:
        shutil.move(file_path, cleaned_dir)
        print(f"Original log file moved to: {os.path.join(cleaned_dir, os.path.basename(file_path))}")
    except Exception as e:
        print(f"Error moving original file {file_path}: {e}")