**Role:** Act as a Senior Python Solutions Architect specializing in Terminal User Interfaces (TUIs).
**Goal:** Create a Python-based TUI application. The application will serve as a visual dashboard and controller for existing Command Line Interface (CLI) tools.
**The Stack:**
* Language: Python 3.10+
* Primary Framework: **Textual** (by Textualize)
* Subprocess Management: `asyncio`


**Core Features:**
1. **Command Palette:** A sidebar or menu allowing the user to select predefined system commands (e.g., "Check Disk Space", "Git Status", "Ping Server").
2. **Output Window:** A central pane that displays the `stdout` and `stderr` of the executed command in real-time.
3. **Non-Blocking Execution:** The UI must remain responsive (scrollable, clickable) while a long-running command (like a build process or network request) is executing.


**Please cover the following sections:**
1. **High-Level Architecture:**
* Explain how the "Main Event Loop" interacts with the "Worker" that runs the commands.
* Diagram the data flow: User Click -Async Worker -Capture Output -Update UI Widget.


2. **Configuration Schema:**
* Define a JSON or YAML structure where I can define my commands easily (e.g., Command Name, The actual shell command to run, and a description).


3. **Key Component Design:**
* **The Runner:** Provide a code snippet or logic explanation for using `asyncio.create_subprocess_shell` to capture output line-by-line so the UI updates live (streaming), rather than waiting for the command to finish.
* **The UI Layout:** Suggest a standard layout using Textual's CSS (e.g., Docked Sidebar on left, Scrollable Log view on right).


4. **Error Handling Strategy:**
* How do we handle if a command fails (non-zero exit code)?
* How do we display `stderr` vs `stdout` (maybe different colors)?

5. **Always use separation of concerns and SOLID software design principles**


