function displayResults(results, resultContainer) {
    resultContainer.textContent = results;
}

processButton.addEventListener("click", function () {
    const fileInput = document.getElementById("fastaFile");
    const resultContainer = document.getElementById("resultContainer");

    const selectedFile = fileInput.files[0];

    if (selectedFile) {
        const reader = new FileReader();

        reader.onload = function (event) {
            const fileContent = event.target.result;

            const entryIds = parseFastaFile(fileContent);

            sendEntryIdsToBackend(entryIds, resultContainer);
        };

        reader.readAsText(selectedFile);
    } else {
        resultContainer.textContent = "Please select a file.";
    }
});

function parseFastaFile(fileContent) {
    const lines = fileContent.split("\n");
    const entryIds = [];

    let currentEntryId = null;
    for (const line of lines) {
        if (line.startsWith(">")) {
            currentEntryId = line.substring(1).trim();
            entryIds.push(currentEntryId);
        }
    }

    return entryIds;
}

function sendEntryIdsToBackend(entryIds, resultContainer) {
    fetch("/classify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ entryIds }),
    })
        .then(response => response.json())
        .then(data => {
            displayResults(data.results, resultContainer);
        })
        .catch(error => {
            console.error("Error sending data to backend:", error);
        });
}
