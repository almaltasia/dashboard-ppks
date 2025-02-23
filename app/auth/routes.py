from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from sqlalchemy import or_
from app.auth import bp
from app.auth.models import db, User
from app.auth.forms import LoginForm, AddUserForm, ForgetPasswordForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Check if identity is email or NIP
            user = User.query.filter(
                or_(
                    User.email == form.identity.data,
                    User.nomor_identitas == form.identity.data
                )
            ).first()
            
            if user and user.check_password(form.password.data):
                # Check if user is active
                if not user.is_active:
                    flash('Akun anda tidak aktif. Silahkan hubungi administrator.', 'danger')
                    return render_template('auth/login.html', form=form)
                
                # Update last login time
                user.updated_at = datetime.utcnow()
                db.session.commit()
                
                # Log the user in
                login_user(user, remember=form.remember_me.data)
                
                # Get the next page from args or default to dashboard
                next_page = request.args.get('next')
                if not next_page or not next_page.startswith('/'):
                    next_page = url_for('main.dashboard')
                
                return redirect(next_page)
            else:
                flash('Email/NIP atau password tidak valid', 'danger')
        else:
            # If form validation failed, flash the errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{error}', 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter(
            or_(
                User.email == form.identity.data,
                User.nomor_identitas == form.identity.data
            )
        ).first()
        
        if user:
            # Disini bisa ditambahkan logika untuk:
            # 1. Generate token reset password
            # 2. Kirim email dengan link reset
            flash('Instruksi reset password telah dikirim ke email terdaftar.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Email/NIP tidak ditemukan dalam sistem.', 'danger')
    
    return render_template('auth/forget_password.html', form=form)