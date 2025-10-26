"""
Screenings routes
"""

from flask import render_template, request, abort, redirect, url_for
from database.db import get_screenings_by_movie, get_screenings_by_cinema, get_all_screenings
from backend.models.screening import Screening
from backend.services import MovieService, CinemaService
from datetime import date


def register_screenings_routes(app):
    """Register screenings routes"""
    
    @app.route('/movie/<int:movie_id>/screenings')
    def movie_screenings(movie_id):
        """Movie screenings page with filters"""
        # Get movie
        movie = MovieService.get_movie_by_id(movie_id)
        if not movie:
            abort(404)
        
        # Get all screenings for this movie
        screenings_data = get_screenings_by_movie(movie_id)
        all_screenings = [Screening.from_db_row(s) for s in screenings_data]
        
        # Get filter parameters
        cinema_id = request.args.get('cinema', type=int)
        screening_date = request.args.get('date', type=str)
        
        # Filter screenings
        filtered_screenings = all_screenings
        
        if cinema_id:
            filtered_screenings = [s for s in filtered_screenings if s.cinema_id == cinema_id]
        
        if screening_date:
            try:
                filter_date = date.fromisoformat(screening_date)
                filtered_screenings = [s for s in filtered_screenings if s.screening_date == filter_date]
            except ValueError:
                screening_date = None
        
        # Get all cinemas for filter dropdown
        all_cinemas = CinemaService.get_all_cinemas()
        
        # Get available dates
        available_dates = sorted(list(set(s.screening_date for s in all_screenings if s.screening_date >= date.today())))
        
        # Get cinema info for each screening
        from database.db import get_cinema_by_id
        screenings_with_info = []
        for screening in filtered_screenings:
            cinema_data = get_cinema_by_id(screening.cinema_id)
            if cinema_data:
                from backend.models.cinema import Cinema
                cinema = Cinema.from_db_row(cinema_data)
                screenings_with_info.append((screening, cinema))
        
        return render_template('movie_screenings.html',
                              movie=movie,
                              screenings=screenings_with_info,
                              all_cinemas=all_cinemas,
                              available_dates=available_dates,
                              selected_cinema_id=cinema_id,
                              selected_date=screening_date)
    
    @app.route('/cinema/<int:cinema_id>/screenings')
    def cinema_screenings(cinema_id):
        """Cinema screenings page with filters"""
        # Get cinema
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        if not cinema:
            abort(404)
        
        # Get all screenings for this cinema
        screenings_data = get_screenings_by_cinema(cinema_id)
        all_screenings = [Screening.from_db_row(s) for s in screenings_data]
        
        # Get filter parameters
        movie_id = request.args.get('movie', type=int)
        screening_date = request.args.get('date', type=str)
        
        # Filter screenings
        filtered_screenings = all_screenings
        
        if movie_id:
            filtered_screenings = [s for s in filtered_screenings if s.movie_id == movie_id]
        
        if screening_date:
            try:
                filter_date = date.fromisoformat(screening_date)
                filtered_screenings = [s for s in filtered_screenings if s.screening_date == filter_date]
            except ValueError:
                screening_date = None
        
        # Get all movies for filter dropdown
        all_movies = MovieService.get_all_movies()
        
        # Get available dates
        available_dates = sorted(list(set(s.screening_date for s in all_screenings if s.screening_date >= date.today())))
        
        # Get movie info for each screening
        from database.db import get_movie_by_id
        screenings_with_info = []
        for screening in filtered_screenings:
            movie_data = get_movie_by_id(screening.movie_id)
            if movie_data:
                from backend.models.movie import Movie
                movie = Movie.from_db_row(movie_data)
                screenings_with_info.append((screening, movie))
        
        return render_template('cinema_screenings.html',
                              cinema=cinema,
                              screenings=screenings_with_info,
                              all_movies=all_movies,
                              available_dates=available_dates,
                              selected_movie_id=movie_id,
                              selected_date=screening_date)

