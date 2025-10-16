#!/bin/bash

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

    # Execute the command and log it with script.
    script -q -c "gemini $query" "${FILE_NAME}"
}
