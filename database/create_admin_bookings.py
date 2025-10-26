"""
Create sample bookings for admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db_connection
import random
from datetime import datetime, timedelta


def generate_booking_number():
    """Generate a unique booking number"""
    import time
    # Add timestamp and random to ensure uniqueness
    timestamp = int(time.time() * 1000) % 1000000
    random_num = random.randint(100, 999)
    return f"BK{timestamp}{random_num}"


def get_all_screenings():
    """Get all screenings"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT screening_id, ticket_price FROM screenings")
        screenings = cursor.fetchall()
        cursor.close()
        conn.close()
        return screenings
    except Exception as e:
        print(f"Error getting screenings: {e}")
        if conn:
            conn.close()
        return []


def get_available_seats_for_screening(screening_id):
    """Get available seats for a screening"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        # Get hall_id for this screening
        cursor.execute("SELECT hall_id FROM screenings WHERE screening_id = %s", (screening_id,))
        hall_result = cursor.fetchone()
        
        if not hall_result:
            cursor.close()
            conn.close()
            return []
        
        hall_id = hall_result[0]
        
        # Get booked seats for this screening
        cursor.execute("""
            SELECT DISTINCT seat_id 
            FROM seat_bookings sb
            JOIN bookings b ON sb.booking_id = b.booking_id
            WHERE b.screening_id = %s
        """, (screening_id,))
        booked_seats = {row[0] for row in cursor.fetchall()}
        
        # Get all active seats for this hall
        cursor.execute("""
            SELECT seat_id FROM seats 
            WHERE hall_id = %s AND is_active = TRUE
        """, (hall_id,))
        all_seats = [row[0] for row in cursor.fetchall()]
        
        # Return available seats
        available_seats = [seat_id for seat_id in all_seats if seat_id not in booked_seats]
        
        cursor.close()
        conn.close()
        return available_seats
    except Exception as e:
        print(f"Error getting available seats: {e}")
        if conn:
            conn.close()
        return []


def create_admin_bookings():
    """Create sample bookings for admin user"""
    conn = get_db_connection()
    if not conn:
        print("Database connection failed")
        return
    
    try:
        cursor = conn.cursor()
        
        # Get admin user IDs (user_id 1007 for Leo, user_id 1005 for admin)
        admin_user_ids = [1007, 1005]
        
        # Get all screenings
        screenings = get_all_screenings()
        if not screenings:
            print("No screenings found")
            cursor.close()
            conn.close()
            return
        
        print(f"Creating bookings for admin users...")
        
        booking_count = 0
        
        for user_id in admin_user_ids:
            # Each admin makes 8-12 bookings
            num_bookings = random.randint(8, 12)
            
            for _ in range(num_bookings):
                # Select a random screening
                screening_id, ticket_price = random.choice(screenings)
                
                # Get available seats for this screening
                available_seats = get_available_seats_for_screening(screening_id)
                
                if not available_seats:
                    continue
                
                # Random number of tickets (2-4)
                num_tickets = random.randint(2, 4)
                
                # Check if enough seats available
                if len(available_seats) < num_tickets:
                    continue
                
                # Select random seats
                selected_seats = random.sample(available_seats, num_tickets)
                
                # Generate booking number
                booking_number = generate_booking_number()
                
                # Calculate total amount (ticket_price * num_tickets)
                total_amount = float(ticket_price) * num_tickets
                
                # Admin bookings are always confirmed and paid
                booking_status = 'confirmed'
                payment_status = 'paid'
                
                # Random booking date (within last month)
                days_ago = random.randint(1, 30)
                booking_date = datetime.now() - timedelta(days=days_ago)
                
                # Insert booking
                cursor.execute("""
                    INSERT INTO bookings (user_id, screening_id, booking_number, num_tickets,
                                        total_amount, booking_status, payment_status, booking_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING booking_id
                """, (user_id, screening_id, booking_number, num_tickets, total_amount,
                      booking_status, payment_status, booking_date))
                
                booking_id = cursor.fetchone()[0]
                
                # Insert seat bookings
                for seat_id in selected_seats:
                    cursor.execute("""
                        INSERT INTO seat_bookings (booking_id, seat_id)
                        VALUES (%s, %s)
                    """, (booking_id, seat_id))
                
                booking_count += 1
                
                if booking_count % 5 == 0:
                    conn.commit()
                    print(f"Created {booking_count} admin bookings...")
        
        # Final commit
        conn.commit()
        print(f"\nSuccessfully created {booking_count} bookings for admin users!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating bookings: {e}")
        if conn:
            conn.rollback()
            conn.close()


if __name__ == '__main__':
    print("Creating sample bookings for admin users...")
    create_admin_bookings()

