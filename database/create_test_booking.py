"""
Create a test booking that starts soon (for testing cancellation policy)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db_connection
from datetime import datetime, timedelta
import random


def generate_booking_number():
    """Generate a unique booking number"""
    import time
    timestamp = int(time.time() * 1000) % 1000000
    random_num = random.randint(100, 999)
    return f"BK{timestamp}{random_num}"


def create_test_booking():
    """Create a test booking that starts in less than 2 hours"""
    conn = get_db_connection()
    if not conn:
        print("Database connection failed")
        return
    
    try:
        cursor = conn.cursor()
        
        # Get admin user_id
        cursor.execute("SELECT user_id FROM users WHERE username = 'admin'")
        admin_user = cursor.fetchone()
        if not admin_user:
            print("Admin user not found")
            cursor.close()
            conn.close()
            return
        
        user_id = admin_user[0]
        
        # Create a test screening that starts in 1 hour (within the cancellation window)
        screening_datetime = datetime.now() + timedelta(hours=1, minutes=30)
        
        # Get or create a movie
        cursor.execute("SELECT movie_id FROM movies LIMIT 1")
        movie_result = cursor.fetchone()
        if not movie_result:
            print("No movies found")
            cursor.close()
            conn.close()
            return
        
        movie_id = movie_result[0]
        
        # Get a cinema
        cursor.execute("SELECT cinema_id FROM cinemas LIMIT 1")
        cinema_result = cursor.fetchone()
        cinema_id = cinema_result[0]
        
        # Get a hall
        cursor.execute("SELECT hall_id FROM cinema_halls WHERE cinema_id = %s LIMIT 1", (cinema_id,))
        hall_result = cursor.fetchone()
        if not hall_result:
            print("No halls found")
            cursor.close()
            conn.close()
            return
        
        hall_id = hall_result[0]
        
        # Create screening that starts in 1.5 hours
        start_time = screening_datetime.time()
        end_time = (screening_datetime + timedelta(hours=2)).time()
        
        cursor.execute("""
            INSERT INTO screenings (movie_id, cinema_id, hall_id, screening_date, start_time, end_time, 
                                 ticket_price, screening_type, language, subtitles)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING screening_id
        """, (movie_id, cinema_id, hall_id, screening_datetime.date(), start_time, end_time,
              25.00, 'Standard', 'English', 'English'))
        
        screening_id = cursor.fetchone()[0]
        
        # Get available seats
        cursor.execute("SELECT seat_id FROM seats WHERE hall_id = %s AND is_active = TRUE LIMIT 2", (hall_id,))
        seats = [row[0] for row in cursor.fetchall()]
        
        if len(seats) < 2:
            print("Not enough available seats")
            cursor.close()
            conn.close()
            return
        
        # Create booking
        booking_number = generate_booking_number()
        num_tickets = 2
        total_amount = 25.00 * num_tickets
        
        cursor.execute("""
            INSERT INTO bookings (user_id, screening_id, booking_number, num_tickets,
                                total_amount, booking_status, payment_status, booking_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING booking_id
        """, (user_id, screening_id, booking_number, num_tickets, total_amount,
              'confirmed', 'paid', datetime.now()))
        
        booking_id = cursor.fetchone()[0]
        
        # Insert seat bookings
        for seat_id in seats:
            cursor.execute("""
                INSERT INTO seat_bookings (booking_id, seat_id)
                VALUES (%s, %s)
            """, (booking_id, seat_id))
        
        conn.commit()
        print(f"Successfully created test booking:")
        print(f"  Booking ID: {booking_id}")
        print(f"  Booking Number: {booking_number}")
        print(f"  Screening starts at: {screening_datetime.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Time until screening: ~1.5 hours (within cancellation window)")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating test booking: {e}")
        if conn:
            conn.rollback()
            conn.close()


if __name__ == '__main__':
    print("Creating test booking for admin user...")
    create_test_booking()

