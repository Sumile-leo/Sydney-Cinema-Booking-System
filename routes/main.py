"""
Main routes
"""

from flask import render_template, redirect, url_for, session, flash
from backend.services import CinemaService, MovieService


def register_main_routes(app):
    """Register main routes"""
    
    @app.route('/')
    def index():
        """Homepage with latest movies and cinemas"""
        # Get latest movies (limit to 3 for homepage)
        all_movies = MovieService.get_all_movies()
        latest_movies = [m for m in all_movies if m.is_active][:3]
        
        # Get top cinemas (limit to 3 for homepage)
        all_cinemas = CinemaService.get_all_cinemas()
        popular_cinemas = [c for c in all_cinemas if c.is_active][:3]
        
        return render_template('index.html', movies=latest_movies, cinemas=popular_cinemas)

    @app.route('/screenings')
    def screenings():
        """Screenings page (placeholder)"""
        flash('Screenings page coming soon!', 'info')
        return redirect(url_for('index'))

    @app.route('/bookings')
    def bookings():
        """Bookings page (placeholder)"""
        if 'user_id' not in session:
            flash('Please login to view your bookings', 'error')
            return redirect(url_for('login'))
        flash('My Bookings page coming soon!', 'info')
        return redirect(url_for('index'))

    @app.route('/admin_dashboard')
    def admin_dashboard():
        """Admin dashboard (placeholder)"""
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('login'))
        flash('Admin dashboard coming soon!', 'info')
        return redirect(url_for('index'))
