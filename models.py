"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
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

class Post(db.Model):
    """Minimalist Post"""
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.String(500), nullable = False)
    created_at = db.Column(db.DateTime, default= datetime.datetime.now, nullable = False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)


class Tag(db.Model):
    """Represents tags for listing posts topics"""
    __tablename__='tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable = False)
    posts = db.relationship('Post', secondary = 'posts_tags', backref='tags')

class PostTag(db.Model):
    """Many to many relationship between tags, posts and users"""
    __tablename__="posts_tags"
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)




def Add_seed_users():
    """Fills db with some data for testing"""
    Paul = User(first_name = 'Paul', last_name = 'McCartney', image_url = 'https://www.freeiconspng.com/uploads/snapchat-logo-6.jpg')
    John = User(first_name = 'John', last_name = 'Lennon', image_url = 'https://www.freeiconspng.com/uploads/citizen-icon-7.jpg')
    Ringo = User(first_name = 'Ringo', last_name = 'Star', image_url = 'https://www.freeiconspng.com/uploads/bus-driver-icon-png-9.png')
    db.session.add(Paul)
    db.session.add(John)
    db.session.add(Ringo)
    db.session.commit()

def Add_seed_posts():
    """Fills db with some posts for testing"""
    post1 = Post(title = "Post1", content = "This is the first post!", user = 1)
    post2 = Post(title = "Post2", content = "This is the second post! Huurray!", user = 2)
    post3 = Post(title = "Post3", content = "This is the third post! Silver medal!", user = 3)
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.commit()

def Add_seed_tags():
    """Fills db with some tags for testing"""
    tag1 = Tag(name = "Soccer")
    tag2 = Tag(name = "Funny")
    tag3 = Tag(name = "Amazing")
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.commit()

def Add_seed_posttags():
    """Fill posts_tags with some data for testing"""
    post_tag1 = PostTag(post_id=1, tag_id=1)
    post_tag2 = PostTag(post_id=2, tag_id=2)
    post_tag3 = PostTag(post_id=3, tag_id=3)
    post_tag4 = PostTag(post_id=1, tag_id=2)
    db.session.add(post_tag1)
    db.session.add(post_tag2)
    db.session.add(post_tag3)
    db.session.add(post_tag4)
    db.session.commit()

def Delete_tables():
    """Emptie users table"""
    db.drop_all()
    db.create_all()
    User.query.delete()
    Post.query.delete()