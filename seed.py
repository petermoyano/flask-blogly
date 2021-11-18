from models import User, Post, Tag, Add_seed_tags, Add_seed_posts, Add_seed_users, Add_seed_posttags
from app import app, db

db.drop_all()
db.create_all()

Add_seed_users()
Add_seed_posts()
Add_seed_tags()
Add_seed_posttags()
