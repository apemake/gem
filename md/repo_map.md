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