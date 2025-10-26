"""
Script to create sample screenings for movies and cinemas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg
from datetime import date, timedelta, time
import random

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'cinema_db',
    'user': 'postgres',
    'password': 'postgres'
}

# Screening types
SCREENING_TYPES = ['Standard', '3D', 'IMAX', 'Gold Class', 'VIP']

# Common show times
START_TIMES = [
    time(10, 0),   # 10:00 AM
    time(11, 30),  # 11:30 AM
    time(13, 0),   # 1:00 PM
    time(14, 30),  # 2:30 PM
    time(16, 0),   # 4:00 PM
    time(17, 30),  # 5:30 PM
    time(19, 0),   # 7:00 PM
    time(20, 30),  # 8:30 PM
    time(22, 0),   # 10:00 PM
]

# Price tiers
PRICES = {
    'Standard': 18.00,
    '3D': 22.00,
    'IMAX': 28.00,
    'Gold Class': 35.00,
    'VIP': 45.00
}


def calculate_end_time(start_time, duration_minutes):
    """Calculate end time from start time and duration"""
    total_minutes = start_time.hour * 60 + start_time.minute + duration_minutes
    hours = (total_minutes // 60) % 24  # Wrap around 24 hours
    minutes = total_minutes % 60
    return time(hours, minutes)


def create_sample_screenings():
    """Create sample screenings for movies"""
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Get all active movies
        cursor.execute("SELECT movie_id, title, duration_minutes, language, subtitles FROM movies WHERE is_active = true")
        movies = cursor.fetchall()
        
        if not movies:
            print("No active movies found.")
            return
        
        # Get all active cinemas
        cursor.execute("SELECT cinema_id, cinema_name FROM cinemas WHERE is_active = true")
        cinemas = cursor.fetchall()
        
        if not cinemas:
            print("No active cinemas found.")
            return
        
        # Get all halls for each cinema
        cursor.execute("SELECT hall_id, cinema_id, hall_name, hall_type FROM cinema_halls")
        halls_data = cursor.fetchall()
        
        # Group halls by cinema
        cinema_halls = {}
        for hall_id, cinema_id, hall_name, hall_type in halls_data:
            if cinema_id not in cinema_halls:
                cinema_halls[cinema_id] = []
            cinema_halls[cinema_id].append((hall_id, hall_name, hall_type))
        
        screening_count = 0
        today = date.today()
        
        # Create screenings for next 14 days
        for day_offset in range(14):
            screening_date = today + timedelta(days=day_offset)
            
            for movie_id, title, duration_minutes, movie_language, movie_subtitles in movies:
                # Randomly select 3-5 cinemas to show this movie
                num_cinemas = random.randint(3, min(5, len(cinemas)))
                selected_cinemas = random.sample(cinemas, num_cinemas)
                
                for cinema_id, cinema_name in selected_cinemas:
                    if cinema_id not in cinema_halls:
                        continue
                    
                    # Select a random hall from this cinema
                    hall_id, hall_name, hall_type = random.choice(cinema_halls[cinema_id])
                    
                    # Determine screening type based on hall type
                    if hall_type and 'IMAX' in hall_type:
                        screening_type = 'IMAX'
                    elif hall_type and ('Gold' in hall_type or 'VIP' in hall_type):
                        screening_type = random.choice(['Gold Class', 'VIP'])
                    elif random.random() < 0.3:
                        screening_type = '3D'
                    else:
                        screening_type = 'Standard'
                    
                    # Select 2-4 show times for this movie at this cinema
                    num_shows = random.randint(2, 4)
                    selected_times = random.sample(START_TIMES, num_shows)
                    
                    for start_time in selected_times:
                        # Calculate end time
                        end_time = calculate_end_time(start_time, duration_minutes or 120)
                        
                        # Set price based on screening type
                        ticket_price = PRICES.get(screening_type, 18.00)
                        
                        # Use movie's language and subtitles
                        language = movie_language or 'English'
                        subtitles = movie_subtitles or 'English'
                        
                        # Check if this screening already exists
                        cursor.execute(
                            """SELECT screening_id FROM screenings 
                               WHERE movie_id = %s AND cinema_id = %s AND hall_id = %s 
                               AND screening_date = %s AND start_time = %s""",
                            (movie_id, cinema_id, hall_id, screening_date, start_time)
                        )
                        
                        if cursor.fetchone():
                            continue
                        
                        # Insert screening
                        cursor.execute(
                            """INSERT INTO screenings (movie_id, cinema_id, hall_id, 
                                                       screening_date, start_time, end_time,
                                                       ticket_price, screening_type, language, subtitles)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (movie_id, cinema_id, hall_id, screening_date, start_time, end_time,
                             ticket_price, screening_type, language, subtitles)
                        )
                        screening_count += 1
        
        conn.commit()
        print(f"\n✅ Successfully created {screening_count} screenings!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Creating sample screenings...")
    print("-" * 50)
    create_sample_screenings()
    print("-" * 50)
    print("\n✅ Done!")

