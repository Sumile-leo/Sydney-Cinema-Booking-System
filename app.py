"""
Sydney Cinema Booking System - Flask App
Main application file
"""

from flask import Flask
from flask_cors import CORS
from routes.auth import register_auth_routes
from routes.main import register_main_routes
from routes.cinemas import register_cinemas_routes


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
    
    return app


def main():
    """Main function to run Flask app"""
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)


if __name__ == '__main__':
    main()
