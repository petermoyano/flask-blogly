"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension, toolbar
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post, Add_seed_users, Add_seed_posts

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.debug = DebugToolbarExtension
app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def list_all_users():
    """Shows all current users with links to view details of each one."""
    #Have a link here to the add-user form. 
    all_users = User.query.all()
    return render_template("home.html", all_users=all_users)

@app.route("/users/new")
def show_new_user_form():
    """Show an add form for users"""
    return render_template("new_user_form.html")

@app.route("/users/new", methods=['POST'])
def process_new_user_form():
    """Process the add form, adding a new user and going back to /users"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] if request.form["image_url"] else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    
    return redirect(f"/users/{new_user.id}")

@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Shows information about the given user."""
    # Have a button to edit the user.    
    current_user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter(Post.user == user_id).all()

    return render_template("list_user_posts.html", current_user=current_user, user_posts=user_posts)


@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """Show form to edit a user"""
    return render_template("edit_user.html", user_id=user_id)



@app.route("/users/<int:user_id>/edit", methods=['POST'])
def edit_user(user_id):
    """Process the edit form, returning the user to the /users page."""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] if request.form["image_url"] else None

    current_user = User.query.get_or_404(user_id)
    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.image_url = image_url

    db.session.commit()
    flash("User has been edited!")
#Have a button to get to to delete the user.
#Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
    return redirect("/")


@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    flash(f"You've succesfully deleted {User.first_name} {User.last_name} from the database!")
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

############### PART TWO #######################
@app.route("/users/<int:user_id>/posts/new")
def show_form_add_post(user_id):
    """Shows form page for a specific user to add a post"""
    current_user = User.query.filter(User.id == user_id).one()
    return render_template("new_post.html", current_user=current_user)

@app.route("/users/<int:user_id>/posts/new", methods = ['POST'])
def handle_new_post(user_id):
    """Commits new post to the db, and re-direct to the users detail page"""
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user=user_id )
    db.session.add(new_post)
    db.session.commit()
    current_user = User.query.filter(User.id == user_id).one()
    flash(f"You have succesfully added a post to the db, {current_user.first_name}!")
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show a post. Also Show buttons to edit and delete the post."""
    current_post = Post.query.filter(Post.id == post_id).one()
    return render_template("show_post.html", current_post=current_post)


@app.route("/posts/<int:post_id>/edit", methods=['POST'])
def edit_post(post_id):
    """Handle Editing of a post and save it to the db. Redirect back to the post view."""
    title = request.form["title"]
    content = request.form["content"]

    current_post = Post.query.get(post_id)

    current_post.title = title
    current_post.content = content

    db.session.add(current_post)
    db.session.commit()

    #Not sure if it's necesary to "reload" current_post because it's been updated
    current_post = Post.query.get(post_id)

    flash("You have succesfully edited the post!")

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/edit") 
def show_edit_page(post_id):
    """Show form to edit a post and to cancel (back to user page)."""
    post_id = post_id
    post = Post.query.filter(Post.id == post_id).one()
    title = post.title
    content = post.content
    return render_template("edit_post.html", post_id=post_id, title=title, content=content)

@app.route("/posts/<int:post_id>/delete", methods=['DELETE', 'POST'])
def delete_post(post_id):
    """Handle post deletion and redirect to the root route"""
    current_post = Post.query.get_or_404(post_id)
    current_user_id = current_post.user
    current_user = User.query.get_or_404(current_user_id)
    flash(f"You've succesfully deleted {current_post.title} from the database!")
    db.session.delete(current_post)
    db.session.commit()
    user_posts = Post.query.filter(current_post.user == current_user_id).all()
    return redirect(f"/users/{current_user_id}")

