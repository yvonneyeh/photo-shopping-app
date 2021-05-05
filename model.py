"""Models for photo shopping app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db

# db = SQLAlchemy()

class User(db.Model):
    """An app user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    transaction = db.relationship('Transaction')


    def __repr__(self):
        """Show info about user."""

        return f"<User_id= {self.user_id} username= {self.username}>"


class Photo(db.Model):
    """A photo listing."""

    __tablename__ = "photos"

    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    img_url = db.Column(db.String, nullable=False)

    transaction = db.relationship('Transaction')

    def price_str(self):
        """Return price formatted as string $x.xx"""

        return "${:.2f}".format(self.price)

    def __repr__(self):
        return f"<Photo id= {self.photo_id}>"


class Transaction(db.Model):
    """A user's purchased photo."""

    __tablename__ = "transactions"

    trans_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.photo_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    purchase_date = db.Column(db.DateTime)
    buy_price = db.Column(db.Integer)
    purchased = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='transactions')
    photo = db.relationship('Photo', backref=db.backref('transactions', order_by=photo_id))
        
    def __repr__(self):
        return f'<Transaction trans_id={self.trans_id} photo_id={self.photo_id} ${self.buy_price}>'



# -------------------- CONNECT TO DATABASE -------------------- #

# # Call connect_to_db(app, echo=False) to prevent printing out all SQLAlchemy queries 
# def connect_to_db(flask_app, db_uri='postgresql:///photos', echo=False):
#     """Connect the database to Flask app."""
#     flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#     flask_app.config['SQLALCHEMY_ECHO'] = echo
#     flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#     db.app = flask_app
#     db.init_app(flask_app)
#     print('Connected to db!')

# # if __name__ == '__main__':
# #     from server import app    
# #     connect_to_db(app)
# #     db.create_all()
# #     print('Connected to db!')


# def connect_to_db(flask_app, db_uri='postgresql:///photos', echo=True):
#     """Connect the database to Flask app."""
#     flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#     flask_app.config['SQLALCHEMY_ECHO'] = echo
#     flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#     db.app = flask_app
#     db.init_app(flask_app)
#     print('Connected to the db!')

# def connect_to_db(app, db_uri='postgresql:///photos', echo=True):
#     """Connect the database to Flask app."""
#     app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#     app.config['SQLALCHEMY_ECHO'] = echo
#     # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#     db.init_app(app)
#     print('Connected to the db!')

# if __name__ == '__main__':
#     # from server import app    
#     connect_to_db(app, echo=False)
#     db.create_all()
#     print('Connected to db!')