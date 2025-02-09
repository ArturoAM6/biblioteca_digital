from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo
from models import GenreEnum

class LoginForm(FlaskForm):
    user = StringField('User', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=100)])

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=50)])
    user = StringField('User', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Las contraseñas deben ser iguales.')])
    admin = BooleanField('Admin', default=False)

class AddBookForm(FlaskForm):
    author = StringField('Author', validators=[InputRequired(), Length(min=4, max=100)])
    title = StringField('Title', validators=[InputRequired(), Length(max=150)])
    genre = SelectField('Genre', choices=[(p.name, p.value) for p in GenreEnum], validators=[InputRequired()], coerce=str)
    synopsis = TextAreaField('Synopsis', validators=[Length(max=300)])
    release_date = DateField('Release Date', validators=[InputRequired()])

class AddLoanForm(FlaskForm):
    user_id = StringField('User', validators=[InputRequired()])
    book_id = IntegerField('Book', validators=[InputRequired()])
    loan_date = DateField('Loan Date', validators=[InputRequired()])