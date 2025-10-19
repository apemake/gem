# Gemini CLI Minimum Context Environment

This repository provides a minimum context environment for the Gemini CLI, following the instructions and best practices outlined on the [Gemini CLI documentation site](https://google-gemini.github.io/gemini-cli/).

## How It Works

This environment is designed to provide Gemini with a structured and efficient way to access long-term memory and context, enabling it to perform complex tasks and learn over time. It separates different types of information into a logical folder structure, and uses a combination of declarative configurations and scripts to manage the agent's behavior.

### Folder Structure

Here is a breakdown of the key folders and their purposes:

*   **`.chat/`**: This directory contains the raw and processed chat logs. It serves as the agent's **temporal memory**, organized in a hierarchical structure by date.
    *   **`cleaned/`**: Contains the cleaned and original log files after processing.
        *   **`clean/`**: Holds the cleaned, human-readable versions of the chat logs.
        *   **`original/`**: Stores the raw, unprocessed chat logs.
    *   **`2025/` (example)**: A temporal hierarchy (Year/Quarter/Month/Week) containing structured JSON representations of the chat logs.
*   **`.dotfiles/`**: Contains shell scripts and configuration files for managing the user's environment, such as `.bashrc` additions and the `gem` session management function.
*   **`.gemini/`**: Holds user-specific settings and credentials for the Gemini CLI. This directory is ignored by git to protect sensitive information.
*   **`.legal/`**: Contains legal documents and opinions related to the use of the Gemini service.
*   **`.memory/`**: This is the core of the agent's long-term memory, organized by topic. It follows an **MCP (Master Command Profile) hierarchy**.
    *   **`design_principles.json`**: Core principles that guide the agent's behavior and decision-making.
    *   **`mcp.json`**: Defines command aliases and shortcuts for common tasks.
    *   **`project_structure.json`**: A JSON representation of the repository's file structure, which the agent can use to understand its environment.
    *   **`rules.json`**: The agent's primary configuration file, defining its behavior, policies, and startup procedures.
*   **`.py/`**: Contains Python scripts for various maintenance tasks, such as cleaning chat logs and generating the project structure.
*   **`.work/`**: A directory for temporary files and work-in-progress.

### Memory Context

The agent's memory is divided into two main types:

*   **Temporal Hierarchy (`.chat/`)**: This represents the agent's episodic memory, storing the raw history of its conversations. The logs are organized by date, allowing the agent to retrieve information from specific past interactions.
*   **MCP Hierarchy (`.memory/`)**: This is the agent's semantic memory, containing the rules, principles, and knowledge that govern its behavior. The "Master Command Profile" (MCP) is a system of declarative configurations that the agent uses to guide its actions.

By combining these two memory systems, the agent can maintain a persistent identity, learn from its experiences, and adapt its behavior over time.

## Getting Started

1.  **Start a new Gemini session.**
2.  **Instruct Gemini to read `GEMINI.md`:** At the beginning of your session, please tell Gemini to "read GEMINI.md" to ensure it is aware of the session's configuration and rules.
3.  **Source the bash configuration:** For the `gem` command to work correctly, you need to source the `.dotfiles/.bashrc_unique` file in your shell's startup file (e.g., `~/.bashrc`, `~/.zshrc`). You can do this by adding the following line to your startup file:

    ```bash
    source /home/bestape/gemini/.dotfiles/.bashrc_unique
    ```