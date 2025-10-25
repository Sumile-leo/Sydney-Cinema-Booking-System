"""
Cinema Hall Model for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 26, 2025
"""

from .base import BaseModel
from typing import List, Optional
from datetime import datetime


class CinemaHall(BaseModel):
    """Cinema hall model with seat management"""
    
    def __init__(self, hall_id: int = None, cinema_id: int = None, hall_name: str = None,
                 hall_type: str = 'standard', total_rows: int = None, seats_per_row: int = None,
                 total_seats: int = None, screen_size: str = 'standard', sound_system: str = 'standard',
                 created_at: datetime = None, updated_at: datetime = None, is_active: bool = True):
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
        self.is_active = is_active
        
        # Additional properties
        self._cinema = None
        self._seats = None
        self._screenings = None
    
    @classmethod
    def from_db_row(cls, row):
        """Create CinemaHall instance from database row"""
        if not row:
            return None
        return cls(
            hall_id=row[0],
            cinema_id=row[1],
            hall_name=row[2],
            hall_type=row[3],
            total_rows=row[4],
            seats_per_row=row[5],
            total_seats=row[6],
            screen_size=row[7],
            sound_system=row[8],
            created_at=row[9],
            updated_at=row[10],
            is_active=row[11]
        )
    
    @classmethod
    def get_by_cinema_id(cls, cinema_id: int):
        """Get halls by cinema ID"""
        query = """
            SELECT * FROM cinema_halls 
            WHERE cinema_id = %s AND is_active = TRUE
            ORDER BY hall_name
        """
        results = cls.execute_query(query, (cinema_id,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_hall_type(cls, hall_type: str):
        """Get halls by hall type"""
        query = """
            SELECT * FROM cinema_halls 
            WHERE hall_type = %s AND is_active = TRUE
            ORDER BY cinema_id, hall_name
        """
        results = cls.execute_query(query, (hall_type,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_id(cls, table_name: str, hall_id: int):
        """Get hall by ID"""
        query = f"SELECT * FROM {table_name} WHERE hall_id = %s"
        result = cls.execute_query(query, (hall_id,), fetch_one=True)
        return cls.from_db_row(result) if result else None
    
    def get_cinema(self):
        """Get cinema for this hall"""
        if self._cinema is None:
            from .cinema import Cinema
            self._cinema = Cinema.get_by_id('cinemas', self.cinema_id)
        return self._cinema
    
    def get_seats(self) -> List:
        """Get all seats for this hall"""
        if self._seats is None:
            from .seat import Seat
            self._seats = Seat.get_all('seats', 'hall_id = %s', (self.hall_id,))
        return self._seats
    
    def get_available_seats(self, screening_id: int) -> List:
        """Get available seats for a specific screening"""
        from .seat import Seat
        return Seat.get_available_for_screening(screening_id, self.hall_id)
    
    def get_screenings(self) -> List:
        """Get screenings for this hall"""
        if self._screenings is None:
            from .screening import Screening
            self._screenings = Screening.get_by_hall_id(self.hall_id)
        return self._screenings
    
    def get_seat_map(self, screening_id: int = None) -> dict:
        """Get seat map for this hall"""
        seats = self.get_seats()
        seat_map = {}
        
        for seat in seats:
            row = seat.row_number
            if row not in seat_map:
                seat_map[row] = {}
            
            seat_info = {
                'seat_id': seat.seat_id,
                'seat_number': seat.seat_number,
                'seat_type': seat.seat_type,
                'price_multiplier': seat.price_multiplier,
                'is_available': True
            }
            
            # Check if seat is booked for specific screening
            if screening_id:
                from .seat import Seat
                if not Seat.is_available_for_screening(seat.seat_id, screening_id):
                    seat_info['is_available'] = False
            
            seat_map[row][seat.seat_number] = seat_info
        
        return seat_map
    
    def get_occupancy_rate(self, screening_id: int = None) -> float:
        """Get occupancy rate for this hall"""
        if screening_id:
            available_seats = len(self.get_available_seats(screening_id))
            return ((self.total_seats - available_seats) / self.total_seats) * 100
        return 0.0
    
    def is_available(self, screening_id: int = None) -> bool:
        """Check if hall has available seats"""
        if screening_id:
            return len(self.get_available_seats(screening_id)) > 0
        return True
    
    def get_hall_info(self) -> dict:
        """Get comprehensive hall information"""
        cinema = self.get_cinema()
        
        return {
            'hall_id': self.hall_id,
            'hall_name': self.hall_name,
            'hall_type': self.hall_type,
            'total_seats': self.total_seats,
            'total_rows': self.total_rows,
            'seats_per_row': self.seats_per_row,
            'screen_size': self.screen_size,
            'sound_system': self.sound_system,
            'cinema_name': cinema.cinema_name if cinema else 'Unknown',
            'cinema_address': cinema.address if cinema else 'Unknown'
        }
    
    def __str__(self):
        cinema = self.get_cinema()
        return f"CinemaHall({self.hall_name} at {cinema.cinema_name if cinema else 'Unknown'}, {self.hall_type})"
    
    def __repr__(self):
        return f"CinemaHall(hall_id={self.hall_id}, cinema_id={self.cinema_id}, hall_name='{self.hall_name}')"
