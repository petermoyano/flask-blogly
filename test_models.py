from app import app
from unittest import TestCase
from models import db, User, Post, Add_seed_posts, Add_seed_users, Delete_tables, DEFAULT_IMG

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///test_blogly_db'

db.drop_all()
db.create_all()



class converterTestCase(TestCase):

    def setUp(self):
        """Populate tables with data"""
        Add_seed_users()
        Add_seed_posts()
    def tearDown(self):
        """Empty all tables and reset session"""
        db.session.rollback()
        Delete_tables()

    def test_populate_db(self):
        """Tests for user info in db when updated"""
        with app.test_client() as client:
            self.assertEqual(User.query.get(1).first_name, 'Paul')
            self.assertEqual(User.query.get(1).last_name, 'McCartney')
            self.assertEqual(Post.query.get(1).title, 'Post1')
            self.assertEqual(Post.query.get(1).content, 'This is the first post!')

    def test_edit_user(self):
        """Tests for user info in db when updated"""
        with app.test_client() as client:
            res = client.post("/users/1/edit", data={'first_name':'Pedro', 'last_name':'Moyano', 'image_url':DEFAULT_IMG})
            self.assertEqual(User.query.get(1).first_name, 'Pedro')
            self.assertEqual(User.query.get(1).last_name, 'Moyano')

    def test_edit_post(self):
        """Tests for user info in db when updated"""
        with app.test_client() as client:
            res=client.post("/posts/2/edit", data={'title':'new title', 'content':'new content'})
            self.assertEqual(Post.query.get(2).title, 'new title')
            self.assertEqual(Post.query.get(2).content, 'new content')

    def test_new_post(self):
        """Tests presence of new post in db when created"""
        with app.test_client() as client:
            res=client.post("/users/2/posts/new", data={'title':'new title2', 'content':'new content2'})
            self.assertEqual(Post.query.get(4).title, 'new title2')
            self.assertEqual(Post.query.get(4).content, 'new content2')
    
#    def test_new_user(self):
#        """Tests presence of new user in db when created"""
#        with app.test_client() as client:
#            res=client.post("/users/new", data={'first_name':'Peter', 'last_name':'Bailish', 'image_url':DEFAULT_IMG})
#            self.assertEqual(User.query.get(4).first_name, 'Peter')
#            self.assertEqual(User.query.get(4).last_name, 'Bailish')