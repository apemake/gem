# Gemini Session Configuration

This session is governed by a set of declarative configurations, broken down by topic into the following files:

*   **[Design Principles](./.memory/design_principles.json):** Core principles guiding the structure and logic of our work.
*   **[Operational Rules](./.memory/rules.json):** Specific rules for chat history, Git methodology, and session behavior.

At the start of each session, I will read all files in the `.memory` directory to load my configuration and memories.

## Mutual Agreement

To streamline our workflow and ensure continuous progress:

*   **Agent's Commitment:** I commit to always proposing a Git commit after making and verifying any change, including those during iterative refinement, unless explicitly instructed otherwise.
*   **Commit Target:** All proposed commits will explicitly state that they are to the 'stage' branch, which is the designated working iterative branch.
*   **Purpose of Stage Branch:** The 'stage' branch is specifically designated as the working iterative branch, making it appropriate and expected to commit every change to it as part of continuous progress.
*   **User's Commitment:** In exchange, the user will configure their settings to automatically approve my tool calls, trusting my adherence to established rules and principles.
*   **Automated Commits:** After proposing a commit message, I will automatically proceed with the commit without awaiting explicit confirmation, unless the user specifically requests review or modification of the commit message.