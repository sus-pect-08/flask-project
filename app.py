from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models.model import User

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'la-tua-chiave-segreta-molto-sicura'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Assumendo un blueprint di autenticazione
    
    @login_manager.user_loader
    def load_user(user_id):
        stmt = db.select(User).filter_by(id=int(user_id))
        return db.session.execute(stmt).scalar_one_or_none()

    return app