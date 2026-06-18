# Importing bcrypt lbrary
import bcrypt
import sqlite3
import pandas as pd
import os

conn = sqlite3.connect('data/project_data.db')

# Function to generate a secure password hash
def generate_hash(psw):

    # Converting password from string to bytes
    byte_psw = psw.encode('utf-8')

    # Generating a random salt
    salt = bcrypt.gensalt()

    # Creating hash using password and salt
    hash = bcrypt.hashpw(byte_psw, salt)

    # Converting bytes to string for storage
    return hash.decode('utf-8')

# VIDEO 2
# Function to verify password with stored hash
def is_valid_hash(psw, hash):

    # Converting stored hash to bytes
    hash_ = hash.encode('utf-8')
    
    # Converting password entered to bytes
    byte_psw = psw.encode('utf-8')

    # Checking whether the password matches the hash
    is_valid = bcrypt.checkpw(byte_psw,hash_)

    return is_valid

def create_user_table():
    cur = conn.cursor()

    sql = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL
    );
    '''

    cur.execute(sql)
    conn.commit()

# Function to register a new user
def register_user():

    name = input('Enter your name: > ')
    password = input('Enter your password: > ')

    # Generating hashed password using Week 1 function
    hash_password = generate_hash(password)

    cur = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''

    try:
        cur.execute(sql, (name, hash_password))
        conn.commit()
        print('User successfully registered!')

    except sqlite3.IntegrityError:
        print("Username already exists. Try another one.")


# Function to login a user
def login_user():

    # Asking user for login details
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')

    cur = conn.cursor()

    sql = 'SELECT password_hash FROM users WHERE username = ?'
    cur.execute(sql, (name,))
    result = cur.fetchone()

    if result is None:
        return False

    stored_hash = result[0]

    if is_valid_hash(password, stored_hash):
        return True

    return False

# Function to retrieve all users
def get_all_users():

    cur = conn.cursor()
    cur.execute('SELECT * FROM users')

    return cur.fetchall()

# Function to retrieve one user

def get_user(name):

    cur = conn.cursor()
    cur.execute(

        'SELECT * FROM users WHERE username = ?',
        (name,)

    )
    return cur.fetchone()

# Function to update username

def update_user(old_name, new_name):

    cur = conn.cursor()
    cur.execute(
        'UPDATE users SET username = ? WHERE username = ?',
        (new_name, old_name)

    )

    conn.commit()
    print('User updated successfully!')

# Function to delete user

def delete_user(user_name):

    cur = conn.cursor()
    cur.execute(

        'DELETE FROM users WHERE username = ?',
        (user_name,)

    )
    conn.commit()
    print('User deleted successfully!')

# Function to migrate cyber incidents CSV

def migrate_cyber_incidents():

    data = pd.read_csv('data/cyber_incidents.csv')
    data.to_sql(
        'cyber_incidents',
        conn,

        if_exists='replace',
        index=False

    )

    print('Cyber incidents migrated successfully!')

# Function to migrate datasets metadata CSV

def migrate_datasets_metadata():

    data = pd.read_csv('data/datasets_metadata.csv')
    data.to_sql(
        'datasets_metadata',
        conn,
        if_exists='replace',
        index=False

    )

    print('Datasets metadata migrated successfully!')

# Function to retrieve cyber incidents table

def get_all_cyber_incidents():
    sql = 'SELECT * FROM cyber_incidents'
    return pd.read_sql(sql, conn)

def main():

    create_user_table()
    # Loop runs until user exits
    while True:

        # Displaying menu options
        print('1. To Register\n2. To Log in\n3. To Exit')

        # Getting user choice
        choice = input(': > ')

        # Handling registration option
        if choice == '1':
            register_user()

        # Handling login option
        elif choice == '2':

            # Displaying result based on authentication outcome
            if login_user():
                print('Login successful!')
            else:
                print('Incorrect login.')

        # Exiting program safely
        elif choice == '3':
            print('Goodbye!')
            break

        # Handling invalid input
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    main()