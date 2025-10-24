import re
import json
import sys

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
        r"\\[NORMAL\\]", r"\\[INSERT\\]", # Terminal prompts
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
        print("Usage: python parse_chat_log.py <path_to_chat_file>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    parsed_data = parse_chat_log(file_path)

    for turn in parsed_data:
        print(f"User: {turn['user']}\n")
        print(f"Gemini: {turn['gemini']}\n")
