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
    if ! command -v gemini &> /dev/null; then
        echo "Error: 'gemini' command not found. Please ensure it is installed and in your PATH." >&2
        return 1
    fi

    local query="$@"

    # Create the .chat directory for logs if it doesn't exist.
    mkdir -p ".chat"

    # Generate a timestamp for the log file.
    local TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    # Create a unique file name for the session log in the .chat directory.
    local FILE_NAME=".chat/${TIMESTAMP}_gemini_chat.txt"

    if [ -n "$STY" ]; then
        # We are inside a screen session. Create a new window.
        screen -X screen -t "Gemini" bash -c "script -q -c \"gemini $query\" \"${FILE_NAME}\"; exec bash"
    else
        # We are not in a screen session. Run in the current shell.
        script -q -c "gemini $query" "${FILE_NAME}"
    fi
}
