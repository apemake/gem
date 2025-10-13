# {
#   "script_description": "A shell function to initialize and manage a Gemini session within a screen environment, with logging.",
#   "function_name": "gem",
#   "arguments": [
#     {
#       "name": "FOLDER_NAME",
#       "type": "string",
#       "optional": true,
#       "description": "The target directory for the Gemini session. If provided, the script will go to this folder or create it if it doesn't exist."
#     }
#   ],
#   "behavior": [
#     {
#       "step": 1,
#       "action": "Directory Handling",
#       "details": [
#         {
#           "condition": "A <FOLDER_NAME> is provided (e.g., 'gem my_project').",
#           "task": "Navigate to the specified <FOLDER_NAME>. If the folder does not exist, it should be created first."
#         },
#         {
#           "condition": "No <FOLDER_NAME> is provided (e.g., 'gem').",
#           "task": "Navigate to the '$HOME/gemini' directory."
#         }
#       ]
#     },
#     {
#       "step": 2,
#       "action": "Screen Session Setup",
#       "details": [
#         {
#           "task": "Create a new 'screen' environment using the machine's default settings, as written by Balaji."
#         },
#         {
#           "task": "Rename the first tab (window) within the screen session to 'gemini'."
#         }
#       ]
#     },
#     {
#       "step": 3,
#       "action": "Gemini Instance and Logging",
#       "details": [
#         {
#           "task": "Inside the screen session, start a 'gemini' instance."
#         },
#         {
#           "task": "Use the 'script' command to capture the standard output of the 'gemini' instance."
#         },
#         {
#           "task": "The output should be saved to a log file with a specific path and name.",
#           "log_file_path": "<TARGET_FOLDER>/.chat/<TIMESTAMP>_gemini_chat.txt",
#           "notes": [
#             "<TARGET_FOLDER> is either the provided <FOLDER_NAME> or '$HOME/gemini'.",
#             "<TIMESTAMP> should be a timestamp in the format YYYYMMDD-HHMMSS."
#           ]
#         }
#       ]
#     }
#   ]
# }
gem() {
    # Check for required commands
    if ! command -v screen &> /dev/null; then
        echo "Error: 'screen' command not found. Please install it to use this function." >&2
        return 1
    fi

    if ! command -v gemini &> /dev/null; then
        echo "Error: 'gemini' command not found. Please ensure it is installed and in your PATH." >&2
        return 1
    fi

    # Ref: behavior.step[2].action - Screen Session Setup
    # Define the name of the screen session.
    local SESSION_NAME="gem"

    # Check if a screen session with the specified name already exists.
    if screen -ls | grep -q ".${SESSION_NAME}[[:space:]]"; then
        # If the session exists, reattach to it.
        screen -d -r "${SESSION_NAME}"
    else
        # If the session does not exist, create a new one.

        # Ref: behavior.step[1].action - Directory Handling
        local TARGET_DIR
        if [ -n "$1" ]; then
            # Ref: arguments[0] - FOLDER_NAME
            # If an argument is provided, use it as the target directory.
            TARGET_DIR="$1"
            # Create the directory if it doesn't exist.
            if [ ! -d "$TARGET_DIR" ]; then
                mkdir -p "$TARGET_DIR"
            fi
        else
            # If no argument is provided, use the gemini directory in the user's home directory.
            TARGET_DIR="$HOME/gemini"
            # Ensure the default directory exists.
            if [ ! -d "$TARGET_DIR" ]; then
                mkdir -p "$TARGET_DIR"
            fi
        fi

        # Get the absolute path of the target directory.
        local ABS_TARGET_DIR
        ABS_TARGET_DIR=$(cd "${TARGET_DIR}" && pwd)

        # Ref: behavior.step[3].action - Gemini Instance and Logging
        # Create the .chat directory for logs.
        mkdir -p "${ABS_TARGET_DIR}/.chat"

        # Generate a timestamp for the log file.
        local TIMESTAMP=$(date +%Y%m%d-%H%M%S)
        # Create a unique file name for the session log in the .chat directory.
        # Ref: behavior.step[3].details[2].log_file_path
        local FILE_NAME=".chat/${TIMESTAMP}_gemini_chat.txt"

        # Ref: behavior.step[2].action - Screen Session Setup
        # Construct the command to be executed inside the screen session.
        local SCREEN_COMMAND="cd '${ABS_TARGET_DIR}' && script -q -c gemini '${FILE_NAME}'"

        # Create a new screen session in detached mode.
        screen -d -m -S "${SESSION_NAME}"

        # Send the command to the new screen session.
        screen -S "${SESSION_NAME}" -p 0 -X stuff "${SCREEN_COMMAND}\n"

        # Rename the window title to "gemini".
        # Ref: behavior.step[2].details[1].task
        screen -S "${SESSION_NAME}" -p 0 -X title "gemini"

        # Create a new window with bash at index 1 and name it bash.
        screen -S "${SESSION_NAME}" -X screen -t bash 1

        # Select window 1 to be the active window.
        screen -S "${SESSION_NAME}" -X select 1

        # Reattach to the newly created session.
        screen -r "${SESSION_NAME}"
    fi
}
