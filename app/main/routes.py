from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.main import bp
from app.auth.models import User

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html')

@bp.route('/user-management')
@login_required
def user_management():
    if current_user.roles not in ['super_admin', 'admin']:
        flash('Anda tidak memiliki akses ke halaman ini')
        return redirect(url_for('main.dashboard'))
    users = User.query.filter(User.delete_at.is_(None)).all()
    return render_template('dashboard/user_management.html', users=users)