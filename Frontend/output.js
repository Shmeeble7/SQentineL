

function addBox(key_num) {
    const container = document.getElementById('results');

    const key = "key-" + key_num;
    container.innerHTML += `<div class="d-flex info_div flex-column pt-3">
            <div class="info-div-header d-flex flex-row justify-content-center align-items-center rounded">
                <h4 class="severity p-2">SEVERITY </h4>
                <p class=" title p-2 pt-3 text-center"></p>
                <button onclick="openInfo('`+ key + `')" type="button" class="caret-down btn p-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="bi bi-caret-down" >
                        <path d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"/>
                    </svg>
                </button>
            </div>
            <div id = "` + key + `" class="hidden-box flex-column info-div-body justify-content-center align-items-center rounded">
                <div class="align-items-left d-flex flex-row line pe-3">Line: </div>
                <div class="align-items-left d-flex flex-row code_snippet"></div>
                <div class="d-flex align-items-left">
                    <h5 class="d-flex pt-3">Explanation</h5>
                </div>
                <div class="d-flex flex-row align-items-left explanation"></div>
                <div class = "d-flex flex-row align-items-left danger"> </div>
                <div class="d-flex align-items-left">
                    <h5 class="d-flex align-items-left pt-3 pe-5">Example Payload</h5>
                    <div class="d-flex align-items-left example_payload"></div>
                </div>
                <div class="d-flex align-items-left">
                    <h5 class="d-flex align-items-left pt-3 pe-5">Example Fix</h5>
                    <div class="d-flex align-items-left example_fix"></div>
                </div>
            </div>
        </div>`;

}

function openInfo(key) {
    console.log(key)
    const div = document.getElementById(key);
    div.classList.toggle("hidden-box");
}
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
            addBox(x);
        }



        let iter = 0;
        for (const [key, value] of Object.entries(localStorage)) {
            for (const [result_key, result_value] of Object.entries(JSON.parse(localStorage.getItem(key)))) {
                const contentElement = document.getElementsByClassName(result_key)[iter];
                if (contentElement != null && result_value != null) {
                    contentElement.innerHTML += result_value;
                }
            }
            iter += 1;
        }
    }

};

