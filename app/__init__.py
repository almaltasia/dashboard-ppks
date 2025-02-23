from flask import Flask
from app.config import Config
from app.auth.models import db
from app.auth import bp as auth_bp, init_login

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize login manager
    init_login(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Create database tables if they don't exist
    # Comment this out if tables already exist
    # with app.app_context():
    #     db.create_all()
    
    return app