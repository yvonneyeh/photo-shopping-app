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

#---------------------------------------------------------------------#

# if __name__ == '__main__':
#     model.connect_to_db(server.app, echo=False)

#     # Create tables if not already created. Delete all existing entries in tables.
#     model.db.create_all()
#     print("Tables created. Deleting all rows and creating new seed data.")

#     # Seed sample data into the database

#     print("Sample data seeded")