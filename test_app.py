from app import app
from unittest import TestCase
from models import db, User, Post, Add_seed_posts, Add_seed_users, Delete_tables, DEFAULT_IMG

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///test_blogly_db'
app.config['TESTING']=True # Turns errors into real Python errors
app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar'] # Avoid html of the debug toolbar

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

    def test_home(self):
        """Tests for status code and html content of response obtained by requesting to the root"""
        with app.test_client() as client:
            home = client.get("/")
            html = home.get_data(as_text = True)
            self.assertIn("<h1>Welcome to Peter's social network!</h1>", html)
            self.assertEqual(home.status_code, 200)

    def test_new_user(self):
        """Tests for status code and html content of response obtained by requesting to make a new user"""
        with app.test_client() as client:
            res = client.get("/users/new") 
            html = res.get_data(as_text = True)
            self.assertIn("<h1>New user form.</h1>", html)
            self.assertEqual(res.status_code, 200)

    def test_redirect_new_post(self):
        with app.test_client() as client:
            res=client.post("/users/2/posts/new", data={'title':'new title2', 'content':'new content2'})
            self.assertEqual(res.location, 'http://localhost/users/2')
            self.assertEqual(Post.query.get(4).title, 'new title2')
    
#    def test_redirect_new_user(self):
#        with app.test_client() as client:
#            res=client.post("/users/new", data={'first_name':'Peter', 'last_name':'Bailish', 'image_url':DEFAULT_IMG})
#            self.assertEqual(res.location, 'http://localhost/users/4')
    