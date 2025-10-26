"""
Business logic services
"""

from database.db import (
    get_user_by_username, create_user, check_username_or_email_exists,
    get_all_cinemas, get_cinema_by_id, create_cinema,
    get_all_movies, get_movie_by_id, create_movie,
    get_bookings_with_details, get_seats_by_booking, can_cancel_booking
)
from backend.models.user import User
from backend.models.cinema import Cinema
from backend.models.movie import Movie
from backend.models.booking import Booking


class UserService:
    """User business logic service"""
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate a user
        Returns User object if successful, None otherwise
        """
        user_row = get_user_by_username(username)
        if not user_row:
            return None
        
        # Plain text password comparison
        if user_row[2] == password:  # user_row[2] is password field
            return User.from_db_row(user_row)
        return None
    
    @staticmethod
    def register_user(username, email, password, first_name, last_name, phone):
        """
        Register a new user
        Returns True if successful, False otherwise
        """
        # Check if user already exists
        if check_username_or_email_exists(username, email):
            return False
        
        # Create user
        return create_user(username, email, password, first_name, last_name, phone)


class CinemaService:
    """Cinema business logic service"""
    
    @staticmethod
    def get_all_cinemas():
        """
        Get all cinemas
        Returns list of Cinema objects
        """
        cinema_rows = get_all_cinemas()
        return [Cinema.from_db_row(row) for row in cinema_rows]
    
    @staticmethod
    def get_cinema_by_id(cinema_id):
        """
        Get cinema by ID
        Returns Cinema object or None
        """
        cinema_row = get_cinema_by_id(cinema_id)
        if cinema_row:
            return Cinema.from_db_row(cinema_row)
        return None
    
    @staticmethod
    def create_cinema(cinema_name, address, suburb, postcode, phone=None, email=None, facilities=None, is_active=True):
        """
        Create a new cinema
        Returns True if successful, False otherwise
        """
        return create_cinema(cinema_name, address, suburb, postcode, phone, email, facilities, is_active)


class MovieService:
    """Movie business logic service"""
    
    @staticmethod
    def get_all_movies():
        """
        Get all movies
        Returns list of Movie objects
        """
        movie_rows = get_all_movies()
        return [Movie.from_db_row(row) for row in movie_rows]
    
    @staticmethod
    def get_movie_by_id(movie_id):
        """
        Get movie by ID
        Returns Movie object or None
        """
        movie_row = get_movie_by_id(movie_id)
        if movie_row:
            return Movie.from_db_row(movie_row)
        return None
    
    @staticmethod
    def create_movie(title, description, genre, duration_minutes, release_date, director, cast, language, subtitles, is_active=True):
        """
        Create a new movie
        Returns True if successful, False otherwise
        """
        return create_movie(title, description, genre, duration_minutes, release_date, director, cast, language, subtitles, is_active)


class BookingService:
    """Booking business logic service"""
    
    @staticmethod
    def get_user_bookings_with_seats(user_id):
        """
        Get all bookings for a user with detailed screening and seat information
        Returns list of booking dictionaries
        """
        bookings_data = get_bookings_with_details(user_id)
        result = []
        
        for booking_row in bookings_data:
            booking = Booking.from_db_row(booking_row)
            
            # Get seats for this booking
            seats_data = get_seats_by_booking(booking.booking_id)
            seats = []
            for seat_row in seats_data:
                seats.append({
                    'seat_id': seat_row[0],
                    'row_number': seat_row[1],
                    'seat_number': seat_row[2],
                    'seat_type': seat_row[3] if len(seat_row) > 3 else 'standard'
                })
            
            # Format seat numbers for display - one ticket per line
            seat_display = '<br>'.join([f"Row {seat['row_number']}, Seat {seat['seat_number']}" for seat in seats])
            
            # Check if booking can be cancelled
            can_cancel, cancel_message = can_cancel_booking(booking.booking_id)
            
            # Create booking dictionary with screening details
            booking_dict = {
                'booking_id': booking.booking_id,
                'booking_number': booking.booking_number,
                'num_tickets': booking.num_tickets,
                'total_amount': float(booking.total_amount),
                'booking_status': booking.booking_status,
                'payment_status': booking.payment_status,
                'booking_date': booking.booking_date,
                'can_cancel': can_cancel,
                'cancel_message': cancel_message,
                # Screening details
                'screening_date': booking_row[11] if len(booking_row) > 11 else None,
                'start_time': booking_row[12] if len(booking_row) > 12 else None,
                'end_time': booking_row[13] if len(booking_row) > 13 else None,
                'movie_title': booking_row[14] if len(booking_row) > 14 else 'Unknown Movie',
                'cinema_name': booking_row[15] if len(booking_row) > 15 else 'Unknown Cinema',
                'cinema_address': f"{booking_row[16] if len(booking_row) > 16 else ''}, {booking_row[17] if len(booking_row) > 17 else ''}",
                'seats': seats,
                'seats_display': seat_display if seat_display else 'No seats assigned'
            }
            
            result.append(booking_dict)
        
        return result
