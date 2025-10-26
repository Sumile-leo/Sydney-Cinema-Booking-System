"""
Main routes
"""

from flask import render_template, redirect, url_for, session, flash
from backend.services import CinemaService, MovieService


def register_main_routes(app):
    """Register main routes"""
    
    @app.route('/')
    def index():
        """Homepage with latest movies"""
        # Get latest movies (limit to 3 for homepage)
        all_movies = MovieService.get_all_movies()
        latest_movies = [m for m in all_movies if m.is_active][:3]
        
        return render_template('index.html', movies=latest_movies)

    @app.route('/screenings')
    def screenings():
        """Screenings page"""
        from database.db import get_all_screenings
        from backend.models.screening import Screening
        from backend.services import MovieService, CinemaService
        
        # Get all screenings
        screenings_data = get_all_screenings()
        screenings_list = [Screening.from_db_row(s) for s in screenings_data]
        
        # Get today and next 7 days
        from datetime import date, timedelta
        today = date.today()
        end_date = today + timedelta(days=7)
        
        # Filter screenings for the next 7 days
        upcoming_screenings = [
            s for s in screenings_list 
            if s.screening_date >= today and s.screening_date <= end_date
        ]
        
        # Group by date
        screenings_by_date = {}
        for screening in upcoming_screenings:
            date_str = screening.screening_date.strftime('%Y-%m-%d')
            if date_str not in screenings_by_date:
                screenings_by_date[date_str] = []
            screenings_by_date[date_str].append(screening)
        
        return render_template('screenings.html', 
                              screenings_by_date=screenings_by_date,
                              today=today)

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
