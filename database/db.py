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


# Screening-related database operations
def get_all_screenings():
    """Get all screenings"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT screening_id, movie_id, cinema_id, hall_id, screening_date,
                      start_time, end_time, ticket_price, screening_type,
                      language, subtitles, created_at, updated_at
               FROM screenings ORDER BY screening_date, start_time"""
        )
        screenings = cursor.fetchall()
        cursor.close()
        conn.close()
        return screenings
    except Exception as e:
        print(f"Error getting screenings: {e}")
        if conn:
            conn.close()
        return []


def get_screenings_by_movie(movie_id):
    """Get screenings for a specific movie"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT screening_id, movie_id, cinema_id, hall_id, screening_date,
                      start_time, end_time, ticket_price, screening_type,
                      language, subtitles, created_at, updated_at
               FROM screenings WHERE movie_id = %s 
               ORDER BY screening_date, start_time""",
            (movie_id,)
        )
        screenings = cursor.fetchall()
        cursor.close()
        conn.close()
        return screenings
    except Exception as e:
        print(f"Error getting screenings for movie: {e}")
        if conn:
            conn.close()
        return []


def get_screenings_by_cinema(cinema_id):
    """Get screenings for a specific cinema"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT screening_id, movie_id, cinema_id, hall_id, screening_date,
                      start_time, end_time, ticket_price, screening_type,
                      language, subtitles, created_at, updated_at
               FROM screenings WHERE cinema_id = %s 
               ORDER BY screening_date, start_time""",
            (cinema_id,)
        )
        screenings = cursor.fetchall()
        cursor.close()
        conn.close()
        return screenings
    except Exception as e:
        print(f"Error getting screenings for cinema: {e}")
        if conn:
            conn.close()
        return []


def get_screening_by_id(screening_id):
    """Get screening by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT screening_id, movie_id, cinema_id, hall_id, screening_date,
                      start_time, end_time, ticket_price, screening_type,
                      language, subtitles, created_at, updated_at
               FROM screenings WHERE screening_id = %s""",
            (screening_id,)
        )
        screening = cursor.fetchone()
        cursor.close()
        conn.close()
        return screening
    except Exception as e:
        print(f"Error getting screening: {e}")
        if conn:
            conn.close()
        return None


# Booking-related database operations
def get_bookings_by_user(user_id):
    """Get all bookings for a user"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT booking_id, user_id, screening_id, booking_number,
                      num_tickets, total_amount, booking_status, payment_status,
                      booking_date, created_at, updated_at
               FROM bookings WHERE user_id = %s 
               ORDER BY booking_date DESC""",
            (user_id,)
        )
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
        return bookings
    except Exception as e:
        print(f"Error getting bookings for user: {e}")
        if conn:
            conn.close()
        return []


def get_booking_by_id(booking_id):
    """Get booking by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT booking_id, user_id, screening_id, booking_number,
                      num_tickets, total_amount, booking_status, payment_status,
                      booking_date, created_at, updated_at
               FROM bookings WHERE booking_id = %s""",
            (booking_id,)
        )
        booking = cursor.fetchone()
        cursor.close()
        conn.close()
        return booking
    except Exception as e:
        print(f"Error getting booking: {e}")
        if conn:
            conn.close()
        return None


def get_seats_by_booking(booking_id):
    """Get all seats for a booking with enhanced info"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT seats.seat_id, seats.row_number, seats.seat_number, seats.seat_type
               FROM seat_bookings
               JOIN seats ON seat_bookings.seat_id = seats.seat_id
               WHERE seat_bookings.booking_id = %s
               ORDER BY seats.row_number, seats.seat_number""",
            (booking_id,)
        )
        seats = cursor.fetchall()
        cursor.close()
        conn.close()
        return seats
    except Exception as e:
        print(f"Error getting seats for booking: {e}")
        if conn:
            conn.close()
        return []


def get_bookings_with_details(user_id):
    """Get all bookings for a user with screening and seat details"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT b.booking_id, b.user_id, b.screening_id, b.booking_number,
                      b.num_tickets, b.total_amount, b.booking_status, b.payment_status,
                      b.booking_date, b.created_at, b.updated_at,
                      s.screening_date, s.start_time, s.end_time,
                      m.title as movie_title,
                      c.cinema_name, c.address, c.suburb
               FROM bookings b
               JOIN screenings s ON b.screening_id = s.screening_id
               JOIN movies m ON s.movie_id = m.movie_id
               JOIN cinemas c ON s.cinema_id = c.cinema_id
               WHERE b.user_id = %s
               ORDER BY b.booking_date DESC""",
            (user_id,)
        )
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
        return bookings
    except Exception as e:
        print(f"Error getting bookings with details: {e}")
        if conn:
            conn.close()
        return []


def can_cancel_booking(booking_id):
    """Check if a booking can be cancelled (at least 2 hours before screening)"""
    from datetime import datetime, timedelta
    
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        # Get screening date and time for this booking
        cursor.execute("""
            SELECT b.booking_status, s.screening_date, s.start_time
            FROM bookings b
            JOIN screenings s ON b.screening_id = s.screening_id
            WHERE b.booking_id = %s
        """, (booking_id,))
        
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return False, "Booking not found"
        
        booking_status, screening_date, start_time = result
        
        # Check if already cancelled
        if booking_status == 'cancelled':
            cursor.close()
            conn.close()
            return False, "Booking already cancelled"
        
        # Check if can be cancelled (2 hours before screening)
        screening_datetime = datetime.combine(screening_date, start_time)
        current_datetime = datetime.now()
        time_diff = screening_datetime - current_datetime
        
        # Must be at least 2 hours before screening
        if time_diff < timedelta(hours=2):
            cursor.close()
            conn.close()
            return False, f"Cannot cancel within 2 hours of screening. Screening starts in {time_diff.total_seconds() / 60:.0f} minutes."
        
        cursor.close()
        conn.close()
        return True, "Booking can be cancelled"
    except Exception as e:
        print(f"Error checking cancellation eligibility: {e}")
        if conn:
            conn.close()
        return False, f"Error: {str(e)}"


def cancel_booking(booking_id):
    """Cancel a booking"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        # Update booking status to cancelled
        cursor.execute("""
            UPDATE bookings 
            SET booking_status = 'cancelled', updated_at = CURRENT_TIMESTAMP
            WHERE booking_id = %s AND booking_status != 'cancelled'
        """, (booking_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return success
    except Exception as e:
        print(f"Error cancelling booking: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False


def get_booking_user_id(booking_id):
    """Get the user_id of a booking"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM bookings WHERE booking_id = %s", (booking_id,))
        result = cursor.fetchone()
        user_id = result[0] if result else None
        cursor.close()
        conn.close()
        return user_id
    except Exception as e:
        print(f"Error getting booking user_id: {e}")
        if conn:
            conn.close()
        return None
