from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

notes_bp = Blueprint("notes", import_name=__name__)

@main_bp.route("/base")
def base():
    return render_template("base.html")