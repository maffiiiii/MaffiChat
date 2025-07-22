var socket = io();
// var chat_id = "{{chat.id if chat else ''}}"
// var current_user_id = "{{current_user.id }}"
var date = new Date().toISOString()

socket.emit("join_chat_list", {user_id: current_user_id});
if (chat_id){
    socket.emit("join", {chat_id: chat_id});
}

socket.on('message', function(msg){
    var div = document.createElement("div");
    div.className = msg.user_id == current_user_id ? 'me' : 'other';
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


document.getElementById("message").addEventListener("keypress", function(n){
    if (n.key==="Enter"){send_message()};
});




// ФУНКЦІЯ ОНОВЛЮЄ СПИСОК В ТВОМУ ХТМЛ, Я ТАМ ДОДАВ АЙДІ chat-list І ПРОСТО ЯКЩО ЧАТ СТВОРИВСЯ ТО ДОДАЄМО ЙОГО ЯК НОВИЙ ЕЛЕМЕНТ
// ІЗ ПОСИЛАННЯМ НА ЧАТ ПО id, ЩОСЬ ТИПУ ТОГО САМОГО ЯК В ТЕБЕ ДОДАЮТЬ НА СТОРІНКУ ПОВІДОМЛЕННЯ
socket.on('update_chat_list', function(data) {
            var chatList = document.getElementById('chat-list');
            
            var existingChat = document.getElementById('chat-' + data.chat_id);
            if (!existingChat) {
                var newChat = document.createElement('a');
                newChat.href = "/chat/chat/" + data.chat_id;
                newChat.className = "chat-button";
                newChat.id = "chat-" + data.chat_id;
                newChat.textContent = data.username;
                
                chatList.insertBefore(newChat, chatList.firstChild);
            }
        });