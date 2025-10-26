"""
Main routes
"""

from flask import render_template, redirect, url_for, session, flash, request, abort
from backend.services import CinemaService, MovieService, BookingService
from database.db import cancel_booking, get_booking_user_id, can_cancel_booking, get_screening_by_id, get_cinema_hall_by_id, get_seats_by_hall, get_cinema_by_id
from backend.models.screening import Screening
from backend.models.cinema_hall import CinemaHall
from backend.models.movie import Movie
from backend.models.cinema import Cinema


def register_main_routes(app):
    """Register main routes"""
    
    @app.route('/')
    def index():
        """Homepage with latest movies"""
        # Get latest movies (limit to 3 for homepage)
        all_movies = MovieService.get_all_movies()
        latest_movies = [m for m in all_movies if m.is_active][:3]
        
        return render_template('index.html', movies=latest_movies)

    @app.route('/bookings')
    def bookings():
        """My Bookings page"""
        if 'user_id' not in session:
            flash('Please login to view your bookings', 'error')
            return redirect(url_for('login'))
        
        # Get user's bookings with detailed information
        bookings = BookingService.get_user_bookings_with_seats(session['user_id'])
        
        return render_template('bookings.html', bookings=bookings)
    
    @app.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
    def cancel_booking_route(booking_id):
        """Cancel a booking"""
        if 'user_id' not in session:
            flash('Please login to cancel bookings', 'error')
            return redirect(url_for('login'))
        
        # Verify that the booking belongs to the current user
        booking_user_id = get_booking_user_id(booking_id)
        if booking_user_id != session['user_id']:
            flash('You can only cancel your own bookings', 'error')
            return redirect(url_for('bookings'))
        
        # Check if booking can be cancelled (2 hours before screening)
        can_cancel, message = can_cancel_booking(booking_id)
        
        if not can_cancel:
            flash(message, 'error')
            return redirect(url_for('bookings'))
        
        # Cancel the booking
        success = cancel_booking(booking_id)
        
        if success:
            flash('Booking cancelled successfully', 'success')
        else:
            flash('Failed to cancel booking. It may have already been cancelled.', 'error')
        
        return redirect(url_for('bookings'))

    @app.route('/book/<int:screening_id>')
    def book_ticket(screening_id):
        """Book ticket page with seat selection"""
        if 'user_id' not in session:
            flash('Please login to book tickets', 'error')
            return redirect(url_for('login'))
        
        # Get screening
        screening_data = get_screening_by_id(screening_id)
        if not screening_data:
            abort(404)
        
        screening = Screening.from_db_row(screening_data)
        
        # Get movie
        movie_data = MovieService.get_movie_by_id(screening.movie_id)
        if not movie_data:
            abort(404)
        
        # Get cinema
        cinema_data = get_cinema_by_id(screening.cinema_id)
        if not cinema_data:
            abort(404)
        
        cinema = Cinema.from_db_row(cinema_data)
        
        # Get hall
        hall_data = get_cinema_hall_by_id(screening.hall_id)
        if not hall_data:
            abort(404)
        
        hall = CinemaHall.from_db_row(hall_data)
        
        # Get seats for this hall
        seats_data = get_seats_by_hall(screening.hall_id)
        seats = []
        for seat_row in seats_data:
            seats.append({
                'seat_id': seat_row[0],  # seat_id
                'row_number': seat_row[2],  # row_number (index 2 after hall_id)
                'seat_number': seat_row[3],  # seat_number (index 3)
                'seat_type': seat_row[4] if len(seat_row) > 4 else 'standard',  # seat_type (index 4)
                'price_multiplier': float(seat_row[5]) if len(seat_row) > 5 and isinstance(seat_row[5], (int, float)) else 1.0,  # price_multiplier (index 5)
                'is_active': seat_row[6] if len(seat_row) > 6 else True  # is_active (index 6)
            })
        
        # Get already booked seats for this screening
        from database.db import get_db_connection
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT sb.seat_id 
                    FROM seat_bookings sb
                    JOIN bookings b ON sb.booking_id = b.booking_id
                    WHERE b.screening_id = %s AND b.booking_status != 'cancelled'
                """, (screening_id,))
                booked_seats = {row[0] for row in cursor.fetchall()}
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error getting booked seats: {e}")
                booked_seats = set()
                if conn:
                    conn.close()
        else:
            booked_seats = set()
        
        return render_template('book_ticket.html', 
                              screening=screening, 
                              movie=movie_data, 
                              cinema=cinema,
                              hall=hall,
                              seats=seats,
                              booked_seats=booked_seats)
    
    @app.route('/create_booking', methods=['POST'])
    def create_booking():
        """Create a new booking"""
        if 'user_id' not in session:
            flash('Please login to create bookings', 'error')
            return redirect(url_for('login'))
        
        screening_id = request.form.get('screening_id')
        seat_ids_str = request.form.get('seat_ids')
        
        if not screening_id or not seat_ids_str:
            flash('Invalid booking data', 'error')
            return redirect(url_for('bookings'))
        
        # Parse seat IDs
        seat_ids = [int(sid) for sid in seat_ids_str.split(',') if sid.strip()]
        
        if not seat_ids:
            flash('Please select at least one seat', 'error')
            return redirect(url_for('book_ticket', screening_id=screening_id))
        
        if len(seat_ids) > 5:
            flash('You can only book up to 5 seats', 'error')
            return redirect(url_for('book_ticket', screening_id=screening_id))
        
        # Create booking in database
        from database.db import get_db_connection
        import time
        import random
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed', 'error')
            return redirect(url_for('book_ticket', screening_id=screening_id))
        
        try:
            cursor = conn.cursor()
            
            # Get screening price
            cursor.execute("SELECT ticket_price FROM screenings WHERE screening_id = %s", (screening_id,))
            ticket_price = cursor.fetchone()[0]
            
            # Calculate total amount
            total_amount = len(seat_ids) * float(ticket_price)
            
            # Generate booking number
            booking_number = f"BK{int(time.time() * 1000) % 1000000}{random.randint(100, 999)}"
            
            # Create booking
            cursor.execute("""
                INSERT INTO bookings (user_id, screening_id, booking_number, num_tickets,
                                    total_amount, booking_status, payment_status)
                VALUES (%s, %s, %s, %s, %s, 'confirmed', 'paid')
                RETURNING booking_id
            """, (session['user_id'], screening_id, booking_number, len(seat_ids), total_amount))
            
            booking_id = cursor.fetchone()[0]
            
            # Create seat bookings
            for seat_id in seat_ids:
                cursor.execute("""
                    INSERT INTO seat_bookings (booking_id, seat_id)
                    VALUES (%s, %s)
                """, (booking_id, seat_id))
            
            conn.commit()
            flash(f'Booking confirmed! Your booking number is {booking_number}', 'success')
            
            cursor.close()
            conn.close()
            
            return redirect(url_for('bookings'))
            
        except Exception as e:
            print(f"Error creating booking: {e}")
            if conn:
                conn.rollback()
                conn.close()
            flash('Failed to create booking. Please try again.', 'error')
            return redirect(url_for('book_ticket', screening_id=screening_id))
    
    @app.route('/admin_dashboard')
    def admin_dashboard():
        """Admin dashboard (placeholder)"""
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('login'))
        flash('Admin dashboard coming soon!', 'info')
        return redirect(url_for('index'))
