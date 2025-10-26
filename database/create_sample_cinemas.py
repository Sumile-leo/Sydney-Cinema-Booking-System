"""
Script to create sample cinema test data
"""

import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'cinema_db',
    'user': 'postgres',
    'password': 'postgres'
}


# Sample data for random generation
CINEMA_NAMES = [
    "Event Cinemas", "Hoyts", "Village Cinemas", "Palace Cinemas",
    "Reading Cinemas", "Luna Cinemas", "Ritz Cinemas", "Cinema Nova"
]

SUBIURBS = [
    ("Sydney CBD", "2000"), ("Bondi Junction", "2022"), ("Parramatta", "2150"),
    ("Chatswood", "2067"), ("Hurstville", "2220"), ("Burwood", "2134"),
    ("Miranda", "2228"), ("Castle Hill", "2154"), ("Bankstown", "2200"),
    ("Cronulla", "2230")
]

ADDRESSES = [
    "George Street", "Pitt Street", "Market Street", "Oxford Street",
    "King Street", "New South Head Road", "Victoria Avenue", "Bay Street"
]

FACILITIES_OPTIONS = [
    "IMAX, Gold Class, VMAX, Parking",
    "IMAX, Dolby Atmos, Recliners",
    "Gold Class, VMAX, Food Court",
    "IMAX, 4DX, Kids Club",
    "Gold Class, VMAX, Wheelchair Access",
    "IMAX, 3D, Parking, Food Court"
]


def create_sample_cinemas(count=10):
    """Create sample cinemas in the database"""
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        for i in range(count):
            # Generate random cinema data
            cinema_name = f"{random.choice(CINEMA_NAMES)} {random.choice(SUBIURBS)[0]}"
            suburb, postcode = random.choice(SUBIURBS)
            street_number = random.randint(1, 500)
            address = f"{street_number} {random.choice(ADDRESSES)}"
            
            # Generate phone (Australian format)
            phone = f"02 {random.randint(1000, 9999)} {random.randint(1000, 9999)}"
            
            # Generate email
            email = f"{suburb.lower().replace(' ', '')}@{cinema_name.lower().replace(' ', '')}.com"
            
            # Random facilities
            facilities = random.choice(FACILITIES_OPTIONS)
            
            # Randomly make some cinemas inactive
            is_active = random.choice([True, True, True, False])  # 75% active
            
            # Insert into database
            cursor.execute(
                """INSERT INTO cinemas (cinema_name, address, suburb, postcode, phone, email, facilities, is_active)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (cinema_name, address, suburb, postcode, phone, email, facilities, is_active)
            )
            
            print(f"Created: {cinema_name} - {suburb}")
        
        conn.commit()
        print(f"\n✅ Successfully created {count} sample cinemas!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Creating sample cinemas...")
    print("-" * 50)
    create_sample_cinemas(10)
    print("-" * 50)
    print("\n✅ Done!")
