# Repository Map

This document outlines the tracked and untracked items at the root level of the `gemini/` repository, reflecting the state after the pre-release reorganization.

## Tracked at Root Level:

These files and directories contain content that is actively tracked by Git.

*   `.dotfiles/` (Directory)
*   `.gemini/` (Directory - **Note:** While the directory itself is ignored, some files *within* it, like `.secrets.baseline` and `settings.json`, are explicitly tracked.)
*   `.memory/` (Directory)
*   `md/` (Directory - Contains repository documentation and maps)
*   `scripts/` (Directory)
*   `GEMINI.md` (File)
*   `.gitignore` (File)
*   `package.json` (File)
*   `.pre-commit-config.yaml` (File)
*   `README.md` (File)
*   `requirements.txt` (File)

## Not Tracked at Root Level:

These are files and directories that exist in the local project but are not committed to the repository.

### Ignored by `.gitignore`:
These items are explicitly ignored by rules in the `.gitignore` file.

*   `.chat/` (Directory for session logs)
*   `repos/` (Directory for other repositories)
*   `.venv/` (Directory for Python virtual environment)
*   `.venv_precommit/` (Directory for pre-commit hooks' environment)

---

## Detailed File Manifest

This manifest provides a detailed explanation for every file tracked in the repository, clarifying its purpose and justifying its inclusion in this public boilerplate.

### Core Configuration & Documentation

-   **`README.md`**: The primary entry point for new users. It explains the purpose of the repository, how to install and configure the `gem` command, and provides a high-level overview of the key concepts. It is essential for making the project understandable and usable.
-   **`GEMINI.md`**: The core instruction set for the AI agent at the start of each session. It defines the initialization tasks and mutual agreements between the user and the agent, ensuring a consistent and predictable startup sequence. This is the agent's primary "mission briefing".
-   **`.gitignore`**: A critical file that defines which files and directories should be ignored by Git. It is configured to ignore local development environments, session-specific logs, and other repositories, which is essential for keeping the public boilerplate clean and free of user-specific data.
-   **`package.json`**: Defines Node.js project metadata and dependencies. It is included to support potential future web-based or Node.js extensions of the agent's capabilities or for providing a UI.
-   **`requirements.txt`**: Lists the Python dependencies required by the various scripts in the `scripts/` directory. It is essential for ensuring that the agent's tools and helper scripts run correctly in a reproducible environment.
-   **`.pre-commit-config.yaml`**: The configuration file for the `pre-commit` framework. It sets up the automatic secret scanning (`detect-secrets`) that runs before each commit, acting as a critical security guardrail for the repository.

### Agent Memory (`.memory/`)

This directory is the agent's long-term memory and personality. Each file defines a core aspect of the agent's behavior, making the agent's logic transparent and configurable.

-   **`.memory/design_principles.json`**: The agent's core ethical and operational philosophy. It defines concepts like "Boomerang Feedback" and virtues like "Efficiency" and "Integrity". This file is the agent's conscience and the foundation of its collaborative personality.
-   **`.memory/rules.json`**: Defines the agent's specific, low-level operational rules for command interpretation, file handling, and other procedural tasks. It acts as the agent's "Standard Operating Procedures".
-   **`.memory/git_workflow.json`**: The agent's understanding of Git. It defines the rules for creating commits, managing branches, and interacting with the repository, ensuring a consistent and safe Git history.
-   **`.memory/mcp.json`, `.memory/parsing_config.json`, `.memory/session_tricks.json`**: These files contain configurations for command aliases, parsing logic, and other learned "tricks", allowing the agent's capabilities to be extended without changing its core code.
-   **`.memory/swarm_protocol.json`, `.memory/job_takeover_protocol.json`**: These define the rules for inter-agent communication and collaboration, allowing multiple agents to work together effectively within a "swarm".
-   **`...` (and all other `.memory/` files)**: Each file similarly holds a piece of the agent's core identity, from error handling protocols to project structure knowledge. They are all essential for the agent's function and a key feature of this boilerplate.

### Dotfiles (`.dotfiles/`)

This directory contains the shell configurations that make the `gem` command and its environment work.

-   **`.dotfiles/gem_function.sh`**: The heart of the boilerplate's functionality. It defines the `gem` shell function, which intelligently manages Gemini sessions within GNU Screen, handles logging, and provides a seamless user experience.
-   **`.dotfiles/.bashrc_unique`**: The shell script that is sourced by the user's personal `.bashrc`. Its job is to load the `gem` function into the user's environment.
-   **`.dotfiles/.screenrc`**: A pre-configured setup file for GNU Screen, ensuring that when the `gem` command creates a screen session, it has a consistent and user-friendly appearance and behavior.

### Agent-Specific Settings (`.gemini/`)

This directory is mostly ignored, but contains specific boilerplate settings.

-   **`.gemini/.secrets.baseline`**: A configuration file for the `detect-secrets` tool. It is **not** a file of secrets, but an "allow-list" of false positives. Including it ensures new users don't have their commits blocked by harmless code in the boilerplate that happens to look like a secret.
-   **`.gemini/settings.json`**: A default settings file for the Gemini CLI, providing a good starting configuration for UI preferences and tool behavior.

### Scripts (`scripts/`)

This directory contains Python and shell scripts that extend the agent's capabilities, allowing it to perform complex, repeatable tasks.

-   **`scripts/py/send_swarm_message.py`, `scripts/py/read_swarm_messages.py`**: A pair of scripts that form the basis of the inter-agent communication system, allowing agents to send and receive structured messages.
-   **`scripts/py/*_chat_logs.py`, `scripts/py/*_summaries.py`**: A suite of tools for processing and summarizing chat logs, essential for the agent's long-term memory and context retention.
-   **`...` (and all other `scripts/` files)**: Each script provides a discrete, useful function that the agent can call upon, from validating project structure to showing recent chats. They are the agent's toolset.

### Documentation (`md/`)

This directory holds all human-readable documentation for the repository.

-   **`md/repo_map.md`**: This very file. It provides a map of the repository's structure and a manifest of its contents, serving as a key for understanding the project.
-   **`md/safe_public_commits_report.md`**: Essential documentation that explains the repository's built-in secret-scanning security features to the user.
-   **`md/tree_liturgy.md`**: A "lore" document that explains the philosophical purpose of the `.memory/` files, giving the boilerplate a unique and memorable character.
