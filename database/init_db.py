#!/usr/bin/env python3
"""
Database Initialization Script for Sydney Cinema Booking System (PostgreSQL)

Author: Zhou Li
Course: COMP9001
Date: October 11, 2025
"""

import psycopg
from psycopg import Error
import os
import sys
from datetime import datetime

# Add backend directory to path for config import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from config import config

# Database configuration from config file
DB_CONFIG = config.get_database_config()

def create_database():
    """Create the database if it doesn't exist - 创建数据库（如果不存在）"""
    try:
        # Connect to PostgreSQL server (default database)
        connection = psycopg.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port'],
            dbname='postgres'  # Connect to default postgres database
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['dbname'],))
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['dbname']}")
            print(f"✅ Database '{DB_CONFIG['dbname']}' created successfully")
        else:
            print(f"✅ Database '{DB_CONFIG['dbname']}' already exists")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        sys.exit(1)

def run_schema():
    """Run the schema.sql file - 运行schema.sql文件"""
    try:
        connection = psycopg.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Read and execute schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        if not os.path.exists(schema_path):
            print(f"❌ Schema file not found: {schema_path}")
            sys.exit(1)
        
        with open(schema_path, 'r', encoding='utf-8') as file:
            schema_sql = file.read()
        
        # Execute the entire schema file
        try:
            cursor.execute(schema_sql)
            connection.commit()
            print("✅ Database schema executed successfully")
        except Error as e:
            print(f"⚠️  Warning executing schema: {e}")
            # Try to continue with individual statements
            statements = schema_sql.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                        connection.commit()
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            print(f"⚠️  Warning executing statement: {e}")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error running schema: {e}")
        sys.exit(1)

def test_connection():
    """Test database connection - 测试数据库连接"""
    try:
        connection = psycopg.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM movies")
        movie_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM cinemas")
        cinema_count = cursor.fetchone()[0]
        
        print(f"✅ Database connection successful!")
        print(f"   - Users: {user_count}")
        print(f"   - Movies: {movie_count}")
        print(f"   - Cinemas: {cinema_count}")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error testing connection: {e}")
        sys.exit(1)

def create_sample_data():
    """Create additional sample data if needed - 创建额外的示例数据（如果需要）"""
    try:
        connection = psycopg.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Check if we need more sample data
        cursor.execute("SELECT COUNT(*) FROM movies")
        movie_count = cursor.fetchone()[0]
        
        if movie_count < 10:
            print("📝 Adding more sample movies...")
            
            # Add more sample movies
            additional_movies = [
                ("Spider-Man: No Way Home", "Peter Parker's secret identity is revealed to the world", "Action", 148, "2021-12-17", "M", "Jon Watts", "Tom Holland, Zendaya, Benedict Cumberbatch", "English", "Chinese, Korean"),
                ("Dune", "Paul Atreides leads a rebellion to restore his family's honor", "Sci-Fi", 155, "2021-10-22", "M", "Denis Villeneuve", "Timothée Chalamet, Rebecca Ferguson, Oscar Isaac", "English", "Chinese, Korean"),
                ("No Time to Die", "James Bond's final mission as 007", "Action", 163, "2021-10-08", "M", "Cary Joji Fukunaga", "Daniel Craig, Ana de Armas, Rami Malek", "English", "Chinese, Korean"),
                ("Encanto", "A magical family in Colombia discovers their powers", "Animation", 109, "2021-11-24", "PG", "Jared Bush", "Stephanie Beatriz, María Cecilia Botero, John Leguizamo", "English", "Chinese, Korean"),
                ("Shang-Chi and the Legend of the Ten Rings", "Shang-Chi must confront his past and family", "Action", 132, "2021-09-03", "M", "Destin Daniel Cretton", "Simu Liu, Awkwafina, Tony Leung", "English", "Chinese, Korean")
            ]
            
            for movie in additional_movies:
                cursor.execute("""
                    INSERT INTO movies (title, description, genre, duration_minutes, release_date, rating, director, "cast", language, subtitles)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, movie)
            
            connection.commit()
            print(f"✅ Added {len(additional_movies)} additional movies")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error creating sample data: {e}")
        sys.exit(1)

def main():
    """Main initialization function - 主初始化函数"""
    print("🎬 Sydney Cinema Booking System - Database Initialization")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    create_database()
    print()
    
    # Step 2: Run schema
    print("Step 2: Running database schema...")
    run_schema()
    print()
    
    # Step 3: Test connection
    print("Step 3: Testing database connection...")
    test_connection()
    print()
    
    # Step 4: Create additional sample data
    print("Step 4: Creating additional sample data...")
    create_sample_data()
    print()
    
    print("🎉 Database initialization completed successfully!")
    print()
    print("📋 Next steps:")
    print("   1. Update database configuration in your application")
    print("   2. Run the Flask application: python backend/app.py")
    print("   3. Access web interface at: http://localhost:5001")
    print()
    print("🔐 Default login credentials:")
    print("   - Admin: admin / admin123")
    print("   - Staff: staff1 / staff123")
    print("   - Customer: john_doe / customer123")

if __name__ == "__main__":
    main()
