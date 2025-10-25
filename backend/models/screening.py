"""
Screening Model for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 17, 2025
"""

from .base import BaseModel
from typing import List, Optional
from datetime import datetime, date, time


class Screening(BaseModel):
    """Screening model with booking relationships"""
    
    def __init__(self, screening_id: int = None, movie_id: int = None, cinema_id: int = None,
                 screen_number: int = None, screening_date: date = None, start_time: time = None,
                 end_time: time = None, ticket_price: float = None, available_seats: int = None,
                 total_seats: int = None, screening_type: str = 'standard', language: str = 'English',
                 subtitles: str = None, created_at: datetime = None, updated_at: datetime = None,
                 is_active: bool = True):
        self.screening_id = screening_id
        self.movie_id = movie_id
        self.cinema_id = cinema_id
        self.screen_number = screen_number
        self.screening_date = screening_date
        self.start_time = start_time
        self.end_time = end_time
        self.ticket_price = ticket_price
        self.available_seats = available_seats
        self.total_seats = total_seats
        self.screening_type = screening_type
        self.language = language
        self.subtitles = subtitles
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        
        # Additional properties
        self._movie = None
        self._cinema = None
        self._bookings = None
        self._total_bookings = None
        self._occupancy_rate = None
    
    @classmethod
    def from_db_row(cls, row):
        """Create Screening instance from database row"""
        return cls(
            screening_id=row[0],
            movie_id=row[1],
            cinema_id=row[2],
            screen_number=row[3],
            screening_date=row[4],
            start_time=row[5],
            end_time=row[6],
            ticket_price=row[7],
            available_seats=row[8],
            total_seats=row[9],
            screening_type=row[10],
            language=row[11],
            subtitles=row[12],
            created_at=row[13],
            updated_at=row[14],
            is_active=row[15]
        )
    
    @classmethod
    def get_by_date(cls, date: str):
        """Get screenings by date"""
        query = """
            SELECT s.* FROM screenings s
            WHERE s.screening_date = %s AND s.is_active = TRUE
            ORDER BY s.start_time
        """
        results = cls.execute_query(query, (date,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_cinema_and_date(cls, cinema_id: int, date: str):
        """Get screenings by cinema and date"""
        query = """
            SELECT s.* FROM screenings s
            WHERE s.cinema_id = %s AND s.screening_date = %s AND s.is_active = TRUE
            ORDER BY s.start_time
        """
        results = cls.execute_query(query, (cinema_id, date), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_movie_and_cinema(cls, movie_id: int, cinema_id: int):
        """Get screenings by movie and cinema"""
        query = """
            SELECT s.* FROM screenings s
            WHERE s.movie_id = %s AND s.cinema_id = %s AND s.is_active = TRUE
            ORDER BY s.screening_date, s.start_time
        """
        results = cls.execute_query(query, (movie_id, cinema_id), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_upcoming(cls, limit: int = 10):
        """Get upcoming screenings"""
        query = """
            SELECT s.* FROM screenings s
            WHERE s.screening_date >= CURRENT_DATE AND s.is_active = TRUE
            ORDER BY s.screening_date, s.start_time
            LIMIT %s
        """
        results = cls.execute_query(query, (limit,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    def get_movie(self):
        """Get movie for this screening"""
        if self._movie is None:
            from .movie import Movie
            self._movie = Movie.get_by_id('movies', self.movie_id)
        return self._movie
    
    def get_cinema(self):
        """Get cinema for this screening"""
        if self._cinema is None:
            from .cinema import Cinema
            self._cinema = Cinema.get_by_id('cinemas', self.cinema_id)
        return self._cinema
    
    def get_bookings(self) -> List:
        """Get bookings for this screening"""
        if self._bookings is None:
            from .booking import Booking
            self._bookings = Booking.get_by_screening_id(self.screening_id)
        return self._bookings
    
    def get_total_bookings(self) -> int:
        """Get total number of bookings"""
        if self._total_bookings is None:
            query = """
                SELECT COUNT(*) FROM bookings 
                WHERE screening_id = %s AND booking_status != 'cancelled'
            """
            result = self.execute_query(query, (self.screening_id,), fetch_one=True)
            self._total_bookings = result[0] if result else 0
        return self._total_bookings
    
    def get_occupancy_rate(self) -> float:
        """Get occupancy rate as percentage"""
        if self._occupancy_rate is None:
            if self.total_seats > 0:
                occupied_seats = self.total_seats - self.available_seats
                self._occupancy_rate = (occupied_seats / self.total_seats) * 100
            else:
                self._occupancy_rate = 0.0
        return self._occupancy_rate
    
    def is_available(self) -> bool:
        """Check if screening has available seats"""
        return self.available_seats > 0
    
    def is_full(self) -> bool:
        """Check if screening is full"""
        return self.available_seats == 0
    
    def is_today(self) -> bool:
        """Check if screening is today"""
        return self.screening_date == date.today()
    
    def is_upcoming(self) -> bool:
        """Check if screening is upcoming"""
        return self.screening_date >= date.today()
    
    def get_time_formatted(self) -> str:
        """Get formatted time string"""
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    def get_date_formatted(self) -> str:
        """Get formatted date string"""
        return self.screening_date.strftime('%Y-%m-%d')
    
    def get_datetime_formatted(self) -> str:
        """Get formatted datetime string"""
        return f"{self.get_date_formatted()} {self.get_time_formatted()}"
    
    def get_price_formatted(self) -> str:
        """Get formatted price string"""
        return f"${self.ticket_price:.2f}"
    
    def get_screening_info(self) -> dict:
        """Get comprehensive screening information"""
        movie = self.get_movie()
        cinema = self.get_cinema()
        
        return {
            'screening_id': self.screening_id,
            'movie_title': movie.title if movie else 'Unknown',
            'cinema_name': cinema.cinema_name if cinema else 'Unknown',
            'screen_number': self.screen_number,
            'date': self.get_date_formatted(),
            'time': self.get_time_formatted(),
            'datetime': self.get_datetime_formatted(),
            'price': self.get_price_formatted(),
            'available_seats': self.available_seats,
            'total_seats': self.total_seats,
            'occupancy_rate': f"{self.get_occupancy_rate():.1f}%",
            'screening_type': self.screening_type,
            'language': self.language,
            'subtitles': self.subtitles,
            'is_available': self.is_available(),
            'is_full': self.is_full()
        }
    
    def book_seats(self, num_seats: int) -> bool:
        """Book seats for this screening"""
        if self.available_seats >= num_seats:
            new_available = self.available_seats - num_seats
            update_data = {
                'available_seats': new_available,
                'updated_at': datetime.now()
            }
            
            result = self.update('screenings', self.screening_id, update_data)
            if result:
                self.available_seats = new_available
                return True
        return False
    
    def cancel_booking(self, num_seats: int) -> bool:
        """Cancel booking and free up seats"""
        new_available = min(self.available_seats + num_seats, self.total_seats)
        update_data = {
            'available_seats': new_available,
            'updated_at': datetime.now()
        }
        
        result = self.update('screenings', self.screening_id, update_data)
        if result:
            self.available_seats = new_available
            return True
        return False
    
    def update_screening(self, **kwargs):
        """Update screening information"""
        allowed_fields = ['screen_number', 'screening_date', 'start_time', 'end_time',
                         'ticket_price', 'available_seats', 'total_seats', 'screening_type',
                         'language', 'subtitles']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if update_data:
            update_data['updated_at'] = datetime.now()
            return self.update('screenings', self.screening_id, update_data)
        return None
    
    def __str__(self):
        movie = self.get_movie()
        cinema = self.get_cinema()
        return f"Screening({movie.title if movie else 'Unknown'} at {cinema.cinema_name if cinema else 'Unknown'}, {self.get_datetime_formatted()})"
    
    def __repr__(self):
        return f"Screening(screening_id={self.screening_id}, movie_id={self.movie_id}, cinema_id={self.cinema_id})"
