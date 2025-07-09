from flask import render_template, redirect, url_for, flash, request, abort, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app.main.blueprint import chat_bp
# from app import socketio
from flask_socketio import send, join_room, leave_room
from app.models import User, Message, Chat
from app.db import db


@chat_bp.route("/")
@login_required
def index():
    messages = Message.query.all()
    users = User.query.all()
    return render_template("chat/chat.html", messages=messages, users=users)


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
            flash("this username does not exist")
            return redirect(url_for("chat.index"))


        
        chat = Chat.query.filter(Chat.sender_id==current_user.id, Chat.receiver_id==user.id).first()
        if chat:
            return redirect(url_for("chat.chat", chat_id=chat.id))
        else:
            chat = Chat(sender_id=current_user.id, receiver_id=user.id)
            db.session.add(chat)
            db.session.commit()
            

        
        return redirect(url_for("chat.chat", chat_id=chat.id))

        
    
    
# @chat_bp.route("/start_chat/<int:user_id", methods=["GET", "POST"])
# @login_required

