"""
Create demo users for testing
"""

import psycopg
import bcrypt

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'cinema_db',
    'user': 'postgres',
    'password': 'postgres'
}

def create_demo_users():
    """Create admin and customer demo users"""
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Hash passwords
        admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        customer_password = bcrypt.hashpw('customer123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create admin user
        cursor.execute(
            """INSERT INTO users (username, email, password, first_name, last_name, user_type)
               VALUES ('admin', 'admin@cinema.com', %s, 'Admin', 'User', 'admin')
               ON CONFLICT (username) DO NOTHING""",
            (admin_password,)
        )
        
        # Create customer user
        cursor.execute(
            """INSERT INTO users (username, email, password, first_name, last_name, user_type)
               VALUES ('john_doe', 'john.doe@example.com', %s, 'John', 'Doe', 'customer')
               ON CONFLICT (username) DO NOTHING""",
            (customer_password,)
        )
        
        conn.commit()
        print("Demo users created successfully!")
        print("\nDemo Credentials:")
        print("Admin: admin / admin123")
        print("Customer: john_doe / customer123")
        
    except Exception as e:
        print(f"Error creating demo users: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    create_demo_users()
