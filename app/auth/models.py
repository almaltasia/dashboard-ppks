from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.dialects.postgresql import TIMESTAMP

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id_users = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    nomor_identitas = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    roles = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    jurusan = db.Column(db.String(100), nullable=True)
    prodi = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    delete_at = db.Column(TIMESTAMP(timezone=True), nullable=True)
    
    def get_id(self):
        return str(self.id_users)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'