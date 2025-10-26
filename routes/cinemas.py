"""
Cinemas routes
"""

from flask import render_template
from backend.services import CinemaService


def register_cinemas_routes(app):
    """Register cinemas routes"""
    
    @app.route('/cinemas')
    def cinemas():
        """Cinemas list page"""
        # Get all cinemas using service layer
        cinemas_list = CinemaService.get_all_cinemas()
        
        # Pass cinemas to template
        return render_template('cinemas.html', cinemas=cinemas_list)
    
    @app.route('/cinema/<int:cinema_id>')
    def cinema_detail(cinema_id):
        """Cinema detail page"""
        # Get cinema by ID using service layer
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        
        if not cinema:
            from flask import abort
            abort(404)  # Cinema not found
        
        return render_template('cinema_detail.html', cinema=cinema)
