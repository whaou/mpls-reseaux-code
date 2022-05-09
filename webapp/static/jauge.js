
var NBMSG = document.querySelector('.NBMSG');

const url = new URL(window.location.href);

var ws = new WebSocket("ws://" + url.hostname + ":8000/");
ws.onmessage = function (event) {
    data = JSON.parse(event.data);
    console.log(data);

    // affiche le nombre de messages reçus  
    NBMSG.textContent = data.NBMSG.toString()
    
    if ((data.CARTE.toString() == num_carte) || (num_carte == "99" )){
        decode_json(data)
    }
};


function decode_json(data) {

    var jauge = document.getElementById("".concat('jauge', data.CARTE));

    if (!jauge) {
        jauge = document.getElementById('jauge99').cloneNode(true);
        jauge.id = "".concat('jauge', data.CARTE.toString());
        jauge.style.removeProperty("display");
        document.body.appendChild(jauge);
        console.log("creation .", jauge);
    }
    in_VAL.value = data.VAL;

    div_datas.innerHTML = data.LASTCMD.toString();
    
    /* TODO test en css et js sans jquery ... 
    bar = jauge.querySelector('.bar');
    bar.style.transform = 'rotate(60deg)';
    */

    // Anime la jauge et met à jour VAL 
    anim_circle_id("".concat('jauge', data.CARTE), data.VAL, data.NAME.toString() , data.LASTCMD.toString() );
}

function anim_circle(){
    
  $(".progress").each(function(){
    var $bar = $(this).find(".bar");
    var $val = $(this).find("span");
    var perc = parseInt( $val.text(), 10);
   
    $({p:0}).animate({p:perc}, {
      duration: 3000,
      easing: "swing",
      step: function(p) {
        $bar.css({
          transform: "rotate("+ (45+(p*1.8)) +"deg)", // 100%=180° so: ° = % * 1.8
          // 45 is to add the needed rotation to have the green borders at the bottom
        });
        $val.text(p|0);
      }
    });
  });
}

function anim_circle_id(id_circle, val, namejauge, last_cmd){
    
    var $_this_circle = $("#"+id_circle);
    var $bar = $_this_circle.find(".bar");
    //var $val = $_this_circle.find("span");
    var $val = $_this_circle.find(".val");
    $val.text(val);
    
    var $namejauge = $_this_circle.find(".namejauge");
    $namejauge.text(namejauge);
        
    var $last_cmd = $_this_circle.find(".last_cmd");
    $last_cmd.text(last_cmd);
        
    var perc = parseInt( $val.text(), 10);
   
    $({p:0}).animate({p:perc}, {
      duration: 3000,
      easing: "swing",
      step: function(p) {
        $bar.css({
          transform: "rotate("+ (45+(p*1.8)) +"deg)", // 100%=180° so: ° = % * 1.8
          // 45 is to add the needed rotation to have the green borders at the bottom
        });
        $val.text(p|0);
      }
    });

}