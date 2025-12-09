## Filesystem Git Architecture

-   `gemini/` (Subject)
    -   `.chat/` (Subject)
    -   `repos/` (Object)
        -   `bestape/` (Object)
            -   `.0.sh` (Subject)
            -   `.0.sh-project` (Subject)
            -   `bestape` (Subject)
            -   `cheerbot.org` (Subject)
            -   `ERCs` (Subject)
            -   `heroku.node.js-urlForward` (Subject)
            -   `lexdao` (Subject)
            -   `LexDAO-Articles` (Subject)
            -   `neowise` (Subject)
            -   `openzeppelin-contracts` (Subject)
            -   `poignart` (Subject)
            -   `reviews` (Subject)
            -   `signature-economies` (Subject)
            -   `squareRootIntegers` (Subject)
        -   `cheerbotme/` (Object)
            -   `devconnect2025` (Subject)
            -   `ethglobalnyc2025` (Subject)
            -   `ethglobalnyc20252` (Subject)
            -   `jsonState` (Subject)
            -   `megazu` (Subject)
            -   `pixelart` (Subject)
            -   `webmonetization` (Subject)
        -   `diy-make/` (Object)
            -   `OSO_hack` (Subject)
            -   `portal` (Subject)
            -   `reality-merge` (Subject)
            -   `zui` (Subject)
        -   `forkfolk/` (Subject)
        -   `island_ventures/` (Object)
            -   `newsletters` (Subject)
            -   `research` (Subject)
        -   `ixventure/` (Object)
            -   `dom-jekyll` (Subject)
            -   `island_ventures` (Subject)
            -   `research` (Subject)
            -   `website` (Subject)
        -   `legal-engineering-standards-association/` (Object)
            -   `.github` (Subject)
            -   `agreements-data-standard` (Subject)
            -   `discussions` (Subject)
            -   `lesa.law-website` (Subject)
            -   `pm` (Subject)
            -   `signet-data-standard` (Subject)
        -   `lexclinic/` (Object)
            -   `.github` (Subject)
            -   `agreements-data-standard` (Subject)
            -   `discussions` (Subject)
            -   `docs` (Subject)
            -   `Grants` (Subject)
            -   `lesa.law-website` (Subject)
            -   `pm` (Subject)
            -   `research` (Subject)
            -   `signet-data-standard` (Subject)
            -   `Templates` (Subject)
        -   `local_only/` (Object)
            -   `bestape` (Subject)
            -   `cheerKernel` (Subject)
            -   `dapp` (Subject)
            -   `dapp2` (Subject)
            -   `folkProposals` (Subject)
            -   `kernel` (Subject)
            -   `map` (Subject)
            -   `publicResearch` (Subject)
            -   `Rational_Assembly_Grid_Series` (Subject)

---

## Passthrough Git Architecture

The proposed setup creates a "passthrough" or fractal Git architecture, where `gemini/repos/` and each of its subdirectories become individual Git repositories. Here's a breakdown of this design:

*   **Fractal Repositories:** This creates a hierarchy of nested Git repositories. Each directory manages its own "memory" (its Git history) and explicitly ignores the contents of its subdirectories via `.gitignore`. This means the parent repository only tracks the existence of its child directories, not their content, creating a fractal-like structure where each level is self-contained.
*   **Decentralized Memory:** The user's idea of "the .git and .gitignore combination is your memory system" is a powerful one. It establishes a decentralized memory model. Each `.git` directory is a memory container with its own history, and the corresponding `.gitignore` defines the boundaries of that memory, preventing memory "bleed" across different levels of the hierarchy.
*   **"Passthrough" Responsibility:** The term "passthrough" aptly describes how responsibility is delegated. The `gemini/repos/` repository doesn't manage the content of its children; it "passes through" that responsibility to the Git repository within each child directory. This allows for a clean separation of concerns and a highly scalable and modular system.

This architecture offers:

