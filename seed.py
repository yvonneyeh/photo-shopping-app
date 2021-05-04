"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb photos')
os.system('createdb photos')


#---------------------------------------------------------------------#

if __name__ == '__main__':
    model.connect_to_db(server.app, echo=False)

    # Create tables if not already created. Delete all existing entries in tables.
    model.db.create_all()
    print("Tables created. Deleting all rows and creating new seed data.")

    # Seed sample data into the database

    print("Sample data seeded")