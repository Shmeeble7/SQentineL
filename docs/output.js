function addBox(key_num) {
    const container = document.getElementById('results');

    const key = "key-" + key_num;
    const key_header = "key-header-" + key_num;
    const key_btn = "key-btn-" + key_num;
    container.innerHTML += `<div class="d-flex info_div flex-column pt-3">
            <div class="info-div-header d-flex flex-row align-items-center rounded">
                <h4 class="` + key_header + ` justify-content-left ps-3 severity p-2">SEVERITY </h4>
                <p class="` + key_header + ` title mt-3 me-auto "></p>
                <button onclick="openInfo('`+ key_num + `')" type="button" class="caret-down btn p-2 ms-auto">
                    <svg class="active-caret ` + key_btn + `" xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="bi bi-caret-down" >
                        <path d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"/>
                    </svg>
                    <svg class="inactive-caret ` + key_btn + `" xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="bi bi-caret-down" >
                        <path d="M3.204 11h9.592L8 5.519zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659"/>                    </svg>
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
                <div class="d-flex flex-row">
                    <h5 class="d-flex align-items-left pt-3 pe-5">Example Payload</h5>
                    <div class="d-flex align-items-right pt-3 ms-5 example_payload"></div>
                </div>
                <div class="d-flex flex-row">
                    <h5 class="d-flex align-items-left pt-3 pe-5">Example Fix</h5>
                    <div class="d-flex align-items-right pt-3 example_fix"></div>
                </div>
            </div>
        </div>`;

}

function openInfo(key_num) {
    key = "key-" + key_num
    btn_key = "key-btn-" + key_num
    console.log(key)
    const div = document.getElementById(key);
    div.classList.toggle("hidden-box");

    const btns = document.getElementsByClassName(btn_key);
    for (let x = 0; x < btns.length; x++) {
        btns[x].classList.toggle("active-caret");
        btns[x].classList.toggle("inactive-caret");
    }
}
window.onload = function () {


    if (localStorage.length == 0) {
        const safe_div = this.document.getElementById("safe-div");
        safe_div.style.display = "block";
        const img = document.getElementById("squid-img")
        img.src = "Assets/ExcitedSquid.png";
    }
    else {

        for (let x = 0; x < localStorage.length; x++) {
            addBox(x);
        }

        let iter = 0;
        let low = 0;
        let med = 0;
        let high = 0;
        let crit = 0;
        for (const [key, value] of Object.entries(localStorage)) {

            for (const [result_key, result_value] of Object.entries(JSON.parse(localStorage.getItem(key)))) {
                const contentElement = document.getElementsByClassName(result_key)[iter];
                if (contentElement != null && result_value != null) {
                    contentElement.innerHTML += result_value;
                    if (result_key == "severity") {
                        console.log(result_value);
                        let color = "black";
                        if (result_value == "LOW") {
                            color = "#A17F1A";
                            low += 1;
                        }
                        else if (result_value == "MEDIUM") {
                            color = "orange";
                            med += 1;
                        }
                        else if (result_value == "HIGH") {
                            color = "red";
                            high += 1;
                        }
                        else {
                            color = "maroon";
                            crit += 1;
                        }
                        const header_key = "key-header-" + iter;
                        const headers = document.getElementsByClassName(header_key);
                        for (let x = 0; x < headers.length; x++) {
                            headers[x].style.color = color;
                        }
                    }
                }
            }
            iter += 1;
        }
        const img = document.getElementById("squid-img")
        if (crit > 0 || high > 0) {
            img.src = "Assets/AngrySquid.png";
            console.log("HERE");
        }
        else if (med > 0 || low > 0) {
            img.src = "Assets/MehSquid.png";
        }
        else {
            img.src = "Assets/Squid.png";
        }
    }

};
