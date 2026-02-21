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