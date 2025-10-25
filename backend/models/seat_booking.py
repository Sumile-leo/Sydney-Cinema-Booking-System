"""
Seat Booking Model for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 26, 2025
"""

from .base import BaseModel
from typing import List, Optional
from datetime import datetime


class SeatBooking(BaseModel):
    """Seat booking model linking bookings to specific seats"""
    
    def __init__(self, seat_booking_id: int = None, booking_id: int = None, seat_id: int = None,
                 screening_id: int = None, booking_date: datetime = None):
        self.seat_booking_id = seat_booking_id
        self.booking_id = booking_id
        self.seat_id = seat_id
        self.screening_id = screening_id
        self.booking_date = booking_date
        
        # Additional properties
        self._booking = None
        self._seat = None
        self._screening = None
    
    @classmethod
    def from_db_row(cls, row):
        """Create SeatBooking instance from database row"""
        if not row:
            return None
        return cls(
            seat_booking_id=row[0],
            booking_id=row[1],
            seat_id=row[2],
            screening_id=row[3],
            booking_date=row[4]
        )
    
    @classmethod
    def get_by_booking_id(cls, booking_id: int):
        """Get seat bookings by booking ID"""
        query = """
            SELECT * FROM seat_bookings 
            WHERE booking_id = %s
            ORDER BY booking_date
        """
        results = cls.execute_query(query, (booking_id,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_screening_id(cls, screening_id: int):
        """Get seat bookings by screening ID"""
        query = """
            SELECT * FROM seat_bookings 
            WHERE screening_id = %s
            ORDER BY booking_date
        """
        results = cls.execute_query(query, (screening_id,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_seat_id(cls, seat_id: int):
        """Get seat bookings by seat ID"""
        query = """
            SELECT * FROM seat_bookings 
            WHERE seat_id = %s
            ORDER BY booking_date DESC
        """
        results = cls.execute_query(query, (seat_id,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def create_seat_booking(cls, booking_id: int, seat_id: int, screening_id: int) -> 'SeatBooking':
        """Create new seat booking"""
        data = {
            'booking_id': booking_id,
            'seat_id': seat_id,
            'screening_id': screening_id,
            'booking_date': datetime.now()
        }
        
        result = cls.create('seat_bookings', data)
        return result
    
    @classmethod
    def cancel_seat_booking(cls, booking_id: int, seat_id: int, screening_id: int) -> bool:
        """Cancel a seat booking"""
        query = """
            DELETE FROM seat_bookings 
            WHERE booking_id = %s AND seat_id = %s AND screening_id = %s
        """
        result = cls.execute_query(query, (booking_id, seat_id, screening_id))
        return result > 0
    
    def get_booking(self):
        """Get booking for this seat booking"""
        if self._booking is None:
            from .booking import Booking
            self._booking = Booking.get_by_id('bookings', self.booking_id)
        return self._booking
    
    def get_seat(self):
        """Get seat for this seat booking"""
        if self._seat is None:
            from .seat import Seat
            self._seat = Seat.get_by_id('seats', self.seat_id)
        return self._seat
    
    def get_screening(self):
        """Get screening for this seat booking"""
        if self._screening is None:
            from .screening import Screening
            self._screening = Screening.get_by_id('screenings', self.screening_id)
        return self._screening
    
    def get_seat_booking_info(self) -> dict:
        """Get comprehensive seat booking information"""
        booking = self.get_booking()
        seat = self.get_seat()
        screening = self.get_screening()
        
        return {
            'seat_booking_id': self.seat_booking_id,
            'booking_number': booking.booking_number if booking else 'Unknown',
            'seat_label': seat.get_seat_label() if seat else 'Unknown',
            'seat_type': seat.seat_type if seat else 'Unknown',
            'screening_date': screening.get_date_formatted() if screening else 'Unknown',
            'screening_time': screening.get_time_formatted() if screening else 'Unknown',
            'booking_date': self.booking_date.strftime('%Y-%m-%d %H:%M') if self.booking_date else 'Unknown'
        }
    
    def __str__(self):
        seat = self.get_seat()
        booking = self.get_booking()
        return f"SeatBooking({seat.get_seat_label() if seat else 'Unknown'} for {booking.booking_number if booking else 'Unknown'})"
    
    def __repr__(self):
        return f"SeatBooking(seat_booking_id={self.seat_booking_id}, booking_id={self.booking_id}, seat_id={self.seat_id})"
