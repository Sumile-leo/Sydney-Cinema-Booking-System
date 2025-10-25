"""
Cinema Model for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 15, 2025
"""

from .base import BaseModel
from typing import List, Optional
from datetime import datetime


class Cinema(BaseModel):
    """Cinema model with screening relationships"""
    
    def __init__(self, cinema_id: int = None, cinema_name: str = None, address: str = None,
                 suburb: str = None, postcode: str = None, phone: str = None,
                 total_screens: int = None, facilities: str = None, parking_info: str = None,
                 public_transport: str = None, created_at: datetime = None,
                 updated_at: datetime = None, is_active: bool = True):
        self.cinema_id = cinema_id
        self.cinema_name = cinema_name
        self.address = address
        self.suburb = suburb
        self.postcode = postcode
        self.phone = phone
        self.total_screens = total_screens
        self.facilities = facilities
        self.parking_info = parking_info
        self.public_transport = public_transport
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        
        # Additional properties
        self._screenings = None
        self._movies = None
        self._total_screenings = None
        self._available_screens = None
    
    @classmethod
    def from_db_row(cls, row):
        """Create Cinema instance from database row"""
        return cls(
            cinema_id=row[0],
            cinema_name=row[1],
            address=row[2],
            suburb=row[3],
            postcode=row[4],
            phone=row[5],
            total_screens=row[6],
            facilities=row[7],
            parking_info=row[8],
            public_transport=row[9],
            created_at=row[10],
            updated_at=row[11],
            is_active=row[12]
        )
    
    @classmethod
    def get_by_suburb(cls, suburb: str):
        """Get cinemas by suburb"""
        query = "SELECT * FROM cinemas WHERE suburb ILIKE %s AND is_active = TRUE"
        results = cls.execute_query(query, (f"%{suburb}%",), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def search_by_name(cls, name: str):
        """Search cinemas by name"""
        query = "SELECT * FROM cinemas WHERE cinema_name ILIKE %s AND is_active = TRUE"
        results = cls.execute_query(query, (f"%{name}%",), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    def get_screenings(self, date: str = None) -> List:
        """Get screenings for this cinema"""
        if self._screenings is None or date:
            from .screening import Screening
            if date:
                query = """
                    SELECT s.* FROM screenings s
                    WHERE s.cinema_id = %s AND s.screening_date = %s AND s.is_active = TRUE
                    ORDER BY s.start_time
                """
                results = self.execute_query(query, (self.cinema_id, date), fetch_all=True)
            else:
                query = """
                    SELECT s.* FROM screenings s
                    WHERE s.cinema_id = %s AND s.is_active = TRUE
                    ORDER BY s.screening_date, s.start_time
                """
                results = self.execute_query(query, (self.cinema_id,), fetch_all=True)
            
            if results:
                self._screenings = [Screening.from_db_row(row) for row in results]
            else:
                self._screenings = []
        
        return self._screenings
    
    def get_movies(self) -> List:
        """Get movies currently showing at this cinema"""
        if self._movies is None:
            from .movie import Movie
            query = """
                SELECT DISTINCT m.* FROM movies m
                JOIN screenings s ON m.movie_id = s.movie_id
                WHERE s.cinema_id = %s AND s.is_active = TRUE AND m.is_active = TRUE
                ORDER BY m.title
            """
            results = self.execute_query(query, (self.cinema_id,), fetch_all=True)
            
            if results:
                self._movies = [Movie.from_db_row(row) for row in results]
            else:
                self._movies = []
        
        return self._movies
    
    def get_total_screenings(self) -> int:
        """Get total number of screenings"""
        if self._total_screenings is None:
            query = """
                SELECT COUNT(*) FROM screenings 
                WHERE cinema_id = %s AND is_active = TRUE
            """
            result = self.execute_query(query, (self.cinema_id,), fetch_one=True)
            self._total_screenings = result[0] if result else 0
        return self._total_screenings
    
    def get_available_screens(self) -> int:
        """Get number of available screens (not currently in use)"""
        if self._available_screens is None:
            query = """
                SELECT COUNT(DISTINCT screen_number) FROM screenings 
                WHERE cinema_id = %s AND screening_date = CURRENT_DATE AND is_active = TRUE
            """
            result = self.execute_query(query, (self.cinema_id,), fetch_one=True)
            used_screens = result[0] if result else 0
            self._available_screens = self.total_screens - used_screens
        return self._available_screens
    
    def get_facilities_list(self) -> List[str]:
        """Get facilities as a list"""
        if self.facilities:
            return [facility.strip() for facility in self.facilities.split(',')]
        return []
    
    def has_facility(self, facility: str) -> bool:
        """Check if cinema has specific facility"""
        facilities = self.get_facilities_list()
        return any(facility.lower() in f.lower() for f in facilities)
    
    def get_full_address(self) -> str:
        """Get full address string"""
        return f"{self.address}, {self.suburb} {self.postcode}"
    
    def get_location_info(self) -> dict:
        """Get location information as dictionary"""
        return {
            'address': self.address,
            'suburb': self.suburb,
            'postcode': self.postcode,
            'full_address': self.get_full_address(),
            'parking': self.parking_info,
            'transport': self.public_transport
        }
    
    def get_screening_stats(self) -> dict:
        """Get screening statistics"""
        return {
            'total_screens': self.total_screens,
            'available_screens': self.get_available_screens(),
            'total_screenings': self.get_total_screenings(),
            'movies_showing': len(self.get_movies())
        }
    
    def add_screening(self, movie_id: int, screen_number: int, screening_date: str,
                     start_time: str, end_time: str, ticket_price: float,
                     total_seats: int, screening_type: str = 'standard'):
        """Add new screening to this cinema"""
        from .screening import Screening
        
        data = {
            'movie_id': movie_id,
            'cinema_id': self.cinema_id,
            'screen_number': screen_number,
            'screening_date': screening_date,
            'start_time': start_time,
            'end_time': end_time,
            'ticket_price': ticket_price,
            'available_seats': total_seats,
            'total_seats': total_seats,
            'screening_type': screening_type,
            'is_active': True
        }
        
        return Screening.create('screenings', data)
    
    def update_info(self, **kwargs):
        """Update cinema information"""
        allowed_fields = ['cinema_name', 'address', 'suburb', 'postcode', 'phone',
                         'total_screens', 'facilities', 'parking_info', 'public_transport']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if update_data:
            update_data['updated_at'] = datetime.now()
            return self.update('cinemas', self.cinema_id, update_data)
        return None
    
    def __str__(self):
        return f"Cinema({self.cinema_name}, {self.suburb})"
    
    def __repr__(self):
        return f"Cinema(cinema_id={self.cinema_id}, name='{self.cinema_name}', suburb='{self.suburb}')"
