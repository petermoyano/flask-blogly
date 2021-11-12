"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.visitors import ReplacingCloningVisitor

db = SQLAlchemy()

DEFAULT_IMG = "https://www.freeiconspng.com/uploads/computer-user-icon-15.png"


def connect_db(app):
    """From within app.py we import this function to connect our Flask app to our db"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Represents a table with basic users information"""
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default=DEFAULT_IMG)



def Add_testing_data():
    """Fills db with some data for testing"""
    Paul = User(first_name = 'Paul', last_name = 'McCartney', image_url = 'https://www.freeiconspng.com/uploads/snapchat-logo-6.jpg')
    John = User(first_name = 'John', last_name = 'Lennon', image_url = 'https://www.freeiconspng.com/uploads/citizen-icon-7.jpg')
    Ringo = User(first_name = 'Ringo', last_name = 'Star', image_url = 'https://www.freeiconspng.com/uploads/bus-driver-icon-png-9.png')
    db.session.add(Paul)
    db.session.add(John)
    db.session.add(Ringo)
    db.session.commit()