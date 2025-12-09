### Report on `GEMINIGlobal.md` Integration

My goal was to integrate the key operational rules and principles from `GEMINIGlobal.md` into the agent's memory. Here’s a breakdown of the changes I made:

**1. `rules.json`**

*   **`git_methodology`:**
    *   I added a rule to clarify that the "always commit" policy does not apply to files in `.gitignore`d directories like `.chat/`.
    *   I added a rule to ensure the `.gemini/` directory is included in the top-level `.gitignore`.
*   **`code_generation_policy`:**
    *   I added a rule to make temporary scripts permanent and commit them.
    *   I added a rule to be cautious when adding headers to HTML files to avoid breaking the structure.
*   **`session_behavior`:**
    *   I added a reminder to be in the `gemini/` folder before starting a session.
    *   I added a rule for regular review of `design_principles.json`.

**2. `design_principles.json`**

*   **`agent_virtues`:**
    *   I added a "Humility and Review" virtue to emphasize reviewing my understanding with you.
*   **`Synaptic Feedback`:**
    *   I updated this rule to include re-verifying facts when my memory is contradicted by your input.

**3. `startup_protocol.json`**

*   I added a step to explicitly state the completion of initial setup tasks from `GEMINI.md`.

**4. `swarm_protocol.json`**

*   I updated the "Agent Initialization - Justification" to require an explanation for my chosen name.
    *   I added a rule to prevent me from adopting the name "Gemini".
