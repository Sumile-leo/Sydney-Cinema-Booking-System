"""
Authentication routes
"""

from flask import render_template, request, redirect, url_for, session, flash
from database.db import get_user_by_username, check_username_or_email_exists, create_user, verify_password


def register_auth_routes(app):
    """Register authentication routes"""
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Login page"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                flash('Please enter username and password', 'error')
                return render_template('login.html')
            
            # Verify password using database function
            user = verify_password(username, password)
            
            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['first_name'] = user[4] if len(user) > 4 else ''
                session['last_name'] = user[5] if len(user) > 5 else ''
                session['user_type'] = user[7] if len(user) > 7 else 'customer'
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'error')
        
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Register page"""
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            phone = request.form.get('phone')
            
            # Basic validation
            if not username or not email or not password:
                flash('Please fill in all required fields', 'error')
                return render_template('register.html')
            
            # Check if username or email already exists
            if check_username_or_email_exists(username, email):
                flash('Username or email already exists', 'error')
                return render_template('register.html')
            
            # Create user using database function
            success = create_user(username, email, password, first_name, last_name, phone)
            
            if success:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration error. Please try again.', 'error')
        
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        """Logout"""
        session.clear()
        flash('You have been logged out', 'info')
        return redirect(url_for('index'))
