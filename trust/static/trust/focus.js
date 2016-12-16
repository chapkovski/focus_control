

var status_message;
var statuses = { focusw:"window is in focus; visible",
                 blurw:"window lost focus; partly visible",
                 focust:"tab is in focus; partly visible",
                 blurt:"tab lost focus; not visible",
               };


/////////////////////////////////////////
// main visibility API function
// check if current tab is active or not
var vis = (function(){
    var stateKey,
        eventKey,
        keys = {
                hidden: "visibilitychange",
                webkitHidden: "webkitvisibilitychange",
                mozHidden: "mozvisibilitychange",
                msHidden: "msvisibilitychange"
    };
    for (stateKey in keys) {
        if (stateKey in document) {
            eventKey = keys[stateKey];
            break;
        }
    }
    return function(c) {
        if (c) document.addEventListener(eventKey, c);
        return !document[stateKey];
    }
})();


/////////////////////////////////////////
// check if current tab is active or not
vis(function(){

    if(vis()){

        // the setTimeout() is used due to a delay
        // before the tab gains focus again, very important!
	      setTimeout(function(){
       whattodo('focust');
        },300);

    } else {
      whattodo('blurt');
    }
});


/////////////////////////////////////////
// check if browser window has focus
var notIE = (document.documentMode === undefined),
    isChromium = window.chrome;

if (notIE && !isChromium) {

    // checks for Firefox and other  NON IE Chrome versions
    $(window).on("focusin", function () {
        setTimeout(function(){

   whattodo('focusw');

        },300);

    }).on("focusout", function () {
   whattodo('blurw');
    });

} else {

    // checks for IE and Chromium versions
    if (window.addEventListener) {

        // bind focus event
        window.addEventListener("focus", function (event) {
            setTimeout(function(){
       whattodo('focusw');
            },300);

        }, false);

        // bind blur event
        window.addEventListener("blur", function (event) {
      whattodo('blurw');
        }, false);


    } else {

        // bind focus event
        window.attachEvent("focus", function (event) {

            setTimeout(function(){
    whattodo('focusw');
            },300);

        });
        // bind focus event
        window.attachEvent("blur", function (event) {
      whattodo('blurw');
        });
    }
}

function whattodo(status) {
  status_message=statuses[status];
  // whenhappens = models.CharField()
  //   whathappens = models.CharField()
  //   wherehappens

  var msg = {
     wherehappens : $(document).attr('title'),
     player: playerpk,
     grouppk: grouppk,
     whenhappens: new Date().toString(),
     whathappens: status_message,
   };
   console.log(msg);
  // console.log(status_message);
  if(socket.readyState === socket.OPEN){
   socket.send(JSON.stringify(msg));
}

  return(status_message);
}
