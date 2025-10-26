"""
Authentication routes
"""

from flask import render_template, request, redirect, url_for, session, flash
from database.db import get_db_connection


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
            
            conn = get_db_connection()
            if not conn:
                flash('Database connection error', 'error')
                return render_template('login.html')
            
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT user_id, username, password FROM users WHERE username = %s",
                    (username,)
                )
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                
                # Simple password comparison (plain text)
                if user and user[2] == password:
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    flash('Login successful!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password', 'error')
                
            except Exception as e:
                print(f"Login error: {e}")
                flash('Login error. Please try again.', 'error')
        
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
            
            conn = get_db_connection()
            if not conn:
                flash('Database connection error', 'error')
                return render_template('register.html')
            
            try:
                cursor = conn.cursor()
                
                # Check if username or email already exists
                cursor.execute(
                    "SELECT user_id FROM users WHERE username = %s OR email = %s",
                    (username, email)
                )
                if cursor.fetchone():
                    flash('Username or email already exists', 'error')
                    cursor.close()
                    conn.close()
                    return render_template('register.html')
                
                # Insert user (plain text password)
                cursor.execute(
                    """INSERT INTO users (username, email, password, first_name, last_name, phone, user_type)
                       VALUES (%s, %s, %s, %s, %s, %s, 'customer')""",
                    (username, email, password, first_name, last_name, phone)
                )
                conn.commit()
                cursor.close()
                conn.close()
                
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
                
            except Exception as e:
                print(f"Registration error: {e}")
                flash('Registration error. Please try again.', 'error')
            finally:
                if conn:
                    conn.close()
        
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        """Logout"""
        session.clear()
        flash('You have been logged out', 'info')
        return redirect(url_for('index'))
