## Gemini Agent Instructions

Gemini, at the beginning of each session, please run `GEMINI.md` and do it.

When performing the tasks in `GEMINI.md`, you must follow the 'Boomerang Feedback' process (defined in `.memory/design_principles.json`), which means telling the user what is happening and asking for approval in an informed way at each step.

**Note to Agent:** After completing the `GEMINI.md` tasks, you may disregard the rest of this `README.md` file, as it is intended for human users or for the initial, one-time setup of the environment.
---
# Gemini CLI Enhanced Environment

This repository provides an enhanced context environment for the Gemini CLI. It builds upon the foundation of the official [Gemini CLI](https://github.com/google-gemini/gemini-cli) to provide a more structured and persistent way for the agent to learn and evolve.

This environment is designed to be a starting point for users who want to have a more advanced and customized experience with the Gemini CLI.

## Prerequisites

Before you begin, ensure you have the following installed and available in your system's PATH:

*   **`bash`**: The shell interpreter (standard on most Linux/macOS systems).
*   **`screen`**: For GNU Screen session management (e.g., `sudo apt install screen` on Debian/Ubuntu, `brew install screen` on macOS).
*   **`script`**: For GNU Script session logging (usually part of `util-linux` on Linux, or available by default on macOS).
*   **`gemini`**: The Gemini CLI executable itself. You can find installation instructions on the [official Gemini CLI documentation site](https://google-gemini.github.io/gemini-cli/).
*   **`git`**: For version control.
*   **`python3`**: For running Python helper scripts.

Once these system-level prerequisites are met, ensure you have a working installation of the Gemini CLI.

## Installation & Setup

This guide explains how to set up the `gem` command and its session management features so they can be used from anywhere in your system.

1.  **Clone this Repository:**
    If you haven't already, clone this repository to a permanent location on your local machine.
    ```bash
    git clone https://github.com/diy-make/gemini.git
    ```

2.  **Set the `$GEMINI_ROOT` Environment Variable:**
    Add the following line to your shell's startup file (e.g., `~/.bashrc`, `~/.zshrc`). This variable must point to the **absolute path** where you cloned the repository.

    *Replace `/path/to/your/gemini` with the actual path.*
    ```bash
    export GEMINI_ROOT="/path/to/your/gemini"
    ```

3.  **Install Dependencies:**
    The helper scripts in this repository require Python dependencies. It is highly recommended to use a virtual environment.
    ```bash
    # Navigate to your repository clone
    cd $GEMINI_ROOT

    # Create a virtual environment
    python3 -m venv .venv

    # Activate the virtual environment
    source .venv/bin/activate

    # Install the required packages
    pip install -r requirements.txt
    ```

4.  **Source the `bashrc_unique` File:**
    Immediately after the export line in your shell's startup file, add the following line to source the `gem` function into your shell environment:
    ```bash
    source "$GEMINI_ROOT/.dotfiles/.bashrc_unique"
    ```
    (These dotfiles are maintained at [https://github.com/bestape/.0.sh](https://github.com/bestape/.0.sh) and should be kept updated.)

5.  **Reload Your Shell:**
    To apply the changes, open a new terminal or run `source ~/.bashrc` (or your respective shell configuration file).

6.  **Start a Session:**
    You can now start a new Gemini session from any directory by simply running:
    ```bash
    gem
    ```

## How It Works

This environment provides Gemini with a structured way to access long-term memory and context, enabling it to perform complex tasks and learn over time.

### Key Concepts

*   **`.memory/` directory:** This is the core of the agent's long-term memory. It contains configuration files, rules, and design principles that govern the agent's behavior.
*   **`.chat/` directory:** This is a nested Git repository for storing and tracking all local chat logs. It is ignored by the main boilerplate repository, allowing users to maintain a private, version-controlled history of their sessions.
*   **`GEMINI.md`:** This file contains the agent's core directives and initialization tasks for each session.
*   **`repos/` directory:** This directory is for your own projects and repositories. It is ignored by the top-level git repository, so you can manage your projects independently.

## Customization

This environment is designed to be customized. You can modify the files in the `.memory/` directory to change the agent's behavior, add new command aliases in `mcp.json`, or even create new scripts in the `scripts/` directory to extend the agent's capabilities.
