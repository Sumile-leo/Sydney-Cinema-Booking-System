"""
Screenings routes
Author: Zhou Li
Date: 2025-10-21
"""

from flask import render_template, request, abort, redirect, url_for
from backend.services import MovieService, CinemaService, ScreeningService


def register_screenings_routes(app):
    """Register screenings routes"""
    
    @app.route('/movie/<int:movie_id>/screenings')
    def movie_screenings(movie_id):
        """Movie screenings page with filters"""
        # Get movie
        movie = MovieService.get_movie_by_id(movie_id)
        if not movie:
            abort(404)
        
        # Get filter parameters
        cinema_id = request.args.get('cinema', type=int)
        screening_date = request.args.get('date', type=str)
        
        # Get screenings with cinema info using service
        screenings_with_info, available_dates = ScreeningService.get_screenings_for_movie_with_cinema(
            movie_id, cinema_id, screening_date
        )
        
        # Get all cinemas for filter dropdown
        all_cinemas = CinemaService.get_all_cinemas()
        
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
        
        # Get filter parameters
        movie_id = request.args.get('movie', type=int)
        screening_date = request.args.get('date', type=str)
        
        # Get screenings with movie info using service
        screenings_with_info, available_dates = ScreeningService.get_screenings_for_cinema_with_movie(
            cinema_id, movie_id, screening_date
        )
        
        # Get all movies for filter dropdown
        all_movies = MovieService.get_all_movies()
        
        return render_template('cinema_screenings.html',
                              cinema=cinema,
                              screenings=screenings_with_info,
                              all_movies=all_movies,
                              available_dates=available_dates,
                              selected_movie_id=movie_id,
                              selected_date=screening_date)

