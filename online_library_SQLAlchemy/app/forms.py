from wtforms import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(Form):
    name = StringField('Name', [
        Length(min=3, max=50, message='''User name must be min. 3 max. 50
         letters''')
    ])

    password = PasswordField('Password', [DataRequired()])


class Registration(LoginForm):
    email = StringField('E-mail', [Email(message='Invalid email address.')])
    password = PasswordField('Password', [
        EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('Confirm password')


class Book(Form):
    book_name = StringField('Book name', [Length(min=1, max=200)])
    author_name = StringField('Author name', [Length(min=1, max=200)])
