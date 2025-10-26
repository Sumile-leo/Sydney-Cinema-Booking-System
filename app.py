"""
Sydney Cinema Booking System - Flask App
Simple and clean implementation
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
import psycopg
from datetime import datetime

app = Flask(__name__, 
            template_folder='web/templates',
            static_folder='web/static')
app.secret_key = 'your-secret-key-change-this-in-production'
CORS(app, supports_credentials=True)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'cinema_db',
    'user': 'postgres',
    'password': 'postgres'
}


def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


# Routes
@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')


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
            
            # Debug print
            print(f"DEBUG - Username received: {username}")
            print(f"DEBUG - Password received: {password}")
            if user:
                print(f"DEBUG - User found: {user[1]}")
                print(f"DEBUG - Stored password: {user[2]}")
                print(f"DEBUG - Password match: {user[2] == password}")
                print(f"DEBUG - Password type: {type(user[2])}, {type(password)}")
                print(f"DEBUG - Password repr: {repr(user[2])}, {repr(password)}")
            else:
                print(f"DEBUG - User NOT found in database")
            
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
