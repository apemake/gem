# Gemini Project Configuration

## 1. Chat History

*   **Location:** Chat history is saved to `chat.txt` in the project root directory.

## 2. Git Methodology

*   **Initialization:** Initialize a Git repository with a `main` branch and a `stage` branch.
*   **Committing:** All code changes should be committed to and remain on the `stage` branch.
*   **Merging to Main:** The user is responsible for merging the `stage` branch into the `main` branch after significant milestones are reached and the `stage` branch is stable.

## 3. Startup Behavior

*   **Explanation:** Upon startup, explain the contents of this `GEMINI.md` file to the user.
*   **Command Interpretation:** Upon startup, I will generate a list of available shell commands (e.g., using `compgen -c`). For each subsequent user prompt, I will compare the input against this dynamically generated list. If the input matches an available command, I will execute it as a shell command. Otherwise, I will treat the input as a text message.