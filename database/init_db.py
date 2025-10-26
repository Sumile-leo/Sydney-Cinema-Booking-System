"""
Initialize database - create tables from schema.sql
"""

import psycopg

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'postgres',  # Connect to default postgres db first
    'user': 'postgres',
    'password': 'postgres'
}

def init_database():
    """Initialize cinema database"""
    try:
        # Connect to postgres database
        conn = psycopg.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'cinema_db'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Creating database cinema_db...")
            cursor.execute('CREATE DATABASE cinema_db')
            print("Database created successfully!")
        else:
            print("Database cinema_db already exists")
        
        cursor.close()
        conn.close()
        
        # Connect to cinema_db and create tables
        db_config = DB_CONFIG.copy()
        db_config['dbname'] = 'cinema_db'
        
        conn = psycopg.connect(**db_config)
        cursor = conn.cursor()
        
        # Read and execute schema.sql
        print("Creating tables from schema.sql...")
        with open('database/schema.sql', 'r') as f:
            schema_sql = f.read()
            cursor.execute(schema_sql)
        
        conn.commit()
        print("Tables created successfully!")
        
        cursor.close()
        conn.close()
        
        print("\nDatabase initialization completed!")
        print("You can now run the Flask app with: python3 app.py")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    
    return True

if __name__ == '__main__':
    init_database()
