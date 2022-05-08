
var NBMSG = document.querySelector('.NBMSG');

function btnA_cmd() {
    console.log("Envoyer au WS appuie BtnA ...", num_carte);
    ws.send(JSON.stringify({ "CARTE": num_carte, "COMMAND": 'btnA' }));
}

function btnB_cmd() {
    console.log("Envoyer au WS appuie BtnB ...", num_carte);
    ws.send(JSON.stringify({ "CARTE": num_carte, "COMMAND": 'btnB' }));
}
function VAL_cmd(obj) {
    var num_carte = obj.parentNode.id
    console.log("Envoyer au WS envoi VAL ...", num_carte);
    ws.send(JSON.stringify({ "CARTE": num_carte, "COMMAND": obj.value }));
}

const url = new URL(window.location.href);

var ws = new WebSocket("ws://" + url.hostname + ":8000/");
ws.onmessage = function (event) {
    data = JSON.parse(event.data);
    console.log(data);

    // affiche le nombre de messages reçus  
    NBMSG.textContent = data.NBMSG.toString()
    
    if (data.CARTE.toString() == num_carte) {
        decode_json(data)
    }
};


function decode_json(data) {

    in_VAL.value = data.VAL;

    if (Number.parseInt(data.RGB.substr(0, 9)) == 0) { // dans ce cas LED éteinte = tout NOIR !! donc fond noir mais on ne voit plus le texte ... donc je met blanc !!
        color_RGB.style.backgroundColor = "rgb(255,255,255)";
    } else {
        color_RGB.style.backgroundColor = "rgb(" + data.RGB.substr(0, 3) + "," + data.RGB.substr(3, 3) + "," + data.RGB.substr(6) + ")"; // "rgb(60,179,113)";
    }

    if (data.A == "1") {
        btnA.style.fill = "red"
    } else {
        btnA.style.fill = "black"
    }
    if (data.B == "1") {
        btnB.style.fill = "red"
    } else {
        btnB.style.fill = "black"
    }

    div_datas.innerHTML = data.LASTCMD.toString();

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