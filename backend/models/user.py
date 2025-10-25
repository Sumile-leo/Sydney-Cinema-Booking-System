"""
User Model for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 14, 2025
"""

from .base import BaseModel
from typing import List, Optional
from datetime import datetime
import hashlib


class User(BaseModel):
    """User model with booking relationships"""
    
    def __init__(self, user_id: int = None, username: str = None, email: str = None, 
                 password_hash: str = None, first_name: str = None, last_name: str = None,
                 phone: str = None, user_type: str = 'customer', created_at: datetime = None,
                 updated_at: datetime = None, is_active: bool = True):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.user_type = user_type
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        
        # Additional properties
        self._bookings = None
        self._total_bookings = None
        self._total_spent = None
    
    @classmethod
    def from_db_row(cls, row):
        """Create User instance from database row"""
        return cls(
            user_id=row[0],
            username=row[1],
            email=row[2],
            password_hash=row[3],
            first_name=row[4],
            last_name=row[5],
            phone=row[6],
            user_type=row[7],
            created_at=row[8],
            updated_at=row[9],
            is_active=row[10]
        )
    
    @classmethod
    def get_by_username(cls, username: str):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = %s AND is_active = TRUE"
        result = cls.execute_query(query, (username,), fetch_one=True)
        
        if result:
            return cls.from_db_row(result)
        return None
    
    @classmethod
    def get_by_email(cls, email: str):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %s AND is_active = TRUE"
        result = cls.execute_query(query, (email,), fetch_one=True)
        
        if result:
            return cls.from_db_row(result)
        return None
    
    @classmethod
    def authenticate(cls, username: str, password: str):
        """Authenticate user with username and password"""
        user = cls.get_by_username(username)
        if user and user.check_password(password):
            return user
        return None
    
    @classmethod
    def create_user(cls, username: str, email: str, password: str, 
                   first_name: str, last_name: str, phone: str = None):
        """Create new user"""
        # Check if username or email already exists
        if cls.get_by_username(username) or cls.get_by_email(email):
            return None
        
        password_hash = cls.hash_password(password)
        data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'user_type': 'customer',
            'is_active': True
        }
        
        return cls.create('users', data)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches hash"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def get_bookings(self) -> List:
        """Get all bookings for this user"""
        if self._bookings is None:
            from .booking import Booking
            self._bookings = Booking.get_by_user_id(self.user_id)
        return self._bookings
    
    def get_total_bookings(self) -> int:
        """Get total number of bookings"""
        if self._total_bookings is None:
            query = """
                SELECT COUNT(*) FROM bookings 
                WHERE user_id = %s AND booking_status != 'cancelled'
            """
            result = self.execute_query(query, (self.user_id,), fetch_one=True)
            self._total_bookings = result[0] if result else 0
        return self._total_bookings
    
    def get_total_spent(self) -> float:
        """Get total amount spent on bookings"""
        if self._total_spent is None:
            query = """
                SELECT COALESCE(SUM(total_amount), 0) FROM bookings 
                WHERE user_id = %s AND booking_status = 'confirmed'
            """
            result = self.execute_query(query, (self.user_id,), fetch_one=True)
            self._total_spent = float(result[0]) if result else 0.0
        return self._total_spent
    
    def get_recent_bookings(self, limit: int = 5) -> List:
        """Get recent bookings"""
        from .booking import Booking
        query = """
            SELECT b.* FROM bookings b
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
            LIMIT %s
        """
        results = self.execute_query(query, (self.user_id, limit), fetch_all=True)
        if results:
            return [Booking.from_db_row(row) for row in results]
        return []
    
    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.user_type == 'admin'
    
    def is_staff(self) -> bool:
        """Check if user is staff"""
        return self.user_type in ['staff', 'admin']
    
    def is_customer(self) -> bool:
        """Check if user is customer"""
        return self.user_type == 'customer'
    
    def get_full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def update_profile(self, **kwargs):
        """Update user profile"""
        allowed_fields = ['first_name', 'last_name', 'phone', 'email']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if update_data:
            update_data['updated_at'] = datetime.now()
            return self.update('users', self.user_id, update_data)
        return None
    
    def deactivate(self):
        """Deactivate user account"""
        return self.update('users', self.user_id, {
            'is_active': False,
            'updated_at': datetime.now()
        })
    
    def __str__(self):
        return f"User({self.username}, {self.get_full_name()})"
    
    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', user_type='{self.user_type}')"