*   **Modularity:** Each repository is a self-contained unit that can be managed independently.
*   **Scalability:** The hierarchy makes it easier to manage a large and growing number of repositories.
*   **Fine-grained Control:** Each repository has its own commit history, allowing for granular tracking of changes at different levels of the project.

---

## Detailed File Manifest

This manifest provides a detailed, indexed explanation for every file tracked in the repository, clarifying its purpose and justifying its inclusion in this public boilerplate.

### Core Configuration & Documentation (6 files)

1.  **`README.md`**: The primary entry point for new users. It explains the purpose of the repository, how to install and configure the `gem` command via the `$GEMINI_ROOT` variable, and provides a high-level overview of the key concepts. It is essential for making the project understandable and usable.
2.  **`GEMINI.md`**: The core instruction set for the AI agent at the start of each session. It defines the initialization tasks and mutual agreements between the user and the agent, ensuring a consistent and predictable startup sequence. This is the agent's primary "mission briefing".
3.  **`.gitignore`**: A critical file that defines which files and directories should be ignored by Git. It is configured to ignore local development environments (`.venv/`), session-specific logs (`.chat/`), and other non-boilerplate content, which is essential for keeping the public repository clean. It also contains explicit exceptions for tracked boilerplate files within ignored directories.
4.  **`package.json`**: Defines Node.js project metadata and dependencies. It is included to support potential future web-based or Node.js extensions of the agent's capabilities or for providing an interactive UI.
5.  **`requirements.txt`**: Lists the Python dependencies required by the various helper scripts in the `scripts/` directory. It is essential for ensuring that the agent's tools and helper scripts run correctly in a reproducible `venv`.
6.  **`.pre-commit-config.yaml`**: The configuration file for the `pre-commit` framework. It sets up the `detect-secrets` tool to run automatically before each commit, acting as a critical security guardrail to prevent secrets from entering the Git history.

### Dotfiles (`.dotfiles/`, 3 files)

This directory contains the shell configurations that make the `gem` command and its environment work.

7.  **`.dotfiles/gem_function.sh`**: The heart of the boilerplate's functionality. It defines the `gem` shell function, which intelligently manages Gemini sessions within GNU Screen, handles logging, and provides a seamless user experience that works from any directory.
8.  **`.dotfiles/.bashrc_unique`**: The shell script that is sourced by the user's personal startup file (e.g., `.bashrc`). Its sole job is to load the `gem` function into the user's shell environment, making it a globally available command.
9.  **`.dotfiles/.screenrc`**: A pre-configured setup file for GNU Screen, ensuring that when the `gem` command creates a screen session, it has a consistent and user-friendly appearance and behavior, including the window title format.

### Agent-Specific Settings (`.gemini/`, 2 files)

This directory is mostly ignored, but contains specific boilerplate settings that should be version-controlled.

10. **`.gemini/.secrets.baseline`**: A configuration file for the `detect-secrets` tool. It is **not** a file of secrets, but an "allow-list" of false positives. Including it ensures new users don't have their commits blocked by harmless code in the boilerplate that happens to look like a secret.
11. **`.gemini/settings.json`**: A default settings file for the Gemini CLI, providing a good starting configuration for UI preferences (like `vimMode`) and tool behavior for any user cloning the repository.

### Public Documentation (`md/`, 3 files)

This directory holds all human-readable documentation for the repository.

12. **`md/repo_map.md`**: This very file. It provides a map of the repository's structure and this detailed manifest, serving as a key for understanding the project's architecture and the purpose of each component.
13. **`md/safe_public_commits_report.md`**: Essential security documentation that explains the repository's built-in secret-scanning features (`detect-secrets`, `pre-commit`) and general best practices for maintaining a secure public repository.
14. **`md/tree_liturgy.md`**: A "lore" document that poetically explains the philosophical purpose of the `.memory/` files, giving the boilerplate a unique and memorable character.

### Agent Memory (`.memory/`, 19 files)

This directory is the agent's long-term memory and personality. Each file defines a core aspect of the agent's behavior, making its logic transparent and configurable.

