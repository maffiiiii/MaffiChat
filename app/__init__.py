from flask import Flask
from flask_login import LoginManager
from app.db import db
from flask_migrate import Migrate
from app.models import User
# from app.main.errors import register_error_handlers
from app.main.blueprint import main_bp
from app.notes.routes import notes_bp
from app.auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "maffi17"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maffi.db'  # приклад на SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    app.register_blueprint(main_bp)
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    return app