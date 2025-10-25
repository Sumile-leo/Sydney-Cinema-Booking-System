#!/usr/bin/env python3
"""
Flask Backend Application for Sydney Cinema Booking System

Author: Zhou Li
Course: COMP9001
Date: October 12, 2025
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from functools import wraps

# Import configuration and models
from config import config
from models import User, Cinema, Movie, Screening, Booking

# Initialize Flask app
app = Flask(__name__,
            template_folder='../web/templates',
            static_folder='../web/static')

# Load configuration from config file
flask_config = config.get_flask_config()
app.secret_key = flask_config['secret_key']
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
CORS(app, supports_credentials=True)

# Database configuration is now handled by models
# No need for direct database connection functions

def login_required(f):
    """Decorator to require login - 需要登录的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin access - 需要管理员权限的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('user_type') != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes - 路由

@app.route('/')
def index():
    """Home page - 首页"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page - 登录页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')
        
        # Use User model for authentication
        user = User.authenticate(username, password)
        
        if user:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['user_type'] = user.user_type
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page - 注册页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        
        # Validation
        if not all([username, email, password, first_name, last_name]):
            flash('Please fill in all required fields.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Use User model to create new user
        user = User.create_user(username, email, password, first_name, last_name, phone)
        
        if user:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout - 登出"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - 用户仪表板"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return render_template('dashboard.html')
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get upcoming events
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.start_datetime, e.base_price, v.venue_name, v.city
            FROM events e
            JOIN venues v ON e.venue_id = v.venue_id
            WHERE e.status = 'upcoming' AND e.start_datetime > NOW()
            ORDER BY e.start_datetime
            LIMIT 10
        """)
        upcoming_events = cursor.fetchall()
        
        # Get user's recent orders
        cursor.execute("""
            SELECT o.order_id, o.order_number, o.total_amount, o.order_status, o.order_date,
                   e.event_name, e.start_datetime, v.venue_name
            FROM orders o
            JOIN events e ON o.event_id = e.event_id
            JOIN venues v ON e.venue_id = v.venue_id
            WHERE o.user_id = %s
            ORDER BY o.order_date DESC
            LIMIT 5
        """, (session['user_id'],))
        recent_orders = cursor.fetchall()
        
        # Format datetime for display
        for event in upcoming_events:
            event['start_datetime'] = event['start_datetime'].strftime('%Y-%m-%d %H:%M')
        
        for order in recent_orders:
            order['order_date'] = order['order_date'].strftime('%Y-%m-%d %H:%M')
            order['start_datetime'] = order['start_datetime'].strftime('%Y-%m-%d %H:%M')
        
    except Error as e:
        flash('Error loading dashboard data.', 'error')
        upcoming_events = []
        recent_orders = []
    finally:
        cursor.close()
        connection.close()
    
    return render_template('dashboard.html', 
                         upcoming_events=upcoming_events, 
                         recent_orders=recent_orders)

