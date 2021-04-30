"""Models for photo shopping app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """An app user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    photo = db.relationship('Photo')

    def __repr__(self):
        """Show info about user."""

        return f"<User_id= {self.user_id} user_name= {self.user_name}>"

class Photo(db.Model):
    """A photo listing."""

    __tablename__ = "photos"

    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    img_url = db.Column(db.String, nullable=False)

    user = db.relationship('User')

    def __repr__(self):
        return f"<Photo id= {self.photo_id}>"


# ---------- CONNECT TO DATABASE ---------- #


def connect_to_db(flask_app, db_uri='postgresql:///photos', echo=True):
    """Connect the database to Flask app."""
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app    
    # Call connect_to_db(app, echo=False) to prevent printing out all SQLAlchemy queries 
    connect_to_db(app)
    db.create_all()
    print('Connected to db!')

