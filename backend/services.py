"""
Business logic services
"""

from database.db import (
    get_user_by_username, create_user, check_username_or_email_exists,
    get_all_cinemas, get_cinema_by_id, create_cinema
)
from backend.models.user import User
from backend.models.cinema import Cinema


class UserService:
    """User business logic service"""
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate a user
        Returns User object if successful, None otherwise
        """
        user_row = get_user_by_username(username)
        if not user_row:
            return None
        
        # Plain text password comparison
        if user_row[2] == password:  # user_row[2] is password field
            return User.from_db_row(user_row)
        return None
    
    @staticmethod
    def register_user(username, email, password, first_name, last_name, phone):
        """
        Register a new user
        Returns True if successful, False otherwise
        """
        # Check if user already exists
        if check_username_or_email_exists(username, email):
            return False
        
        # Create user
        return create_user(username, email, password, first_name, last_name, phone)


class CinemaService:
    """Cinema business logic service"""
    
    @staticmethod
    def get_all_cinemas():
        """
        Get all cinemas
        Returns list of Cinema objects
        """
        cinema_rows = get_all_cinemas()
        return [Cinema.from_db_row(row) for row in cinema_rows]
    
    @staticmethod
    def get_cinema_by_id(cinema_id):
        """
        Get cinema by ID
        Returns Cinema object or None
        """
        cinema_row = get_cinema_by_id(cinema_id)
        if cinema_row:
            return Cinema.from_db_row(cinema_row)
        return None
    
    @staticmethod
    def create_cinema(cinema_name, address, suburb, postcode, phone=None, email=None, facilities=None, is_active=True):
        """
        Create a new cinema
        Returns True if successful, False otherwise
        """
        return create_cinema(cinema_name, address, suburb, postcode, phone, email, facilities, is_active)
