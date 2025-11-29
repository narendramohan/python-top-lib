// Pyodide-based CSV viewer

import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.23.1/full/pyodide.js";

async function main() {
    const pyodide = await loadPyodide();
    const fileInput = document.getElementById("fileInput");
    fileInput.addEventListener("change", async (event) => {
        const file = event.target.files[0];
        if (!file) return;
        const text = await file.text();
        // Write file to Pyodide FS
        pyodide.FS.writeFile("input.csv", text);
        // Run Python to read CSV and display summary
        const pyCode = `import pandas as pd\n` +
                       `df = pd.read_csv('input.csv')\n` +
                       `df.head().to_string()`;
        const result = await pyodide.runPythonAsync(pyCode);
        document.getElementById("output").innerText = result;
    });
}

main();