function themeClair () {
    let request = "oui";
    if (request == "oui"){
        let d = document.getElementById("container");
        d.style.backgroundColor="gainsboro";
        d.style.color="black";
        d.style.transitionDuration="1s";
    }
    else {
        alert("action annulée");
    }
}

function themeSombre () {
    let request = "oui";
    if (request == "oui"){
        let d = document.getElementById("container");
        d.style.backgroundColor="#333333";
        d.style.color="gainsboro";
        d.style.transitionDuration="1s";
    }
    else {
        alert("action annulée");
    }
}

function texteGrossi() {
    let request = "oui";
    if (request == "oui"){
        let d = document.getElementById("container");
        d.style.fontSize = "20px";
        d.style.transitionDuration="1s";
    }
    else {
        alert("action annulée");
    }
}

function textePetit () {
    let request = "oui";
    if (request == "oui"){
        let d = document.getElementById("container");
        d.style.fontSize = "10px";
        d.style.transitionDuration="1s";
    }
    else {
        alert("action annulée");
    }
}
