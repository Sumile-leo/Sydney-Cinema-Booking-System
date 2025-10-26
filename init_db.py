"""
Database initialization script with sample data
Author: Zhou Li
Date: 2025-10-10 to 2025-10-29
"""

import psycopg
from datetime import datetime, date, time, timedelta
import random


def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg.connect(
            host="localhost",
            port=5432,
            dbname="cinema_db",
            user="lizhou",
            password=""
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def init_cinemas(conn):
    """Initialize cinemas with sample data (skip if already exists)"""
    print("Initializing cinemas...")
    cursor = conn.cursor()
    
    try:
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM cinemas")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✓ Cinemas already initialized ({count} cinemas exist)")
            return
        
        # Sample cinemas are already in schema.sql, so this is just for verification
        cursor.execute("SELECT COUNT(*) FROM cinemas")
        count = cursor.fetchone()[0]
        print(f"✓ Found {count} cinemas")
    except Exception as e:
        print(f"Error checking cinemas: {e}")
        conn.rollback()


def init_movies(conn):
    """Initialize movies with sample data"""
    print("Initializing movies...")
    cursor = conn.cursor()
    
    # Sample movies with actual movie posters from previous setup
    movies = [
        ("Avatar: The Way of Water", "Set more than a decade after the first film, Avatar: The Way of Water begins to tell the story of the Sully family.", "Action", 192, date(2022, 12, 16), "James Cameron", "Sam Worthington, Zoe Saldana, Sigourney Weaver", "English", "English", True, "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"),
        ("The Dark Knight", "Batman raises the stakes in his war on crime with the help of Lt. Jim Gordon and District Attorney Harvey Dent.", "Action", 152, date(2008, 7, 18), "Christopher Nolan", "Christian Bale, Heath Ledger, Aaron Eckhart", "English", "English", True, "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"),
        ("Inception", "A thief who steals corporate secrets through dream-sharing technology.", "Science Fiction", 148, date(2010, 7, 16), "Christopher Nolan", "Leonardo DiCaprio, Marion Cotillard, Elliot Page", "English", "English", True, "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg"),
        ("The Matrix", "A computer hacker learns about the true nature of reality.", "Science Fiction", 136, date(1999, 3, 31), "Lana Wachowski", "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss", "English", "English", True, "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"),
        ("Interstellar", "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel.", "Science Fiction", 169, date(2014, 11, 7), "Christopher Nolan", "Matthew McConaughey, Anne Hathaway, Jessica Chastain", "English", "English", True, "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"),
        ("The Shawshank Redemption", "Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life.", "Drama", 142, date(1994, 9, 23), "Frank Darabont", "Tim Robbins, Morgan Freeman, Bob Gunton", "English", "English", True, "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg"),
        ("Pulp Fiction", "A burger-loving hit man, his philosophical partner, a drug-addled gangster's moll and a washed-up boxer converge in this exploration.", "Crime", 154, date(1994, 10, 14), "Quentin Tarantino", "John Travolta, Uma Thurman, Samuel L. Jackson", "English", "English", True, "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg"),
        ("Fight Club", "A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy.", "Drama", 139, date(1999, 10, 15), "David Fincher", "Brad Pitt, Edward Norton, Helena Bonham Carter", "English", "English", True, "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"),
        ("Forrest Gump", "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold.", "Drama", 142, date(1994, 7, 6), "Robert Zemeckis", "Tom Hanks, Robin Wright, Gary Sinise", "English", "English", True, "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg"),
        ("The Lord of the Rings: The Fellowship", "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring.", "Adventure", 178, date(2001, 12, 19), "Peter Jackson", "Elijah Wood, Ian McKellen, Orlando Bloom", "English", "English", True, "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg"),
        ("Spider-Man: No Way Home", "Peter Parker's life gets turned upside down.", "Action", 148, date(2021, 12, 17), "Jon Watts", "Tom Holland, Zendaya, Benedict Cumberbatch", "English", "English", True, "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg"),
        ("Top Gun: Maverick", "After thirty years, Maverick is still pushing the envelope.", "Action", 130, date(2022, 5, 27), "Joseph Kosinski", "Tom Cruise, Jennifer Connelly, Miles Teller", "English", "English", True, "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg"),
        ("Black Panther: Wakanda Forever", "Queen Ramonda, Shuri, M'Baku and the nation of Wakanda fight to protect their nation in the wake of King T'Challa's death.", "Action", 161, date(2022, 11, 11), "Ryan Coogler", "Letitia Wright, Lupita Nyong'o, Danai Gurira", "English", "English", True, "https://image.tmdb.org/t/p/w500/sv1xJUazXeYqALzczSZ3O6nkH75.jpg"),
    ]
    
    try:
        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✓ Movies already initialized ({count} movies exist)")
            return
        
        for movie in movies:
            cursor.execute(
                """INSERT INTO movies (title, description, genre, duration_minutes, release_date, director, "cast", language, subtitles, is_active, poster_url, created_at, updated_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT DO NOTHING""",
                (movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], movie[7], movie[8], movie[9], movie[10], datetime.now(), datetime.now())
            )
        conn.commit()
        print(f"✓ Inserted {len(movies)} movies")
    except Exception as e:
        print(f"Error inserting movies: {e}")
        conn.rollback()


