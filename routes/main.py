"""
Main routes
Author: Zhou Li
Date: 2025-10-18
"""

from flask import render_template, redirect, url_for, session, flash, request, abort
from backend.services import CinemaService, MovieService, BookingService, ScreeningService, CinemaHallService


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
        
        # Cancel booking using service
        success, message = BookingService.cancel_user_booking(booking_id, session['user_id'])
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        
        return redirect(url_for('bookings'))

    @app.route('/book/<int:screening_id>')
    def book_ticket(screening_id):
        """Book ticket page with seat selection"""
        if 'user_id' not in session:
            flash('Please login to book tickets', 'error')
            return redirect(url_for('login'))
        
        # Get all screening data using service
        booking_data = ScreeningService.get_screening_for_booking(screening_id)
        if not booking_data:
            abort(404)
        
        return render_template('book_ticket.html', 
                              screening=booking_data['screening'], 
                              movie=booking_data['movie'], 
                              cinema=booking_data['cinema'],
                              hall=booking_data['hall'],
                              seats=booking_data['seats'],
                              booked_seats=booking_data['booked_seats'])
    
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
        
        # Create booking using service
        success, message, booking_number = BookingService.create_new_booking(
            session['user_id'], screening_id, seat_ids
        )
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
            return redirect(url_for('book_ticket', screening_id=screening_id))
        
        return redirect(url_for('bookings'))
    
    @app.route('/admin_dashboard')
    def admin_dashboard():
        """Admin dashboard - redirect to admin panel"""
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('login'))
        return redirect(url_for('admin_panel'))
