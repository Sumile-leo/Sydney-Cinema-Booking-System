-- Cinema Booking System Database Schema
-- Created: October 26, 2025

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    user_type VARCHAR(20) DEFAULT 'customer' CHECK (user_type IN ('customer', 'staff', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cinemas table
CREATE TABLE IF NOT EXISTS cinemas (
    cinema_id SERIAL PRIMARY KEY,
    cinema_name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    suburb VARCHAR(50) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    facilities TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Movies table
CREATE TABLE IF NOT EXISTS movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    genre VARCHAR(50),
    duration_minutes INTEGER,
    release_date DATE,
    director VARCHAR(100),
    "cast" TEXT,
    language VARCHAR(50),
    subtitles VARCHAR(50),
    poster_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Cinema Halls table
CREATE TABLE IF NOT EXISTS cinema_halls (
    hall_id SERIAL PRIMARY KEY,
    cinema_id INTEGER NOT NULL,
    hall_name VARCHAR(50) NOT NULL,
    hall_type VARCHAR(50),
    total_rows INTEGER,
    seats_per_row INTEGER,
    total_seats INTEGER,
    screen_size VARCHAR(50),
    sound_system VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cinema_id) REFERENCES cinemas(cinema_id) ON DELETE CASCADE
);
