-- Sydney Cinema Booking System - Updated Schema with Halls and Seats
-- 悉尼电影院购票系统 - 包含影厅和座位的更新架构

-- Drop existing tables if they exist - 如果存在则删除现有表
DROP TABLE IF EXISTS seat_bookings CASCADE;
DROP TABLE IF EXISTS seats CASCADE;
DROP TABLE IF EXISTS cinema_halls CASCADE;
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS screenings CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS cinemas CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table - 创建用户表
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    user_type VARCHAR(20) DEFAULT 'customer' CHECK (user_type IN ('admin', 'staff', 'customer')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create cinemas table - 创建电影院表
CREATE TABLE cinemas (
    cinema_id SERIAL PRIMARY KEY,
    cinema_name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    suburb VARCHAR(50) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(200),
    facilities TEXT,
    parking_info TEXT,
    public_transport TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create movies table - 创建电影表
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    genre VARCHAR(50),
    duration_minutes INTEGER NOT NULL,
    release_date DATE,
    rating VARCHAR(10) CHECK (rating IN ('G', 'PG', 'M', 'MA15+', 'R18+')),
    director VARCHAR(100),
    "cast" TEXT,
    language VARCHAR(50) DEFAULT 'English',
    subtitles VARCHAR(100),
    poster_url VARCHAR(500),
    trailer_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create cinema halls table - 创建影厅表
CREATE TABLE cinema_halls (
    hall_id SERIAL PRIMARY KEY,
    cinema_id INTEGER NOT NULL REFERENCES cinemas(cinema_id) ON DELETE CASCADE,
    hall_name VARCHAR(50) NOT NULL,
    hall_type VARCHAR(20) DEFAULT 'standard' CHECK (hall_type IN ('standard', 'IMAX', 'Gold Class', 'VMAX')),
    total_rows INTEGER NOT NULL DEFAULT 10,
    seats_per_row INTEGER NOT NULL DEFAULT 15,
    total_seats INTEGER NOT NULL,
    screen_size VARCHAR(20) DEFAULT 'standard',
    sound_system VARCHAR(30) DEFAULT 'standard',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create seats table - 创建座位表
CREATE TABLE seats (
    seat_id SERIAL PRIMARY KEY,
    hall_id INTEGER NOT NULL REFERENCES cinema_halls(hall_id) ON DELETE CASCADE,
    row_number INTEGER NOT NULL,
    seat_number INTEGER NOT NULL,
    seat_type VARCHAR(20) DEFAULT 'standard' CHECK (seat_type IN ('standard', 'premium', 'vip', 'wheelchair')),
    price_multiplier DECIMAL(3,2) DEFAULT 1.00,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(hall_id, row_number, seat_number)
);

-- Create screenings table - 创建放映场次表
CREATE TABLE screenings (
    screening_id SERIAL PRIMARY KEY,
    movie_id INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    cinema_id INTEGER NOT NULL REFERENCES cinemas(cinema_id) ON DELETE CASCADE,
    hall_id INTEGER NOT NULL REFERENCES cinema_halls(hall_id) ON DELETE CASCADE,
    screening_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    ticket_price DECIMAL(10,2) NOT NULL,
    screening_type VARCHAR(20) DEFAULT 'standard' CHECK (screening_type IN ('standard', 'IMAX', 'Gold Class', 'VMAX')),
    language VARCHAR(50) DEFAULT 'English',
    subtitles VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create bookings table - 创建预订表
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    screening_id INTEGER NOT NULL REFERENCES screenings(screening_id) ON DELETE CASCADE,
    booking_number VARCHAR(20) UNIQUE NOT NULL,
    num_tickets INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    booking_status VARCHAR(20) DEFAULT 'confirmed' CHECK (booking_status IN ('pending', 'confirmed', 'cancelled', 'completed')),
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create seat bookings table - 创建座位预订表
CREATE TABLE seat_bookings (
    seat_booking_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    seat_id INTEGER NOT NULL REFERENCES seats(seat_id) ON DELETE CASCADE,
    screening_id INTEGER NOT NULL REFERENCES screenings(screening_id) ON DELETE CASCADE,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(seat_id, screening_id)
);

-- Create indexes for better performance - 创建索引以提高性能
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_cinemas_suburb ON cinemas(suburb);
CREATE INDEX idx_movies_title ON movies(title);
CREATE INDEX idx_movies_genre ON movies(genre);
CREATE INDEX idx_screenings_date ON screenings(screening_date);
CREATE INDEX idx_screenings_cinema_movie ON screenings(cinema_id, movie_id);
CREATE INDEX idx_screenings_hall ON screenings(hall_id);
CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_bookings_screening ON bookings(screening_id);
CREATE INDEX idx_bookings_number ON bookings(booking_number);
CREATE INDEX idx_cinema_halls_cinema ON cinema_halls(cinema_id);
CREATE INDEX idx_seats_hall ON seats(hall_id);
CREATE INDEX idx_seat_bookings_booking ON seat_bookings(booking_id);
CREATE INDEX idx_seat_bookings_screening ON seat_bookings(screening_id);

-- Create triggers for updated_at - 创建updated_at触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_cinemas_updated_at BEFORE UPDATE ON cinemas FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_movies_updated_at BEFORE UPDATE ON movies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_cinema_halls_updated_at BEFORE UPDATE ON cinema_halls FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_seats_updated_at BEFORE UPDATE ON seats FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_screenings_updated_at BEFORE UPDATE ON screenings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_bookings_updated_at BEFORE UPDATE ON bookings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample users - 插入示例用户
INSERT INTO users (username, email, password_hash, first_name, last_name, phone, user_type) VALUES
('admin', 'admin@cinema.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'Admin', 'User', '0400-000-001', 'admin'),
('staff1', 'staff1@cinema.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'Staff', 'Member', '0400-000-002', 'staff'),
('john_doe', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'John', 'Doe', '0400-000-003', 'customer');

-- Insert sample cinemas - 插入示例电影院
INSERT INTO cinemas (cinema_name, address, suburb, postcode, phone, email, website, facilities, parking_info, public_transport) VALUES
('Event Cinemas George Street', '505-525 George St', 'Sydney CBD', '2000', '(02) 9273 7300', 'george@eventcinemas.com.au', 'https://www.eventcinemas.com.au', 'IMAX, Gold Class, VMAX, Candy Bar, Cafe', 'Wilson Parking available nearby', 'Town Hall Station, Bus stops'),
('Hoyts Broadway', '188-210 Broadway', 'Broadway', '2007', '(02) 9211 2000', 'broadway@hoyts.com.au', 'https://www.hoyts.com.au', 'VMAX, Gold Class, Candy Bar, Cafe', 'Limited parking available', 'Central Station, Bus stops'),
('Village Cinemas Bondi Junction', '500 Oxford St', 'Bondi Junction', '2022', '(02) 9387 4000', 'bondi@villagecinemas.com.au', 'https://www.villagecinemas.com.au', 'Gold Class, Standard Screens, Candy Bar', 'Westfield parking available', 'Bondi Junction Station, Bus stops');

-- Insert sample movies - 插入示例电影
INSERT INTO movies (title, description, genre, duration_minutes, release_date, rating, director, "cast", language, subtitles, poster_url, trailer_url) VALUES
('Avatar: The Way of Water', 'Set more than a decade after the events of the first film, Avatar: The Way of Water begins to tell the story of the Sully family.', 'Sci-Fi', 192, '2022-12-16', 'M', 'James Cameron', 'Sam Worthington, Zoe Saldana, Sigourney Weaver', 'English', 'Chinese, Korean, Japanese', 'https://example.com/avatar2.jpg', 'https://youtube.com/avatar2'),
('Top Gun: Maverick', 'After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past.', 'Action', 131, '2022-05-27', 'M', 'Joseph Kosinski', 'Tom Cruise, Miles Teller, Jennifer Connelly', 'English', 'Chinese, Korean', 'https://example.com/topgun2.jpg', 'https://youtube.com/topgun2'),
('Black Panther: Wakanda Forever', 'The nation of Wakanda is pitted against intervening world powers as they mourn the loss of their king T''Challa.', 'Action', 161, '2022-11-11', 'M', 'Ryan Coogler', 'Letitia Wright, Lupita Nyong''o, Danai Gurira', 'English', 'Chinese, Korean', 'https://example.com/blackpanther2.jpg', 'https://youtube.com/blackpanther2'),
('The Batman', 'When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate.', 'Action', 176, '2022-03-04', 'M', 'Matt Reeves', 'Robert Pattinson, Zoë Kravitz, Paul Dano', 'English', 'Chinese, Korean', 'https://example.com/batman.jpg', 'https://youtube.com/batman'),
('Jurassic World Dominion', 'Four years after the destruction of Isla Nublar, dinosaurs now live and hunt alongside humans all over the world.', 'Action', 147, '2022-06-10', 'M', 'Colin Trevorrow', 'Chris Pratt, Bryce Dallas Howard, Laura Dern', 'English', 'Chinese, Korean', 'https://example.com/jurassic3.jpg', 'https://youtube.com/jurassic3');

-- Insert sample cinema halls - 插入示例影厅
INSERT INTO cinema_halls (cinema_id, hall_name, hall_type, total_rows, seats_per_row, total_seats, screen_size, sound_system) VALUES
-- Event Cinemas George Street halls
(1, 'Hall 1', 'IMAX', 12, 20, 240, 'IMAX', 'IMAX Sound'),
(1, 'Hall 2', 'standard', 10, 15, 150, 'standard', 'Dolby Digital'),
(1, 'Hall 3', 'Gold Class', 8, 12, 96, 'large', 'Dolby Atmos'),
-- Hoyts Broadway halls
(2, 'Screen 1', 'standard', 10, 18, 180, 'standard', 'Dolby Digital'),
(2, 'Screen 2', 'VMAX', 12, 22, 264, 'VMAX', 'Dolby Atmos'),
(2, 'Screen 3', 'standard', 9, 16, 144, 'standard', 'Dolby Digital'),
-- Village Cinemas Bondi Junction halls
(3, 'Cinema 1', 'standard', 11, 17, 187, 'standard', 'Dolby Digital'),
(3, 'Cinema 2', 'Gold Class', 7, 14, 98, 'large', 'Dolby Atmos'),
(3, 'Cinema 3', 'standard', 10, 15, 150, 'standard', 'Dolby Digital');

-- Insert sample seats for Hall 1 (IMAX) - 为Hall 1插入示例座位
INSERT INTO seats (hall_id, row_number, seat_number, seat_type, price_multiplier) VALUES
-- Row 1 (Premium seats)
(1, 1, 1, 'premium', 1.5), (1, 1, 2, 'premium', 1.5), (1, 1, 3, 'premium', 1.5), (1, 1, 4, 'premium', 1.5), (1, 1, 5, 'premium', 1.5),
(1, 1, 6, 'premium', 1.5), (1, 1, 7, 'premium', 1.5), (1, 1, 8, 'premium', 1.5), (1, 1, 9, 'premium', 1.5), (1, 1, 10, 'premium', 1.5),
(1, 1, 11, 'premium', 1.5), (1, 1, 12, 'premium', 1.5), (1, 1, 13, 'premium', 1.5), (1, 1, 14, 'premium', 1.5), (1, 1, 15, 'premium', 1.5),
(1, 1, 16, 'premium', 1.5), (1, 1, 17, 'premium', 1.5), (1, 1, 18, 'premium', 1.5), (1, 1, 19, 'premium', 1.5), (1, 1, 20, 'premium', 1.5),
-- Rows 2-12 (Standard seats)
(1, 2, 1, 'standard', 1.0), (1, 2, 2, 'standard', 1.0), (1, 2, 3, 'standard', 1.0), (1, 2, 4, 'standard', 1.0), (1, 2, 5, 'standard', 1.0),
(1, 2, 6, 'standard', 1.0), (1, 2, 7, 'standard', 1.0), (1, 2, 8, 'standard', 1.0), (1, 2, 9, 'standard', 1.0), (1, 2, 10, 'standard', 1.0),
(1, 2, 11, 'standard', 1.0), (1, 2, 12, 'standard', 1.0), (1, 2, 13, 'standard', 1.0), (1, 2, 14, 'standard', 1.0), (1, 2, 15, 'standard', 1.0),
(1, 2, 16, 'standard', 1.0), (1, 2, 17, 'standard', 1.0), (1, 2, 18, 'standard', 1.0), (1, 2, 19, 'standard', 1.0), (1, 2, 20, 'standard', 1.0);

-- Insert sample screenings - 插入示例放映场次
INSERT INTO screenings (movie_id, cinema_id, hall_id, screening_date, start_time, end_time, ticket_price, screening_type, language, subtitles) VALUES
-- Event Cinemas George Street screenings
(1, 1, 1, '2025-10-26', '10:00:00', '13:12:00', 25.00, 'IMAX', 'English', 'Chinese'),
(1, 1, 1, '2025-10-26', '14:00:00', '17:12:00', 25.00, 'IMAX', 'English', 'Chinese'),
(1, 1, 1, '2025-10-26', '18:00:00', '21:12:00', 30.00, 'IMAX', 'English', 'Chinese'),
(2, 1, 2, '2025-10-26', '11:00:00', '13:11:00', 22.00, 'standard', 'English', 'Chinese'),
(2, 1, 2, '2025-10-26', '15:00:00', '17:11:00', 22.00, 'standard', 'English', 'Chinese'),
(2, 1, 2, '2025-10-26', '19:00:00', '21:11:00', 27.00, 'standard', 'English', 'Chinese'),
(3, 1, 3, '2025-10-26', '12:00:00', '14:41:00', 35.00, 'Gold Class', 'English', 'Chinese'),
(3, 1, 3, '2025-10-26', '16:00:00', '18:41:00', 35.00, 'Gold Class', 'English', 'Chinese'),
(3, 1, 3, '2025-10-26', '20:00:00', '22:41:00', 40.00, 'Gold Class', 'English', 'Chinese');

-- Insert sample bookings - 插入示例预订
INSERT INTO bookings (user_id, screening_id, booking_number, num_tickets, total_amount, booking_status, payment_status, booking_date) VALUES
(3, 1, 'BKG-2025-001', 2, 50.00, 'confirmed', 'paid', '2025-10-25 10:30:00'),
(3, 2, 'BKG-2025-002', 1, 25.00, 'confirmed', 'paid', '2025-10-25 14:20:00'),
(3, 3, 'BKG-2025-003', 3, 90.00, 'confirmed', 'paid', '2025-10-25 16:45:00');