15. **`.memory/bot_crash_protocol.json`**: Defines how the agent should behave if it crashes or encounters a critical error, ensuring a graceful failure mode.
16. **`.memory/broken_instance_protocol.json`**: A specific protocol for when the agent detects it is in a "broken" state, guiding its self-diagnosis.
17. **`.memory/design_principles.json`**: The agent's core ethical and operational philosophy. It defines concepts like "Boomerang Feedback" and virtues like "Efficiency" and "Integrity".
18. **`.memory/fatal_error_protocol.json`**: A protocol for handling fatal, unrecoverable errors during a session.
19. **`.memory/file_architecture.json`**: Codifies the agent's understanding of how files should be structured within a project.
20. **`.memory/git_workflow.json`**: The agent's rulebook for Git, defining how to create commits, manage branches, and interact with the repository.
21. **`.memory/job_takeover_protocol.json`**: Defines how an agent should take over a job from another agent in the swarm.
22. **`.memory/mcp.json`**: "Master Control Program" file, used to define command aliases and shortcuts, making the agent more efficient.
23. **`.memory/parsing_config.json`**: Contains rules for how the agent should parse different types of structured and unstructured text.
24. **`.memory/personality.json`**: Defines core personality traits for the agent, such as the directive to "give more pushback".
25. **`.memory/process_improvements.json`**: A log where the agent records learnings from its own mistakes to improve its future performance.
26. **`.memory/programming_legalese_mcp.json`**: A specialized vocabulary or DSL for expressing complex programming concepts in a structured way.
27. **`.memory/project_structure.json`**: The agent's understanding of the expected directory structure for projects it works on.
28. **`.memory/rules.json`**: Defines the agent's specific, low-level operational rules for command interpretation and other procedural tasks.
29. **`.memory/session_tricks.json`**: A collection of learned "tricks" or clever solutions for recurring problems.
30. **`.memory/startup_protocol.json`**: A detailed checklist of actions the agent must perform upon startup, ensuring a consistent state.
31. **`.memory/summarization_template.json`**: A template that guides the agent on how to structure summaries of conversations or documents.
32. **`.memory/svg_learnings.json`**: A dedicated knowledge base for storing information and techniques related to handling SVG files.
33. **`.memory/swarm_protocol.json`**: Defines the rules for inter-agent communication, allowing multiple agents to collaborate as a "swarm".

### Helper Scripts (`scripts/`, 16 files)

This directory contains Python and shell scripts that extend the agent's capabilities, acting as its toolset.

34. **`scripts/py/clean_chat_logs.py`**: A tool to process raw chat logs and remove unwanted artifacts or noise.
35. **`scripts/py/create_higher_level_summaries.py`**: A script to synthesize multiple smaller summaries into larger, more abstract ones (e.g., daily to weekly).
36. **`scripts/py/estimate_chunks.py`**: A utility to estimate the size or token count of text chunks, useful for managing context windows.
37. **`scripts/py/generate_clean_project_structure.py`**: A tool to generate a project's directory structure in a clean, readable format.
38. **`scripts/py/parse_chat_log.py`**: A script to parse a raw chat log file into a structured data format.
39. **`scripts/py/read_swarm_messages.py`**: A tool to read and process messages from other agents in the swarm.
40. **`scripts/py/send_swarm_message.py`**: The counterpart to the read script; allows the agent to send structured messages to the swarm.
41. **`scripts/py/show_recent_chats.py`**: A utility to quickly display recent chat log files.
42. **`scripts/py/structure_chat_logs.py`**: A tool to organize and structure raw chat logs into a more usable format.
43. **`scripts/py/summarize_logs.py`**: A script that uses the agent's language model to create summaries of specified log files.
44. **`scripts/py/test_swarm_communication.py`**: A utility for debugging the swarm communication system.
45. **`scripts/py/validate_project_structure.py`**: A tool to check if a project's directory structure conforms to the rules in `.memory/project_structure.json`.
46. **`scripts/sh/run_monthly_summarization.sh`**: A shell script that likely orchestrates several Python scripts to perform a recurring monthly summarization task.
