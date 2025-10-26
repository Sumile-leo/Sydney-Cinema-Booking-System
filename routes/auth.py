"""
Authentication routes
Author: Zhou Li
Date: 2025-10-10
"""

from flask import render_template, request, redirect, url_for, session, flash
from backend.services import UserService


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
            
            # Authenticate user using service layer
            user = UserService.authenticate_user(username, password)
            
            if user:
                # Store user info in session using User object attributes
                session['user_id'] = user.user_id
                session['username'] = user.username
                session['first_name'] = user.first_name or ''
                session['last_name'] = user.last_name or ''
                session['user_type'] = user.user_type
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
            
            # Register user using service layer
            success = UserService.register_user(username, email, password, first_name, last_name, phone)
            
            if success:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username or email already exists, or registration failed.', 'error')
        
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        """Logout"""
        session.clear()
        flash('You have been logged out', 'info')
        return redirect(url_for('index'))
