from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, login_required, logout_user, current_user
from app import db, bcrypt, app
from .models import User, Book, Loan, GenreEnum
from .forms import LoginForm, RegisterForm, AddBookForm
from datetime import date, timedelta

@app.route('/')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)

@app.route('/go-back')
def go_back():
    return redirect(request.referrer)

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
    user_id = current_user.id

    page = request.args.get('page', 1, type=int)
    per_page = 8

    query = Loan.query.filter_by(returned=False)

    if user_id:
        query = query.filter_by(user_id=user_id)

    loans = query.order_by(Loan.loan_date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('accounts/profile.html', loans=loans)

@app.route('/books/register', methods=['GET','POST'])
@login_required
def register_book():
    if not current_user.admin:
        flash('Acceso denegado. Solo los administradores pueden registrar libros', 'error')
        return redirect(url_for('home'))

    form = AddBookForm()
    if form.validate_on_submit():
        author = form.author.data
        title = form.title.data
        genre = form.genre.data
        synopsis = form.synopsis.data
        release_year = form.release_date.data
        release_date = date(release_year, 1, 1)

        new_book = Book(author=author, title=title, genre=genre, synopsis=synopsis, release_date=release_date)
        db.session.add(new_book)
        db.session.commit()

        flash('Nuevo libro agregado exitosamente', 'success')
        return redirect(url_for('register_book'))
    
    return render_template('books/register.html', form=form)

@app.route('/loan/<int:book_id>', methods=['GET','POST'])
@login_required
def loan_book(book_id):
    book = Book.query.get_or_404(book_id)

    if not book.status:
        flash('Este libro no está disponible', 'error')
        return redirect(url_for('go_back'))

    loan_date = date.today()
    devolution_date = loan_date + timedelta(days=7)

    new_loan = Loan(
        loan_date=loan_date,
        devolution_date=devolution_date,
        user_id=current_user.id,
        book_id=book.id
    )

    book.status = False
    book.times_loaned += 1

    db.session.add(new_loan)
    db.session.commit()

    flash(f'Préstamo registrado. Devuelve el libro antes del {devolution_date}.', 'success')
    return redirect(url_for('profile'))

@app.route('/confirm_return/<int:loan_id>', methods=['POST'])
@login_required
def confirm_return(loan_id):
    if not current_user.admin:
        flash('No tienes permisos para aprobar', 'error')
        return redirect(url_for('home'))
    
    loan = Loan.query.get_or_404(loan_id)

    if loan.returned:
        flash('Este prestamo ya ha sido devuelto', 'success')
        return redirect(url_for('admin_loans'))
    
    loan.calculate_fine()
    loan.returned = True

    book = Book.query.get(loan.book_id)
    book.status = True

    db.session.commit()
    flash(f'El libro "{book.title}" marcado como devuelto. Multa ${loan.fine}', 'success')
    
    return redirect(url_for('admin_loans'))

@app.route('/admin/loans')
@login_required
def admin_loans():
    if not current_user.admin:
        flash('No tienes permisos para acceder a esta pagina', 'error')
        return redirect(url_for('home'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    user_id = request.args.get('user_id')
    book_id = request.args.get('book_id')

    query = Loan.query.filter_by(returned=False)

    if user_id:
        query = query.filter_by(user_id=user_id)
    elif book_id:
        loans = query.filter_by(book_id=book_id)

    loans = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('accounts/admin_loans.html', loans=loans, user_id=user_id, book_id=book_id)

@app.route('/books')
def all_books():
    page = request.args.get('page', 1, type=int)
    per_page=12
    books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('books/index.html', books=books)

@app.before_request
def load_genres():
    genres = [genre.value for genre in GenreEnum]
    g.genres = genres

@app.route('/books/genre/<genre_name>')
def books_by_genre(genre_name):
    genre_enum = next((g for g in GenreEnum if g.value.lower() == genre_name.lower()), None)
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    if genre_enum is None:
        flash(f'El género "{genre_name}" no existe.', 'error')
        return redirect(url_for('home'))

    books = Book.query.filter_by(genre=genre_enum).paginate(page=page, per_page=per_page, error_out=False)
    top_books = Book.query.order_by(Book.times_loaned.desc()).filter_by(genre=genre_enum).limit(10).all()
    
    if not books.items:
        flash(f'No hay libros disponibles en el género {genre_name}.', 'error')

    return render_template('books/genre.html', books=books, top_books=top_books, genre=genre_enum.value, current_category=genre_enum.value)

@app.route('/books/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('books/details.html', book=book)

@app.route('/books/popular')
def popular_books():
    books = Book.query.order_by(Book.times_loaned.desc()).all()
    return render_template('books/popular.html', books=books)