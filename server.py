"""Server for photo shopping app."""

import os
import crud
from model import User, Photo, Transaction
from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for
from jinja2 import StrictUndefined
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api
import stripe
from config import db


DATABASE_URL = os.environ['DATABASE_URL']
SECRET_KEY = os.environ['SECRET_KEY']

CLOUD_NAME = os.environ['CLOUD_NAME']
CLOUD_API_KEY = os.environ['CLOUD_API_KEY']
CLOUD_API_SECRET = os.environ['CLOUD_API_SECRET']

STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLIC_KEY = os.environ['STRIPE_PUBLIC_KEY']
stripe_keys = {
  'stripe_secret_key': os.environ['STRIPE_SECRET_KEY'],
  'stripe_public_key': os.environ['STRIPE_PUBLIC_KEY']
}
stripe.api_key = stripe_keys['stripe_secret_key']

# app = create_app()
# db = SQLAlchemy()
# db.init_app(app)

# def create_app():
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.jinja_env.undefined = StrictUndefined
db_uri='postgresql:///photos'
echo = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_ECHO'] = echo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
    # return app

# db.create_all()

cloudinary.config( 
    cloud_name = CLOUD_NAME, 
    api_key = CLOUD_API_KEY, 
    api_secret =  CLOUD_API_SECRET
)

# -------------------- HOMEPAGE -------------------- #

# @app.route('/')
# def homepage():
#     """Show the homepage."""

#     return render_template('index.html')

@app.route('/')
def index():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1InT6KKZcbzeiZVtW5WQSr2k',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return render_template('index.html', 
        checkout_session_id = session['id'], 
        checkout_public_key = STRIPE_PUBLIC_KEY
    )


# @app.route('/')
# def homepage():
#     """Show the homepage."""

#     photos = crud.get_all_photos()

#     return render_template('index.html',
#                             photos=photos)

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

# -------------------- ACCOUNT ROUTES -------------------- #

@app.route("/account")
def display_account_details():
    """Display a user's info & purchased photos"""

    # Query database to find Photo objects purchased by user
    if "user_id" in session:
        user_id = session.get("user_id")
        photos = crud.get_users_photos(user_id)

        return render_template("account.html", photos=photos)

    else:
        flash("You must be logged in to access that page", 'warning')

        return redirect("/login")

# -------------------- PHOTO ROUTES -------------------- #

@app.route('/photos')
def all_photos_page():
    """View all photos."""
    
    photos = crud.get_photos()
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1InT6KKZcbzeiZVtW5WQSr2k',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    
    return render_template('photos.html', photos=photos, 
        checkout_session_id = session['id'], 
        checkout_public_key = STRIPE_PUBLIC_KEY
    )

    # if "user_id" in session:
    #     photos = crud.get_photos()
    #     return render_template('photos.html', photos=photos)
    # else:
    #     flash('Please login or create an account.')
    #     return render_template('login.html')


@app.route('/photos/<int:photo_id>')
def show_photo(photo_id):
    """Show details for a photo."""

    photo = crud.get_photo_by_id(photo_id)
    # title = crud.get_photo_title_by_id(photo_id)
    # desc = 
    # price = 
    # img_url = 

    return render_template("photo_details.html",
                            photo=photo)

    # return render_template("photo_details.html",
    #                         photo=photo,
    #                         title=title,
    #                         desc=desc,
    #                         price=price,
    #                         img_url=img_url)


@app.route('/api/photos', methods=["POST"])
def api_photo():
    """Upload a photo."""

    title = request.form.get('title')
    desc = request.form.get('desc')
    price = request.form.get('price')
    img_url = request.form.get('img_url')

    post = crud.create_photo(photo_id, title, desc, price, img_url)

    return jsonify({'status': 'ok'})


# -------------------- SHOPPING ROUTES -------------------- #

@app.route('/buy')
def buy():
    """View Buy page."""

    if "user_id" in session:
        user_id = session.get("user_id")
        
        return render_template('buy.html')

    else:
        flash("You must be logged in to access that page", 'warning')

        return redirect("/login")


@app.route('/sell')
def sell():
    """View Sell page."""

    return render_template('sell.html')

    # if "user_id" in session:
    #     user_id = session.get("user_id")
        
    #     return render_template('sell.html')

    # else:
    #     flash("You must be logged in to access that page", 'warning')

    #     return redirect("/login")
    


@app.route('/upload', methods=['POST'])
def upload_photo():
    """Uploads user's image to Cloudinary"""

    file = request.files.get('new-img-upload')
    title = request.form['new-img-title']
    desc = request.form['new-img-desc']
    price = request.form['new-img-price']

    response = cloudinary.uploader.upload(file)
    img_url = response['secure_url']

    new_photo = crud.create_photo(title=title, desc=desc, price=price, img_url=img_url)
    
    if new_photo:
        flash("Image uploaded!", "success")
        return redirect('/')


@app.route('/cart')
def shopping_cart():
    """View Shopping Cart page."""

    return render_template('cart.html')


@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1InT6KKZcbzeiZVtW5WQSr2k',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': stripe_keys['stripe_public_key']
    }


@app.route('/thanks')
def thanks():
    """View Thank You page after successful transaction."""

    return render_template('thanks.html')


@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}

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

def connect_to_db(app, db_uri='postgresql:///photos', echo=True):
    """Connect the database to Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = echo
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    print('Connected to the db!')

if __name__ == '__main__':
    # app = create_app()
    app.run(host='0.0.0.0', debug=True)
