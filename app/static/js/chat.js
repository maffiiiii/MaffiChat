var socket = io();
// var chat_id = "{{chat.id if chat else ''}}"
// var current_user_id = "{{current_user.id }}"
var date = new Date().toISOString()
if (chat_id){
    socket.emit("join", {chat_id: chat_id});
}

socket.on('message', function(msg){
    var div = document.createElement("div");
    div.className = msg.user_id == current_user_id ? 'message-sent' : 'message-received';
    div.appendChild(document.createTextNode(msg.text));
    document.getElementById("messages").appendChild(div);
});

function send_message() {
    var message = document.getElementById("message").value;
    socket.emit("message", {
        chat_id : chat_id,
        text : message,
        user_id : current_user_id,
        time: new Date(date.time).toLocaleTimeString()
    });
    document.getElementById("message").value = "";
}