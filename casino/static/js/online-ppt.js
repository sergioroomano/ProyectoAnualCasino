var socket = io>()

socket.on('meassage', function(msg) {

    if(msg.includes('has entered room')){
        var user_id = msg.split(' ')[0];
        var newPlayer = document.getElementById('player-list');
        newPlayer.textContent = "Player: " + user_id;
    }

});