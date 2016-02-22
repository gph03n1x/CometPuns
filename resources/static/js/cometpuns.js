
jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/engine";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            updater.showMessage(JSON.parse(event.data));
        }
    },

    showMessage: function(message) {
        if (message.body[0] == "/") {
            var command = message.body.split(" ");
            var arrayLength = command.length;
            console.log(command);
            if (command[0] == "/channel") {
                $("#roomId").text( "Room Id : #"+command[1]);
            }
            if (command[0] == "/users") {
                console.log("here we go");
                $('#users > tr').remove();
                console.log("here we go - 2");
                for (var i = 1; i < arrayLength; i++) {
                    console.log("here we go - 3");
                    var data = command[i].split(":")
                    $('#users').append("<tr><td id='u"+data[0]+"'>"+data[0]+"</td><td id='s"+data[0]+"'>"+data[1]+"</td></tr>");
                }
                console.log("here we go - 4");
            }
        }
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#chat").append(node);
        node.slideDown();
        $('#chat').stop().animate({
            scrollTop: $("#chat")[0].scrollHeight
        }, 800);
    }
};

$('#chat-input').bind("enterKey",function(e){
   sendChat($('#chat-input').val());
   $('#chat-input').val('');
});

$('#chat-input').keyup(function(e){
    if(e.keyCode == 13)
    {
        $(this).trigger("enterKey");
    }
});


function sendChat (message) {
    updater.socket.send(JSON.stringify(message));
}



String.prototype.format = function () {
        var args = [].slice.call(arguments);
        return this.replace(/(\{\d+\})/g, function (a){
            return args[+(a.substr(1,a.length-2))||0];
        });
};

$(document).ready(function() {
        updater.start();
});