@app.route('/events')
def events():
    """Events listing page - 活动列表页面"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return render_template('events.html', events=[])
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get search parameters
        search = request.args.get('search', '')
        event_type = request.args.get('type', '')
        venue_id = request.args.get('venue', '')
        
        # Build query
        query = """
            SELECT e.event_id, e.event_name, e.description, e.event_type, 
                   e.start_datetime, e.end_datetime, e.base_price, e.status,
                   v.venue_name, v.address, v.city, v.capacity
            FROM events e
            JOIN venues v ON e.venue_id = v.venue_id
            WHERE e.status = 'upcoming' AND e.start_datetime > NOW()
        """
        params = []
        
        if search:
            query += " AND (e.event_name LIKE %s OR e.description LIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        if event_type:
            query += " AND e.event_type = %s"
            params.append(event_type)
        
        if venue_id:
            query += " AND e.venue_id = %s"
            params.append(venue_id)
        
        query += " ORDER BY e.start_datetime"
        
        cursor.execute(query, params)
        events = cursor.fetchall()
        
        # Get venues for filter
        cursor.execute("SELECT venue_id, venue_name FROM venues ORDER BY venue_name")
        venues = cursor.fetchall()
        
        # Format datetime for display
        for event in events:
            event['start_datetime'] = event['start_datetime'].strftime('%Y-%m-%d %H:%M')
            event['end_datetime'] = event['end_datetime'].strftime('%Y-%m-%d %H:%M')
        
    except Error as e:
        flash('Error loading events.', 'error')
        events = []
        venues = []
    finally:
        cursor.close()
        connection.close()
    
    return render_template('events.html', events=events, venues=venues)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    """Event detail page - 活动详情页面"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return redirect(url_for('events'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get event details
        cursor.execute("""
            SELECT e.*, v.venue_name, v.address, v.city, v.capacity, v.venue_type,
                   u.first_name as created_by_first_name, u.last_name as created_by_last_name
            FROM events e
            JOIN venues v ON e.venue_id = v.venue_id
            JOIN users u ON e.created_by = u.user_id
            WHERE e.event_id = %s
        """, (event_id,))
        
        event = cursor.fetchone()
        if not event:
            flash('Event not found.', 'error')
            return redirect(url_for('events'))
        
        # Get available seats
        cursor.execute("""
            SELECT s.seat_id, s.seat_number, s.row_number, s.section, s.seat_type,
                   ROUND(e.base_price * s.price_multiplier, 2) as price
            FROM seats s
            JOIN venues v ON s.venue_id = v.venue_id
            JOIN events e ON e.venue_id = v.venue_id
            LEFT JOIN order_items oi ON s.seat_id = oi.seat_id
            LEFT JOIN orders o ON oi.order_id = o.order_id AND o.order_status IN ('confirmed', 'pending')
            WHERE e.event_id = %s AND s.is_active = TRUE AND oi.seat_id IS NULL
            ORDER BY s.section, s.row_number, s.seat_number
        """, (event_id,))
        
        seats = cursor.fetchall()
        
        # Format datetime for display
        event['start_datetime'] = event['start_datetime'].strftime('%Y-%m-%d %H:%M')
        event['end_datetime'] = event['end_datetime'].strftime('%Y-%m-%d %H:%M')
        
    except Error as e:
        flash('Error loading event details.', 'error')
        return redirect(url_for('events'))
    finally:
        cursor.close()
        connection.close()
    
    return render_template('event_detail.html', event=event, seats=seats)

@app.route('/api/book', methods=['POST'])
@login_required
def book_tickets():
    """Book tickets API - 预订票务API"""
    data = request.get_json()
    
    if not data or 'event_id' not in data or 'seat_ids' not in data:
        return jsonify({'success': False, 'message': 'Invalid request data'})
    
    event_id = data['event_id']
    seat_ids = data['seat_ids']
    
    if not seat_ids:
        return jsonify({'success': False, 'message': 'Please select at least one seat'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor()
        
        # Start transaction
        connection.start_transaction()
        
        # Check if seats are still available
        placeholders = ','.join(['%s'] * len(seat_ids))
        cursor.execute(f"""
            SELECT s.seat_id, s.seat_number, s.row_number, s.section, s.seat_type,
                   ROUND(e.base_price * s.price_multiplier, 2) as price
            FROM seats s
            JOIN venues v ON s.venue_id = v.venue_id
            JOIN events e ON e.venue_id = v.venue_id
            LEFT JOIN order_items oi ON s.seat_id = oi.seat_id
            LEFT JOIN orders o ON oi.order_id = o.order_id AND o.order_status IN ('confirmed', 'pending')
            WHERE e.event_id = %s AND s.seat_id IN ({placeholders}) AND s.is_active = TRUE AND oi.seat_id IS NULL
        """, [event_id] + seat_ids)
        
        available_seats = cursor.fetchall()
        
        if len(available_seats) != len(seat_ids):
            connection.rollback()
            return jsonify({'success': False, 'message': 'Some seats are no longer available'})
        
        # Calculate total amount
        total_amount = sum(seat[5] for seat in available_seats)  # seat[5] is price
        
        # Generate order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"
        
        # Create order
        cursor.execute("""
            INSERT INTO orders (user_id, event_id, order_number, total_amount, order_status)
            VALUES (%s, %s, %s, %s, 'pending')
        """, (session['user_id'], event_id, order_number, total_amount))
        
        order_id = cursor.lastrowid
        
        # Create order items
        for seat in available_seats:
            cursor.execute("""
                INSERT INTO order_items (order_id, seat_id, quantity, unit_price, total_price)
                VALUES (%s, %s, 1, %s, %s)
            """, (order_id, seat[0], seat[5], seat[5]))
        
        # Commit transaction
        connection.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Tickets booked successfully!',
            'order_id': order_id,
            'order_number': order_number,
            'total_amount': total_amount
        })
        
    except Error as e:
        connection.rollback()
        return jsonify({'success': False, 'message': f'Booking error: {str(e)}'})
    finally:
        cursor.close()
        connection.close()

