"""
Create sample bookings data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db_connection
import random
from datetime import datetime, timedelta


def generate_booking_number():
    """Generate a unique booking number"""
    from datetime import datetime
    import random
    import time
    # Add timestamp and random to ensure uniqueness
    timestamp = int(time.time() * 1000) % 1000000
    random_num = random.randint(100, 999)
    return f"BK{timestamp}{random_num}"


def get_random_users(count):
    """Get random user IDs"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users ORDER BY RANDOM() LIMIT %s", (count,))
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return user_ids
    except Exception as e:
        print(f"Error getting users: {e}")
        if conn:
            conn.close()
        return []


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


def create_sample_bookings():
    """Create sample bookings for users"""
    conn = get_db_connection()
    if not conn:
        print("Database connection failed")
        return
    
    try:
        cursor = conn.cursor()
        
        # Get random users (about 50 users)
        user_ids = get_random_users(50)
        if not user_ids:
            print("No users found")
            cursor.close()
            conn.close()
            return
        
        # Get all screenings
        screenings = get_all_screenings()
        if not screenings:
            print("No screenings found")
            cursor.close()
            conn.close()
            return
        
        print(f"Creating bookings for {len(user_ids)} users...")
        
        booking_count = 0
        
        for user_id in user_ids:
            # Each user makes 2-5 bookings randomly
            num_bookings = random.randint(2, 5)
            
            for _ in range(num_bookings):
                # Select a random screening
                screening_id, ticket_price = random.choice(screenings)
                
                # Get available seats for this screening
                available_seats = get_available_seats_for_screening(screening_id)
                
                if not available_seats:
                    continue  # Skip if no available seats
                
                # Random number of tickets (1-4)
                num_tickets = random.randint(1, 4)
                
                # Check if enough seats available
                if len(available_seats) < num_tickets:
                    continue
                
                # Select random seats
                selected_seats = random.sample(available_seats, num_tickets)
                
                # Generate booking number
                booking_number = generate_booking_number()
                
                # Calculate total amount (ticket_price * num_tickets)
                total_amount = float(ticket_price) * num_tickets
                
                # Random booking status (mostly confirmed)
                booking_status = random.choice(['confirmed', 'confirmed', 'confirmed', 'pending'])
                
                # Random payment status
                payment_status = random.choice(['paid', 'paid', 'paid', 'unpaid']) if booking_status == 'confirmed' else 'unpaid'
                
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
                
                # Commit every 10 bookings
                if booking_count % 10 == 0:
                    conn.commit()
                    print(f"Created {booking_count} bookings...")
        
        # Final commit
        conn.commit()
        print(f"\nSuccessfully created {booking_count} bookings!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating bookings: {e}")
        if conn:
            conn.rollback()
            conn.close()


if __name__ == '__main__':
    print("Creating sample bookings...")
    create_sample_bookings()

