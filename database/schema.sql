-- Cinema Booking System Database Schema
-- Author: Zhou Li
-- Date: 2025-10-12

-- Drop all existing tables (in reverse dependency order)
DROP TABLE IF EXISTS seat_bookings CASCADE;
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS screenings CASCADE;
DROP TABLE IF EXISTS seats CASCADE;
DROP TABLE IF EXISTS cinema_halls CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS cinemas CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop trigger and function
DROP TRIGGER IF EXISTS check_screening_status ON screenings CASCADE;
DROP FUNCTION IF EXISTS deactivate_past_screenings() CASCADE;

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

-- Seats table
CREATE TABLE IF NOT EXISTS seats (
    seat_id SERIAL PRIMARY KEY,
    hall_id INTEGER NOT NULL,
    row_number INTEGER NOT NULL,
    seat_number INTEGER NOT NULL,
    seat_type VARCHAR(20),
    price_multiplier NUMERIC(3,2) DEFAULT 1.00,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (hall_id) REFERENCES cinema_halls(hall_id) ON DELETE CASCADE,
    UNIQUE(hall_id, row_number, seat_number)
);

-- Screenings table
CREATE TABLE IF NOT EXISTS screenings (
    screening_id SERIAL PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    cinema_id INTEGER NOT NULL,
    hall_id INTEGER NOT NULL,
    screening_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    ticket_price NUMERIC(10,2) NOT NULL,
    screening_type VARCHAR(20),
    language VARCHAR(50),
    subtitles VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (cinema_id) REFERENCES cinemas(cinema_id) ON DELETE CASCADE,
    FOREIGN KEY (hall_id) REFERENCES cinema_halls(hall_id) ON DELETE CASCADE
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    screening_id INTEGER NOT NULL,
    booking_number VARCHAR(20) UNIQUE NOT NULL,
    num_tickets INTEGER NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,
    booking_status VARCHAR(20) DEFAULT 'pending',
    payment_status VARCHAR(20) DEFAULT 'unpaid',
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (screening_id) REFERENCES screenings(screening_id) ON DELETE CASCADE
);

-- Seat Bookings table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS seat_bookings (
    seat_booking_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(seat_id) ON DELETE CASCADE,
    UNIQUE(booking_id, seat_id)
);

-- Function to automatically deactivate screenings that have passed
CREATE OR REPLACE FUNCTION deactivate_past_screenings()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE screenings
    SET is_active = FALSE
    WHERE (screening_date || ' ' || start_time)::timestamp < CURRENT_TIMESTAMP
      AND is_active = TRUE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to run the deactivation function on schedule
-- Note: This creates a trigger that runs on every INSERT/UPDATE to screenings table
-- For a periodic background job, use pg_cron or a scheduled task
CREATE TRIGGER check_screening_status
AFTER INSERT OR UPDATE ON screenings
FOR EACH ROW
EXECUTE FUNCTION deactivate_past_screenings();

-- Sample Data
-- Insert sample users
INSERT INTO users (username, email, password, first_name, last_name, phone, user_type) VALUES
('admin', 'admin@cinema.com', 'admin123', 'Admin', 'User', '0412345678', 'admin'),
('john_doe', 'john@example.com', 'customer123', 'John', 'Doe', '0487654321', 'customer');

-- Insert sample cinemas
INSERT INTO cinemas (cinema_name, address, suburb, postcode, phone, email, facilities, is_active) VALUES
('Event Cinemas George Street', '505 George St', 'Sydney', '2000', '02 9273 7300', 'info@eventcinemas.com.au', 'IMAX, 3D, Dolby Atmos', true),
('Hoyts Broadway', 'Bay St Broadway', 'Sydney', '2007', '02 9211 6688', 'info@hoyts.com.au', 'VIP Lounges, 3D', true),
('Palace Cinema', '22 Oxford St', 'Paddington', '2021', '02 9361 5399', 'info@palacecinemas.com.au', 'Luxury Seating', true),
('Cinema Renaissance', '261 King St', 'Newtown', '2042', '02 9550 3666', 'info@renaissancecinema.com.au', 'Art House Films', true),
('Randwick Ritz', '45 Saint Pauls St', 'Randwick', '2031', '02 9398 1617', 'info@ritzcinema.com.au', 'Dolby Vision', true);
