"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
from model import User, Photo, Transaction
from server import app, connect_to_db
import crud
from config import db

os.system('dropdb photos')
os.system('createdb photos')

def reset_db():
    """Drop existing database and create new one with current model"""
    os.system('dropdb photos')
    os.system('createdb photos')
    
    with app.app_context():
        connect_to_db(app, echo=False)
        db.create_all()

    print('Reset db complete!')

users_in_db = []
def seed_users():
    email = 'code@yvonneyeh.com'
    username = 'yvonneyeh'
    password = 'test'
    first_name = 'Yvonne'
    last_name = 'Yeh'
    yy = crud.create_user(email, username, password, first_name, last_name)
    users_in_db.append(yy)
    print(users_in_db)

photos_in_db = []
titles = ['Blue Doge', 'Think Doge', 'Yellow Doge', 'Relax Doge', 'Black Doge', 'Happy Doge']
img_url = ['https://res.cloudinary.com/yvonneyeh/image/upload/v1620240466/m6vksxzmpkabkijyjf1i.jpg',
        'https://res.cloudinary.com/yvonneyeh/image/upload/v1620242245/f49ifnpfjfsiptvvirpt.jpg',
        'https://res.cloudinary.com/yvonneyeh/image/upload/v1620242287/zbmbiojelc9qpoaekhbk.jpg',
        'https://res.cloudinary.com/yvonneyeh/image/upload/v1620242312/w97l5kqxuhknosubbj7f.jpg',
        'https://res.cloudinary.com/yvonneyeh/image/upload/v1620242331/ah7m6qz0y8pipwxw8hwv.jpg',
        'https://res.cloudinary.com/yvonneyeh/image/upload/v1620242351/hm46f2n24ts0pi8vv8sl.jpg']

def seed_photos():
    for i in range(5):
        title = titles[i]
        desc = 'Doge Photo'
        price = 99.99
        img_url = img_url[i]
        new_photo = create_photo(title, desc, price, img_url)
        photos_in_db.append(new_photo)
    print(photos_in_db)


#---------------------------------------------------------------------#

if __name__ == '__main__':
    # app = server.create_app()
    # app.run(host='0.0.0.0', debug=True)
    # connect_to_db(app, echo=False)

    # Create tables if not already created. Delete all existing entries in tables.
    with app.app_context():
        db.create_all()
        print("Tables created. Deleting all rows and creating new seed data.")

        # Seed sample data into the database
        seed_users()

    print("Sample data seeded")