"""
Sydney Cinema Booking System - Flask App
Main application file
Author: Zhou Li
Date: 2025-10-20
"""

from flask import Flask
from flask_cors import CORS
from routes.auth import register_auth_routes
from routes.main import register_main_routes
from routes.cinemas import register_cinemas_routes
from routes.dashboard import register_dashboard_routes
from routes.movies import register_movies_routes
from routes.screenings import register_screenings_routes
from routes.admin import register_admin_routes


def create_app():
    """Create and configure Flask app"""
    app = Flask(
        __name__,
        template_folder='web/templates',
        static_folder='web/static'
    )
    
    # Secret key for session management
    app.secret_key = 'your-secret-key-change-this-in-production'
    
    # Enable CORS
    CORS(app, supports_credentials=True)
    
    # Register routes
    register_main_routes(app)
    register_auth_routes(app)
    register_cinemas_routes(app)
    register_dashboard_routes(app)
    register_movies_routes(app)
    register_screenings_routes(app)
    register_admin_routes(app)
    
    # Register error handlers
    from flask import render_template
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    return app


def main():
    """Main function to run Flask app"""
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)


if __name__ == '__main__':
    main()
