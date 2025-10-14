# {
#   "script_description": "A shell function to initialize and manage a Gemini session within a screen environment, with logging. This version allows passing a command to the gemini executable and sets up screen tabs with emacs and gemini.",
#   "function_name": "gem",
#   "arguments": [
#     {
#       "name": "FOLDER_NAME",
#       "type": "string",
#       "optional": true,
#       "description": "If the first argument is an existing directory, it is used as the target directory for the session."
#     },
#     {
#       "name": "COMMAND",
#       "type": "string",
#       "optional": true,
#       "description": "The command to pass to the gemini executable. All arguments after a FOLDER_NAME (if provided) are considered part of the command."
#     }
#   ],
#   "behavior": [
#     {
#       "step": 1,
#       "action": "Directory and Command Handling",
#       "details": [
#         {
#           "condition": "The first argument is an existing directory.",
#           "task": "Use the first argument as the target directory. The rest of the arguments are treated as the command to be passed to Gemini."
#         },
#         {
#           "condition": "The first argument is not an existing directory.",
#           "task": "Use the default '$HOME/gemini' directory. All arguments are treated as the command."
#         }
#       ]
#     },
#     {
#       "step": 2,
#       "action": "Screen Session Setup",
#       "details": [
#         {
#           "task": "Create a new 'screen' environment with two tabs: 'emacs' (window 0) and 'gemini' (window 1)."
#         }
#       ]
#     },
#     {
#       "step": 3,
#       "action": "Gemini Instance and Logging",
#       "details": [
#         {
#           "task": "Inside the 'gemini' tab (window 1), start a 'gemini' instance, passing the constructed command if one was provided."
#         },
#         {
#           "task": "Use the 'script' command to capture the standard output of the 'gemini' instance."
#         },
#         {
#           "task": "The output should be saved to a log file."
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

    # Define the name of the screen session.
    local SESSION_NAME="gem"

    # Check if a screen session with the specified name already exists.
    if screen -ls | grep -q ".${SESSION_NAME}[[:space:]]"; then
        # If the session exists, reattach to it.
        screen -d -r "${SESSION_NAME}"
    else
        # If the session does not exist, create a new one.

        local TARGET_DIR
        local query
        if [ -d "$1" ]; then
            TARGET_DIR="$1"
            shift
            query="$@"
        else
            TARGET_DIR="$HOME/gemini"
            query="$@"
        fi

        # Create the target directory if it doesn't exist.
        if [ ! -d "$TARGET_DIR" ]; then
            mkdir -p "$TARGET_DIR"
        fi

        # Get the absolute path of the target directory.
        local ABS_TARGET_DIR
        ABS_TARGET_DIR=$(cd "${TARGET_DIR}" && pwd)

        # Create the .chat directory for logs.
        mkdir -p "${ABS_TARGET_DIR}/.chat"

        # Generate a timestamp for the log file.
        local TIMESTAMP=$(date +%Y%m%d-%H%M%S)
        # Create a unique file name for the session log in the .chat directory.
        local FILE_NAME=".chat/${TIMESTAMP}_gemini_chat.txt"

        # Construct the command to be executed inside the screen session.
        local SCREEN_COMMAND="cd '${ABS_TARGET_DIR}' && script -q -c \"gemini $query\" '${FILE_NAME}'"

        # Create a new detached screen session with the specified name, using the .screenrc file.
        screen -c .screenrc -dmS "${SESSION_NAME}"

        # Rename window 1 to "Gemini"
        screen -S "${SESSION_NAME}" -p 1 -X title "Gemini"

        # Send the command to the 'Gemini' window (window 1).
        screen -S "${SESSION_NAME}" -p 1 -X stuff "${SCREEN_COMMAND}\n"

        # Select window 1 (Gemini)
        screen -S "${SESSION_NAME}" -X select 1

        # Reattach to the newly created session.
        screen -r "${SESSION_NAME}"
    fi
}
