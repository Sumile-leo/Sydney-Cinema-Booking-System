"""
User model
Author: Zhou Li
Date: 2025-10-10
"""

from typing import Optional, Tuple


class User:
    """User data model"""
    
    def __init__(self, user_id: int, username: str, email: str, password: str = None,
                 first_name: str = None, last_name: str = None, phone: str = None,
                 user_type: str = 'customer'):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.user_type = user_type
    
    @classmethod
    def from_db_row(cls, db_row: Tuple) -> 'User':
        """
        Create User instance from database row tuple
        db_row: (user_id, username, password, email, first_name, last_name, phone, user_type)
        """
        return cls(
            user_id=db_row[0],
            username=db_row[1],
            email=db_row[3] if len(db_row) > 3 else '',
            password=db_row[2] if len(db_row) > 2 else None,
            first_name=db_row[4] if len(db_row) > 4 else None,
            last_name=db_row[5] if len(db_row) > 5 else None,
            phone=db_row[6] if len(db_row) > 6 else None,
            user_type=db_row[7] if len(db_row) > 7 else 'customer'
        )
    
    def to_dict(self, include_password: bool = False) -> dict:
        """Convert User to dictionary"""
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'user_type': self.user_type
        }
        if include_password:
            data['password'] = self.password
        return data
    
    def __repr__(self) -> str:
        return f"<User {self.username} ({self.user_id})>"
