"""
Booking model
Author: Zhou Li
Date: 2025-10-19
"""

from typing import Optional, Tuple
from datetime import datetime


class Booking:
    """Booking data model"""
    
    def __init__(self, booking_id: int, user_id: int, screening_id: int,
                 booking_number: str, num_tickets: int, total_amount: float,
                 booking_status: str = 'pending', payment_status: str = 'unpaid',
                 booking_date: datetime = None, created_at: datetime = None,
                 updated_at: datetime = None):
        self.booking_id = booking_id
        self.user_id = user_id
        self.screening_id = screening_id
        self.booking_number = booking_number
        self.num_tickets = num_tickets
        self.total_amount = total_amount
        self.booking_status = booking_status
        self.payment_status = payment_status
        self.booking_date = booking_date
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db_row(cls, db_row: Tuple) -> 'Booking':
        """
        Create Booking instance from database row tuple
        db_row: (booking_id, user_id, screening_id, booking_number, num_tickets,
                 total_amount, booking_status, payment_status, booking_date,
                 created_at, updated_at)
        """
        return cls(
            booking_id=db_row[0],
            user_id=db_row[1],
            screening_id=db_row[2],
            booking_number=db_row[3],
            num_tickets=db_row[4],
            total_amount=float(db_row[5]) if db_row[5] else 0.00,
            booking_status=db_row[6] if len(db_row) > 6 and db_row[6] else 'pending',
            payment_status=db_row[7] if len(db_row) > 7 and db_row[7] else 'unpaid',
            booking_date=db_row[8] if len(db_row) > 8 else None,
            created_at=db_row[9] if len(db_row) > 9 else None,
            updated_at=db_row[10] if len(db_row) > 10 else None
        )
    
    def to_dict(self) -> dict:
        """Convert Booking to dictionary"""
        return {
            'booking_id': self.booking_id,
            'user_id': self.user_id,
            'screening_id': self.screening_id,
            'booking_number': self.booking_number,
            'num_tickets': self.num_tickets,
            'total_amount': self.total_amount,
            'booking_status': self.booking_status,
            'payment_status': self.payment_status,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self) -> str:
        return f"<Booking {self.booking_number} ({self.booking_id})>"

