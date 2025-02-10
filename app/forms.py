from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo
from .models import GenreEnum

class LoginForm(FlaskForm):
    user = StringField('Matrícula', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Contraseña', validators=[InputRequired(), Length(min=8, max=100)])

class RegisterForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired(), Length(min=4, max=50)])
    user = StringField('Matrícula', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Contraseña', validators=[InputRequired(), Length(min=8, max=100)])
    confirm_password = PasswordField('Confirmar contraseña', validators=[InputRequired(), EqualTo('password', message='Las contraseñas deben ser iguales.')])
    admin = BooleanField('Administrador', default=False)

class AddBookForm(FlaskForm):
    author = StringField('Autor', validators=[InputRequired(), Length(min=4, max=100)])
    title = StringField('Titulo', validators=[InputRequired(), Length(max=150)])
    genre = SelectField('Genero', choices=[(p.name, p.value) for p in GenreEnum], validators=[InputRequired()], coerce=str)
    synopsis = TextAreaField('Sinopsis', validators=[Length(max=300)])
    release_date = DateField('Fecha de publicación', validators=[InputRequired()])

class AddLoanForm(FlaskForm):
    user_id = StringField('Matrícula', validators=[InputRequired()])
    book_id = IntegerField('Libro', validators=[InputRequired()])
    loan_date = DateField('Fecha de préstamo', validators=[InputRequired()])