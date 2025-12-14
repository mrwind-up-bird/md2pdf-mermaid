# MD2PDF-Mermaid Demo Script

## Setup
- **Open VS Code** with the file `examples/1_features_overview.md` active.
- **Open Terminal** (integrated in VS Code or separate) at the project root.
- **Open PDF Viewer** (Preview or Adobe) ready to open the output file.

## Scene 1: The Input (VS Code)
**Goal:** Show that it's just standard Markdown.
1.  **Scroll through the file**:
    *   Highlight the **Basic Syntax** (Headers, bold).
    *   Pause at **Nested Lists** (mention this is a key feature).
    *   Show the **Emoji** (🚀, 📈).
    *   **Crucial**: Stop at the **Mermaid Block**. Show how simple the code is (`graph LR...`).

## Scene 2: The Conversion (Terminal)
**Goal:** Show simplicity and speed.
1.  Type the command clearly:
    ```bash
    md2pdf examples/1_features_overview.md -o demo.pdf
    ```
2.  (Optional) Show off the help menu first to imply power:
    ```bash
    md2pdf --help
    ```
3.  Run the conversion command. Point out the log output:
    *   *"Using HTML/Chromium engine"* (shows modern tech).
    *   *"PDF created"* (shows success).

## Scene 3: The Result (PDF)
**Goal:** "Wow" factor.
1.  Open `demo.pdf`.
2.  **Zoom in** on the text to show it's vector/crisp (not a screenshot).
3.  **Scroll to the Mermaid Diagram**:
    *   Emphasize the high quality/resolution.
    *   Note that the layout matches what you defined in code.
4.  **Show the Nested List**: Verify the indentation is perfect.

## Bonus Round (Optional)
If you have time, quickly run the **Roadmap** example to show a different use case:
```bash
md2pdf examples/2_project_roadmap.md -o roadmap.pdf
```
*   Opening this shows a professional Gantt chart, great for "Manager" appeal.
