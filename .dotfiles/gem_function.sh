# {
#   "script_description": "A shell function to intelligently manage Gemini sessions within GNU screen.",
#   "function_name": "gem",
#   "version": "2.0",
#   "author": "bestape",
#   "behavior": {
#     "summary": "This function provides a single entry point (`gem`) to manage Gemini chat sessions. It automatically handles screen creation, reattachment, and window naming, while ensuring all interactions are logged.",
#     "scenarios": [
#       {
#         "context": "Running in a standard shell (not inside screen)",
#         "behavior": [
#           "If a screen session named 'gem' exists, it reattaches to it.",
#           "If no such session exists, it creates a new detached session named 'gem', starts a Gemini instance within it (logged by the `script` command), and then reattaches to the new session."
#         ]
#       },
#       {
#         "context": "Running inside a screen session",
#         "behavior": "It renames the current screen window to 'Gemini' and starts a new logged Gemini session in the same window."
#       }
#     ]
#   },
#   "dependencies": ["GNU Screen", "gemini"],
#   "arguments": {
#     "name": "COMMAND",
#     "type": "string",
#     "optional": true,
#     "description": "The command to pass to the gemini executable. All arguments are treated as the command."
#   }
# }
alias snakes="echo 'are in the grass'"

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
        local SESSION_NAME="gem"
        local project_root
        project_root=$(git rev-parse --show-toplevel)
        local target_directory="$project_root" # Default directory

        # Check if the first argument is a valid directory
        if [ -n "$1" ] && [ -d "$1" ]; then
            target_directory="$1"
            shift # Remove the directory argument from the query
            query="$@" # Update query with remaining arguments
        fi
    
        cd "$target_directory" || { echo "Error: Could not change to $target_directory" >&2; return 1; }

    # Create the .chat directory for logs if it doesn't exist.
    mkdir -p ".chat"
    mkdir -p ".chat/unclean"
    local TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    local FILE_NAME=".chat/unclean/${TIMESTAMP}_gemini_chat.txt"
    local SCRIPT_COMMAND="script -q -c \"gemini $query\" ${FILE_NAME}"

    if [ -n "$STY" ]; then
        # We are inside a screen session
        screen -X title "Gemini"
        eval "$SCRIPT_COMMAND"
    else
        # We are not in a screen session
        if screen -ls | grep -q ".${SESSION_NAME}[[:space:]]"; then
            # Session exists, reattach
            screen -d -r "${SESSION_NAME}"
        else
            # Session does not exist, create it
            screen -c "$project_root/.dotfiles/.screenrc" -dmS "${SESSION_NAME}"
            screen -S "${SESSION_NAME}" -p 1 -X title "Gemini"
            screen -S "${SESSION_NAME}" -p 1 -X stuff "${SCRIPT_COMMAND}\n"
            screen -r "${SESSION_NAME}"
        fi
    fi
}