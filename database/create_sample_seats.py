"""
Script to create seats for existing cinema halls
"""

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


def create_seats_for_all_halls():
    """Create seats for all existing cinema halls"""
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Get all halls
        cursor.execute("SELECT hall_id, total_rows, seats_per_row FROM cinema_halls")
        halls = cursor.fetchall()
        
        if not halls:
            print("No cinema halls found. Please create cinema halls first.")
            return
        
        total_seats_created = 0
        
        for hall_id, total_rows, seats_per_row in halls:
            if not total_rows or not seats_per_row:
                print(f"Skipping hall {hall_id} - missing row/seat information")
                continue
            
            # Check if seats already exist for this hall
            cursor.execute("SELECT COUNT(*) FROM seats WHERE hall_id = %s", (hall_id,))
            existing_count = cursor.fetchone()[0]
            
            if existing_count > 0:
                print(f"Hall {hall_id} already has {existing_count} seats. Skipping.")
                continue
            
            # Determine seat types based on hall type
            cursor.execute("SELECT hall_type FROM cinema_halls WHERE hall_id = %s", (hall_id,))
            result = cursor.fetchone()
            hall_type = result[0] if result else None
            
            seats_created = 0
            
            # Create seats with different types based on row position
            for row in range(1, total_rows + 1):
                # Front rows (1-3): premium seats for some halls
                # Middle rows (4-8): standard seats
                # Back rows (9+): standard or vip for special halls
                
                for seat in range(1, seats_per_row + 1):
                    # Determine seat type
                    seat_type = 'standard'
                    price_multiplier = 1.00
                    
                    if hall_type in ['VIP', 'Gold Class']:
                        # All seats are premium in VIP/Gold Class
                        if row <= 3:
                            seat_type = 'vip'
                            price_multiplier = 2.00
                        elif row <= 6:
                            seat_type = 'premium'
                            price_multiplier = 1.50
                        else:
                            seat_type = 'standard'
                            price_multiplier = 1.00
                    elif hall_type == 'IMAX':
                        # IMAX halls have premium front rows
                        if row <= 4:
                            seat_type = 'premium'
                            price_multiplier = 1.50
                        else:
                            seat_type = 'standard'
                            price_multiplier = 1.00
                    else:
                        # Standard halls - occasional premium seats in front
                        if row <= 3 and seat % 3 == 1:
                            seat_type = 'premium'
                            price_multiplier = 1.50
                        else:
                            seat_type = 'standard'
                            price_multiplier = 1.00
                    
                    cursor.execute(
                        """INSERT INTO seats (hall_id, row_number, seat_number, seat_type, 
                                               price_multiplier, is_active)
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (hall_id, row, seat, seat_type, price_multiplier, True)
                    )
                    seats_created += 1
            
            print(f"Created {seats_created} seats for hall {hall_id} ({total_rows} rows × {seats_per_row} seats)")
            total_seats_created += seats_created
        
        conn.commit()
        print(f"\n✅ Successfully created {total_seats_created} seats!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Creating seats for cinema halls...")
    print("-" * 50)
    create_seats_for_all_halls()
    print("-" * 50)
    print("\n✅ Done!")

