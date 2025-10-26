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

    @app.route('/movies')
    def movies():
        """Movies page (placeholder)"""
        return render_template('index.html')  # Temporary redirect to home



    @app.route('/screenings')
    def screenings():
        """Screenings page (placeholder)"""
        return render_template('index.html')  # Temporary redirect to home

    @app.route('/bookings')
    def bookings():
        """Bookings page (placeholder)"""
        if 'user_id' not in session:
            flash('Please login to view your bookings', 'error')
            return redirect(url_for('login'))
        return render_template('index.html')  # Temporary redirect to home

    @app.route('/dashboard')
    def dashboard():
        """Dashboard page (placeholder)"""
        if 'user_id' not in session:
            flash('Please login to access dashboard', 'error')
            return redirect(url_for('login'))
        return render_template('index.html')  # Temporary redirect to home

    @app.route('/admin_dashboard')
    def admin_dashboard():
        """Admin dashboard (placeholder)"""
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('login'))
        return render_template('index.html')  # Temporary redirect to home
