from flask import render_template, redirect, url_for, flash, request, abort, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app.main.blueprint import chat_bp
# from app import socketio
from flask_socketio import send, join_room, leave_room
from app.models import User, Message, Chat
from app.db import db
from app.things import socketio


@chat_bp.route("/")
@login_required
def index():
    messages = Message.query.all()
    users = User.query.all()
    chats = Chat.query.filter(
        (Chat.sender_id == current_user.id) or (Chat.receiver_id == current_user.id)
    ).all() 
    return render_template("chat/chat.html", messages=messages, users=users, chats=chats)


@chat_bp.route("/chat/<int:chat_id>", methods=["GET"])
@login_required
def chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if current_user.id not in [chat.receiver_id, chat.sender_id]:
        flash("you are not a part of this conversation")
    messages = Message.query.filter_by(chat_id=chat.id).order_by(Message.time.asc()).all()
    return render_template("chat/chat.html", messages=messages, chat=chat)


@chat_bp.route("/search_users", methods=["GET", "POST"])    #it is not very nice without javascript but it is all i can do cause i dont know javascript
@login_required
def search():
    if request.method == "POST":
        user_name = request.form["username"]     #username in html form must be username
        user = User.query.filter_by(username=user_name).first()
        if not user:
            flash("This username does not exist")
            return redirect(url_for("chat.index"))


        
        chat = Chat.query.filter(((Chat.receiver_id == user.id) and (Chat.sender_id == current_user.id) or (Chat.receiver_id == current_user.id) and (Chat.sender_id == user.id))).first()
        if chat:
            return redirect(url_for("chat.chat", chat_id=chat.id))
        else:
            chat = Chat(sender_id=current_user.id, receiver_id=user.id)
            db.session.add(chat)
            db.session.commit()
            

        
            return redirect(url_for("chat.chat", chat_id=chat.id))



        
    
    
@socketio.on("message")
def handle_message(data):
    text = data["text"]
    user_id = data["user_id"]
    chat_id = data["chat_id"]
    message = Message(text=text, user_id=user_id, chat_id=chat_id)
    db.session.add(message)
    db.session.commit()
    send({
        "chat_id": chat_id,
        "text": text,
        "user_id": user_id,
        "time": message.time.strftime("%Y-%m-%d %H:%M:%S"),
    }, room=str(chat_id))


@socketio.on("join")
def handle_join(data):
    chat_id = data["chat_id"]
    join_room(chat_id)


@socketio.on("leave")
def handle_leave(data):
    chat_id = data["chat_id"]
    leave_room(chat_id)

