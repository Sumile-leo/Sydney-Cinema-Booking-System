"""
Main routes
"""

from flask import render_template, redirect, url_for, session, flash


def register_main_routes(app):
    """Register main routes"""
    
    @app.route('/')
    def index():
        """Homepage"""
        return render_template('index.html')

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
        return redirect(url_for('dashboard'))

    @app.route('/admin_dashboard')
    def admin_dashboard():
        """Admin dashboard (placeholder)"""
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('login'))
        flash('Admin dashboard coming soon!', 'info')
        return redirect(url_for('dashboard'))
