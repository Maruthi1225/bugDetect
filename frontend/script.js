document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const output = document.getElementById("output");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Show loading indicator and hide previous results
        loading.style.display = "block";
        result.style.display = "none";
        output.innerHTML = "";

        const file = fileInput.files[0];
        if (!file) {
            alert("Please select a file to upload.");
            loading.style.display = "none";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            // Call Python backend at localhost:5000/api/analyze
            const response = await fetch("http://localhost:5000/api/analyze", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.json();
            
            // Display formatted JSON with syntax highlighting
            output.innerHTML = formatJSON(data);

        } catch (error) {
            output.innerHTML = "🚨 Error analyzing the code. Please try again!";
            console.error("Error:", error);
        } finally {
            loading.style.display = "none";
            result.style.display = "block";
        }
    });

    // Helper function to format and highlight JSON
    function formatJSON(json) {
        if (typeof json !== "object") {
            json = JSON.parse(json);
        }
        return `<pre class="json-output">${syntaxHighlight(JSON.stringify(json, null, 2))}</pre>`;
    }

    // Syntax highlighting for JSON output
    function syntaxHighlight(json) {
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g, function (match) {
            let cls = "number";
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = "key";
                } else {
                    cls = "string";
                }
            } else if (/true|false/.test(match)) {
                cls = "boolean";
            } else if (/null/.test(match)) {
                cls = "null";
            }
            return `<span class="${cls}">${match}</span>`;
        });
    }
});
