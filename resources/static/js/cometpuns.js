
jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

function startTimer(duration) {
    var percentage = 0;
    var step = 100/duration;
    
    function timer() {
        percentage += step;

        $('#countdown').progress({
            percent: percentage
        });
        if (percentage >= 100) {
            clearInterval(refreshIntervalId);
        }
    };
    timer();
    var refreshIntervalId = setInterval(timer, 1000);
}

function startCountdown(seconds){
    $('#countdown').progress({percent: 0});
    startTimer(seconds);
}

function refreshRooms(command) {
    $(".positive").removeClass( "positive" ).addClass( "error" );
    sendChat(command);
}

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
        if (message.body[0] == "/" && message.user == "System") {
            var command = message.body.split(" ");
            var arrayLength = command.length;
            console.log(command);
            if (command[0] == "/choice") {
                $("#options").append(message.data_html);
            }
            if (command[0] == "/opener") {
                $("#opener").empty();
                $("#opener").append(message.data_html);
            }
            if (command[0] == "/isready") {
                $("#td"+command[1]).removeClass( "error" ).addClass( "positive" );
            }
            if (command[0] == "/channel") {
                $("#roomId").text( "Room Id : #"+command[1]);
            }
            if (command[0] == "/users") {
                $('#users > tr').remove();
                for (var i = 1; i < arrayLength; i++) {
                    var data = command[i].split(":")
                    $('#users').append("<tr id='td"+data[0]+"' class='error'><td id='u"+data[0]+"'>"+data[0]+"</td><td id='s"+data[0]+"'>"+data[1]+"</td></tr>");
                }
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
