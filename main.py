# Importing bcrypt lbrary
import bcrypt

# Function to generate a secure password hash
def generate_hash(psw):

    # Converting password from string to bytes
    byte_psw = psw.encode('utf-8')

    # Generating a random salt
    salt = bcrypt.gensalt

    # Creating hash using password and salt
    hash = bcrypt.hash.pw(byte_psw, salt)

    # Converting bytes to string for storage
    return hash.decode('utf-8')

# Function to verify password with stored hash
def is_valid_hash(psw, hash):

    # Converting stored hash to bytes
    hash_ = hash.encode('utf-8')
    
    # Converting password entered to bytes
    byte_psw = psw.encode('utf-8')

    # Checking whether the password matches the hash
    is_valid = bcrypt.checkpw(byte_psw,hash_)

    return is_valid