// récupère les paramètres dans l'URL si il y a une paramètre
// "?CARTE=01" alors on affiche que cette carte avec tous les détails
// dans toute la suite sinon on affiche toutes les cartes reçues
const urlParams = new URLSearchParams(window.location.search);
var CARTE_GET = urlParams.get('CARTE');
if (!(CARTE_GET)) {
    CARTE_GET = urlParams.get('C');
}
console.log(CARTE_GET);

var NBMSG = document.querySelector('.NBMSG');

function btnA_cmd(obj) {
    var num_carte = obj.parentNode.id
    console.log("Envoyer au WS appuie BtnA ...", num_carte);
    ws.send(JSON.stringify({ "C": num_carte, "COMMAND": 'btnA' }));
}
function btnB_cmd(obj) {
    var num_carte = obj.parentNode.id
    console.log("Envoyer au WS appuie BtnB ...", num_carte);
    ws.send(JSON.stringify({ "C": num_carte, "COMMAND": 'btnB' }));
}
function VAL_cmd(obj) {
    var num_carte = obj.parentNode.id
    console.log("Envoyer au WS envoi VAL ...", num_carte);
    ws.send(JSON.stringify({ "C": num_carte, "COMMAND": obj.value }));
}

const url = new URL(window.location.href);
//console.log(url.hostname);

//var ws = new WebSocket("ws://192.168.1.59:8000/");
var ws = new WebSocket("ws://" + url.hostname + ":8000/");
ws.onmessage = function (event) {
    data = JSON.parse(event.data);
    console.log(data);

    if (CARTE_GET) {
        if (CARTE_GET != data.CARTE) return 0;
    }

    // affiche le nombre de messages reçus  
    NBMSG.textContent = data.NBMSG.toString()

    decode_json(data)
};


function decode_json(data) {
    var carte = document.getElementById("".concat('CARTE', data.CARTE));

    if (!carte) {
        carte = document.getElementById('CARTE99').cloneNode(true);
        carte.id = "".concat('CARTE', data.CARTE.toString());
        carte.style.removeProperty("display");
        document.body.appendChild(carte);
        console.log("creation .", carte);
    }
    var div_datas = carte.querySelector('.datas'),
        num_mb = carte.querySelector('.num'),
        in_VAL = carte.querySelector('.VAL'),
        btnA = carte.querySelector('.btnA'),
        btnB = carte.querySelector('.btnB');

    num_mb.textContent = data.CARTE.toString();
    in_VAL.value = data.VAL;

    if (Number.parseInt(data.RGB.substr(0, 9)) == 0) { // dans ce cas LED éteinte = tout NOIR !! donc fond noir mais on ne voit plus le texte ... donc je met blanc !!
        carte.style.backgroundColor = "rgb(255,255,255)";
    } else {
        //carte.style.backgroundColor = "".concat("rgb(", data.RGB.substr(0,3), "," , data.RGB.substr(3,3), ",", data.RGB.substr(6), ")"); // "rgb(60,179,113)";
        carte.style.backgroundColor = "rgb(" + data.RGB.substr(0, 3) + "," + data.RGB.substr(3, 3) + "," + data.RGB.substr(6) + ")"; // "rgb(60,179,113)";
    }

    if (data.A == "1") {
        btnA.style.backgroundColor = "red";
        btnA.style.color = "black";
    } else {
        btnA.style.removeProperty("background-color");
        btnA.style.removeProperty("color");
    }
    if (data.B == "1") {
        btnB.style.backgroundColor = "green";
        btnB.style.color = "black";
    } else {
        btnB.style.removeProperty("background-color");
        btnB.style.removeProperty("color");
    }

    div_datas.innerHTML = data.LASTCMD.toString();

    if (CARTE_GET) {
        var div_all_datas = document.getElementById('all_datas');

        if (!div_all_datas) {
            div_all_datas = document.createElement('div') //<div id="all_datas" ></div>
            div_all_datas.id = "all_datas";
            document.body.appendChild(div_all_datas);
        }

        div_all_datas.innerHTML = "";
        datas = "";

        datas = " NAME=" + data.NAME
            + "<br>" + "TEMP=" + data.TEMP
            + "<br>" + "A=" + data.A
            + "<br>" + "B=" + data.B
            + "<br>" + "AB=" + data.AB
            + "<br>" + "P0=" + data.P0
            + "<br>" + "P1=" + data.P1
            + "<br>" + "P2=" + data.P2
            + "<br>" + "RGB=" + data.RGB
            + "<br>" + "PITCH=" + data.PITCH
            + "<br>" + "ROLL=" + data.ROLL
            + "<br>" + "ACCX=" + data.ACCX
            + "<br>" + "ACCY=" + data.ACCY
            + "<br>" + "ACCZ=" + data.ACCZ
            + "<br>" + "DIST=" + data.DIST
            + "<br>" + "MVT=" + data.MVT
            + "<br>" + "LASTCMD=" + data.LASTCMD.toString();

        div_all_datas.innerHTML = datas;
    }
}