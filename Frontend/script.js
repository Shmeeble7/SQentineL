document.getElementById("sendBtn").addEventListener("click", function () {
    const api_url = 'http://localhost:8000/api/data'; // Replace with your backend URL

    fetch(api_url)
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Update your UI with the data
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}