from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.auth import auth_bp
from app.models import User
from app.db import db



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if User.query.filter_by(username=username).first():
            flash("this username is already taken", category="warning")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(email=email).first():
            flash("this email is already taken", category="warning")
            return redirect(url_for("auth.register"))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main.base"))
    
    return render_template("auth/register.html")




@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        login = request.form["login"]
        password = request.form["password"]
        user = User.query.filter((User.email==login)or (User.username==login)).first()
        if not user or not user.read_password(password):
            flash("wrong login data", category="warning")
            return redirect(url_for("auth.login"))
        login_user(user)
        return redirect(url_for("main.base"))
    return render_template("auth/login.html")

#def logout