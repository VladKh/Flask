from flask import flash, redirect, url_for, session, render_template, request
from app import app
from database import db_session
from models import Users, Bookcase, BookNames, Authors
from forms import LoginForm, Registration, AddBook, DeleteBook

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def nonexistent_author(author):
    return bool(Authors.query.filter_by(author_name=author).first())

def check_login():
    try:
         session['user_name']
    except KeyError:
        return False
    return True

def insert_book_to_db(author, book_name):
    #Check for a nonexistent author
    if not nonexistent_author(author):
        a = Authors(author_name=author)
        db_session.add(a)
        db_session.commit()

    author_id = Authors.query.filter_by(author_name=author).first().id
    if not BookNames.query.filter_by(book_name=book_name).first():
        db_session.add(BookNames(book_name))
        db_session.commit()

        db_session.add(Bookcase(
            authors_id=author_id,
            book_id=BookNames.query.filter_by(book_name=book_name).first().id))
        db_session.commit()
    else:
        flash('Such book already exist')

@app.route('/')
@app.route('/index')
def index():
    variables = {
        'title': 'Home',
    }

    return render_template('index.html', **variables)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user_name = request.form['name']
        user_password = request.form['password']
        user = Users.query.filter(Users.name == user_name,
                                  Users.password == user_password).first()
        if user:
            session['user_name'] = user_name
            flash('''You are successful login!
                  Now you can add or delete books.''')
            return redirect(url_for('index'))
        else:
            flash('Incorrect user name or password!', 'error')

    variables = {
        'title': 'Login',
        'form': form,
        'session': session
    }
    return render_template('login.html', **variables)

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    flash('You are logged out!')
    return render_template('index.html', title='Home')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Registration(request.form)
    if request.method == 'POST' and form.validate():
        user_name = request.form['name']
        user_password = request.form['password']
        user_email = request.form['email']

        user = Users.query.filter(Users.name == user_name,
                                  Users.password == user_password,
                                  Users.email == user_email).first()
        if user:
            flash('Failed! Such User already exist!', 'error')
        else:
            u = Users(name=user_name,
                      email=user_email,
                      password=user_password)
            db_session.add(u)
            db_session.commit()

            session['user_name'] = user_name
            flash('You are successful login!')
            return redirect(url_for('index'))

    return render_template('registration.html', form=form)

@app.route('/authors')
def all_authors():
    authors_list = Authors.query.all()
    variables = {
        'title': 'Authors',
        'authors_list': sorted(authors_list,
                               key=lambda author: author.author_name)
    }

    return render_template('authors.html', **variables)

@app.route('/books')
def books():
    books = BookNames.query.all()

    books_list = []
    for book in books:
        url_authors = []
        id_book_author = Bookcase.query.filter_by(book_id=book.id).all()
        for ids in id_book_author:
            author_name = str(Authors.query.get(ids.authors_id).author_name)
            url_authors.append(author_name)

        books_list.append({book: url_authors})

    variables = {
        'title': 'Books',
        'books_list': sorted(books_list,
                             key=lambda book: book.keys()[0].book_name)
    }

    return render_template('books.html', **variables)

@app.route('/<author>/', methods=['GET', 'POST'])
def author_books(author):
    #Check for a nonexistent author
    if not nonexistent_author(author):
        return redirect(url_for('index'))

    author_id = Authors.query.filter_by(author_name=author).first().id
    id_book_author = Bookcase.query.filter_by(authors_id=author_id).all()

    auhtor_books = []
    for ids in id_book_author:
        auhtor_books.append(
            BookNames.query.filter_by(id=ids.book_id).first().book_name)

    form = AddBook(request.form)
    if request.method == 'POST' and form.validate() and check_login():
        book_name = request.form['book_name']
        insert_book_to_db(author, book_name)

    variables = {'author': author,
                 'auhtor_books': auhtor_books,
                 'form': form
                 }
    return render_template('author_page.html', **variables)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if not check_login():
        flash('Only authorised user can add book. Please, login.', 'error')
        return redirect(url_for('login'))

    author = ''
    form = AddBook(request.form)

    if request.method == 'POST' and form.validate():
        book_name = request.form['book_name']
        author = request.form['author_name']

        insert_book_to_db(author, book_name)
        flash('Book %s added to author %s.' % (book_name, author))
        return redirect(url_for('books'))

    variables = {'author': author,
                 'form': form
                 }
    return render_template('add_book.html', **variables)

@app.route('/delete_book', methods=['GET', 'POST'])
def delete_book():
    if not check_login():
        flash('Only authorised user can delete book. Please, login.', 'error')
        return redirect(url_for('login'))

    author = ''
    form = DeleteBook(request.form)

    if request.method == 'POST' and form.validate():
        book_name = request.form['book_name']
        book = BookNames.query.filter_by(book_name=book_name).first()
        if book:
            #Delete book dependency in Bookcase table
            id_book_author = Bookcase.query.filter_by(book_id=book.id).all()
            for ids in id_book_author:
                db_session.delete(ids)
                db_session.commit()

            #Delete book in BookNames table
            db_session.delete(book)
            db_session.commit()
            flash('Book "%s" successful delete.' % book_name)
            return redirect(url_for('books'))
        else:
            flash('No such book %s.' % book_name)

    variables = {'form': form}
    return render_template('delete_book.html', **variables)