from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, NumberRange
from .models import GenreEnum, User

class LoginForm(FlaskForm):
    user = StringField('Matrícula', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Contraseña', validators=[InputRequired(), Length(min=8, max=100)])

    def validate_user(self, field):
        if not User.query.filter_by(id=field.data).first():
            raise ValidationError('Esta matrícula no está registrada')

class RegisterForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired(), Length(min=4, max=50)])
    user = StringField('Matrícula', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Contraseña', validators=[InputRequired(), Length(min=8, max=100)])
    confirm_password = PasswordField('Confirmar contraseña', validators=[InputRequired(), EqualTo('password', message='Las contraseñas deben ser iguales.')])
    admin = BooleanField('Administrador', default=False)

    def validate_user(self, field):
        if User.query.filter_by(id=field.data).first():
            raise ValidationError('Esta matrícula ya está registrada.')
        
class AddBookForm(FlaskForm):
    author = StringField('Autor', validators=[InputRequired(), Length(min=4, max=100)])
    title = StringField('Titulo', validators=[InputRequired(), Length(max=150)])
    genre = SelectField('Genero', choices=[(p.name, p.value) for p in GenreEnum], validators=[InputRequired()], coerce=str)
    synopsis = TextAreaField('Sinopsis', validators=[Length(max=2000)])
    release_date = IntegerField('Año de publicación', validators=[InputRequired(), NumberRange(min=500, max=2100, message="Ingrese un año válido")])