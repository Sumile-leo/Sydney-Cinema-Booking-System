"""
Database configuration and connection
"""

import psycopg

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'cinema_db',
    'user': 'postgres',
    'password': 'postgres'
}


def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


# User-related database operations
def get_user_by_username(username):
    """Get user by username"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, username, password, email, first_name, last_name, phone, user_type FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        print(f"Error getting user: {e}")
        if conn:
            conn.close()
        return None


def check_username_or_email_exists(username, email):
    """Check if username or email already exists"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM users WHERE username = %s OR email = %s",
            (username, email)
        )
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking user existence: {e}")
        if conn:
            conn.close()
        return False


def create_user(username, email, password, first_name, last_name, phone, user_type='customer'):
    """Create a new user"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO users (username, email, password, first_name, last_name, phone, user_type)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (username, email, password, first_name, last_name, phone, user_type)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        if conn:
            conn.close()
        return False


def verify_password(username, password):
    """Verify user password (plain text comparison)"""
    user = get_user_by_username(username)
    if not user:
        return None
    
    # Plain text password comparison
    if user[2] == password:  # user[2] is password field
        return user  # Return user data if password matches
    return None


# Cinema-related database operations
def get_all_cinemas():
    """Get all cinemas"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT cinema_id, cinema_name, address, suburb, postcode, phone, email, facilities, created_at, updated_at, is_active FROM cinemas ORDER BY cinema_name"
        )
        cinemas = cursor.fetchall()
        cursor.close()
        conn.close()
        return cinemas
    except Exception as e:
        print(f"Error getting cinemas: {e}")
        if conn:
            conn.close()
        return []


def get_cinema_by_id(cinema_id):
    """Get cinema by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT cinema_id, cinema_name, address, suburb, postcode, phone, email, facilities, created_at, updated_at, is_active FROM cinemas WHERE cinema_id = %s",
            (cinema_id,)
        )
        cinema = cursor.fetchone()
        cursor.close()
        conn.close()
        return cinema
    except Exception as e:
        print(f"Error getting cinema: {e}")
        if conn:
            conn.close()
        return None


def create_cinema(cinema_name, address, suburb, postcode, phone, email, facilities, is_active=True):
    """Create a new cinema"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO cinemas (cinema_name, address, suburb, postcode, phone, email, facilities, is_active)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (cinema_name, address, suburb, postcode, phone, email, facilities, is_active)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating cinema: {e}")
        if conn:
            conn.close()
        return False
