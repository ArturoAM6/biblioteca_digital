from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField, DateField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo
from models import GenreEnum

class LoginForm(FlaskForm):
    user = IntegerField('User', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=100)])

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=50)])
    user = IntegerField('User', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=150)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='The passwords must be the same.')])
    admin = RadioField('Admin', choices=[('True', 'Admin'), ('False', 'User')], default='False',validators=[InputRequired()])

class AddBookForm(FlaskForm):
    author = StringField('Author', validators=[InputRequired(), Length(min=4, max=100)])
    title = StringField('Title', validators=[InputRequired(), Length(max=150)])
    genre = SelectField('Genre', choices=[(p.name, p.value) for p in GenreEnum], validators=[InputRequired()])
    synopsis = TextAreaField('Synopsis', validators=[Length(max=300)])
    release_date = DateField('Release Date', validators=[InputRequired()])

class AddLoanForm(FlaskForm):
    user_id = IntegerField('User', validators=[InputRequired()])
    book_id = IntegerField('Book', validators=[InputRequired()])
    loan_date = DateField('Loan Date', validators=[InputRequired()])