@app.route('/orders')
@login_required
def orders():
    """User orders page - 用户订单页面"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return render_template('orders.html', orders=[])
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT o.order_id, o.order_number, o.total_amount, o.order_status, 
                   o.payment_status, o.order_date, o.payment_date,
                   e.event_name, e.start_datetime, v.venue_name
            FROM orders o
            JOIN events e ON o.event_id = e.event_id
            JOIN venues v ON e.venue_id = v.venue_id
            WHERE o.user_id = %s
            ORDER BY o.order_date DESC
        """, (session['user_id'],))
        
        orders = cursor.fetchall()
        
        # Format datetime for display
        for order in orders:
            order['order_date'] = order['order_date'].strftime('%Y-%m-%d %H:%M')
            if order['payment_date']:
                order['payment_date'] = order['payment_date'].strftime('%Y-%m-%d %H:%M')
            order['start_datetime'] = order['start_datetime'].strftime('%Y-%m-%d %H:%M')
        
    except Error as e:
        flash('Error loading orders.', 'error')
        orders = []
    finally:
        cursor.close()
        connection.close()
    
    return render_template('orders.html', orders=orders)

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard - 管理员仪表板"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'error')
        return render_template('admin/dashboard.html')
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) as total_users FROM users WHERE is_active = TRUE")
        total_users = cursor.fetchone()['total_users']
        
        cursor.execute("SELECT COUNT(*) as total_events FROM events")
        total_events = cursor.fetchone()['total_events']
        
        cursor.execute("SELECT COUNT(*) as total_orders FROM orders")
        total_orders = cursor.fetchone()['total_orders']
        
        cursor.execute("SELECT SUM(total_amount) as total_revenue FROM orders WHERE payment_status = 'paid'")
        total_revenue = cursor.fetchone()['total_revenue'] or 0
        
        # Get recent orders
        cursor.execute("""
            SELECT o.order_id, o.order_number, o.total_amount, o.order_status, o.order_date,
                   u.username, u.first_name, u.last_name, e.event_name
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN events e ON o.event_id = e.event_id
            ORDER BY o.order_date DESC
            LIMIT 10
        """)
        recent_orders = cursor.fetchall()
        
        # Format datetime for display
        for order in recent_orders:
            order['order_date'] = order['order_date'].strftime('%Y-%m-%d %H:%M')
        
    except Error as e:
        flash('Error loading admin dashboard.', 'error')
        total_users = total_events = total_orders = total_revenue = 0
        recent_orders = []
    finally:
        cursor.close()
        connection.close()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_events=total_events,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

# Error handlers - 错误处理器

@app.errorhandler(404)
def not_found(error):
    """404 error handler - 404错误处理器"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler - 500错误处理器"""
    return render_template('errors/500.html'), 500

# Web routes - Web路由

@app.route('/movies')
def movies():
    """Movies page - 电影页面"""
    return render_template('movies.html')

@app.route('/cinemas')
def cinemas():
    """Cinemas page - 电影院页面"""
    return render_template('cinemas.html')

