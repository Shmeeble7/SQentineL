
window.onload = function () {
    for (const [key, value] of Object.entries(localStorage)) {
        for (const [result_key, result_value] of Object.entries(JSON.parse(localStorage.getItem(key)))) {
            const contentElement = document.getElementById(result_key);
            if (contentElement != null) {
                contentElement.innerHTML = result_value;
            }
        }
    }
};

