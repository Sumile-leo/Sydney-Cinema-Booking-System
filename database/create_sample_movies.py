"""
Script to create sample movie test data
"""

import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg
from datetime import date, timedelta

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'cinema_db',
    'user': 'postgres',
    'password': 'postgres'
}

# Sample movies - each movie appears only once
MOVIES = [
    ("Avatar: The Way of Water", "An epic adventure that takes you on a journey through time and space.", 
     "Adventure", "James Cameron", "Sam Worthington, Zoe Saldana", 192, "English", "English, Mandarin"),
    ("The Dark Knight", "A thrilling tale of mystery and suspense that will keep you on the edge of your seat.", 
     "Action", "Christopher Nolan", "Christian Bale, Heath Ledger", 152, "English", "English"),
    ("Inception", "A gripping narrative that challenges conventional storytelling.", 
     "Sci-Fi", "Christopher Nolan", "Leonardo DiCaprio, Marion Cotillard", 148, "English", "English, Mandarin"),
    ("The Matrix", "An action-packed spectacle with stunning visual effects and compelling performances.", 
     "Action", "The Wachowskis", "Keanu Reeves, Carrie-Anne Moss", 136, "English", "English"),
    ("Interstellar", "A thought-provoking exploration of complex themes and human nature.", 
     "Sci-Fi", "Christopher Nolan", "Matthew McConaughey, Anne Hathaway", 169, "English", "English"),
    ("The Shawshank Redemption", "A powerful story of redemption and hope against all odds.", 
     "Drama", "Frank Darabont", "Tim Robbins, Morgan Freeman", 142, "English", "English, Cantonese"),
    ("Pulp Fiction", "An emotional rollercoaster that tugs at your heartstrings.", 
     "Crime", "Quentin Tarantino", "John Travolta, Samuel L. Jackson", 154, "English", "English"),
    ("Fight Club", "A heartwarming story of friendship and courage in the face of adversity.", 
     "Drama", "David Fincher", "Brad Pitt, Edward Norton", 139, "English", "English"),
    ("Forrest Gump", "A visually stunning masterpiece with groundbreaking cinematography.", 
     "Drama", "Robert Zemeckis", "Tom Hanks, Robin Wright", 142, "English", "English"),
    ("The Lord of the Rings: The Fellowship", "A cinematic experience that redefines the boundaries of filmmaking.", 
     "Fantasy", "Peter Jackson", "Elijah Wood, Ian McKellen", 178, "English", "English, Mandarin"),
    ("Spider-Man: No Way Home", "A thrilling superhero adventure that will leave you breathless.", 
     "Action", "Jon Watts", "Tom Holland, Zendaya", 148, "English", "English"),
    ("Top Gun: Maverick", "An action-packed sequel that lives up to the original.", 
     "Action", "Joseph Kosinski", "Tom Cruise, Miles Teller", 130, "English", "English, Mandarin"),
    ("Black Panther: Wakanda Forever", "An emotional journey through loss, legacy, and love.", 
     "Action", "Ryan Coogler", "Letitia Wright, Angela Bassett", 161, "English", "English"),
    ("Everything Everywhere All at Once", "A mind-bending multiverse adventure with heart.", 
     "Sci-Fi", "Daniels", "Michelle Yeoh, Stephanie Hsu", 139, "English", "English, Mandarin"),
    ("The Batman", "A dark and gritty take on the iconic superhero.", 
     "Action", "Matt Reeves", "Robert Pattinson, Zoë Kravitz", 176, "English", "English"),
]


def create_sample_movies():
    """Create sample movies in the database"""
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Shuffle movies to randomize order
        movies = MOVIES[:]
        random.shuffle(movies)
        
        for movie_data in movies:
            # Unpack movie data: title, description, genre, director, cast, duration, language, subtitles
            title, description, genre, director, cast, duration, language, subtitles = movie_data
            
            # Generate release date (last 2 years to future 6 months)
            days_ago = random.randint(-180, 730)
            release_date = date.today() - timedelta(days=days_ago)
            
            # Set all movies to active by default
            is_active = True
            
            # Check if movie already exists
            cursor.execute("SELECT COUNT(*) FROM movies WHERE title = %s", (title,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert into database
                cursor.execute(
                    """INSERT INTO movies (title, description, genre, duration_minutes, release_date, 
                                          director, "cast", language, subtitles, is_active)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (title, description, genre, duration, release_date, director, cast, language, subtitles, is_active)
                )
                print(f"Created: {title} - {genre} ({language}, {subtitles})")
            else:
                print(f"Skipped: {title} (already exists)")
        
        conn.commit()
        print(f"\n✅ Successfully created/updated {len(MOVIES)} sample movies!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Creating sample movies...")
    print("-" * 50)
    create_sample_movies()
    print("-" * 50)
    print("\n✅ Done!")
