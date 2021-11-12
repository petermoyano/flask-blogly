"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension, toolbar
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Add_testing_data

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
    print(new_user.id)
    return redirect(f"/users/{new_user.id}")

@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Shows information about the given user."""
    # Have a button to edit the user.    
    current_user = User.query.get_or_404(user_id)
    return render_template("details.html", current_user=current_user)


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
    all_users = User.query.all()
    return render_template("home.html", all_users=all_users)


@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    flash(f"You've succesfully deleted {User.first_name} {User.last_name} from the database!")
    db.session.delete(user)
    db.session.commit()
    all_users = User.query.all()
    return render_template("home.html", all_users=all_users)


