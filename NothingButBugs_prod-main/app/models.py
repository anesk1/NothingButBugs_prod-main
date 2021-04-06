from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), nullable = False)
    author = db.Column(db.String(64), nullable = False)
    isbn = db.Column(db.Integer, nullable = False)
    condition = db.Column(db.String(128))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reserved = db.Column(db.Boolean, nullable = False)

    def __repr__(self):
        return self.title + " by: " + self.author

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), nullable = False)
    email = db.Column(db.String(64), nullable = False)
    password_hash = db.Column(db.String(256), unique = True)
    books = db.relationship('Book', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.
@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))
