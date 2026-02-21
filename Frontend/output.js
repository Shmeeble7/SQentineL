

function addBox(key_num) {
    const container = document.getElementById('results');

    const key = "key-" + key_num;
    container.innerHTML += `<div class="d-flex info_div flex-column">
            <div class="info_div_header d-flex flex-row justify-content-center align-items-center">
                <h4 class="severity p-2"></h4>
                <button onclick="openInfo('` + key + `')" type="button" class="caret-down btn p-2" data-bs-toggle="modal" data-bs-target="#myModal">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="bi bi-caret-down" >
                        <path d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"/>
                    </svg>
                </button>
            </div>
            <div class="d-flex flex-column justify-content-center align-items-center">
                <div class=" ` + key + ` p-2 line">Line: </div>
                <div class=" ` + key + ` p-2 code_snippet">Code Snippet: </div>
            </div>
        </div>`;


    const divs = document.getElementsByClassName(key);

    for (let x = 0; x < divs.length; x++) {
        divs[x].style.display = "none";
    }

}

function openInfo(key) {
    console.log(key)
    const divs = document.getElementsByClassName(key);
    for (let x = 0; x < divs.length; x++) {
        divs[x].style.display = "block";
    }
}
const tags = ["line", "severity", "confidence", "title", "explanation", "danger", "fix", "example_paylod", "example_fix", "code_snippet"]
window.onload = function () {
    if (localStorage.length == 0) {
        const info_divs = this.document.getElementsByClassName("info_div");
        for (let x = 0; x < info_divs.length; x++) {
            info_divs[x].style.display = "none";
        }

        const safe_div = this.document.getElementById("safe_div");
        safe_div.style.display = "block";

    }
    else {

        for (let x = 0; x < localStorage.length; x++) {
            addBox(x)
        }

        let iter = 0;
        for (const [key, value] of Object.entries(localStorage)) {
            for (const [result_key, result_value] of Object.entries(JSON.parse(localStorage.getItem(key)))) {
                const contentElement = document.getElementsByClassName(result_key)[iter];
                if (contentElement != null) {
                    contentElement.innerHTML += result_value;
                }
            }
            iter += 1;
        }
    }

};

