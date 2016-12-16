
     $(function() {
       var msgArea = $('#msgArea')
       var elementMessage = $('#message')
       alert('filka mudak');
      //  $( "p" ).text( "The DOM is now loaded and can be manipulated." );
       socket = new WebSocket("ws://" + window.location.host + "/chat/"+grouppk);

   socket.onmessage = function(message) {
       var data = JSON.parse(message.data)
       console.log(data);
       if (data.player!=playerpk) {
       msgArea.append('<p><strong>'+ data.sender + '</strong>: ' + data.curpage + " // " + data.player+" //GROUP " + data.group+'</p>');
     }
   }

   socket.onopen = function() {
     var msg = {
        wherehappens : $(document).attr('title'),
        player: playerpk,
        grouppk: grouppk,
        whenhappens: new Date().toString(),
        whathappens: "hellow",//status_message,
      };
     // console.log(status_message);

      socket.send(JSON.stringify(msg));

      //  tosend = JSON.stringify({ 'curpage': current_title });
      //  socket.send(msg);
   }
        });
