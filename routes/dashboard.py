"""
Dashboard routes
"""

from flask import render_template, redirect, url_for, session, flash
from backend.services import BookingService


def register_dashboard_routes(app):
    """Register dashboard routes"""
    
    @app.route('/dashboard')
    def dashboard():
        """User dashboard page"""
        # Check if user is logged in
        if 'user_id' not in session:
            flash('Please login to access dashboard', 'error')
            return redirect(url_for('login'))
        
        user_id = session.get('user_id')
        
        # Get user info from session
        user_info = {
            'user_id': user_id,
            'username': session.get('username'),
            'first_name': session.get('first_name', ''),
            'last_name': session.get('last_name', ''),
            'user_type': session.get('user_type', 'customer')
        }
        
        # Get booking statistics
        bookings = BookingService.get_user_bookings_with_seats(user_id)
        
        # Calculate statistics
        total_bookings = len(bookings)
        upcoming = len([b for b in bookings if b.get('can_cancel', False)])
        cancelled = len([b for b in bookings if b.get('status') == 'cancelled'])
        
        # Count unique movies watched (confirmed bookings only, by movie_id)
        from datetime import datetime
        movies_watched_ids = set()
        for booking in bookings:
            # Count confirmed bookings and get unique movies
            if booking.get('status') == 'confirmed' and booking.get('movie_id'):
                movies_watched_ids.add(booking.get('movie_id'))
        movies_watched = len(movies_watched_ids)
        
        # Get recent activity (last 5 bookings)
        recent_bookings = sorted(bookings, key=lambda x: x.get('booking_date', ''), reverse=True)[:5]
        
        # Pass data to template
        return render_template('dashboard.html', 
                             user=user_info,
                             total_bookings=total_bookings,
                             movies_watched=movies_watched,
                             upcoming=upcoming,
                             cancelled=cancelled,
                             recent_bookings=recent_bookings)
