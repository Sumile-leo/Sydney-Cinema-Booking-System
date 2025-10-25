"""
Movie Model for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 16, 2025
"""

from .base import BaseModel
from typing import List, Optional
from datetime import datetime, date


class Movie(BaseModel):
    """Movie model with screening relationships"""
    
    def __init__(self, movie_id: int = None, title: str = None, description: str = None,
                 genre: str = None, duration_minutes: int = None, release_date: date = None,
                 rating: str = None, director: str = None, cast: str = None,
                 language: str = 'English', subtitles: str = None, poster_url: str = None,
                 trailer_url: str = None, created_at: datetime = None,
                 updated_at: datetime = None, is_active: bool = True):
        self.movie_id = movie_id
        self.title = title
        self.description = description
        self.genre = genre
        self.duration_minutes = duration_minutes
        self.release_date = release_date
        self.rating = rating
        self.director = director
        self.cast = cast
        self.language = language
        self.subtitles = subtitles
        self.poster_url = poster_url
        self.trailer_url = trailer_url
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        
        # Additional properties
        self._screenings = None
        self._cinemas = None
        self._total_screenings = None
        self._average_rating = None
        self._duration_formatted = None
    
    @classmethod
    def from_db_row(cls, row):
        """Create Movie instance from database row"""
        if not row:
            return None
        return cls(
            movie_id=row[0],
            title=row[1],
            description=row[2],
            genre=row[3],
            duration_minutes=int(row[4]) if row[4] else 0,
            release_date=row[5],
            rating=row[6],
            director=row[7],
            cast=row[8],
            language=row[9],
            subtitles=row[10],
            poster_url=row[11],
            trailer_url=row[12],
            created_at=row[13],
            updated_at=row[14],
            is_active=row[15]
        )
    
    @classmethod
    def get_by_genre(cls, genre: str):
        """Get movies by genre"""
        query = "SELECT * FROM movies WHERE genre ILIKE %s AND is_active = TRUE ORDER BY release_date DESC"
        results = cls.execute_query(query, (f"%{genre}%",), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_by_rating(cls, rating: str):
        """Get movies by rating"""
        query = "SELECT * FROM movies WHERE rating = %s AND is_active = TRUE ORDER BY release_date DESC"
        results = cls.execute_query(query, (rating,), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def search_by_title(cls, title: str):
        """Search movies by title"""
        query = "SELECT * FROM movies WHERE title ILIKE %s AND is_active = TRUE ORDER BY release_date DESC"
        results = cls.execute_query(query, (f"%{title}%",), fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def get_now_showing(cls):
        """Get movies currently showing"""
        query = """
            SELECT DISTINCT m.* FROM movies m
            JOIN screenings s ON m.movie_id = s.movie_id
            WHERE s.screening_date >= CURRENT_DATE AND s.is_active = TRUE AND m.is_active = TRUE
            ORDER BY m.release_date DESC
        """
        results = cls.execute_query(query, fetch_all=True)
        
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    def get_screenings(self, cinema_id: int = None, date: str = None) -> List:
        """Get screenings for this movie"""
        if self._screenings is None or cinema_id or date:
            from .screening import Screening
            
            query = "SELECT s.* FROM screenings s WHERE s.movie_id = %s AND s.is_active = TRUE"
            params = [self.movie_id]
            
            if cinema_id:
                query += " AND s.cinema_id = %s"
                params.append(cinema_id)
            
            if date:
                query += " AND s.screening_date = %s"
                params.append(date)
            
            query += " ORDER BY s.screening_date, s.start_time"
            
            results = self.execute_query(query, tuple(params), fetch_all=True)
            
            if results:
                self._screenings = [Screening.from_db_row(row) for row in results]
            else:
                self._screenings = []
        
        return self._screenings
    
    def get_cinemas(self) -> List:
        """Get cinemas showing this movie"""
        if self._cinemas is None:
            from .cinema import Cinema
            query = """
                SELECT DISTINCT c.* FROM cinemas c
                JOIN screenings s ON c.cinema_id = s.cinema_id
                WHERE s.movie_id = %s AND s.is_active = TRUE AND c.is_active = TRUE
                ORDER BY c.cinema_name
            """
            results = self.execute_query(query, (self.movie_id,), fetch_all=True)
            
            if results:
                self._cinemas = [Cinema.from_db_row(row) for row in results]
            else:
                self._cinemas = []
        
        return self._cinemas
    
    def get_total_screenings(self) -> int:
        """Get total number of screenings"""
        if self._total_screenings is None:
            query = """
                SELECT COUNT(*) FROM screenings 
                WHERE movie_id = %s AND is_active = TRUE
            """
            result = self.execute_query(query, (self.movie_id,), fetch_one=True)
            self._total_screenings = result[0] if result else 0
        return self._total_screenings
    
    def get_duration_formatted(self) -> str:
        """Get formatted duration string"""
        if self._duration_formatted is None:
            try:
                duration = int(self.duration_minutes) if self.duration_minutes else 0
                hours = duration // 60
                minutes = duration % 60
                
                if hours > 0:
                    self._duration_formatted = f"{hours}h {minutes}m"
                else:
                    self._duration_formatted = f"{minutes}m"
            except (ValueError, TypeError):
                self._duration_formatted = "Unknown"
        
        return self._duration_formatted
    
    def get_cast_list(self) -> List[str]:
        """Get cast as a list"""
        if self.cast:
            return [actor.strip() for actor in self.cast.split(',')]
        return []
    
    def get_subtitles_list(self) -> List[str]:
        """Get subtitles as a list"""
        if self.subtitles:
            return [subtitle.strip() for subtitle in self.subtitles.split(',')]
        return []
    
    def is_now_showing(self) -> bool:
        """Check if movie is currently showing"""
        return len(self.get_screenings()) > 0
    
    def get_release_status(self) -> str:
        """Get release status"""
        if not self.release_date:
            return "Unknown"
        
        today = date.today()
        if self.release_date > today:
            days_until = (self.release_date - today).days
            return f"Coming Soon ({days_until} days)"
        elif self.release_date == today:
            return "Released Today"
        else:
            days_since = (today - self.release_date).days
            if days_since < 7:
                return f"New Release ({days_since} days ago)"
            elif days_since < 30:
                return f"Recently Released ({days_since} days ago)"
            else:
                return f"Released ({days_since} days ago)"
    
    def get_movie_info(self) -> dict:
        """Get comprehensive movie information"""
        return {
            'title': self.title,
            'genre': self.genre,
            'rating': self.rating,
            'duration': self.get_duration_formatted(),
            'director': self.director,
            'cast': self.get_cast_list(),
            'language': self.language,
            'subtitles': self.get_subtitles_list(),
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'release_status': self.get_release_status(),
            'poster_url': self.poster_url,
            'trailer_url': self.trailer_url,
            'description': self.description
        }
    
    def get_screening_info(self) -> dict:
        """Get screening information"""
        screenings = self.get_screenings()
        cinemas = self.get_cinemas()
        
        return {
            'total_screenings': self.get_total_screenings(),
            'cinemas_count': len(cinemas),
            'cinemas': [cinema.cinema_name for cinema in cinemas],
            'is_showing': self.is_now_showing(),
            'next_screening': screenings[0] if screenings else None
        }
    
    def add_screening(self, cinema_id: int, screen_number: int, screening_date: str,
                     start_time: str, end_time: str, ticket_price: float,
                     total_seats: int, screening_type: str = 'standard'):
        """Add new screening for this movie"""
        from .screening import Screening
        
        data = {
            'movie_id': self.movie_id,
            'cinema_id': cinema_id,
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
        """Update movie information"""
        allowed_fields = ['title', 'description', 'genre', 'duration_minutes', 'release_date',
                         'rating', 'director', 'cast', 'language', 'subtitles', 'poster_url', 'trailer_url']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if update_data:
            update_data['updated_at'] = datetime.now()
            return self.update('movies', self.movie_id, update_data)
        return None
    
    def __str__(self):
        return f"Movie({self.title}, {self.genre})"
    
    def __repr__(self):
        return f"Movie(movie_id={self.movie_id}, title='{self.title}', rating='{self.rating}')"
