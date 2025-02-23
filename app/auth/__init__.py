from flask import Blueprint
from flask_login import LoginManager

bp = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silahkan login terlebih dahulu untuk mengakses halaman ini.'

def init_login(app):
    login_manager.init_app(app)
    
    from app.auth.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

from app.auth import routes