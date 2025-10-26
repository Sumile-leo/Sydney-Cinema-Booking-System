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

# Sample data for random generation
MOVIE_TITLES = [
    ("Avatar: The Way of Water", "Adventure", "James Cameron", "Sam Worthington, Zoe Saldana", 192),
    ("The Dark Knight", "Action", "Christopher Nolan", "Christian Bale, Heath Ledger", 152),
    ("Inception", "Sci-Fi", "Christopher Nolan", "Leonardo DiCaprio, Marion Cotillard", 148),
    ("The Matrix", "Action", "The Wachowskis", "Keanu Reeves, Carrie-Anne Moss", 136),
    ("Interstellar", "Sci-Fi", "Christopher Nolan", "Matthew McConaughey, Anne Hathaway", 169),
    ("The Shawshank Redemption", "Drama", "Frank Darabont", "Tim Robbins, Morgan Freeman", 142),
    ("Pulp Fiction", "Crime", "Quentin Tarantino", "John Travolta, Samuel L. Jackson", 154),
    ("Fight Club", "Drama", "David Fincher", "Brad Pitt, Edward Norton", 139),
    ("Forrest Gump", "Drama", "Robert Zemeckis", "Tom Hanks, Robin Wright", 142),
    ("The Lord of the Rings: The Fellowship", "Fantasy", "Peter Jackson", "Elijah Wood, Ian McKellen", 178),
]

DESCRIPTIONS = [
    "An epic adventure that takes you on a journey through time and space.",
    "A thrilling tale of mystery and suspense that will keep you on the edge of your seat.",
    "A heartwarming story of friendship and courage in the face of adversity.",
    "An action-packed spectacle with stunning visual effects and compelling performances.",
    "A thought-provoking exploration of complex themes and human nature.",
    "A gripping narrative that challenges conventional storytelling.",
    "An emotional rollercoaster that tugs at your heartstrings.",
    "A visually stunning masterpiece with groundbreaking cinematography.",
    "A powerful story of redemption and hope against all odds.",
    "A cinematic experience that redefines the boundaries of filmmaking.",
]

LANGUAGES = ["English", "English", "English", "Mandarin", "Japanese"]
SUBTITLES = ["English", "Mandarin", "Korean", "Japanese", "Spanish"]


def create_sample_movies(count=10):
    """Create sample movies in the database"""
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        for i in range(count):
            # Get random movie data
            title, genre, director, cast, duration = random.choice(MOVIE_TITLES)
            
            # Generate description
            description = random.choice(DESCRIPTIONS)
            
            # Generate release date (last 2 years to future 6 months)
            days_ago = random.randint(-180, 730)
            release_date = date.today() - timedelta(days=days_ago)
            
            # Random language and subtitles
            language = random.choice(LANGUAGES)
            subtitles = random.choice(SUBTITLES)
            
            # Randomly make some movies inactive
            is_active = random.choice([True, True, True, True, False])  # 80% active
            
            # Insert into database
            cursor.execute(
                """INSERT INTO movies (title, description, genre, duration_minutes, release_date, 
                                      director, "cast", language, subtitles, is_active)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (title, description, genre, duration, release_date, director, cast, language, subtitles, is_active)
            )
            
            print(f"Created: {title} - {genre}")
        
        conn.commit()
        print(f"\n✅ Successfully created {count} sample movies!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Creating sample movies...")
    print("-" * 50)
    create_sample_movies(10)
    print("-" * 50)
    print("\n✅ Done!")
