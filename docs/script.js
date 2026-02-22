
const textarea = document.getElementById("messageBox");

textarea.addEventListener("input", () => {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
});



window.onload = function () {

    const fileInput = document.getElementById('fileInput');

    fileInput.addEventListener('change', (event) => {
        const fileList = event.target.files;

        const file = fileList[0];


        if (file) {
            const reader = new FileReader();

            reader.onload = async (e) => {
                const fileContent = e.target.result;
                const dataToSend = { "text": fileContent };
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
                        localStorage.setItem(key, JSON.stringify(data.results[x]))
                    }

                    window.location.href = "results.html";


                } catch (error) {
                    console.error("Error:", error);
                    window.alert("The backend is down!");
                }

            };
            reader.readAsText(file);
        }
    });

};



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
                localStorage.setItem(key, JSON.stringify(data.results[x]))
            }

            window.location.href = "results.html";


        } catch (error) {
            console.error("Error:", error);
            window.alert("The backend is down!");
        }
    }

    sendData();
}