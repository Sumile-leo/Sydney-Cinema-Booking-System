"""
Seat model
Author: Zhou Li
Date: 2025-10-15
"""

from typing import Optional, Tuple
from datetime import datetime


class Seat:
    """Seat data model"""
    
    def __init__(self, seat_id: int, hall_id: int, row_number: int, seat_number: int,
                 seat_type: str = None, price_multiplier: float = 1.00, is_active: bool = True):
        self.seat_id = seat_id
        self.hall_id = hall_id
        self.row_number = row_number
        self.seat_number = seat_number
        self.seat_type = seat_type
        self.price_multiplier = price_multiplier
        self.is_active = is_active
    
    @classmethod
    def from_db_row(cls, db_row: Tuple) -> 'Seat':
        """
        Create Seat instance from database row tuple
        db_row: (seat_id, hall_id, row_number, seat_number, seat_type, price_multiplier, is_active)
        """
        return cls(
            seat_id=db_row[0],
            hall_id=db_row[1],
            row_number=db_row[2],
            seat_number=db_row[3],
            seat_type=db_row[4] if len(db_row) > 4 and db_row[4] else None,
            price_multiplier=float(db_row[5]) if len(db_row) > 5 and db_row[5] else 1.00,
            is_active=db_row[6] if len(db_row) > 6 else True
        )
    
    def to_dict(self) -> dict:
        """Convert Seat to dictionary"""
        return {
            'seat_id': self.seat_id,
            'hall_id': self.hall_id,
            'row_number': self.row_number,
            'seat_number': self.seat_number,
            'seat_type': self.seat_type,
            'price_multiplier': self.price_multiplier,
            'is_active': self.is_active
        }
    
    def __repr__(self) -> str:
        return f"<Seat Row {self.row_number} Seat {self.seat_number} ({self.seat_id})>"

