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


# Movie-related database operations
def get_all_movies():
    """Get all movies"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT movie_id, title, description, genre, duration_minutes, release_date, 
                      director, "cast", language, subtitles, poster_url, created_at, updated_at, is_active 
               FROM movies ORDER BY release_date DESC"""
        )
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
        return movies
    except Exception as e:
        print(f"Error getting movies: {e}")
        if conn:
            conn.close()
        return []


def get_movie_by_id(movie_id):
    """Get movie by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT movie_id, title, description, genre, duration_minutes, release_date, 
                      director, "cast", language, subtitles, poster_url, created_at, updated_at, is_active 
               FROM movies WHERE movie_id = %s""",
            (movie_id,)
        )
        movie = cursor.fetchone()
        cursor.close()
        conn.close()
        return movie
    except Exception as e:
        print(f"Error getting movie: {e}")
        if conn:
            conn.close()
        return None


def create_movie(title, description, genre, duration_minutes, release_date, director, cast, language, subtitles, is_active=True):
    """Create a new movie"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO movies (title, description, genre, duration_minutes, release_date, 
                                   director, cast, language, subtitles, is_active)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (title, description, genre, duration_minutes, release_date, director, cast, language, subtitles, is_active)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating movie: {e}")
        if conn:
            conn.close()
        return False


# Cinema Hall-related database operations
def get_cinema_halls_by_cinema(cinema_id):
    """Get all cinema halls for a specific cinema"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT hall_id, cinema_id, hall_name, hall_type, total_rows, seats_per_row, 
                      total_seats, screen_size, sound_system, created_at, updated_at 
               FROM cinema_halls WHERE cinema_id = %s ORDER BY hall_name""",
            (cinema_id,)
        )
        halls = cursor.fetchall()
        cursor.close()
        conn.close()
        return halls
    except Exception as e:
        print(f"Error getting cinema halls: {e}")
        if conn:
            conn.close()
        return []


def get_cinema_hall_by_id(hall_id):
    """Get cinema hall by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT hall_id, cinema_id, hall_name, hall_type, total_rows, seats_per_row, 
                      total_seats, screen_size, sound_system, created_at, updated_at 
               FROM cinema_halls WHERE hall_id = %s""",
            (hall_id,)
        )
        hall = cursor.fetchone()
        cursor.close()
        conn.close()
        return hall
    except Exception as e:
        print(f"Error getting cinema hall: {e}")
        if conn:
            conn.close()
        return None


def create_cinema_hall(cinema_id, hall_name, hall_type=None, total_rows=None,
                        seats_per_row=None, total_seats=None, screen_size=None,
                        sound_system=None):
    """Create a new cinema hall"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO cinema_halls (cinema_id, hall_name, hall_type, total_rows, seats_per_row, 
                                       total_seats, screen_size, sound_system)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (cinema_id, hall_name, hall_type, total_rows, seats_per_row,
             total_seats, screen_size, sound_system)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating cinema hall: {e}")
        if conn:
            conn.close()
        return False


# Seat-related database operations
def get_seats_by_hall(hall_id):
    """Get all seats for a specific hall"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT seat_id, hall_id, row_number, seat_number, seat_type, 
                      price_multiplier, is_active 
               FROM seats WHERE hall_id = %s ORDER BY row_number, seat_number""",
            (hall_id,)
        )
        seats = cursor.fetchall()
        cursor.close()
        conn.close()
        return seats
    except Exception as e:
        print(f"Error getting seats: {e}")
        if conn:
            conn.close()
        return []


def get_seat_by_id(seat_id):
    """Get seat by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT seat_id, hall_id, row_number, seat_number, seat_type, 
                      price_multiplier, is_active 
               FROM seats WHERE seat_id = %s""",
            (seat_id,)
        )
        seat = cursor.fetchone()
        cursor.close()
        conn.close()
        return seat
    except Exception as e:
        print(f"Error getting seat: {e}")
        if conn:
            conn.close()
        return None


def create_seats_for_hall(hall_id, total_rows, seats_per_row, seat_types=None):
    """Create all seats for a hall"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        seat_type = seat_types or {}
        
        for row in range(1, total_rows + 1):
            for seat in range(1, seats_per_row + 1):
                # Determine seat type based on row
                seat_type_value = seat_type.get(row, 'standard')
                price_multiplier = 1.00
                
                if seat_type_value == 'premium':
                    price_multiplier = 1.50
                elif seat_type_value == 'vip':
                    price_multiplier = 2.00
                
                cursor.execute(
                    """INSERT INTO seats (hall_id, row_number, seat_number, seat_type, 
                                         price_multiplier, is_active)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (hall_id, row, seat, seat_type_value, price_multiplier, True)
                )
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating seats for hall: {e}")
        if conn:
            conn.close()
        return False
