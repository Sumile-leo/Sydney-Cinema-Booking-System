"""
Business logic services
"""

from database.db import get_user_by_username, create_user, check_username_or_email_exists


class UserService:
    """User business logic service"""
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate a user
        Returns user data if successful, None otherwise
        """
        user = get_user_by_username(username)
        if not user:
            return None
        
        # Plain text password comparison
        if user[2] == password:  # user[2] is password field
            return user
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
