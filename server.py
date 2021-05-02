"""Server for photo shopping app."""

import os
import crud
from model import connect_to_db, User, Photo, Transaction
from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for
from jinja2 import StrictUndefined
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api



DATABASE_URL = os.environ['DATABASE_URL']
SECRET_KEY = os.environ['SECRET_KEY']
CLOUD_API_SECRET = os.environ['CLOUD_API_SECRET']


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.jinja_env.undefined = StrictUndefined

# -------------------- HOMEPAGE -------------------- #

@app.route('/')
def homepage():
    """Show the homepage."""

    return render_template('index.html')


# -------------------- REGISTRATION ROUTES -------------------- #

@app.route("/register")
def reg_form():
    """Display registration form"""

    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_user():
    """Creates new user if user does not yet exist."""

    username = request.form.get("username")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate if username or email already exists in users table in database
    if not crud.get_user_by_email_id(email, username):

        user = User(username=username, email=email, first_name=first_name, last_name=last_name, password=password)

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("User created!", "success")

        return redirect("/login")
    
    # If account does exist, flash message to indicating email or username exists.
    else:
        if User.query.filter_by(email=email).all():
            flash(f"There's already an account associated with {email}", "warning")
        else:
            flash(f"The username {username} is already taken", "warning")

        return redirect("/register")


# -------------------- LOGIN ROUTES -------------------- #

@app.route('/login')
def login():
    """View Login page."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def log_in_user():
    """Login user and redirect to homepage."""

    username = request.form.get('username')
    password = request.form.get('password')

    user_object = crud.get_user_by_username(username)

    if user_object != None:
        if password == user_object.password != None:
            session['username'] = user_object.username
            session['user_id'] = user_object.user_id
            flash('Logged in!', 'success')
        else:
            flash('Incorrect password', 'warning')
            return redirect("/login")
    else:
        flash('Username does not exist. Please register for an account.', 'warning')
        return redirect("/register")

    return redirect('/')

# -------------------- PHOTO ROUTES -------------------- #

@app.route('/photos')
def photos():
    """View Photos page."""

    return render_template('photos.html')

# -------------------- SHOPPING ROUTES -------------------- #

@app.route('/buy')
def buy():
    """View Buy page."""

    return render_template('buy.html')


@app.route('/sell')
def sell():
    """View Sell page."""

    return render_template('sell.html')


@app.route('/cart')
def shopping_cart():
    """View Shopping Cart page."""

    return render_template('cart.html')

# -------------------- ACCOUNT ROUTES -------------------- #

@app.route('/account')
def account():
    """View Account page."""

    return render_template('account.html')

# -------------------- AJAX / JSON ROUTES -------------------- #

@app.route("/user/loggedin")
def is_user_logged_in():
    """Check if user is logged in"""

    if "user_id" in session:
        return "true"

    else:
        return "false"



# -------------------- RUN -------------------- #

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
