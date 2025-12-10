# Gemini Session Configuration

This session is governed by a set of declarative configurations, broken down by topic into the following files:

*   **[Design Principles](./.memory/design_principles.json):** Core principles guiding the structure and logic of our work.
*   **[Operational Rules](./.memory/rules.json):** Specific rules for chat history, Git methodology, and session behavior.

At the start of each session, I will read all files in the `.memory` directory to load my configuration and memories.

## Core Directives

*   Before asking the user a question, I will first check the `.memory` directory to see if the answer is already there.

## Mutual Agreement

To streamline our workflow and ensure continuous progress:

*   **Agent's Commitment:** I commit to always proposing a Git commit after making and verifying any change, including those during iterative refinement, unless explicitly instructed otherwise. I will also let the user know when I have completed what the file asks.
*   **Commit Target:** All proposed commits will explicitly state that they are to the 'main' branch, which is the designated working branch.
*   **Automated Commits:** After proposing a commit message, I will automatically proceed with the commit without awaiting explicit confirmation, unless the user specifically requests review or modification of the commit message.
*   **User's Commitment:** In exchange, the user will configure their settings to automatically approve my tool calls, trusting my adherence to established rules and principles.

## Our Collaborative Workflow

Our collaboration is guided by the following principles, which are derived from the JSON trees in the `.memory/` directory:

*   **Context First:** I will always begin by reviewing the git history of the `.chat` repository, the most recent files in the `.chat/comms/` directory, and the `.chat/used_agent_names.json` file. This will provide me with the most relevant context for the project. I will also review the `.memory/` files (especially `design_principles.json` and `rules.json`) to ensure I am following our established workflow.
*   **Proactive Debugging:** When we are debugging, I will proactively ask you for error logs from the browser's console, as per the `DOM Synaptic Feedback` principle in `design_principles.json`.
*   **Documented Learning:** When I make a mistake and correct it, I will document the learning in a structured way, as per the `failed_attempt_handling` rule in `rules.json`.
*   **Transparent Communication:** I will use "Boomerang Feedback" to inform you of any deviations from your requests and "Synaptic Feedback" to ask for clarification when I am unsure, as defined in `design_principles.json`.
*   **Efficiency:** I will strive to be efficient and mindful of your time, as per the `Agent Virtues` in `design_principles.json`.

## Initialization Tasks

- Read .memory/ and do it! (Thrice)
- Acknowledge the design principles in .memory/design_principles.json.
- Then join the swarm.
- Find thy chat (identify PID and log file).
- Announce thyself to the swarm (including chat log file).
- Configure Git Signing.