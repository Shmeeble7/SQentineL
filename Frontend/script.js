document.getElementById("sendBtn").addEventListener("click", function () {


    const api_url = 'http://localhost:8000/analyze';

    dataToSend = "Malicious SQL Query"

    fetch(api_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control': 'Allow-Origin'
        },
        body: JSON.stringify(dataToSend)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
})

const textarea = document.getElementById("messageBox");

textarea.addEventListener("input", () => {
    textarea.style.height = "auto";              // Reset height
    textarea.style.height = textarea.scrollHeight + "px";  // Expand to fit content
});

async function sendText() {
    const textValue = document.getElementById("sendBtn").value;

    const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: textValue
        })
    });

    const data = await response.json();
    console.log(data);
    alert(data.message);
}