
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
