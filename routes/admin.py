"""
Admin panel routes
Author: Zhou Li
Date: 2025-10-25
"""

from flask import render_template, redirect, url_for, session, flash, request
from backend.services import CinemaService, CinemaHallService, MovieService, ScreeningService
from database.db import get_db_connection
from backend.models.screening import Screening


def register_admin_routes(app):
    """Register admin panel routes"""
    
    def is_admin():
        """Check if current user is admin"""
        return session.get('user_type') == 'admin'
    
    @app.route('/admin')
    def admin_panel():
        """Admin panel main page"""
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('login'))
        
        if not is_admin():
            flash('Access denied. Admin only.', 'error')
            return redirect(url_for('index'))
        
        # Get counts for dashboard
        conn = get_db_connection()
        stats = {}
        if conn:
            try:
                cursor = conn.cursor()
                
                # Get cinema count
                cursor.execute("SELECT COUNT(*) FROM cinemas WHERE is_active = TRUE")
                stats['cinemas'] = cursor.fetchone()[0]
                
                # Get halls count
                cursor.execute("SELECT COUNT(*) FROM cinema_halls")
                stats['halls'] = cursor.fetchone()[0]
                
                # Get movies count
                cursor.execute("SELECT COUNT(*) FROM movies WHERE is_active = TRUE")
                stats['movies'] = cursor.fetchone()[0]
                
                # Get screenings count
                cursor.execute("SELECT COUNT(*) FROM screenings WHERE is_active = TRUE")
                stats['screenings'] = cursor.fetchone()[0]
                
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error getting admin stats: {e}")
                if conn:
                    conn.close()
        
        return render_template('admin/admin_panel.html', stats=stats)
    
    # Cinema management routes
    @app.route('/admin/cinemas')
    def admin_cinemas():
        """Manage cinemas"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        cinemas = CinemaService.get_all_cinemas()
        return render_template('admin/cinemas.html', cinemas=cinemas)
    
    @app.route('/admin/cinemas/add', methods=['GET', 'POST'])
    def add_cinema():
        """Add a new cinema"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            # Get form data
            cinema_name = request.form.get('cinema_name')
            address = request.form.get('address')
            suburb = request.form.get('suburb')
            postcode = request.form.get('postcode')
            phone = request.form.get('phone')
            email = request.form.get('email')
            facilities = request.form.get('facilities', '')
            
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        """INSERT INTO cinemas (cinema_name, address, suburb, postcode, phone, email, facilities, is_active)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)""",
                        (cinema_name, address, suburb, postcode, phone, email, facilities)
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    flash('Cinema added successfully', 'success')
                except Exception as e:
                    print(f"Error adding cinema: {e}")
                    if conn:
                        conn.close()
                    flash('Failed to add cinema', 'error')
            
            return redirect(url_for('admin_cinemas'))
        
        return render_template('admin/add_cinema.html')
    
    @app.route('/admin/cinemas/<int:cinema_id>/halls')
    def admin_cinema_halls(cinema_id):
        """Manage halls for a specific cinema"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        # Get cinema info
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        if not cinema:
            flash('Cinema not found', 'error')
            return redirect(url_for('admin_cinemas'))
        
        # Get halls for this cinema
        halls = CinemaHallService.get_halls_by_cinema(cinema_id)
        
        return render_template('admin/cinema_halls.html', cinema=cinema, halls=halls)
    
    @app.route('/admin/cinemas/<int:cinema_id>/halls/add', methods=['GET', 'POST'])
    def add_cinema_hall(cinema_id):
        """Add a new hall to a cinema"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        # Get cinema info
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        if not cinema:
            flash('Cinema not found', 'error')
            return redirect(url_for('admin_cinemas'))
        
        if request.method == 'POST':
            # Get form data
            hall_name = request.form.get('hall_name')
            hall_type = request.form.get('hall_type')
            total_rows = int(request.form.get('total_rows'))
            seats_per_row = int(request.form.get('seats_per_row'))
            screen_size = request.form.get('screen_size')
            sound_system = request.form.get('sound_system')
            total_seats = total_rows * seats_per_row
            
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        """INSERT INTO cinema_halls (cinema_id, hall_name, hall_type, total_rows, seats_per_row, 
                           total_seats, screen_size, sound_system) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (cinema_id, hall_name, hall_type, total_rows, seats_per_row, total_seats, screen_size, sound_system)
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    flash('Hall added successfully', 'success')
                except Exception as e:
                    print(f"Error adding hall: {e}")
                    if conn:
                        conn.close()
                    flash('Failed to add hall', 'error')
            
            return redirect(url_for('admin_cinema_halls', cinema_id=cinema_id))
        
        return render_template('admin/add_cinema_hall.html', cinema=cinema)
    
    # Cinema halls management routes
    @app.route('/admin/halls')
    def admin_halls():
        """Manage cinema halls"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        halls = CinemaHallService.get_all_halls()
        return render_template('admin/halls.html', halls=halls)
    
    # Movies management routes
    @app.route('/admin/movies')
    def admin_movies():
        """Manage movies"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        movies = MovieService.get_all_movies()
        return render_template('admin/movies.html', movies=movies)
    
    @app.route('/admin/movies/add', methods=['GET', 'POST'])
    def add_movie():
        """Add a new movie"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            # Get form data
            title = request.form.get('title')
            description = request.form.get('description', '')
            genre = request.form.get('genre')
            duration_minutes = int(request.form.get('duration_minutes'))
            release_date = request.form.get('release_date')
            director = request.form.get('director')
            cast = request.form.get('cast', '')
            language = request.form.get('language')
            subtitles = request.form.get('subtitles', '')
            poster_url = request.form.get('poster_url', '')
            
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        """INSERT INTO movies (title, description, genre, duration_minutes, release_date, 
                           director, "cast", language, subtitles, poster_url, is_active) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)""",
                        (title, description, genre, duration_minutes, release_date, director, cast, language, subtitles, poster_url)
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    flash('Movie added successfully', 'success')
                except Exception as e:
                    print(f"Error adding movie: {e}")
                    if conn:
                        conn.close()
                    flash('Failed to add movie', 'error')
            
            return redirect(url_for('admin_movies'))
        
        return render_template('admin/add_movie.html')
    
    # Screenings management routes
    @app.route('/admin/screenings')
    def admin_screenings():
        """Manage screenings"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        # Get filter parameters
        cinema_id = request.args.get('cinema_id', '').strip()
        movie_id = request.args.get('movie_id', '').strip()
        screening_date = request.args.get('screening_date', '').strip()
        
        # Get all cinemas and movies for filters
        cinemas = CinemaService.get_all_cinemas()
        movies = MovieService.get_all_movies()
        
        # Get screenings based on filters
        conn = get_db_connection()
        screenings = []
        if conn:
            try:
                cursor = conn.cursor()
                query = """SELECT screening_id, movie_id, cinema_id, hall_id, screening_date, 
                          start_time, end_time, ticket_price, screening_type, language, subtitles, 
                          is_active, created_at, updated_at 
                          FROM screenings WHERE 1=1"""
                params = []
                
                if cinema_id:
                    query += " AND cinema_id = %s"
                    params.append(int(cinema_id))
                
                if movie_id:
                    query += " AND movie_id = %s"
                    params.append(int(movie_id))
                
                if screening_date:
                    query += " AND screening_date = %s"
                    params.append(screening_date)
                
                query += " ORDER BY screening_date, start_time"
                
                cursor.execute(query, tuple(params))
                screenings_data = cursor.fetchall()
                screenings = [Screening.from_db_row(row) for row in screenings_data]
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error getting screenings: {e}")
                if conn:
                    conn.close()
        
        return render_template('admin/screenings.html', screenings=screenings, cinemas=cinemas, movies=movies)
    
    # Toggle cinema status
    @app.route('/admin/cinemas/<int:cinema_id>/toggle', methods=['POST'])
    def toggle_cinema(cinema_id):
        """Toggle cinema active status"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Get current cinema status
                cursor.execute(
                    "SELECT is_active FROM cinemas WHERE cinema_id = %s",
                    (cinema_id,)
                )
                current_status = cursor.fetchone()
                if not current_status:
                    flash('Cinema not found', 'error')
                    return redirect(url_for('admin_cinemas'))
                
                is_currently_active = current_status[0]
                
                # Toggle is_active status
                cursor.execute(
                    "UPDATE cinemas SET is_active = NOT is_active WHERE cinema_id = %s",
                    (cinema_id,)
                )
                
                # If deactivating cinema, also deactivate all screenings and cancel all bookings
                if is_currently_active:  # Currently active, so we're deactivating
                    # Deactivate all screenings for this cinema
                    cursor.execute(
                        "UPDATE screenings SET is_active = FALSE WHERE cinema_id = %s",
                        (cinema_id,)
                    )
                    
                    # Get all booking IDs for screenings at this cinema
                    cursor.execute(
                        "SELECT booking_id FROM bookings WHERE screening_id IN (SELECT screening_id FROM screenings WHERE cinema_id = %s)",
                        (cinema_id,)
                    )
                    booking_ids = cursor.fetchall()
                    
                    # Cancel all bookings
                    if booking_ids:
                        cursor.execute(
                            "UPDATE bookings SET booking_status = 'cancelled' WHERE screening_id IN (SELECT screening_id FROM screenings WHERE cinema_id = %s)",
                            (cinema_id,)
                        )
                    
                    flash('Cinema deactivated. All screenings and bookings have been cancelled.', 'success')
                else:  # Currently inactive, so we're activating
                    flash('Cinema activated successfully', 'success')
                
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error toggling cinema status: {e}")
                if conn:
                    conn.close()
                flash('Failed to update cinema status', 'error')
        
        return redirect(url_for('admin_cinemas'))
    
    # Toggle movie status
    @app.route('/admin/movies/<int:movie_id>/toggle', methods=['POST'])
    def toggle_movie(movie_id):
        """Toggle movie active status"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Get current movie status
                cursor.execute(
                    "SELECT is_active FROM movies WHERE movie_id = %s",
                    (movie_id,)
                )
                current_status = cursor.fetchone()
                if not current_status:
                    flash('Movie not found', 'error')
                    return redirect(url_for('admin_movies'))
                
                is_currently_active = current_status[0]
                
                # If deactivating movie, check if there are active screenings
                if is_currently_active:  # Currently active, so we're deactivating
                    cursor.execute(
                        "SELECT COUNT(*) FROM screenings WHERE movie_id = %s AND is_active = TRUE",
                        (movie_id,)
                    )
                    active_screenings_count = cursor.fetchone()[0]
                    
                    if active_screenings_count > 0:
                        flash(f'Cannot deactivate movie. There are {active_screenings_count} active screenings for this movie.', 'error')
                        cursor.close()
                        conn.close()
                        return redirect(url_for('admin_movies'))
                    
                    # Deactivate movie
                    cursor.execute(
                        "UPDATE movies SET is_active = FALSE WHERE movie_id = %s",
                        (movie_id,)
                    )
                    flash('Movie deactivated successfully', 'success')
                else:  # Currently inactive, so we're activating
                    cursor.execute(
                        "UPDATE movies SET is_active = TRUE WHERE movie_id = %s",
                        (movie_id,)
                    )
                    flash('Movie activated successfully', 'success')
                
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error toggling movie status: {e}")
                if conn:
                    conn.close()
                flash('Failed to update movie status', 'error')
        
        return redirect(url_for('admin_movies'))
    
    # Toggle screening status
    @app.route('/admin/screenings/<int:screening_id>/toggle', methods=['POST'])
    def toggle_screening(screening_id):
        """Toggle screening active status"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Get current screening status
                cursor.execute(
                    "SELECT is_active FROM screenings WHERE screening_id = %s",
                    (screening_id,)
                )
                current_status = cursor.fetchone()
                if not current_status:
                    flash('Screening not found', 'error')
                    return redirect(url_for('admin_screenings'))
                
                is_currently_active = current_status[0]
                
                # If deactivating screening, also cancel all bookings
                if is_currently_active:  # Currently active, so we're deactivating
                    # Cancel all bookings for this screening
                    cursor.execute(
                        "UPDATE bookings SET booking_status = 'cancelled' WHERE screening_id = %s",
                        (screening_id,)
                    )
                    
                    # Deactivate screening
                    cursor.execute(
                        "UPDATE screenings SET is_active = FALSE WHERE screening_id = %s",
                        (screening_id,)
                    )
                    
                    flash('Screening deactivated. All bookings have been cancelled.', 'success')
                else:  # Currently inactive, so we're activating
                    cursor.execute(
                        "UPDATE screenings SET is_active = TRUE WHERE screening_id = %s",
                        (screening_id,)
                    )
                    flash('Screening activated successfully', 'success')
                
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error toggling screening status: {e}")
                if conn:
                    conn.close()
                flash('Failed to update screening status', 'error')
        
        return redirect(url_for('admin_screenings'))
    
    # Delete hall
    @app.route('/admin/halls/<int:hall_id>/delete', methods=['POST'])
    def delete_hall(hall_id):
        """Delete a cinema hall"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cinema_halls WHERE hall_id = %s", (hall_id,))
                conn.commit()
                cursor.close()
                conn.close()
                flash('Hall deleted successfully', 'success')
            except Exception as e:
                print(f"Error deleting hall: {e}")
                if conn:
                    conn.close()
                flash('Failed to delete hall', 'error')
        
        return redirect(url_for('admin_halls'))
    
    @app.route('/admin/screenings/add', methods=['GET', 'POST'])
    def add_screening():
        """Add a new screening"""
        if not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            from datetime import datetime, timedelta
            
            # Get form data
            movie_id = int(request.form.get('movie_id'))
            cinema_id = int(request.form.get('cinema_id'))
            hall_id = int(request.form.get('hall_id'))
            screening_date = request.form.get('screening_date')
            start_time = request.form.get('start_time')
            ticket_price = float(request.form.get('ticket_price'))
            screening_type = request.form.get('screening_type', '')
            language = request.form.get('language', '')
            subtitles = request.form.get('subtitles', '')
            
            # Calculate end time from movie duration
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    
                    # Get movie duration
                    cursor.execute("SELECT duration_minutes FROM movies WHERE movie_id = %s", (movie_id,))
                    duration_row = cursor.fetchone()
                    if not duration_row:
                        flash('Movie not found', 'error')
                        return redirect(url_for('admin_screenings'))
                    
                    duration_minutes = duration_row[0]
                    
                    # Calculate end time
                    start_datetime = datetime.strptime(f"{screening_date} {start_time}", "%Y-%m-%d %H:%M")
                    end_datetime = start_datetime + timedelta(minutes=duration_minutes)
                    end_time = end_datetime.strftime("%H:%M:%S")
                    
                    # Insert screening
                    cursor.execute(
                        """INSERT INTO screenings (movie_id, cinema_id, hall_id, screening_date, 
                           start_time, end_time, ticket_price, screening_type, language, subtitles, is_active) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)""",
                        (movie_id, cinema_id, hall_id, screening_date, start_time, end_time, 
                         ticket_price, screening_type, language, subtitles)
                    )
                    
                    conn.commit()
                    cursor.close()
                    conn.close()
                    flash('Screening added successfully', 'success')
                except Exception as e:
                    print(f"Error adding screening: {e}")
                    if conn:
                        conn.close()
                    flash('Failed to add screening', 'error')
            
            return redirect(url_for('admin_screenings'))
        
        # GET request - show form
        # Get all cinemas, movies for dropdowns
        cinemas = CinemaService.get_all_cinemas()
        movies = MovieService.get_all_movies()
        
        return render_template('admin/add_screening.html', cinemas=cinemas, movies=movies)