def init_cinema_halls(conn):
    """Initialize cinema halls"""
    print("Initializing cinema halls...")
    cursor = conn.cursor()
    
    hall_types = ["Standard", "IMAX", "VIP", "3D", "Dolby"]
    screen_sizes = ["Small", "Medium", "Large", "IMAX"]
    sound_systems = ["Stereo", "Surround 5.1", "Dolby Atmos", "IMAX"]
    
    try:
        cursor.execute("SELECT cinema_id FROM cinemas")
        cinema_ids = [row[0] for row in cursor.fetchall()]
        
        for cinema_id in cinema_ids:
            # Add 2-4 halls per cinema
            num_halls = random.randint(2, 4)
            for i in range(num_halls):
                hall_name = f"Hall {chr(65 + i)}"
                hall_type = random.choice(hall_types)
                total_rows = random.choice([10, 12, 14, 16, 18])
                seats_per_row = random.choice([15, 18, 20, 22])
                total_seats = total_rows * seats_per_row
                
                cursor.execute(
                    """INSERT INTO cinema_halls (cinema_id, hall_name, hall_type, total_rows, seats_per_row, total_seats, screen_size, sound_system, created_at, updated_at)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (cinema_id, hall_name, hall_type, total_rows, seats_per_row, total_seats,
                     random.choice(screen_sizes), random.choice(sound_systems), datetime.now(), datetime.now())
                )
        conn.commit()
        print("✓ Inserted cinema halls")
    except Exception as e:
        print(f"Error inserting cinema halls: {e}")
        conn.rollback()


def init_seats(conn):
    """Initialize seats for all halls"""
    print("Initializing seats...")
    cursor = conn.cursor()
    
    seat_types = ["standard", "premium", "vip"]
    price_multipliers = {"standard": 1.0, "premium": 1.5, "vip": 2.0}
    
    try:
        cursor.execute("SELECT hall_id, total_rows, seats_per_row FROM cinema_halls")
        halls = cursor.fetchall()
        
        for hall_id, total_rows, seats_per_row in halls:
            for row in range(1, total_rows + 1):
                for seat_num in range(1, seats_per_row + 1):
                    # Determine seat type based on row (front rows are VIP/Premium)
                    if row <= 3:
                        seat_type = random.choice(["premium", "vip"])
                    elif row <= total_rows * 0.4:
                        seat_type = random.choice(["premium", "standard"])
                    else:
                        seat_type = "standard"
                    
                    price_multiplier = price_multipliers[seat_type]
                    
                    cursor.execute(
                        """INSERT INTO seats (hall_id, row_number, seat_number, seat_type, price_multiplier, is_active)
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (hall_id, row, seat_num, seat_type, price_multiplier, True)
                    )
        conn.commit()
        print("✓ Inserted seats")
    except Exception as e:
        print(f"Error inserting seats: {e}")
        conn.rollback()


def init_screenings(conn):
    """Initialize screenings"""
    print("Initializing screenings...")
    cursor = conn.cursor()
    
    screening_types = ["2D", "3D", "IMAX", "Dolby Vision"]
    
    try:
        cursor.execute("SELECT movie_id FROM movies WHERE is_active = TRUE")
        movie_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT cinema_id FROM cinemas WHERE is_active = TRUE")
        cinema_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT hall_id, cinema_id FROM cinema_halls")
        halls = cursor.fetchall()
        
        # Generate screenings for the next 7 days
        for day in range(7):
            screening_date = date.today() + timedelta(days=day)
            
            for hall_id, cinema_id in halls:
                # Random chance for each hall to have a screening
                if random.random() > 0.6:
                    # Pick a random movie
                    movie_id = random.choice(movie_ids)
                    
                    # Get movie duration
                    cursor.execute("SELECT duration_minutes FROM movies WHERE movie_id = %s", (movie_id,))
                    duration_result = cursor.fetchone()
                    if not duration_result:
                        continue
                    duration_minutes = duration_result[0]
                    
                    # Generate 3-5 time slots per day
                    for time_slot in random.sample([10, 13, 16, 19, 22], random.randint(2, 4)):
                        start_time = time(time_slot, random.choice([0, 15, 30, 45]))
                        end_minutes = duration_minutes % 60
                        end_hour = (time_slot * 60 + duration_minutes) // 60
                        end_time = time(end_hour % 24, end_minutes)
                        
                        ticket_price = round(random.uniform(25.0, 45.0), 2)
                        screening_type = random.choice(screening_types)
                        
                        cursor.execute(
                            """INSERT INTO screenings (movie_id, cinema_id, hall_id, screening_date, start_time, end_time, ticket_price, screening_type, language, subtitles, is_active, created_at, updated_at)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (movie_id, cinema_id, hall_id, screening_date, start_time, end_time, ticket_price,
                             screening_type, "English", "English", True, datetime.now(), datetime.now())
                        )
        conn.commit()
        print("✓ Inserted screenings")
    except Exception as e:
        print(f"Error inserting screenings: {e}")
        conn.rollback()


def main():
    """Main initialization function"""
    print("=" * 50)
    print("Database Initialization Script")
    print("Author: Zhou Li")
    print("=" * 50)
    
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    try:
        init_cinemas(conn)
        init_movies(conn)
        init_cinema_halls(conn)
        init_seats(conn)
        init_screenings(conn)
        
        print("\n" + "=" * 50)
        print("✓ Database initialization completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

