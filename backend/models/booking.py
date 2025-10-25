"""
Booking Model for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 18, 2025
"""

from .base import BaseModel
from typing import List, Optional
from datetime import datetime
import secrets
import string


class Booking(BaseModel):
    """Booking model with user and screening relationships"""
    
    def __init__(self, booking_id: int = None, user_id: int = None, screening_id: int = None,
                 booking_number: str = None, num_tickets: int = None, total_amount: float = None,
                 booking_status: str = 'confirmed', payment_method: str = None,
                 payment_status: str = 'pending', payment_date: datetime = None,
                 booking_date: datetime = None, created_at: datetime = None,
                 updated_at: datetime = None):
        self.booking_id = booking_id
        self.user_id = user_id
        self.screening_id = screening_id
        self.booking_number = booking_number
        self.num_tickets = num_tickets
        self.total_amount = total_amount
        self.booking_status = booking_status
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.payment_date = payment_date
        self.booking_date = booking_date
        self.created_at = created_at
        self.updated_at = updated_at
        
        # Additional properties
        self._user = None
        self._screening = None
        self._movie = None
        self._cinema = None
    
    @classmethod
    def from_db_row(cls, row):
        """Create Booking instance from database row"""
        return cls(
            booking_id=row[0],
            user_id=row[1],
            screening_id=row[2],
            booking_number=row[3],
            num_tickets=row[4],
            total_amount=row[5],
            booking_status=row[6],
            payment_method=row[7],
            payment_status=row[8],
            payment_date=row[9],
            booking_date=row[10],
            created_at=row[11],
            updated_at=row[12]
        )
    
    @classmethod
    def get_by_user_id(cls, user_id: int):
        """Get bookings by user ID"""
        query = """
            SELECT b.* FROM bookings b
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """
        results = cls.execute_query(query, (user_id,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_screening_id(cls, screening_id: int):
        """Get bookings by screening ID"""
        query = """
            SELECT b.* FROM bookings b
            WHERE b.screening_id = %s
            ORDER BY b.booking_date DESC
        """
        results = cls.execute_query(query, (screening_id,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_booking_number(cls, booking_number: str):
        """Get booking by booking number"""
        query = "SELECT * FROM bookings WHERE booking_number = %s"
        result = cls.execute_query(query, (booking_number,), fetch_one=True)
        
        if result:
            return cls.from_db_row(result)
        return None
    
    @classmethod
    def create_booking(cls, user_id: int, screening_id: int, num_tickets: int,
                      payment_method: str = None):
        """Create new booking"""
        # Get screening details
        from .screening import Screening
        screening = Screening.get_by_id('screenings', screening_id)
        
        if not screening:
            return None
        
        # Check if enough seats available
        if screening.available_seats < num_tickets:
            return None
        
        # Calculate total amount
        total_amount = screening.ticket_price * num_tickets
        
        # Generate unique booking number
        booking_number = cls.generate_booking_number()
        
        # Create booking data
        data = {
            'user_id': user_id,
            'screening_id': screening_id,
            'booking_number': booking_number,
            'num_tickets': num_tickets,
            'total_amount': total_amount,
            'booking_status': 'confirmed',
            'payment_method': payment_method,
            'payment_status': 'pending',
            'booking_date': datetime.now()
        }
        
        # Create booking
        booking = cls.create('bookings', data)
        
        if booking:
            # Update screening available seats
            screening.book_seats(num_tickets)
        
        return booking
    
    @staticmethod
    def generate_booking_number() -> str:
        """Generate unique booking number"""
        prefix = "BKG"
        year = datetime.now().year
        random_part = ''.join(secrets.choices(string.digits, k=6))
        return f"{prefix}-{year}-{random_part}"
    
    def get_user(self):
        """Get user for this booking"""
        if self._user is None:
            from .user import User
            self._user = User.get_by_id('users', self.user_id)
        return self._user
    
    def get_screening(self):
        """Get screening for this booking"""
        if self._screening is None:
            from .screening import Screening
            self._screening = Screening.get_by_id('screenings', self.screening_id)
        return self._screening
    
    def get_movie(self):
        """Get movie for this booking"""
        if self._movie is None:
            screening = self.get_screening()
            if screening:
                self._movie = screening.get_movie()
        return self._movie
    
    def get_cinema(self):
        """Get cinema for this booking"""
        if self._cinema is None:
            screening = self.get_screening()
            if screening:
                self._cinema = screening.get_cinema()
        return self._cinema
    
    def get_booking_info(self) -> dict:
        """Get comprehensive booking information"""
        user = self.get_user()
        screening = self.get_screening()
        movie = self.get_movie()
        cinema = self.get_cinema()
        
        return {
            'booking_id': self.booking_id,
            'booking_number': self.booking_number,
            'user_name': user.get_full_name() if user else 'Unknown',
            'user_email': user.email if user else 'Unknown',
            'movie_title': movie.title if movie else 'Unknown',
            'cinema_name': cinema.cinema_name if cinema else 'Unknown',
            'screening_date': screening.get_date_formatted() if screening else 'Unknown',
            'screening_time': screening.get_time_formatted() if screening else 'Unknown',
            'screen_number': screening.screen_number if screening else 'Unknown',
            'num_tickets': self.num_tickets,
            'total_amount': self.total_amount,
            'price_per_ticket': screening.ticket_price if screening else 0,
            'booking_status': self.booking_status,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None
        }
    
    def get_status_color(self) -> str:
        """Get status color for UI"""
        status_colors = {
            'pending': 'warning',
            'confirmed': 'success',
            'cancelled': 'danger',
            'completed': 'info'
        }
        return status_colors.get(self.booking_status, 'secondary')
    
    def get_payment_status_color(self) -> str:
        """Get payment status color for UI"""
        status_colors = {
            'pending': 'warning',
            'paid': 'success',
            'failed': 'danger',
            'refunded': 'info'
        }
        return status_colors.get(self.payment_status, 'secondary')
    
    def is_confirmed(self) -> bool:
        """Check if booking is confirmed"""
        return self.booking_status == 'confirmed'
    
    def is_cancelled(self) -> bool:
        """Check if booking is cancelled"""
        return self.booking_status == 'cancelled'
    
    def is_paid(self) -> bool:
        """Check if booking is paid"""
        return self.payment_status == 'paid'
    
    def can_cancel(self) -> bool:
        """Check if booking can be cancelled"""
        screening = self.get_screening()
        if not screening:
            return False
        
        # Can cancel if screening is not today and booking is confirmed
        from datetime import date
        return (self.booking_status == 'confirmed' and 
                screening.screening_date > date.today())
    
    def cancel_booking(self) -> bool:
        """Cancel this booking"""
        if not self.can_cancel():
            return False
        
        # Update booking status
        update_data = {
            'booking_status': 'cancelled',
            'updated_at': datetime.now()
        }
        
        result = self.update('bookings', self.booking_id, update_data)
        
        if result:
            self.booking_status = 'cancelled'
            
            # Free up seats in screening
            screening = self.get_screening()
            if screening:
                screening.cancel_booking(self.num_tickets)
            
            return True
        
        return False
    
    def confirm_payment(self, payment_method: str = None) -> bool:
        """Confirm payment for this booking"""
        if self.payment_status == 'paid':
            return True
        
        update_data = {
            'payment_status': 'paid',
            'payment_date': datetime.now(),
            'updated_at': datetime.now()
        }
        
        if payment_method:
            update_data['payment_method'] = payment_method
        
        result = self.update('bookings', self.booking_id, update_data)
        
        if result:
            self.payment_status = 'paid'
            self.payment_date = update_data['payment_date']
            if payment_method:
                self.payment_method = payment_method
            return True
        
        return False
    
    def get_qr_code_data(self) -> str:
        """Get QR code data for this booking"""
        return f"Booking:{self.booking_number}:{self.user_id}:{self.screening_id}"
    
    def get_ticket_info(self) -> dict:
        """Get ticket information for printing"""
        movie = self.get_movie()
        cinema = self.get_cinema()
        screening = self.get_screening()
        
        return {
            'booking_number': self.booking_number,
            'movie_title': movie.title if movie else 'Unknown',
            'cinema_name': cinema.cinema_name if cinema else 'Unknown',
            'cinema_address': cinema.get_full_address() if cinema else 'Unknown',
            'screening_date': screening.get_date_formatted() if screening else 'Unknown',
            'screening_time': screening.get_time_formatted() if screening else 'Unknown',
            'screen_number': screening.screen_number if screening else 'Unknown',
            'num_tickets': self.num_tickets,
            'total_amount': f"${self.total_amount:.2f}",
            'booking_date': self.booking_date.strftime('%Y-%m-%d %H:%M') if self.booking_date else 'Unknown'
        }
    
    def __str__(self):
        return f"Booking({self.booking_number}, {self.num_tickets} tickets, ${self.total_amount})"
    
    def __repr__(self):
        return f"Booking(booking_id={self.booking_id}, booking_number='{self.booking_number}', status='{self.booking_status}')"
