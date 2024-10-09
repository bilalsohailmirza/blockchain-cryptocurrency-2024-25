import hashlib
import json
import os

# File paths for JSON storage
USERS_DB_FILE = 'users_db.json'
TOKEN_BALANCES_FILE = 'token_balances.json'
MEMBERSHIP_DB_FILE = 'membership_db.json'

# Load data from JSON files
def load_data():
    global users_db, token_balances, membership_db
    
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, 'r') as f:
            users_db = json.load(f)
    
    if os.path.exists(TOKEN_BALANCES_FILE):
        with open(TOKEN_BALANCES_FILE, 'r') as f:
            token_balances = json.load(f)
            # Convert values to integers
            token_balances = {k: int(v) for k, v in token_balances.items()}
    
    if os.path.exists(MEMBERSHIP_DB_FILE):
        with open(MEMBERSHIP_DB_FILE, 'r') as f:
            membership_db = set(json.load(f))

# Save data to JSON files
def save_data():
    with open(USERS_DB_FILE, 'w') as f:
        json.dump(users_db, f, indent=4)
    
    with open(TOKEN_BALANCES_FILE, 'w') as f:
        json.dump(token_balances, f, indent=4)
    
    with open(MEMBERSHIP_DB_FILE, 'w') as f:
        json.dump(list(membership_db), f, indent=4)

# Initialize or load existing data
def initialize():
    global users_db, token_balances, membership_db
    users_db = {}
    token_balances = {}
    membership_db = set()
    load_data()

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user with username, password and initial tokens
def register_user(username, password, initial_tokens):
    if username in users_db:
        raise ValueError("User already exists.")
    hashed_password = hash_password(password)
    users_db[username] = hashed_password
    token_balances[username] = initial_tokens
    save_data()

# Add a user to the membership database
def add_to_membership(username):
    membership_db.add(username)
    save_data()

# Burn tokens from a user's balance
def burn_tokens(username, tokens_to_burn):
    if username in token_balances and token_balances[username] >= tokens_to_burn:
        token_balances[username] -= tokens_to_burn
        save_data()
        return True
    return False

# Authenticate a user using username, password and tokens burnt
def authenticate_user(username, password, tokens_to_burn):
    if username not in users_db:
        return False
    
    hashed_password = hash_password(password)
    if users_db[username] != hashed_password:
        return False
    
    if not burn_tokens(username, tokens_to_burn):
        return False
    
    if username not in membership_db:
        return False
    
    return True

# Example usage
if __name__ == "__main__":
    initialize()

    try:
        # Register users
        register_user("alice", "password123", 100)
        register_user("bob", "mypassword", 50)

        # Add users to membership
        add_to_membership("alice")

        # Burn tokens and authenticate
        print(authenticate_user("alice", "password123", 10))  # True
        print(authenticate_user("bob", "mypassword", 10))     # False (not in membership)
        print(authenticate_user("alice", "wrongpassword", 10)) # False (incorrect password)
        print(authenticate_user("alice", "password123", 200))  # False (insufficient tokens)
    except ValueError as e:
        print(e)
