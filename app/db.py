from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

supabase_url = "postgresql://postgres:vazguh-nyzda1-tottIj@db.rjtwlrudyktwrhrlnyqf.supabase.co:5432/postgres"
db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = supabase_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)