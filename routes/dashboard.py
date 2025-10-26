"""
Dashboard routes
"""

from flask import render_template, redirect, url_for, session, flash


def register_dashboard_routes(app):
    """Register dashboard routes"""
    
    @app.route('/dashboard')
    def dashboard():
        """User dashboard page"""
        # Check if user is logged in
        if 'user_id' not in session:
            flash('Please login to access dashboard', 'error')
            return redirect(url_for('login'))
        
        # Get user info from session
        user_info = {
            'user_id': session.get('user_id'),
            'username': session.get('username'),
            'first_name': session.get('first_name', ''),
            'last_name': session.get('last_name', ''),
            'user_type': session.get('user_type', 'customer')
        }
        
        # Pass user info to template
        return render_template('dashboard.html', user=user_info)
