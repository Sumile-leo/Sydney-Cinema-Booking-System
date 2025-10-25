"""
Seat Model for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 26, 2025
"""

from .base import BaseModel
from typing import List, Optional
from datetime import datetime


class Seat(BaseModel):
    """Seat model with booking management"""
    
    def __init__(self, seat_id: int = None, hall_id: int = None, row_number: int = None,
                 seat_number: int = None, seat_type: str = 'standard', price_multiplier: float = 1.0,
                 is_active: bool = True):
        self.seat_id = seat_id
        self.hall_id = hall_id
        self.row_number = row_number
        self.seat_number = seat_number
        self.seat_type = seat_type
        self.price_multiplier = price_multiplier
        self.is_active = is_active
        
        # Additional properties
        self._hall = None
        self._bookings = None
    
    @classmethod
    def from_db_row(cls, row):
        """Create Seat instance from database row"""
        if not row:
            return None
        return cls(
            seat_id=row[0],
            hall_id=row[1],
            row_number=row[2],
            seat_number=row[3],
            seat_type=row[4],
            price_multiplier=float(row[5]) if row[5] else 1.0,
            is_active=row[6]
        )
    
    @classmethod
    def get_by_hall_id(cls, hall_id: int):
        """Get seats by hall ID"""
        query = """
            SELECT * FROM seats 
            WHERE hall_id = %s AND is_active = TRUE
            ORDER BY row_number, seat_number
        """
        results = cls.execute_query(query, (hall_id,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_row(cls, hall_id: int, row_number: int):
        """Get seats by hall and row"""
        query = """
            SELECT * FROM seats 
            WHERE hall_id = %s AND row_number = %s AND is_active = TRUE
            ORDER BY seat_number
        """
        results = cls.execute_query(query, (hall_id, row_number), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_available_for_screening(cls, screening_id: int, hall_id: int = None):
        """Get available seats for a screening"""
        if hall_id:
            query = """
                SELECT s.* FROM seats s
                LEFT JOIN seat_bookings sb ON s.seat_id = sb.seat_id AND sb.screening_id = %s
                WHERE s.hall_id = %s AND s.is_active = TRUE AND sb.seat_id IS NULL
                ORDER BY s.row_number, s.seat_number
            """
            params = (screening_id, hall_id)
        else:
            query = """
                SELECT s.* FROM seats s
                LEFT JOIN seat_bookings sb ON s.seat_id = sb.seat_id AND sb.screening_id = %s
                WHERE s.is_active = TRUE AND sb.seat_id IS NULL
                ORDER BY s.hall_id, s.row_number, s.seat_number
            """
            params = (screening_id,)
        
        results = cls.execute_query(query, params, fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def is_available_for_screening(cls, seat_id: int, screening_id: int) -> bool:
        """Check if seat is available for a specific screening"""
        query = """
            SELECT COUNT(*) FROM seat_bookings 
            WHERE seat_id = %s AND screening_id = %s
        """
        result = cls.execute_query(query, (seat_id, screening_id), fetch_one=True)
        return result[0] == 0 if result else False
    
    @classmethod
    def book_seat(cls, seat_id: int, screening_id: int, booking_id: int) -> bool:
        """Book a seat for a screening"""
        try:
            from .seat_booking import SeatBooking
            data = {
                'seat_id': seat_id,
                'screening_id': screening_id,
                'booking_id': booking_id,
                'booking_date': datetime.now()
            }
            result = SeatBooking.create('seat_bookings', data)
            return result is not None
        except Exception as e:
            print(f"Error booking seat: {e}")
            return False
    
    @classmethod
    def release_seat(cls, seat_id: int, screening_id: int) -> bool:
        """Release a booked seat"""
        query = """
            DELETE FROM seat_bookings 
            WHERE seat_id = %s AND screening_id = %s
        """
        result = cls.execute_query(query, (seat_id, screening_id))
        return result > 0
    
    @classmethod
    def get_by_id(cls, table_name: str, seat_id: int):
        """Get seat by ID"""
        query = f"SELECT * FROM {table_name} WHERE seat_id = %s"
        result = cls.execute_query(query, (seat_id,), fetch_one=True)
        return cls.from_db_row(result) if result else None
    
    def get_bookings(self) -> List:
        """Get bookings for this seat"""
        if self._bookings is None:
            from .seat_booking import SeatBooking
            self._bookings = SeatBooking.get_by_seat_id(self.seat_id)
        return self._bookings
    
    def is_available_for_screening_instance(self, screening_id: int) -> bool:
        """Check if this seat is available for a specific screening"""
        return Seat.is_available_for_screening(self.seat_id, screening_id)
    
    def get_price(self, base_price: float) -> float:
        """Get actual price for this seat"""
        return base_price * self.price_multiplier
    
    def get_seat_label(self) -> str:
        """Get seat label (e.g., 'A1', 'B5')"""
        row_letter = chr(ord('A') + self.row_number - 1)
        return f"{row_letter}{self.seat_number}"
    
    def get_seat_info(self) -> dict:
        """Get comprehensive seat information"""
        hall = self.get_hall()
        
        return {
            'seat_id': self.seat_id,
            'seat_label': self.get_seat_label(),
            'row_number': self.row_number,
            'seat_number': self.seat_number,
            'seat_type': self.seat_type,
            'price_multiplier': self.price_multiplier,
            'hall_name': hall.hall_name if hall else 'Unknown',
            'hall_type': hall.hall_type if hall else 'Unknown'
        }
    
    def __str__(self):
        return f"Seat({self.get_seat_label()}, {self.seat_type})"
    
    def __repr__(self):
        return f"Seat(seat_id={self.seat_id}, hall_id={self.hall_id}, row={self.row_number}, seat={self.seat_number})"
