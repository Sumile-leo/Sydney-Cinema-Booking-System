"""
Main routes
"""

from flask import render_template, redirect, url_for, session, flash
from backend.services import CinemaService, MovieService, BookingService


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

    @app.route('/admin_dashboard')
    def admin_dashboard():
        """Admin dashboard (placeholder)"""
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('login'))
        flash('Admin dashboard coming soon!', 'info')
        return redirect(url_for('index'))
