"""
Script to create sample cinema hall test data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg
import random

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'cinema_db',
    'user': 'postgres',
    'password': 'postgres'
}

# Hall types and configurations
HALL_TYPES = [
    ('Standard', 12, 20, 240, 'Standard', 'Dolby 5.1'),
    ('IMAX', 18, 30, 540, 'IMAX Large', 'Dolby Atmos'),
    ('Gold Class', 8, 15, 120, 'Premium Large', 'Dolby 7.1'),
    ('VIP', 6, 12, 72, 'VIP Large', 'Dolby Atmos'),
]

HALL_NAMES_BASIC = ['A', 'B', 'C', 'D', 'E']
HALL_NAMES_SPECIAL = ['IMAX', 'Gold Class', 'VIP', 'Deluxe']


def create_sample_cinema_halls():
    """Create sample cinema halls for existing cinemas"""
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Get all existing cinemas
        cursor.execute("SELECT cinema_id FROM cinemas")
        cinema_ids = [row[0] for row in cursor.fetchall()]
        
        if not cinema_ids:
            print("No cinemas found. Please create cinemas first.")
            return
        
        hall_count = 0
        
        for cinema_id in cinema_ids:
            # Each cinema gets 3-6 halls
            num_halls = random.randint(3, 6)
            
            for i in range(num_halls):
                # Randomly choose basic name or special hall
                if i == 0 and random.choice([True, False]):
                    # First hall might be special (IMAX, Gold Class, etc.)
                    hall_name = random.choice(HALL_NAMES_SPECIAL)
                    hall_type, total_rows, seats_per_row, total_seats, screen_size, sound_system = random.choice(HALL_TYPES)
                else:
                    # Use basic names (A, B, C, D, E)
                    hall_name = random.choice(HALL_NAMES_BASIC)
                    # Use Standard or slightly varied configuration
                    if random.choice([True, False]):
                        hall_type, total_rows, seats_per_row, total_seats, screen_size, sound_system = HALL_TYPES[0]
                    else:
                        hall_type = 'Standard'
                        total_rows = random.randint(10, 14)
                        seats_per_row = random.randint(18, 22)
                        total_seats = total_rows * seats_per_row
                        screen_size = 'Standard'
                        sound_system = 'Dolby 5.1'
                
                # Check if this hall already exists for this cinema
                cursor.execute(
                    "SELECT hall_id FROM cinema_halls WHERE cinema_id = %s AND hall_name = %s",
                    (cinema_id, hall_name)
                )
                existing = cursor.fetchone()
                
                if not existing:
                    cursor.execute(
                        """INSERT INTO cinema_halls (cinema_id, hall_name, hall_type, total_rows, 
                                                   seats_per_row, total_seats, screen_size, sound_system)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (cinema_id, hall_name, hall_type, total_rows, seats_per_row,
                         total_seats, screen_size, sound_system)
                    )
                    print(f"Created hall '{hall_name}' ({hall_type}) in cinema {cinema_id} - {total_seats} seats")
                    hall_count += 1
                else:
                    print(f"Skipped duplicate hall '{hall_name}' in cinema {cinema_id}")
        
        conn.commit()
        print(f"\n✅ Successfully created {hall_count} cinema halls!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Creating sample cinema halls...")
    print("-" * 50)
    create_sample_cinema_halls()
    print("-" * 50)
    print("\n✅ Done!")

