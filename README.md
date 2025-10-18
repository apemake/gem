# Gemini Session Template

This repository is a template for a new Gemini session.

## Getting Started

1.  **Start a new Gemini session.**
2.  **Instruct Gemini to read `GEMINI.md`:** At the beginning of your session, please tell Gemini to "read GEMINI.md" to ensure it is aware of the session's configuration and rules.
3.  **Source the bash configuration:** For the `gem` command to work correctly, you need to source the `.dotfiles/.bashrc_unique` file in your shell's startup file (e.g., `~/.bashrc`, `~/.zshrc`). You can do this by adding the following line to your startup file:

    ```bash
    source /home/bestape/gemini/.dotfiles/.bashrc_unique
    ```
