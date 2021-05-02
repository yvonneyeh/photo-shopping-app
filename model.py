"""Models for photo shopping app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """An app user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
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
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    img_url = db.Column(db.String, nullable=False)

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
    
    user = db.relationship('User', backref='transactions')
    photo = db.relationship('Photo', backref=db.backref('transactions', order_by=photo_id))
        
    def __repr__(self):
        return f'<Transaction trans_id={self.trans_id} photo_id={self.photo_id} ${self.buy_price}>'



# -------------------- CONNECT TO DATABASE -------------------- #


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

