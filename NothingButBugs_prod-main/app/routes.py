from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm
from app import db
from app.models import Book, User
import sys

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/Post_books')
def post():
    return render_template('Post_books.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Authenticated users are redirected to home page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Query DB for user by username
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Login failed', file=sys.stderr)
            return redirect(url_for('login'))
        # login_user is a flask_login function that starts a session
        login_user(user)
        print('Login successful', file=sys.stderr)
        return redirect(url_for('index'))
    return render_template('login.html', title = "Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/test')
def test():
    user = User(username = 'user', email = 'this@google.com')
    user.set_password('textswap')
    db.session.add(user)
    db.session.commit()

    user_obj = db.session.query(User).filter_by(username = 'user').first()
    b = Book(title = 'book title', author = 'book author', isbn = 1,
                condition = 'well read', user = user_obj, reserved = False)

    db.session.add(b)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/home')
def home():
    return render_template('home.html')
