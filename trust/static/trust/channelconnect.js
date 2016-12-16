
     $(function() {
       var msgArea = $('#msgArea')
       var elementMessage = $('#message')
       alert('filka mudak');
      //  $( "p" ).text( "The DOM is now loaded and can be manipulated." );
       socket = new WebSocket("ws://" + window.location.host + "/chat/"+groupid);

   socket.onmessage = function(message) {
       var data = JSON.parse(message.data)
       console.log(data);
       if (data.player!=playerid) {
       msgArea.append('<p><strong>'+ data.sender + '</strong>: ' + data.curpage + " // " + data.player+" //GROUP " + data.group+'</p>');
     }
   }

   socket.onopen = function() {
console.log("asdf");
     var msg = {
        current_title : $(document).attr('title'),
        player: playerid,
        otreegroup: groupid,
        status: "tttttest",
        date: new Date().toString(),

      };
     // console.log(status_message);

      socket.send(JSON.stringify(msg));

      //  tosend = JSON.stringify({ 'curpage': current_title });
      //  socket.send(msg);
   }
        });
