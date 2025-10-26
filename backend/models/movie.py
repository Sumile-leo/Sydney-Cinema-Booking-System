"""
Movie model
"""

from typing import Optional, Tuple
from datetime import datetime, date


class Movie:
    """Movie data model"""
    
    def __init__(self, movie_id: int, title: str, description: str = None, 
                 genre: str = None, duration_minutes: int = None,
                 release_date: date = None, director: str = None,
                 cast: str = None, language: str = None, subtitles: str = None,
                 created_at: datetime = None, updated_at: datetime = None,
                 is_active: bool = True):
        self.movie_id = movie_id
        self.title = title
        self.description = description
        self.genre = genre
        self.duration_minutes = duration_minutes
        self.release_date = release_date
        self.director = director
        self.cast = cast
        self.language = language
        self.subtitles = subtitles
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
    
    @classmethod
    def from_db_row(cls, db_row: Tuple) -> 'Movie':
        """
        Create Movie instance from database row tuple
        db_row: (movie_id, title, description, genre, duration_minutes, release_date, 
                 director, cast, language, subtitles, created_at, updated_at, is_active)
        """
        return cls(
            movie_id=db_row[0],
            title=db_row[1],
            description=db_row[2] if len(db_row) > 2 and db_row[2] else None,
            genre=db_row[3] if len(db_row) > 3 and db_row[3] else None,
            duration_minutes=db_row[4] if len(db_row) > 4 and db_row[4] else None,
            release_date=db_row[5] if len(db_row) > 5 and db_row[5] else None,
            director=db_row[6] if len(db_row) > 6 and db_row[6] else None,
            cast=db_row[7] if len(db_row) > 7 and db_row[7] else None,
            language=db_row[8] if len(db_row) > 8 and db_row[8] else None,
            subtitles=db_row[9] if len(db_row) > 9 and db_row[9] else None,
            created_at=db_row[10] if len(db_row) > 10 else None,
            updated_at=db_row[11] if len(db_row) > 11 else None,
            is_active=db_row[12] if len(db_row) > 12 else True
        )
    
    def to_dict(self) -> dict:
        """Convert Movie to dictionary"""
        return {
            'movie_id': self.movie_id,
            'title': self.title,
            'description': self.description,
            'genre': self.genre,
            'duration_minutes': self.duration_minutes,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'director': self.director,
            'cast': self.cast,
            'language': self.language,
            'subtitles': self.subtitles,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
    
    def get_duration_formatted(self) -> str:
        """Get formatted duration (e.g., '2h 15m')"""
        if not self.duration_minutes:
            return "N/A"
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        if hours > 0 and minutes > 0:
            return f"{hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"
    
    def get_release_date_formatted(self) -> str:
        """Get formatted release date"""
        if not self.release_date:
            return "TBA"
        return self.release_date.strftime("%B %d, %Y")
    
    def __repr__(self) -> str:
        return f"<Movie {self.title} ({self.movie_id})>"
