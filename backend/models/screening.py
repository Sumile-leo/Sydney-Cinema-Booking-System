"""
Screening model
Author: Zhou Li
Date: 2025-10-16
"""

from typing import Optional, Tuple
from datetime import datetime, date, time


class Screening:
    """Screening data model"""
    
    def __init__(self, screening_id: int, movie_id: int, cinema_id: int, hall_id: int,
                 screening_date: date, start_time: time, end_time: time,
                 ticket_price: float, screening_type: str = None,
                 language: str = None, subtitles: str = None,
                 is_active: bool = True, created_at: datetime = None, updated_at: datetime = None):
        self.screening_id = screening_id
        self.movie_id = movie_id
        self.cinema_id = cinema_id
        self.hall_id = hall_id
        self.screening_date = screening_date
        self.start_time = start_time
        self.end_time = end_time
        self.ticket_price = ticket_price
        self.screening_type = screening_type
        self.language = language
        self.subtitles = subtitles
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db_row(cls, db_row: Tuple) -> 'Screening':
        """
        Create Screening instance from database row tuple
        db_row: (screening_id, movie_id, cinema_id, hall_id, screening_date,
                 start_time, end_time, ticket_price, screening_type, language,
                 subtitles, is_active, created_at, updated_at)
        """
        return cls(
            screening_id=db_row[0],
            movie_id=db_row[1],
            cinema_id=db_row[2],
            hall_id=db_row[3],
            screening_date=db_row[4] if len(db_row) > 4 else None,
            start_time=db_row[5] if len(db_row) > 5 else None,
            end_time=db_row[6] if len(db_row) > 6 else None,
            ticket_price=float(db_row[7]) if len(db_row) > 7 and db_row[7] else 0.00,
            screening_type=db_row[8] if len(db_row) > 8 and db_row[8] else None,
            language=db_row[9] if len(db_row) > 9 and db_row[9] else None,
            subtitles=db_row[10] if len(db_row) > 10 and db_row[10] else None,
            is_active=db_row[11] if len(db_row) > 11 else True,
            created_at=db_row[12] if len(db_row) > 12 else None,
            updated_at=db_row[13] if len(db_row) > 13 else None
        )
    
    def to_dict(self) -> dict:
        """Convert Screening to dictionary"""
        return {
            'screening_id': self.screening_id,
            'movie_id': self.movie_id,
            'cinema_id': self.cinema_id,
            'hall_id': self.hall_id,
            'screening_date': self.screening_date.isoformat() if self.screening_date else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'ticket_price': self.ticket_price,
            'screening_type': self.screening_type,
            'language': self.language,
            'subtitles': self.subtitles,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_time_formatted(self) -> str:
        """Get formatted time (HH:MM)"""
        if not self.start_time:
            return "N/A"
        return self.start_time.strftime("%H:%M")
    
    def __repr__(self) -> str:
        return f"<Screening {self.screening_id}>"

