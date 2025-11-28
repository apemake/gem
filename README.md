# Gemini CLI Enhanced Environment

This repository provides an enhanced context environment for the Gemini CLI. It builds upon the foundation of the official [Gemini CLI](https://github.com/google-gemini/gemini-cli) to provide a more structured and persistent way for the agent to learn and evolve.

This environment is designed to be a starting point for users who want to have a more advanced and customized experience with the Gemini CLI.

## Prerequisites

Before you begin, ensure you have a working installation of the Gemini CLI. You can find the installation instructions on the [official Gemini CLI documentation site](https://google-gemini.github.io/gemini-cli/).

## Getting Started

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/diy-make/gemini.git
    cd gemini
    ```

2.  **Source the bash configuration:**
    For the `gem` command to work correctly, you need to source the `.dotfiles/.bashrc_unique` file in your shell's startup file (e.g., `~/.bashrc`, `~/.zshrc`). You can do this by adding the following line to your startup file:

    ```bash
    source /path/to/your/gemini/repo/.dotfiles/.bashrc_unique
    ```
    *Replace `/path/to/your/gemini/repo` with the actual path to the cloned repository.*

3.  **Start a new Gemini session:**
    ```bash
    gemini
    ```

4.  **Instruct the agent:**
    At the beginning of your session, please tell Gemini to:
    ```
    run README.md and do it
    ```
    This will instruct the agent to read the necessary configuration files and initialize itself for the session.

## How It Works

This environment provides Gemini with a structured way to access long-term memory and context, enabling it to perform complex tasks and learn over time.

### Key Concepts

*   **`.memory/` directory:** This is the core of the agent's long-term memory. It contains configuration files, rules, and design principles that govern the agent's behavior.
*   **`.chat/` directory:** This directory stores the raw and processed chat logs, serving as the agent's temporal memory.
*   **`GEMINI.md`:** This file contains the agent's core directives and initialization tasks for each session.
*   **`repos/` directory:** This directory is for your own projects and repositories. It is ignored by the top-level git repository, so you can manage your projects independently.

## Customization

This environment is designed to be customized. You can modify the files in the `.memory/` directory to change the agent's behavior, add new command aliases in `mcp.json`, or even create new scripts in the `scripts/` directory to extend the agent's capabilities.

---

## Gemini Agent Instructions

Gemini, at the beginning of each session, please run `GEMINI.md` and do it.