@app.route('/bookings')
def bookings():
    """User bookings page - 用户预订页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('bookings.html')

@app.route('/screenings')
def screenings():
    """Screenings page"""
    return render_template('screenings.html')

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Movie detail page"""
    try:
        movie = Movie.get_by_id('movies', movie_id)
        if not movie:
            flash('Movie not found.', 'error')
            return redirect(url_for('movies'))
        
        # Get screenings for this movie
        screenings = Screening.get_all('screenings', 
                                     f"movie_id = {movie_id} AND screening_date >= CURRENT_DATE", 
                                     None)
        
        return render_template('movie_detail.html', movie=movie, screenings=screenings)
    except Exception as e:
        flash('Error loading movie details.', 'error')
        return redirect(url_for('movies'))

@app.route('/cinema/<int:cinema_id>')
def cinema_detail(cinema_id):
    """Cinema detail page"""
    try:
        cinema = Cinema.get_by_id('cinemas', cinema_id)
        if not cinema:
            flash('Cinema not found.', 'error')
            return redirect(url_for('cinemas'))
        
        # Get screenings for this cinema
        screenings = Screening.get_all('screenings', 
                                    f"cinema_id = {cinema_id} AND screening_date >= CURRENT_DATE", 
                                    None)
        
        return render_template('cinema_detail.html', cinema=cinema, screenings=screenings)
    except Exception as e:
        flash('Error loading cinema details.', 'error')
        return redirect(url_for('cinemas'))

@app.route('/screening/<int:screening_id>')
def screening_detail(screening_id):
    """Screening detail page"""
    try:
        screening = Screening.get_by_id('screenings', screening_id)
        if not screening:
            flash('Screening not found.', 'error')
            return redirect(url_for('screenings'))
        
        movie = screening.get_movie()
        cinema = screening.get_cinema()
        
        if not movie or not cinema:
            flash('Screening information incomplete.', 'error')
            return redirect(url_for('screenings'))
        
        return render_template('screening_detail.html', 
                             screening=screening, 
                             movie=movie, 
                             cinema=cinema)
    except Exception as e:
        flash('Error loading screening details.', 'error')
        return redirect(url_for('screenings'))

@app.route('/book_ticket/<int:screening_id>')
@login_required
def book_ticket(screening_id):
    """Book ticket page"""
    screening = Screening.get_by_id('screenings', screening_id)
    if not screening:
        flash('Screening not found.', 'error')
        return redirect(url_for('movies'))
    
    movie = screening.get_movie()
    cinema = screening.get_cinema()
    hall = screening.get_hall()
    
    return render_template('seat_selection.html', 
                         screening=screening, 
                         movie=movie, 
                         cinema=cinema,
                         hall=hall)

# API routes - API路由

