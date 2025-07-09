from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

notes_bp = Blueprint("notes", import_name=__name__, template_folder="templates")  #i added tempalates cause i didnt find a html file

chat_bp = Blueprint("chat", import_name=__name__, template_folder="templates")

