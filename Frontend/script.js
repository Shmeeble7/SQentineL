

const textarea = document.getElementById("messageBox");

textarea.addEventListener("input", () => {
    textarea.style.height = "auto";              // Reset height
    textarea.style.height = textarea.scrollHeight + "px";  // Expand to fit content
});


function getResults() {
    for (const [key, value] of Object.entries(localStorage)) {
        for (const [result_key, result_value] of Object.entries(JSON.parse(localStorage.getItem(key)))) {
            console.log(`${result_key}: ${result_value}`);
        }
    }
}

async function sendText() {

    const dataToSend = {
        "text": textarea.value
    }

    async function sendData() {
        try {
            const response = await fetch("http://127.0.0.1:8000/analyze", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(dataToSend)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();

            console.log("Success:", data.results);

            for (let x = 0; x < data.results.length; x++) {
                let key = "results" + x;
                console.log(data.results[x])
                localStorage.setItem(key, JSON.stringify(data.results[x]))
            }

            getResults();

        } catch (error) {
            console.error("Error:", error);
        }
    }

    sendData();
}