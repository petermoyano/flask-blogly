"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension, toolbar
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.debug = DebugToolbarExtension
app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)

##################### PART ONE USERS ##################################

@app.route("/")
def list_all_users():
    """Shows all current users with links to view details of each one."""
    #Have a link here to the add-user form. 
    all_users = User.query.all()
    all_tags = Tag.query.all()
    return render_template("home.html", all_users=all_users, all_tags=all_tags)

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
    current_user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", current_user=current_user)



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


############### PART TWO: POSTS #######################


@app.route("/users/<int:user_id>/posts/new")
def show_form_add_post(user_id):
    """Shows form page for a specific user to add a post"""
    current_user = User.query.filter(User.id == user_id).one()
    all_tags = Tag.query.all()
    return render_template("new_post.html", current_user=current_user, all_tags=all_tags)

@app.route("/users/<int:user_id>/posts/new", methods = ['POST'])
def handle_new_post(user_id):
    """Commits new post to the db, and re-direct to the users detail page"""
    title = request.form["title"]
    content = request.form["content"]
    tag = request.form.getlist("tag")

    new_post = Post(title=title, content=content, user=user_id )
    
    db.session.add(new_post)
    db.session.commit()

    for t in tag:
        t_id = Tag.query.filter_by(name = t).one().id
        print(t_id)
        new_post_tag = PostTag(post_id=new_post.id, tag_id=t_id)
        db.session.add(new_post_tag)
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


########################## PART THREE: TAGS ############################


@app.route("/tags")
def get_tags():
    """Lists all tags, with links to the tag detail page."""
    all_tags = Tag.query.all()
    return render_template("all_tags.html", all_tags=all_tags)

@app.route("/tags/<int:tag_id>", methods=['POST'])
def get_details_tag(tag_id):
    """Lists all tags, with links to the tag detail page."""

    return redirect()

@app.route("/tags/<int:tag_id>")
def get_one_tag(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    current_tag =  Tag.query.filter(Tag.id == tag_id).one()
    return render_template("show_tag.html", current_tag=current_tag)

@app.route("/tags/new")
def new_tag():
    """Shows a form to add a new tag."""
    all_tags = Tag.query.all()
    return render_template("new_tag_form.html", all_tags=all_tags)

@app.route("/tags/new", methods=['POST'])
def handle_new_tag():
    """Shows a form to add a new tag."""
    name = request.form["name"]

    new_tag = Tag(name = name)
    db.session.add(new_tag)
    db.session.commit()
    flash("New tag, succesfully created!")

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag(tag_id):
    """Show edit form for a tag"""
    return render_template("edit_tag.html", tag_id=tag_id)

@app.route("/tags/<int:tag_id>/edit", methods=['POST'])
def handle_edit_tag(tag_id):
    """Process add form, adds tag, and redirect to tag list."""
    new_name = request.form["name"]
    print(new_name)
    tag = Tag.query.get_or_404(tag_id)
    print(tag.name)
    tag.name = new_name
    db.session.commit()
    flash("Tag succesfully edited!")
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=['POST'])
def delete_tag(tag_id):
    """Delets a tag"""
    current_tag = Tag.query.get_or_404(tag_id)
    db.session.delete(current_tag)
    db.session.commit()
    flash("Tag succesfully deleted!")
    return redirect("/tags")
