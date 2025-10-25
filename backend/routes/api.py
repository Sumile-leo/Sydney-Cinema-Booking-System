#!/usr/bin/env python3
"""
Flask Routes Module for Sydney Ticket Booking System
悉尼票务预订系统Flask路由模块

Author: Zhou Li
Course: COMP9001
Date: October 10, 2025
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from functools import wraps
from datetime import datetime
import secrets

# Create blueprint - 创建蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Database configuration - 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ticket_booking_system',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def get_db_connection():
    """Get database connection - 获取数据库连接"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def login_required(f):
    """Decorator to require login - 需要登录的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin access - 需要管理员权限的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        if session.get('user_type') != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# API Routes - API路由

@api_bp.route('/events')
def get_events():
    """Get all events - 获取所有活动"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get query parameters
        search = request.args.get('search', '')
        event_type = request.args.get('type', '')
        venue_id = request.args.get('venue', '')
        limit = request.args.get('limit', 50, type=int)
        
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
        
        query += " ORDER BY e.start_datetime LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        events = cursor.fetchall()
        
        # Convert datetime to string for JSON serialization
        for event in events:
            event['start_datetime'] = event['start_datetime'].strftime('%Y-%m-%d %H:%M')
            event['end_datetime'] = event['end_datetime'].strftime('%Y-%m-%d %H:%M')
        
        return jsonify({'events': events})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@api_bp.route('/events/<int:event_id>')
def get_event(event_id):
    """Get event details - 获取活动详情"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
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
            return jsonify({'error': 'Event not found'}), 404
        
        # Convert datetime to string
        event['start_datetime'] = event['start_datetime'].strftime('%Y-%m-%d %H:%M')
        event['end_datetime'] = event['end_datetime'].strftime('%Y-%m-%d %H:%M')
        
        return jsonify({'event': event})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@api_bp.route('/events/<int:event_id>/seats')
def get_event_seats(event_id):
    """Get available seats for an event - 获取活动的可用座位"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
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
        
        return jsonify({'seats': seats})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@api_bp.route('/book', methods=['POST'])
@login_required
def book_tickets():
    """Book tickets - 预订票务"""
    data = request.get_json()
    
    if not data or 'event_id' not in data or 'seat_ids' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    event_id = data['event_id']
    seat_ids = data['seat_ids']
    
    if not seat_ids:
        return jsonify({'error': 'Please select at least one seat'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
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
            return jsonify({'error': 'Some seats are no longer available'}), 400
        
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
            'order_id': order_id,
            'order_number': order_number,
            'total_amount': total_amount,
            'message': 'Tickets booked successfully!'
        })
        
    except Error as e:
        connection.rollback()
        return jsonify({'error': f'Booking error: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

@api_bp.route('/orders')
@login_required
def get_user_orders():
    """Get user orders - 获取用户订单"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
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
        
        # Convert datetime to string
        for order in orders:
            order['order_date'] = order['order_date'].strftime('%Y-%m-%d %H:%M')
            if order['payment_date']:
                order['payment_date'] = order['payment_date'].strftime('%Y-%m-%d %H:%M')
            order['start_datetime'] = order['start_datetime'].strftime('%Y-%m-%d %H:%M')
        
        return jsonify({'orders': orders})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@api_bp.route('/venues')
def get_venues():
    """Get all venues - 获取所有场馆"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT venue_id, venue_name, address, city, capacity, venue_type
            FROM venues
            ORDER BY venue_name
        """)
        
        venues = cursor.fetchall()
        
        return jsonify({'venues': venues})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Admin API Routes - 管理员API路由

@admin_bp.route('/stats')
@admin_required
def get_admin_stats():
    """Get admin statistics - 获取管理员统计信息"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
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
        
        cursor.execute("SELECT COUNT(*) as pending_orders FROM orders WHERE order_status = 'pending'")
        pending_orders = cursor.fetchone()['pending_orders']
        
        return jsonify({
            'total_users': total_users,
            'total_events': total_events,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'pending_orders': pending_orders
        })
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@admin_bp.route('/events', methods=['POST'])
@admin_required
def create_event():
    """Create new event - 创建新活动"""
    data = request.get_json()
    
    required_fields = ['event_name', 'description', 'event_type', 'venue_id', 
                      'start_datetime', 'end_datetime', 'base_price']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO events (event_name, description, event_type, venue_id, 
                              start_datetime, end_datetime, base_price, max_tickets_per_user, 
                              status, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'upcoming', %s)
        """, (
            data['event_name'],
            data['description'],
            data['event_type'],
            data['venue_id'],
            data['start_datetime'],
            data['end_datetime'],
            data['base_price'],
            data.get('max_tickets_per_user', 10),
            session['user_id']
        ))
        
        event_id = cursor.lastrowid
        connection.commit()
        
        return jsonify({
            'success': True,
            'event_id': event_id,
            'message': 'Event created successfully'
        })
        
    except Error as e:
        connection.rollback()
        return jsonify({'error': f'Error creating event: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

@admin_bp.route('/events/<int:event_id>', methods=['PUT'])
@admin_required
def update_event(event_id):
    """Update event - 更新活动"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Build update query dynamically
        update_fields = []
        params = []
        
        allowed_fields = ['event_name', 'description', 'event_type', 'venue_id', 
                         'start_datetime', 'end_datetime', 'base_price', 'max_tickets_per_user', 'status']
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        params.append(event_id)
        
        query = f"UPDATE events SET {', '.join(update_fields)} WHERE event_id = %s"
        cursor.execute(query, params)
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Event not found'}), 404
        
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': 'Event updated successfully'
        })
        
    except Error as e:
        connection.rollback()
        return jsonify({'error': f'Error updating event: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

@admin_bp.route('/orders')
@admin_required
def get_all_orders():
    """Get all orders for admin - 获取所有订单（管理员）"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get query parameters
        status = request.args.get('status', '')
        limit = request.args.get('limit', 100, type=int)
        
        query = """
            SELECT o.order_id, o.order_number, o.total_amount, o.order_status, 
                   o.payment_status, o.order_date, o.payment_date,
                   u.username, u.first_name, u.last_name, u.email,
                   e.event_name, e.start_datetime, v.venue_name
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN events e ON o.event_id = e.event_id
            JOIN venues v ON e.venue_id = v.venue_id
        """
        params = []
        
        if status:
            query += " WHERE o.order_status = %s"
            params.append(status)
        
        query += " ORDER BY o.order_date DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        orders = cursor.fetchall()
        
        # Convert datetime to string
        for order in orders:
            order['order_date'] = order['order_date'].strftime('%Y-%m-%d %H:%M')
            if order['payment_date']:
                order['payment_date'] = order['payment_date'].strftime('%Y-%m-%d %H:%M')
            order['start_datetime'] = order['start_datetime'].strftime('%Y-%m-%d %H:%M')
        
        return jsonify({'orders': orders})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@admin_bp.route('/users')
@admin_required
def get_all_users():
    """Get all users for admin - 获取所有用户（管理员）"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT user_id, username, email, first_name, last_name, phone, 
                   user_type, created_at, is_active
            FROM users
            ORDER BY user_type, username
        """)
        
        users = cursor.fetchall()
        
        # Convert datetime to string
        for user in users:
            user['created_at'] = user['created_at'].strftime('%Y-%m-%d %H:%M')
        
        return jsonify({'users': users})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
