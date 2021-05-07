from config import db
from model import User, Photo, Transaction
from datetime import date, datetime, timedelta

# from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- USERS -------------------- #

def create_user(email, username, password, first_name, last_name):
    """Create and return a new user."""

    user = User(email = email,
                username = username,
                password = password,
                # password = generate_password_hash(password, method='sha256'),
                first_name = first_name,
                last_name = last_name)

    db.session.add(user)
    db.session.commit()

    return user


def get_all_users():
    """Return all users."""

    return User.query.all()


def get_user_by_email(email):
    """Find a user by their email address."""

    return User.query.filter(User.email == email).first()


def get_user_by_username(username):
    """Return user given their username"""

    return User.query.filter(User.username == username).first() 


def get_user_by_id(user_id):
    """Return user given their ID"""

    return User.query.filter(User.user_id == user_id).first() 


def get_user_by_email_id(email, username):

    return User.query.filter((User.email == email) |
                             (User.username == username)).all()


def delete_user(user_id):
    """Delete a user from the database."""

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return

# -------------------- PHOTOS -------------------- #

def create_photo(title, desc, price, img_url):
    """Create and return a new photo."""

    photo = Photo(
            title = title,
            desc = desc,
            price = price,
            img_url = img_url)

    db.session.add(photo)
    db.session.commit()

    return photo


def get_photos():
    """Return all photos."""

    return Photo.query.all()


def get_all_photos():
    """Return all photos, sorted alphabetically"""

    return Photo.query.order_by(Photo.title).all()
    

def get_users_photos(user_id):
    """Query database to find Photo objects purchased by user"""

    photos = Transaction.query.filter((Transaction.user_id == user_id)
                                    & (Transaction.purchased.is_(True))).all()

    return photos


def get_photo_by_id(photo_id):
    """Return photos given its ID"""

    return Photo.query.filter(Photo.photo_id == photo_id).first()


def get_photo_by_title(title):
    """Return photos given its title"""

    return Photo.query.filter(Photo.title == title).first() 


def get_photo_id_by_title(title):
    """Return photo's ID given its title"""

    return db.session.query(Photo.photo_id).filter(Photo.title == title).first()


# -------------------- TRANSACTIONS -------------------- #

def create_transactions(photo_id, user_id, purchased=True):
    """Creates new transaction"""

    purchase_date = datetime.today()
    trans = Transaction(photo_id=photo_id, user_id=user_id, purchase_date=purchase_date, buy_price=buy_price, purchased=purchased)

    db.session.add(trans)
    db.session.commit()

    return trans


def get_all_trans():
    """Return all transactions."""

    return Transaction.query.order_by(Transaction.trans_id).all()


def get_trans_by_id(trans_id):
    """Return transaction given its ID"""

    return Transaction.query.filter(Transaction.trans_id == trans_id).first() 


def get_trans_by_photo_id(photo_id):
    """Return all transactions given its photo ID"""

    return Transaction.query.filter(Transaction.photo_id == photo_id).all() 

# -------------------- APP -------------------- #

# if __name__ == '__main__':
#     from server import app
#     connect_to_db(app)
#     db.create_all()