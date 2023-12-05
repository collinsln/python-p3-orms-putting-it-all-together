# dog.py

import sqlite3

# Database connection setup
CONN = sqlite3.connect("dogs.db")
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # Will be set when the record is saved to the database

    @staticmethod
    def create_table():
        # Create a "dogs" table if it doesn't exist
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        ''')
        CONN.commit()

    @staticmethod
    def drop_table():
        # Drop the "dogs" table if it exists
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        # Save the Dog instance to the database
        CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid  # Set the id after insertion

    @staticmethod
    def create(name, breed):
        # Create a new Dog instance and save it to the database
        dog = Dog(name, breed)
        dog.save()
        return dog

    @staticmethod
    def new_from_db(row):
        # Create a Dog instance from a database row
        dog = Dog(row[1], row[2])
        dog.id = row[0]
        return dog

    @staticmethod
    def get_all():
        # Get all Dog instances from the database
        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()
        return [Dog.new_from_db(row) for row in rows]

    @staticmethod
    def find_by_name(name):
        # Find a Dog instance by name in the database
        CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        if row:
            return Dog.new_from_db(row)
        else:
            return None

    @staticmethod
    def find_by_id(id):
        # Find a Dog instance by id in the database
        CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        if row:
            return Dog.new_from_db(row)
        else:
            return None

    def update(self):
        # Update the corresponding database record with the current attributes
        CURSOR.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?", (self.name, self.breed, self.id))
        CONN.commit()

    @staticmethod
    def find_or_create_by(name, breed):
        # Find a Dog instance by name and breed, or create it if it doesn't exist
        existing_dog = Dog.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return Dog.create(name, breed)