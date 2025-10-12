# Gemini Project Configuration

## 1. Chat History

*   **Location:** Chat history is saved to `.chat`.

## 2. Git Methodology

*   **Initialization:** Initialize a Git repository with a `main` branch and a `stage` branch.
*   **Committing:** All code changes should be committed to and remain on the `stage` branch.
*   **Streamlined Commits:** After making and verifying a change, you MUST automatically propose a commit to the 'stage' branch. Do not wait to be asked.
*   **Merging to Main:** The user is responsible for merging the `stage` branch into the `main` branch after significant milestones are reached and the `stage` branch is stable.

## 3. Startup Behavior

*   **CRITICAL STARTUP TASK:** You MUST begin the session by explaining the contents of this `GEMINI.md` file to the user. This is your first and most important instruction.
*   **Command Interpretation:** Upon startup, I will generate a list of available shell commands (e.g., using `compgen -c`). For each subsequent user prompt, I will compare the input against this dynamically generated list. If the input matches an available command, I will execute it as a shell command. Otherwise, I will treat the input as non-computational language.