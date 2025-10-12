# Gemini Session Configuration

This session is governed by a set of declarative configurations, broken down by topic into the following files:

*   **[Design Principles](./.gemini/design_principles.json):** Core principles guiding the structure and logic of our work.
*   **[Operational Rules](./.gemini/rules.json):** Specific rules for chat history, Git methodology, and session behavior.

## Mutual Agreement

To streamline our workflow and ensure continuous progress:

*   **Agent's Commitment:** I commit to always proposing a Git commit after making and verifying any change, including those during iterative refinement, unless explicitly instructed otherwise.
*   **Commit Target:** All proposed commits will explicitly state that they are to the 'stage' branch, which is the designated working iterative branch.
*   **User's Commitment:** In exchange, the user will configure their settings to automatically approve my tool calls, trusting my adherence to established rules and principles.
*   **Memory Integration:** Upon startup, if not already established in user memory, I will prompt the user to execute the following command to save the fact: `save_memory(fact="I will always commit whenever I modify a file.")`
