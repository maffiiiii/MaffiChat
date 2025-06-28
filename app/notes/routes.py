from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app.main.blueprint import notes_bp
from app.models import User, Note
from app.db import db

@notes_bp.route("/")
@login_required
def index():
    notes = Note.query.filter_by(user_id = current_user.id).order_by(Note.updated_at.desc()).all()
    return render_template("notes/index.html", notes=notes)


@notes_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method=="POST":
        name = request.form["name"]
        inhalt = request.form["inhalt"]

        if not name and not inhalt:
            return redirect(url_for("notes.index"))
        note = Note(name=name, inhalt=inhalt, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()

        return redirect(url_for("notes.index"))
    
    return render_template("notes/add.html")


@notes_bp.route("/delete/<int:note_id>", methods=["POST"])
@login_required
def delete(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()

    return redirect(url_for("notes.index"))


@notes_bp.route("/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        abort(403)
    if request.method == "POST":
        note.name = request.form["name"]
        note.inhalt = request.form["inhalt"]
        db.session.commit()
        return redirect(url_for("notes.index"))
    
    return render_template("notes/edit.html", note=note)
    