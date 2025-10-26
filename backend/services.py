"""
Business logic services
Author: Zhou Li
Date: 2025-10-18
"""

from database.db import (
    get_user_by_username, create_user, check_username_or_email_exists,
    get_all_cinemas, get_cinema_by_id, create_cinema,
    get_all_movies, get_movie_by_id, create_movie,
    get_bookings_with_details, get_seats_by_booking, can_cancel_booking,
    cancel_booking, get_booking_user_id, get_screening_by_id, get_cinema_hall_by_id,
    get_seats_by_hall, get_cinema_by_id, get_cinema_halls_by_cinema,
    get_screenings_by_movie, get_screenings_by_cinema, get_all_screenings,
    get_db_connection
)
from backend.models.user import User
from backend.models.cinema import Cinema
from backend.models.movie import Movie
from backend.models.booking import Booking
from backend.models.screening import Screening
from backend.models.cinema_hall import CinemaHall


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
            
            # Format times for display
            start_time_str = None
            if len(booking_row) > 12 and booking_row[12]:
                start_time_str = booking_row[12].strftime("%H:%M") if hasattr(booking_row[12], 'strftime') else str(booking_row[12])[:5]
            
            end_time_str = None
            if len(booking_row) > 13 and booking_row[13]:
                end_time_str = booking_row[13].strftime("%H:%M") if hasattr(booking_row[13], 'strftime') else str(booking_row[13])[:5]
            
            # Create booking dictionary with screening details
            booking_dict = {
                'booking_id': booking.booking_id,
                'booking_number': booking.booking_number,
                'num_tickets': booking.num_tickets,
                'total_amount': float(booking.total_amount),
                'status': booking.booking_status,  # Add 'status' field
                'booking_status': booking.booking_status,
                'payment_status': booking.payment_status,
                'booking_date': booking.booking_date,
                'can_cancel': can_cancel,
                'cancel_message': cancel_message,
                # Screening details
                'screening_id': booking.screening_id,  # Add screening_id
                'screening_date': booking_row[11] if len(booking_row) > 11 else None,
                'screening_time': booking_row[12] if len(booking_row) > 12 else None,
                'start_time': start_time_str,  # Format as string
                'end_time': end_time_str,  # Format as string
                'movie_id': booking_row[14] if len(booking_row) > 14 else None,
                'movie_title': booking_row[15] if len(booking_row) > 15 else 'Unknown Movie',
                'cinema_name': booking_row[16] if len(booking_row) > 16 else 'Unknown Cinema',
                'cinema_address': f"{booking_row[17] if len(booking_row) > 17 else ''}, {booking_row[18] if len(booking_row) > 18 else ''}",
                'seats': seats,
                'seats_display': seat_display if seat_display else 'No seats assigned'
            }
            
            result.append(booking_dict)
        
        return result
    
    @staticmethod
    def cancel_user_booking(booking_id, user_id):
        """Cancel a booking after validation"""
        # Verify booking belongs to user
        booking_user_id = get_booking_user_id(booking_id)
        if booking_user_id != user_id:
            return False, 'You can only cancel your own bookings'
        
        # Check if can be cancelled
        can_cancel, message = can_cancel_booking(booking_id)
        if not can_cancel:
            return False, message
        
        # Cancel the booking
        success = cancel_booking(booking_id)
        if success:
            return True, 'Booking cancelled successfully'
        return False, 'Failed to cancel booking. It may have already been cancelled.'
    
    @staticmethod
    def create_new_booking(user_id, screening_id, seat_ids):
        """Create a new booking"""
        import time
        import random
        
        if len(seat_ids) > 5:
            return False, 'You can only book up to 5 seats', None
        
        conn = get_db_connection()
        if not conn:
            return False, 'Database connection failed', None
        
        try:
            cursor = conn.cursor()
            
            # Get screening price
            cursor.execute("SELECT ticket_price FROM screenings WHERE screening_id = %s", (screening_id,))
            ticket_price = cursor.fetchone()[0]
            
            # Calculate total amount based on seat types
            total_amount = 0.0
            for seat_id in seat_ids:
                cursor.execute("""
                    SELECT s.price_multiplier FROM seats s WHERE s.seat_id = %s
                """, (seat_id,))
                result = cursor.fetchone()
                if result:
                    multiplier = float(result[0]) if result[0] else 1.0
                    total_amount += float(ticket_price) * multiplier
            
            # Generate booking number
            booking_number = f"BK{int(time.time() * 1000) % 1000000}{random.randint(100, 999)}"
            
            # Create booking
            cursor.execute("""
                INSERT INTO bookings (user_id, screening_id, booking_number, num_tickets,
                                    total_amount, booking_status, payment_status)
                VALUES (%s, %s, %s, %s, %s, 'confirmed', 'paid')
                RETURNING booking_id
            """, (user_id, screening_id, booking_number, len(seat_ids), total_amount))
            
            booking_id = cursor.fetchone()[0]
            
            # Create seat bookings
            for seat_id in seat_ids:
                cursor.execute("""
                    INSERT INTO seat_bookings (booking_id, seat_id)
                    VALUES (%s, %s)
                """, (booking_id, seat_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True, f'Booking confirmed! Your booking number is {booking_number}', booking_number
            
        except Exception as e:
            print(f"Error creating booking: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False, 'Failed to create booking. Please try again.', None


class ScreeningService:
    """Screening business logic service"""
    
    @staticmethod
    def get_all_screenings():
        """Get all screenings"""
        from database.db import get_all_screenings as db_get_all_screenings
        screenings_data = db_get_all_screenings()
        return [Screening.from_db_row(screening) for screening in screenings_data]
    
    @staticmethod
    def get_screening_for_booking(screening_id):
        """Get screening with all related info for booking page"""
        screening_data = get_screening_by_id(screening_id)
        if not screening_data:
            return None
        
        screening = Screening.from_db_row(screening_data)
        
        # Get movie
        movie_data = get_movie_by_id(screening.movie_id)
        if not movie_data:
            return None
        movie = Movie.from_db_row(movie_data)
        
        # Get cinema
        cinema_data = get_cinema_by_id(screening.cinema_id)
        if not cinema_data:
            return None
        
        cinema = Cinema.from_db_row(cinema_data)
        
        # Get hall
        hall_data = get_cinema_hall_by_id(screening.hall_id)
        if not hall_data:
            return None
        
        hall = CinemaHall.from_db_row(hall_data)
        
        # Get seats for this hall
        seats_data = get_seats_by_hall(screening.hall_id)
        seats = []
        for seat_row in seats_data:
            seats.append({
                'seat_id': seat_row[0],
                'row_number': seat_row[2],
                'seat_number': seat_row[3],
                'seat_type': seat_row[4] if len(seat_row) > 4 else 'standard',
                'price_multiplier': float(seat_row[5]) if len(seat_row) > 5 else 1.0,
                'is_active': seat_row[6] if len(seat_row) > 6 else True
            })
        
        # Get already booked seats for this screening
        conn = get_db_connection()
        booked_seats = set()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT sb.seat_id 
                    FROM seat_bookings sb
                    JOIN bookings b ON sb.booking_id = b.booking_id
                    WHERE b.screening_id = %s AND b.booking_status != 'cancelled'
                """, (screening_id,))
                booked_seats = {row[0] for row in cursor.fetchall()}
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error getting booked seats: {e}")
                if conn:
                    conn.close()
        
        return {
            'screening': screening,
            'movie': movie,
            'cinema': cinema,
            'hall': hall,
            'seats': seats,
            'booked_seats': booked_seats
        }
    
    @staticmethod
    def get_screenings_for_movie_with_cinema(movie_id, cinema_id=None, screening_date=None):
        """Get screenings for a movie with cinema info"""
        from datetime import date
        
        screenings_data = get_screenings_by_movie(movie_id)
        all_screenings = [Screening.from_db_row(s) for s in screenings_data]
        
        # Filter screenings
        filtered_screenings = all_screenings
        
        if cinema_id:
            filtered_screenings = [s for s in filtered_screenings if s.cinema_id == cinema_id]
        
        if screening_date:
            try:
                filter_date = date.fromisoformat(screening_date) if isinstance(screening_date, str) else screening_date
                filtered_screenings = [s for s in filtered_screenings if s.screening_date == filter_date]
            except ValueError:
                pass
        
        # Get cinema info for each screening
        screenings_with_info = []
        for screening in filtered_screenings:
            cinema_data = get_cinema_by_id(screening.cinema_id)
            if cinema_data:
                cinema = Cinema.from_db_row(cinema_data)
                screenings_with_info.append((screening, cinema))
        
        # Get available dates
        available_dates = sorted(list(set(s.screening_date for s in all_screenings if s.screening_date >= date.today())))
        
        return screenings_with_info, available_dates
    
    @staticmethod
    def get_screenings_for_cinema_with_movie(cinema_id, movie_id=None, screening_date=None):
        """Get screenings for a cinema with movie info"""
        from datetime import date
        
        screenings_data = get_screenings_by_cinema(cinema_id)
        all_screenings = [Screening.from_db_row(s) for s in screenings_data]
        
        # Filter screenings
        filtered_screenings = all_screenings
        
        if movie_id:
            filtered_screenings = [s for s in filtered_screenings if s.movie_id == movie_id]
        
        if screening_date:
            try:
                filter_date = date.fromisoformat(screening_date) if isinstance(screening_date, str) else screening_date
                filtered_screenings = [s for s in filtered_screenings if s.screening_date == filter_date]
            except ValueError:
                pass
        
        # Get movie info for each screening
        screenings_with_info = []
        for screening in filtered_screenings:
            movie_data = get_movie_by_id(screening.movie_id)
            if movie_data:
                movie = Movie.from_db_row(movie_data)
                screenings_with_info.append((screening, movie))
        
        # Get available dates
        available_dates = sorted(list(set(s.screening_date for s in all_screenings if s.screening_date >= date.today())))
        
        return screenings_with_info, available_dates


class CinemaHallService:
    """Cinema Hall business logic service"""
    
    @staticmethod
    def get_halls_by_cinema(cinema_id):
        """Get all halls for a cinema"""
        halls_data = get_cinema_halls_by_cinema(cinema_id)
        return [CinemaHall.from_db_row(hall) for hall in halls_data]
    
    @staticmethod
    def get_hall_by_id(hall_id):
        """Get hall by ID"""
        hall_data = get_cinema_hall_by_id(hall_id)
        if hall_data:
            return CinemaHall.from_db_row(hall_data)
        return None
    
    @staticmethod
    def get_all_halls():
        """Get all halls"""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT hall_id, cinema_id, hall_name, hall_type, total_rows, seats_per_row, total_seats, screen_size, sound_system, created_at, updated_at FROM cinema_halls ORDER BY hall_id")
            halls_data = cursor.fetchall()
            cursor.close()
            conn.close()
            return [CinemaHall.from_db_row(hall) for hall in halls_data]
        except Exception as e:
            print(f"Error getting all halls: {e}")
            if conn:
                conn.close()
            return []
