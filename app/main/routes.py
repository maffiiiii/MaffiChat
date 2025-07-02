from flask import redirect, url_for, abort, render_template
from app.main.blueprint import main_bp

@main_bp.route("/")
def index():
    return redirect(url_for("auth.register"))  # Переходить на /register

@main_bp.route("/500")
def error():
    abort(501)

@main_bp.route("/base")
def base1():
    return render_template("home.html")