@app.route('/api/movies')
def api_movies():
    """API endpoint for movies"""
    try:
        movies = Movie.get_all('movies', 'is_active = TRUE')
        
        # Convert to list of dictionaries
        movie_list = []
        for movie in movies:
            movie_dict = {
                'movie_id': movie.movie_id,
                'title': movie.title,
                'description': movie.description,
                'genre': movie.genre,
                'duration_minutes': movie.duration_minutes,
                'release_date': movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None,
                'rating': movie.rating,
                'director': movie.director,
                'cast': movie.cast,
                'language': movie.language,
                'subtitles': movie.subtitles,
                'poster_url': movie.poster_url,
                'trailer_url': movie.trailer_url
            }
            movie_list.append(movie_dict)
        
        return jsonify({'movies': movie_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cinemas')
def api_cinemas():
    """API endpoint for cinemas"""
    try:
        cinemas = Cinema.get_all('cinemas', 'is_active = TRUE')
        
        # Convert to list of dictionaries
        cinema_list = []
        for cinema in cinemas:
            cinema_dict = {
                'cinema_id': cinema.cinema_id,
                'cinema_name': cinema.cinema_name,
                'address': cinema.address,
                'suburb': cinema.suburb,
                'postcode': cinema.postcode,
                'phone': cinema.phone,
                'total_screens': cinema.total_screens,
                'facilities': cinema.facilities,
                'parking_info': cinema.parking_info,
                'public_transport': cinema.public_transport
            }
            cinema_list.append(cinema_dict)
        
        return jsonify({'cinemas': cinema_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/screenings')
def api_screenings():
    """API endpoint for screenings with filtering support"""
    try:
        # Get filter parameters
        date_filter = request.args.get('date')
        cinema_id = request.args.get('cinema_id')
        movie_id = request.args.get('movie_id')
        
        # Build where clause with proper parameterization
        where_conditions = ['is_active = TRUE']
        params = []
        
        if date_filter:
            where_conditions.append("screening_date = %s")
            params.append(date_filter)
        else:
            where_conditions.append('screening_date >= CURRENT_DATE')
            
        if cinema_id:
            where_conditions.append("cinema_id = %s")
            params.append(int(cinema_id))
            
        if movie_id:
            where_conditions.append("movie_id = %s")
            params.append(int(movie_id))
        
        where_clause = ' AND '.join(where_conditions)
        screenings = Screening.get_all('screenings', where_clause, tuple(params))
        
        # Convert to list of dictionaries with movie and cinema info
        screening_list = []
        for screening in screenings:
            try:
                movie = screening.get_movie()
                cinema = screening.get_cinema()
                
                screening_dict = {
                    'screening_id': screening.screening_id,
                    'hall_id': screening.hall_id,
                    'screening_date': screening.get_date_formatted(),
                    'start_time': screening.get_time_formatted(),
                    'end_time': screening.end_time.strftime('%H:%M') if screening.end_time else 'N/A',
                    'ticket_price': float(screening.ticket_price) if screening.ticket_price else 0.0,
                    'available_seats': screening.get_available_seats(),
                    'total_seats': screening.get_total_seats(),
                    'screening_type': screening.screening_type,
                    'language': screening.language,
                    'subtitles': screening.subtitles,
                    'title': movie.title if movie else 'Unknown',
                    'genre': movie.genre if movie else 'Unknown',
                    'duration_minutes': int(movie.duration_minutes) if movie and movie.duration_minutes else 0,
                    'rating': movie.rating if movie else 'Unknown',
                    'poster_url': movie.poster_url if movie else None,
                    'cinema_name': cinema.cinema_name if cinema else 'Unknown',
                    'suburb': cinema.suburb if cinema else 'Unknown',
                    'address': cinema.address if cinema else 'Unknown'
                }
                screening_list.append(screening_dict)
            except Exception as e:
                print(f"Error processing screening {screening.screening_id}: {e}")
                continue
        
        return jsonify({'screenings': screening_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings')
def api_bookings():
    """API endpoint for user bookings"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        bookings = Booking.get_by_user_id(session['user_id'])
        
        # Convert to list of dictionaries
        booking_list = []
        for booking in bookings:
            booking_dict = {
                'booking_id': booking.booking_id,
                'booking_number': booking.booking_number,
                'num_tickets': booking.num_tickets,
                'total_amount': float(booking.total_amount),
                'booking_status': booking.booking_status,
                'payment_status': booking.payment_status,
                'booking_date': booking.booking_date.strftime('%Y-%m-%d %H:%M') if booking.booking_date else None,
                'screening_date': booking.get_screening().get_date_formatted() if booking.get_screening() else None,
                'start_time': booking.get_screening().get_time_formatted() if booking.get_screening() else None,
                'end_time': booking.get_screening().end_time.strftime('%H:%M') if booking.get_screening() else None,
                'title': booking.get_movie().title if booking.get_movie() else 'Unknown',
                'cinema_name': booking.get_cinema().cinema_name if booking.get_cinema() else 'Unknown'
            }
            booking_list.append(booking_dict)
        
        return jsonify({'bookings': booking_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/book_ticket', methods=['POST'])
@login_required
def api_book_ticket():
    """Book tickets for a screening with seat selection"""
    try:
        screening_id = request.form.get('screening_id')
        selected_seats_json = request.form.get('selected_seats')
        total_amount = float(request.form.get('total_amount', 0))
        
        if not screening_id or not selected_seats_json:
            return jsonify({'error': 'Invalid booking data'}), 400
        
        # Parse selected seats
        import json
        selected_seats = json.loads(selected_seats_json)
        
        if not selected_seats or len(selected_seats) == 0:
            return jsonify({'error': 'No seats selected'}), 400
        
        # Get screening details
        screening = Screening.get_by_id('screenings', int(screening_id))
        if not screening:
            return jsonify({'error': 'Screening not found'}), 404
        
        # Check if seats are still available
        from models.seat import Seat
        for seat_data in selected_seats:
            seat_id = seat_data['seat_id']
            if not Seat.is_available_for_screening(seat_id, int(screening_id)):
                return jsonify({'error': f'Seat {seat_data.get("seat_label", seat_id)} is no longer available'}), 400
        
        # Create booking
        booking = Booking.create_booking(
            user_id=session['user_id'],
            screening_id=int(screening_id),
            num_tickets=len(selected_seats)
        )
        
        if booking:
            # Book the selected seats
            seat_bookings_created = 0
            for seat_data in selected_seats:
                seat_id = seat_data['seat_id']
                if Seat.book_seat(seat_id, int(screening_id), booking.booking_id):
                    seat_bookings_created += 1
            
            if seat_bookings_created == len(selected_seats):
                return jsonify({
                    'success': True,
                    'booking_number': booking.booking_number,
                    'message': f'Successfully booked {len(selected_seats)} seat(s)',
                    'booking_id': booking.booking_id
                })
            else:
                # Some seats failed to book, cancel the booking
                booking.update('bookings', booking.booking_id, {'booking_status': 'cancelled'})
                return jsonify({'error': 'Failed to book some seats'}), 500
        else:
            return jsonify({'error': 'Failed to create booking'}), 500
            
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid seat selection data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        booking = Booking.get_by_id('bookings', booking_id)
        
        if not booking or booking.user_id != session['user_id']:
            return jsonify({'error': 'Booking not found or unauthorized'}), 404
        
        if booking.cancel_booking():
            return jsonify({'success': True, 'message': 'Booking cancelled successfully'})
        else:
            return jsonify({'error': 'Cannot cancel this booking'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/seats/<int:screening_id>')
def api_get_seat_map(screening_id):
    """Get seat map for a screening"""
    try:
        screening = Screening.get_by_id('screenings', screening_id)
        if not screening:
            return jsonify({'error': 'Screening not found'}), 404
        
        hall = screening.get_hall()
        if not hall:
            return jsonify({'error': 'Hall not found'}), 404
        
        # Get all seats for this hall
        seats = hall.get_seats()
        seat_map = []
        occupied_seats = []
        
        for seat in seats:
            # Check if seat is available for this screening
            from models.seat import Seat
            is_available = Seat.is_available_for_screening(seat.seat_id, screening_id)
            
            # Calculate price based on seat type and base price
            base_price = float(screening.ticket_price)
            if seat.seat_type == 'premium':
                price = base_price * 1.5
            elif seat.seat_type == 'vip':
                price = base_price * 2.0
            else:  # standard
                price = base_price
            
            seat_info = {
                'seat_id': seat.seat_id,
                'row_number': seat.row_number,
                'seat_number': seat.seat_number,
                'seat_type': seat.seat_type,
                'price': price,
                'is_available': is_available
            }
            
            seat_map.append(seat_info)
            
            if not is_available:
                occupied_seats.append(seat.seat_id)
        
        return jsonify({
            'success': True,
            'seat_map': seat_map,
            'occupied_seats': occupied_seats,
            'hall_info': hall.get_hall_info(),
            'screening_info': {
                'screening_id': screening.screening_id,
                'date': screening.get_date_formatted(),
                'time': screening.get_time_formatted(),
                'base_price': float(screening.ticket_price)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load application configuration
    app_config = config.get_app_config()
    flask_config = config.get_flask_config()
    
    # Run the Flask application
    print(f"🎬 Starting {app_config['name']}...")
    print(f"👤 Author: {app_config['author']}")
    print(f"📚 Course: {app_config['course']}")
    print(f"🌐 Web interface: http://localhost:{flask_config['port']}")
    print(f"📱 API endpoints: http://localhost:{flask_config['port']}/api/")
    print()
    
    app.run(debug=flask_config['debug'], 
            host=flask_config['host'], 
            port=flask_config['port'])
