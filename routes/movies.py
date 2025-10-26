"""
Movies routes
Author: Zhou Li
Date: 2025-10-16
"""

from flask import render_template, redirect, url_for, session, flash, abort
from backend.services import MovieService

def register_movies_routes(app):
    @app.route('/movies')
    def movies():
        """Display all movies"""
        movies_list = MovieService.get_all_movies()
        return render_template('movies.html', movies=movies_list)
    
    @app.route('/movie/<int:movie_id>')
    def movie_detail(movie_id):
        """Display movie details"""
        movie = MovieService.get_movie_by_id(movie_id)
        if not movie:
            abort(404)
        return render_template('movie_detail.html', movie=movie)
