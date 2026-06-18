# Importing bcrypt lbrary
import bcrypt

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

# Function to register a new user
def register_user():

    name = input('Enter your name: > ')
    password = input('Enter your password: > ')

    # Generating hashed password using Week 1 function
    hash_password = generate_hash(password)

    # Store username and hashed password in file
    with open('users.txt', 'a') as f:
        f.write(f'{name},{hash_password}\n')
    print('User successfully registered!')

# Function to login a user
def login_user():

    # Asking user for login details
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')

    try:
        # Opening database file in read mode
        with open('users.txt', 'r') as f:
            users = f.readlines()

        # Looping through each user record
        for user in users:
            
            # Removing newline character and splitting username & hash
            user_name, user_hash = user.strip().split(',')

            # Checking username and verifying password hash
            if name == user_name and is_valid_hash(password, user_hash):

                # Successful authentication
                return True
        # Login fail
        return False

    except FileNotFoundError:
        # Error handling for no users existing
        print("No users found. Please register first.")
        return False
    
def main():

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