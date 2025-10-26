"""
Cinema Hall model
Author: Zhou Li
Date: 2025-10-14
"""

from typing import Optional, Tuple
from datetime import datetime


class CinemaHall:
    """Cinema Hall data model"""
    
    def __init__(self, hall_id: int, cinema_id: int, hall_name: str,
                 hall_type: str = None, total_rows: int = None,
                 seats_per_row: int = None, total_seats: int = None,
                 screen_size: str = None, sound_system: str = None,
                 created_at: datetime = None, updated_at: datetime = None):
        self.hall_id = hall_id
        self.cinema_id = cinema_id
        self.hall_name = hall_name
        self.hall_type = hall_type
        self.total_rows = total_rows
        self.seats_per_row = seats_per_row
        self.total_seats = total_seats
        self.screen_size = screen_size
        self.sound_system = sound_system
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db_row(cls, db_row: Tuple) -> 'CinemaHall':
        """
        Create CinemaHall instance from database row tuple
        db_row: (hall_id, cinema_id, hall_name, hall_type, total_rows, 
                 seats_per_row, total_seats, screen_size, sound_system, 
                 created_at, updated_at)
        """
        return cls(
            hall_id=db_row[0],
            cinema_id=db_row[1],
            hall_name=db_row[2] if len(db_row) > 2 else None,
            hall_type=db_row[3] if len(db_row) > 3 else None,
            total_rows=db_row[4] if len(db_row) > 4 else None,
            seats_per_row=db_row[5] if len(db_row) > 5 else None,
            total_seats=db_row[6] if len(db_row) > 6 else None,
            screen_size=db_row[7] if len(db_row) > 7 else None,
            sound_system=db_row[8] if len(db_row) > 8 else None,
            created_at=db_row[9] if len(db_row) > 9 else None,
            updated_at=db_row[10] if len(db_row) > 10 else None
        )
    
    def to_dict(self) -> dict:
        """Convert CinemaHall to dictionary"""
        return {
            'hall_id': self.hall_id,
            'cinema_id': self.cinema_id,
            'hall_name': self.hall_name,
            'hall_type': self.hall_type,
            'total_rows': self.total_rows,
            'seats_per_row': self.seats_per_row,
            'total_seats': self.total_seats,
            'screen_size': self.screen_size,
            'sound_system': self.sound_system,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self) -> str:
        return f"<CinemaHall {self.hall_name} ({self.hall_id})>"

