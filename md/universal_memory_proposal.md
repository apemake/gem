## Proposal for Universal `.memory/` Package

I have analyzed the `.memory/` JSON files and I propose the following files to be included in the `.memory/` directory of every repository under `repos/`:

**1. `design_principles.json`:**

*   **Why:** This file contains the core principles that guide my behavior, such as my virtues (Integrity, Efficiency, etc.) and my architectural philosophy. These principles are fundamental to how I operate and should be present in every context to ensure consistent and reliable behavior.

**2. `rules.json` (a "lite" version):**

*   **Why:** This file contains specific operational rules. I propose to include a "lite" version that contains only the general-purpose rules, such as:
    *   `git_methodology`: The core rules for how I interact with Git.
    *   `code_generation_policy`: My rules for generating and commenting code.
    *   `session_behavior` (excluding startup tasks specific to the root repo).
*   **Exclusions:** I would exclude rules that are specific to the root `gemini` repository, such as the detailed `startup_protocol` and `swarm_protocol` references, which are more about the overall agent management than repository-specific tasks.

**3. `schema.json`:**

*   **Why:** This file defines the standard schema for all `.memory/` files. Including it in every `.memory/` directory will ensure that the memory system remains consistent and machine-readable across all repositories. It's the blueprint for my memory's structure.

**Summary of Proposal:**

I propose to include `design_principles.json`, a "lite" version of `rules.json`, and `schema.json` in every `.memory/` directory. This will provide each repository with a core set of principles, rules, and a schema for its memory, while allowing for repository-specific knowledge and rules to be added later.
