from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import random
import string

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String)
    email = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    notes = db.relationship('Note', backref='autor', lazy=True)
    sender = db.relationship('Chat', foreign_keys='Chat.sender_id', backref='sender', lazy=True)
    receiver = db.relationship('Chat', foreign_keys='Chat.receiver_id', backref='receiver', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def read_password(self, password):
        return check_password_hash(self.password_hash, password)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50))
    inhalt = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    text = db.Column(db.String)
    time = db.Column(db.DateTime, default=datetime.now)
    message_type = db.Column(db.String, default="text")
    media_url = db.Column(db.String)
    mime_type = db.Column(db.String)

class Chat(db.Model):
    id = db.Column(db.Integer(), primary_key=True, default=lambda: int(''.join(random.choices(string.digits, k=10))))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship('Message', backref='chat_messages')
