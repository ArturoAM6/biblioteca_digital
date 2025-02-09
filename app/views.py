from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from app import db, bcrypt, app
from models import User, Book, Loan
from forms import LoginForm, RegisterForm, AddBookForm, AddLoanForm

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user.data
        password = form.password.data
        user = User.query.filter_by(user_id=user_id).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login succesful!', 'success')
            return redirect(url_for('home'))
        
        flash('Invalid user ID or password.', 'error')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = form.user.data
        password = form.password.data
        name = form.name.data
        admin = form.admin.data == 'True'
        existing_user = User.query.filter_by(user_id=user_id).first()

        if existing_user:
            flash('User already registered!', 'error')
            return render_template('register.html', form=form), 400
        
        crypt_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(user_id=user_id, password=crypt_password, name=name, admin=admin)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration succesful! Please, log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been succesfully logged out.', 'success')
    return redirect(url_for('login'))
