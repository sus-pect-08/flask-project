from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models.model.User import User
from routes.auth import auth
from routes.calendar import calendar_bp
from config import Config
from models.conn import db
from flask_migrate import Migrate

login_manager = LoginManager()

#Creazione dell'applicazione

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    migrate = Migrate(app, db)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(calendar_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app