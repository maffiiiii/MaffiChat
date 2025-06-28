from flask import render_template
from app.main.blueprint import main_bp


@main_bp.app_errorhandler(404)        #without app if for all blueprints
def page_not_found(e):
        return render_template("errors/404.html"), 404

@main_bp.app_errorhandler(Exception)
def internal_server_error(e):
        if hasattr(e , 'code') and e.code in [500,403,402,401,405,501]:
                status_code = e.code
        else:
                status_code = 500
        return render_template('errors/error.html',error = e, status_code = status_code), status_code
