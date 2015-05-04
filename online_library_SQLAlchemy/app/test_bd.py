import sqlalchemy
from models import Users, Authors, BookNames, Bookcase
from database import db_session
from database import Base
from database import init_db, clear_db


usrs = [{'name': 'Vlad', 'password': 'vlad', 'email': 'v@v.com'},
        {'name': 'Dima', 'password': '12345', 'email': 'd@d.com'},
        {'name': 'Kate', 'password': '67890', 'email': 'k@k.com'},
        {'name': 'Valeriy', 'password': 'qwert', 'email': 'va@va.com'}
        ]

book_author = {'Learning Python': 'Mark Lutz',
               'Flask Web Development': 'Miguel Grinberg',
               'Dead Souls': 'Nikolai Gogol',
               'Eugene Onegin': 'Alexander Pushkin',
               'War and Peace': 'Lev Tolstoy',
               'Anna Karenina ': 'Lev Tolstoy',
               'When We Met': 'Molly McAdams, A.L. Jackson, Christina Lee',
               'Hard to Be a God': 'Arkady Strugatsky, Boris Strugatsky',
               'Roadside Picnic': 'Arkady Strugatsky, Boris Strugatsky'
               }

def add_users_to_db(usrs):
    for us in usrs:
        user = Users(name=us['name'],
                     password=us['password'],
                     email=us['email'])
        db_session.add(user)
        try:
            db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            print('User %s is already in database' % us)
            db_session.rollback()

def add_books_authors_to_db(book_author):
    for book, v in book_author.items():
        b = BookNames(book_name=book)
        db_session.add(b)
        try:
            db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            print('Book %s is already in database' % book)
            db_session.rollback()

        for author in v.split(', '):
            a = Authors(author_name=author)
            db_session.add(a)
            try:
                db_session.commit()
            except Exception:
                print('Author %s is already in database' % author)
                db_session.rollback()

def make_dependency_between_books_authors(book_author):
    for book, v in book_author.items():
        b = BookNames.query.filter_by(book_name=book).first()
        for author in v.split(', '):
            a = Authors.query.filter_by(author_name=author).first()
            book_case = Bookcase(book_id=b.id, authors_id=a.id)
            db_session.add(book_case)
            try:
                db_session.commit()
            except Exception:
                print('Bookcase %s: %s is already in database' % (
                    b.book_name, a.author_name))
                db_session.rollback()

def main():
    clear_db(Base.metadata.tables.keys())
    init_db()

    add_users_to_db(usrs)
    add_books_authors_to_db(book_author)
    make_dependency_between_books_authors(book_author)

    print('New tables: %s' % Base.metadata.tables.keys())
    print('Users: %s' % Users.query.all())
    print('Authors: %s' % Authors.query.all())
    print('Books: %s' % BookNames.query.all())
    print('Bookcase: %s' % Bookcase.query.all())

if __name__ == '__main__':
    main()