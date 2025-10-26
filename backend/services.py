"""
Business logic services
"""

from database.db import get_user_by_username, create_user, check_username_or_email_exists
from backend.models.user import User


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
