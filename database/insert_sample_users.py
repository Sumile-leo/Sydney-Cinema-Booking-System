"""
Insert 1000 sample users into database
"""

import psycopg
import bcrypt
import random
import string

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'cinema_db',
    'user': 'postgres',
    'password': 'postgres'
}

# Sample first names and last names
FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
    'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
    'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
    'Kenneth', 'Carol', 'Kevin', 'Amanda', 'Brian', 'Dorothy', 'George', 'Melissa'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
    'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris',
    'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen',
    'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green',
    'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter'
]

USER_TYPES = ['customer', 'staff', 'admin']

def generate_username(first_name, last_name, index):
    """Generate unique username"""
    base = f"{first_name.lower()}.{last_name.lower()}"
    if index > 0:
        return f"{base}{index}"
    return base

def generate_email(username):
    """Generate email from username"""
    return f"{username}@example.com"

def generate_phone():
    """Generate random phone number"""
    return f"04{random.randint(10000000, 99999999)}"

def generate_password():
    """Generate random password"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def insert_users():
    """Insert 1000 sample users"""
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        print("Inserting 1000 users...")
        
        # Hash a default password for all users
        default_password = "password123"
        hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        users_inserted = 0
        username_counter = {}
        
        for i in range(1000):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            
            # Generate unique username
            base_username = f"{first_name.lower()}.{last_name.lower()}"
            if base_username in username_counter:
                username_counter[base_username] += 1
                username = f"{base_username}{username_counter[base_username]}"
            else:
                username_counter[base_username] = 0
                username = base_username
            
            email = generate_email(username)
            phone = generate_phone()
            
            # Assign user type (mostly customers, some staff, few admins)
            rand = random.random()
            if rand < 0.05:  # 5% admins
                user_type = 'admin'
            elif rand < 0.15:  # 10% staff
                user_type = 'staff'
            else:  # 85% customers
                user_type = 'customer'
            
            try:
                cursor.execute(
                    """INSERT INTO users (username, email, password, first_name, last_name, phone, user_type)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (username, email, hashed_password, first_name, last_name, phone, user_type)
                )
                users_inserted += 1
                
                if users_inserted % 100 == 0:
                    print(f"Inserted {users_inserted} users...")
                    
            except psycopg.IntegrityError:
                # Skip duplicate usernames/emails
                continue
        
        conn.commit()
        print(f"\nSuccessfully inserted {users_inserted} users!")
        print(f"\nDefault password for all users: {default_password}")
        
    except Exception as e:
        print(f"Error inserting users: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    insert_users()
