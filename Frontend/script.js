document.getElementById("sendBtn").addEventListener("click", function () {


    const api_url = 'http://localhost:8000/query';

    data = "Malicious SQL Query"

    fetch(api_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control': 'Allow-Origin'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
})