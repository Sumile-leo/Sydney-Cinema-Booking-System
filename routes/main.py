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
                'seat_id': seat_row[0],
                'row_number': seat_row[1],
                'seat_number': seat_row[2],
                'seat_type': seat_row[3] if len(seat_row) > 3 else 'standard',
                'price_multiplier': float(seat_row[4]) if len(seat_row) > 4 and seat_row[4] else 1.0,
                'is_active': seat_row[5] if len(seat_row) > 5 else True
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
    
    @app.route('/admin_dashboard')
    def admin_dashboard():
        """Admin dashboard (placeholder)"""
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('login'))
        flash('Admin dashboard coming soon!', 'info')
        return redirect(url_for('index'))
