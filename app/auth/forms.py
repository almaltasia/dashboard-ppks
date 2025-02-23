from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import User

class LoginForm(FlaskForm):
    identity = StringField('Email atau NIP', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddUserForm(FlaskForm):
    full_name = StringField('Nama Lengkap', validators=[DataRequired(), Length(max=100)])
    nomor_identitas = StringField('nomor_identitas', validators=[Length(max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password harus minimal 8 karakter')
    ])
    password_confirm = PasswordField('Konfirmasi Password', validators=[
        DataRequired(),
        EqualTo('password', message='Password harus sama')
    ])
    roles = SelectField('Role', choices=[
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('dosen', 'Dosen'),
        ('staf', 'Staf')
    ], validators=[DataRequired()])
    phone = StringField('Nomor Telepon', validators=[Length(max=15)])
    jurusan = StringField('Jurusan')
    prodi = StringField('Program Studi')
    submit = SubmitField('Tambah Pengguna')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email ini sudah terdaftar.')
            
    def nomor_identitas(self, nomor_identitas):
        if nomor_identitas.data:
            user = User.query.filter_by(nomor_identitas=nomor_identitas.data).first()
            if user is not None:
                raise ValidationError('nomor_identitas ini sudah terdaftar.')
            
class ForgetPasswordForm(FlaskForm):
    identity = StringField('Email atau NIP', validators=[
        DataRequired(message='Email atau NIP harus diisi'),
        Length(min=3, max=100, message='Email atau NIP harus antara 3-100 karakter')
    ])
    submit = SubmitField('Kirim Link Reset Password')