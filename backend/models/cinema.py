"""
Cinema model
Author: Zhou Li
Date: 2025-10-13
"""

from typing import Optional, Tuple
from datetime import datetime


class Cinema:
    """Cinema data model"""
    
    def __init__(self, cinema_id: int, cinema_name: str, address: str, 
                 suburb: str, postcode: str, phone: str = None, 
                 email: str = None, facilities: str = None,
                 created_at: datetime = None, updated_at: datetime = None,
                 is_active: bool = True):
        self.cinema_id = cinema_id
        self.cinema_name = cinema_name
        self.address = address
        self.suburb = suburb
        self.postcode = postcode
        self.phone = phone
        self.email = email
        self.facilities = facilities
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
    
    @classmethod
    def from_db_row(cls, db_row: Tuple) -> 'Cinema':
        """
        Create Cinema instance from database row tuple
        db_row: (cinema_id, cinema_name, address, suburb, postcode, phone, email, facilities, created_at, updated_at, is_active)
        """
        return cls(
            cinema_id=db_row[0],
            cinema_name=db_row[1],
            address=db_row[2],
            suburb=db_row[3],
            postcode=db_row[4],
            phone=db_row[5] if len(db_row) > 5 and db_row[5] else None,
            email=db_row[6] if len(db_row) > 6 and db_row[6] else None,
            facilities=db_row[7] if len(db_row) > 7 and db_row[7] else None,
            created_at=db_row[8] if len(db_row) > 8 else None,
            updated_at=db_row[9] if len(db_row) > 9 else None,
            is_active=db_row[10] if len(db_row) > 10 else True
        )
    
    def to_dict(self) -> dict:
        """Convert Cinema to dictionary"""
        return {
            'cinema_id': self.cinema_id,
            'cinema_name': self.cinema_name,
            'address': self.address,
            'suburb': self.suburb,
            'postcode': self.postcode,
            'phone': self.phone,
            'email': self.email,
            'facilities': self.facilities,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
    
    @property
    def full_address(self) -> str:
        """Get full address as a single string"""
        return f"{self.address}, {self.suburb} {self.postcode}"
    
    def __repr__(self) -> str:
        return f"<Cinema {self.cinema_name} ({self.cinema_id})>"
