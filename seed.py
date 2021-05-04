"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import crud
import model
import server

# os.system('dropdb photos')
# os.system('createdb photos')

def reset_db():
    """Drop existing database and create new one with current model"""
    os.system('dropdb photos')
    os.system('createdb photos')

    model.connect_to_db(server.app, echo=False)
    model.db.create_all()

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

#---------------------------------------------------------------------#

if __name__ == '__main__':
    model.connect_to_db(server.app, echo=False)

    # Create tables if not already created. Delete all existing entries in tables.
    model.db.create_all()
    print("Tables created. Deleting all rows and creating new seed data.")

    # Seed sample data into the database
    seed_users()

    print("Sample data seeded")