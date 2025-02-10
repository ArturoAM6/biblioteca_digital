from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from app import db, bcrypt, app
from .models import User, Book, Loan
from .forms import LoginForm, RegisterForm, AddBookForm, AddLoanForm

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        id = form.user.data
        password = form.password.data
        user = User.query.filter_by(id=id).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Ingreso exitoso!', 'success')
            return redirect(url_for('home'))
        
        flash('Matricula o contraseña incorrectas.', 'error')

    return render_template('accounts/login.html', form=form)

@app.route('/register', methods=['GET','POST'])
@login_required
def register():
    if not current_user.admin:
        flash('Acceso denegado. Solo los administradores pueden registrar usuarios', 'error')
        return redirect(url_for('home'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        id = form.user.data
        password = form.password.data
        name = form.name.data
        admin = form.admin.data

        existing_user = User.query.filter_by(id=id).first()

        if existing_user:
            flash('Matricula ya registrada!', 'error')
            return render_template('register.html', form=form), 400
        
        crypt_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(id=id, password=crypt_password, name=name, admin=admin)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso!', 'success')
        return redirect(url_for('home'))
    
    return render_template('accounts/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('accounts/profile.html')

@app.route('/terror')
def terror():
    return render_template('books/terror.html')

@app.route('/autoayuda')
def autoayuda():
    return render_template('books/autoayuda.html')

@app.route('/infantiles')
def infantiles():
    return render_template('books/infantiles.html')