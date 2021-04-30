from model import db, User, Photo, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- USERS -------------------- #

def create_user(email, username, password):
    """Create and return a new user."""

    user = User(email = email,
                username = username,
                password = generate_password_hash(user_password, method='sha256'))

    db.session.add(user)
    db.session.commit()

    return user


def get_all_users():
    """Return all users."""

    return User.query.all()


def get_user_by_email(email):
    """Find a user by their email address."""

    return User.query.filter(User.email == email).first()


def get_user_by_id(user_id):
    """Return user given their ID"""

    return User.query.filter(User.user_id == user_id).first() 


def delete_user(user_id):
    """Delete a user from the database."""

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return

# -------------------- PHOTOS -------------------- #



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()