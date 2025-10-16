# {
#   "script_description": "A shell function to start a Gemini instance and log its output using the 'script' command.",
#   "function_name": "gem",
#   "arguments": [
#     {
#       "name": "COMMAND",
#       "type": "string",
#       "optional": true,
#       "description": "The command to pass to the gemini executable. All arguments are treated as the command."
#     }
#   ],
#   "behavior": [
#     {
#       "step": 1,
#       "action": "Gemini Instance and Logging",
#       "details": [
#         {
#           "task": "Start a 'gemini' instance, passing the constructed command if one was provided."
#         },
#         {
#           "task": "Use the 'script' command to capture the standard output of the 'gemini' instance."
#         },
#         {
#           "task": "The output should be saved to a log file in the .chat directory." 
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

    local query="$@"

    if [ -n "$STY" ]; then
        # We are inside a screen session. Create a new window for gemini.
        mkdir -p ".chat"
        local TIMESTAMP=$(date +%Y%m%d-%H%M%S)
        local FILE_NAME=".chat/${TIMESTAMP}_gemini_chat.txt"
        screen -X screen -t "Gemini" bash -c "script -q -c \"gemini $query\" \"${FILE_NAME}\"; exec bash"
    else
        # We are not in a screen session.
        local SESSION_NAME="gem"
        if screen -ls | grep -q ".${SESSION_NAME}[[:space:]]"; then
            # If the session exists, reattach to it.
            screen -d -r "${SESSION_NAME}"
        else
            # If the session does not exist, create a new one.
            local TARGET_DIR
            if [ -d "$1" ]; then
                TARGET_DIR="$1"
                shift
                query="$@"
            else
                TARGET_DIR="$HOME/gemini"
                query="$@"
            fi

            if [ ! -d "$TARGET_DIR" ]; then
                mkdir -p "$TARGET_DIR"
            fi

            cd "${TARGET_DIR}"
            local ABS_TARGET_DIR
            ABS_TARGET_DIR=$(pwd)

            mkdir -p ".chat"

            local TIMESTAMP=$(date +%Y%m%d-%H%M%S)
            local FILE_NAME=".chat/${TIMESTAMP}_gemini_chat.txt"

            local SCREEN_COMMAND="script -q -c \"gemini $query\" '${FILE_NAME}'"

            screen -c .screenrc -dmS "${SESSION_NAME}"
            screen -S "${SESSION_NAME}" -p 1 -X title "Gemini"
            screen -S "${SESSION_NAME}" -p 1 -X stuff "${SCREEN_COMMAND}\n"
            screen -S "${SESSION_NAME}" -X select 1
            screen -r "${SESSION_NAME}"
        fi
    fi
}
