-- Sydney Cinema Booking System Database Schema
-- PostgreSQL Version
-- Date: October 10, 2025

-- Drop existing tables if they exist
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS screenings CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS cinemas CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    user_type VARCHAR(20) DEFAULT 'customer' CHECK (user_type IN ('customer', 'admin', 'staff')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Cinemas table
CREATE TABLE cinemas (
    cinema_id SERIAL PRIMARY KEY,
    cinema_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    suburb VARCHAR(50) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    total_screens INTEGER NOT NULL,
    facilities TEXT,
    parking_info TEXT,
    public_transport TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Movies table
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

-- Screenings table
CREATE TABLE screenings (
    screening_id SERIAL PRIMARY KEY,
    movie_id INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    cinema_id INTEGER NOT NULL REFERENCES cinemas(cinema_id) ON DELETE CASCADE,
    screen_number INTEGER NOT NULL,
    screening_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    ticket_price DECIMAL(10,2) NOT NULL,
    available_seats INTEGER NOT NULL,
    total_seats INTEGER NOT NULL,
    screening_type VARCHAR(20) DEFAULT 'standard' CHECK (screening_type IN ('standard', '3D', 'IMAX', 'VIP', 'Gold Class')),
    language VARCHAR(50) DEFAULT 'English',
    subtitles VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Bookings table
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    screening_id INTEGER NOT NULL REFERENCES screenings(screening_id) ON DELETE CASCADE,
    booking_number VARCHAR(20) UNIQUE NOT NULL,
    num_tickets INTEGER NOT NULL CHECK (num_tickets > 0),
    total_amount DECIMAL(10,2) NOT NULL,
    booking_status VARCHAR(20) DEFAULT 'confirmed' CHECK (booking_status IN ('pending', 'confirmed', 'cancelled', 'completed')),
    payment_method VARCHAR(20) CHECK (payment_method IN ('credit_card', 'debit_card', 'paypal', 'cash')),
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
    payment_date TIMESTAMP,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

-- Create seat bookings table - 创建座位预订表
CREATE TABLE seat_bookings (
    seat_booking_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    seat_id INTEGER NOT NULL REFERENCES seats(seat_id) ON DELETE CASCADE,
    screening_id INTEGER NOT NULL REFERENCES screenings(screening_id) ON DELETE CASCADE,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(seat_id, screening_id)
);

-- Update screenings table to reference halls - 更新场次表引用影厅
ALTER TABLE screenings ADD COLUMN hall_id INTEGER REFERENCES cinema_halls(hall_id);
ALTER TABLE screenings DROP COLUMN screen_number;
ALTER TABLE screenings DROP COLUMN total_seats;
ALTER TABLE screenings DROP COLUMN available_seats;

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
CREATE TRIGGER update_screenings_updated_at BEFORE UPDATE ON screenings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_bookings_updated_at BEFORE UPDATE ON bookings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample users - 插入示例用户
INSERT INTO users (username, email, password_hash, first_name, last_name, phone, user_type) VALUES
('admin', 'admin@cinema.com', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'Admin', 'User', '0412345678', 'admin'),
('staff1', 'staff1@cinema.com', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'Staff', 'Member', '0412345679', 'staff'),
('john_doe', 'john.doe@email.com', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'John', 'Doe', '0412345680', 'customer'),
('jane_smith', 'jane.smith@email.com', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'Jane', 'Smith', '0412345681', 'customer'),
('mike_wilson', 'mike.wilson@email.com', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'Mike', 'Wilson', '0412345682', 'customer');

-- Insert sample cinemas - 插入示例电影院
INSERT INTO cinemas (cinema_name, address, suburb, postcode, phone, total_screens, facilities, parking_info, public_transport) VALUES
('Event Cinemas George Street', '505-525 George St, Sydney NSW 2000', 'Sydney CBD', '2000', '(02) 9273 7300', 9, 'IMAX, Gold Class, VMAX, Candy Bar, Cafe', 'Wilson Parking nearby', 'Town Hall Station, Bus stops'),
('Hoyts Broadway', '185-211 Broadway, Chippendale NSW 2008', 'Chippendale', '2008', '(02) 9211 1900', 8, 'IMAX, Xtremescreen, Candy Bar, Cafe', 'Paid parking available', 'Central Station, Bus stops'),
('Village Cinemas Bondi Junction', '500 Oxford St, Bondi Junction NSW 2022', 'Bondi Junction', '2022', '(02) 9389 4000', 6, 'Gold Class, VMAX, Candy Bar', 'Westfield parking', 'Bondi Junction Station'),
('Palace Cinemas Norton Street', '99 Norton St, Leichhardt NSW 2040', 'Leichhardt', '2040', '(02) 9550 3666', 4, 'Art House, Cafe, Bar', 'Street parking', 'Bus stops, Leichhardt'),
('Reading Cinemas Newtown', '261-263 King St, Newtown NSW 2042', 'Newtown', '2042', '(02) 9557 2000', 5, 'Standard screens, Candy Bar', 'Limited parking', 'Newtown Station, Bus stops'),
('Event Cinemas Macquarie', 'Macquarie Shopping Centre, North Ryde NSW 2113', 'North Ryde', '2113', '(02) 9887 7300', 7, 'IMAX, Gold Class, VMAX', 'Shopping centre parking', 'Macquarie University Station'),
('Village Cinemas Top Ryde', '109-129 Blaxland Rd, Ryde NSW 2112', 'Ryde', '2112', '(02) 9808 4000', 6, 'Gold Class, VMAX, Candy Bar', 'Shopping centre parking', 'Top Ryde City Bus'),
('Hoyts Blacktown', '17 Patrick St, Blacktown NSW 2148', 'Blacktown', '2148', '(02) 9831 1900', 8, 'IMAX, Xtremescreen, Candy Bar', 'Free parking', 'Blacktown Station'),
('Event Cinemas Castle Hill', 'Castle Towers Shopping Centre, Castle Hill NSW 2154', 'Castle Hill', '2154', '(02) 9634 7300', 6, 'IMAX, Gold Class, VMAX', 'Shopping centre parking', 'Castle Hill Station'),
('Palace Cinemas Central', 'Level 3, Central Park, Chippendale NSW 2008', 'Chippendale', '2008', '(02) 8080 4000', 4, 'Premium screens, Bar, Restaurant', 'Central Park parking', 'Central Station');

-- Insert sample movies
INSERT INTO movies (title, description, genre, duration_minutes, release_date, rating, director, "cast", language, subtitles, poster_url, trailer_url) VALUES
('Avatar: The Way of Water', 'Set more than a decade after the events of the first film, Avatar: The Way of Water begins to tell the story of the Sully family.', 'Sci-Fi', 192, '2022-12-16', 'M', 'James Cameron', 'Sam Worthington, Zoe Saldana, Sigourney Weaver', 'English', 'Chinese, Korean, Japanese', 'https://example.com/avatar2.jpg', 'https://youtube.com/avatar2'),
('Top Gun: Maverick', 'After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past.', 'Action', 131, '2022-05-27', 'M', 'Joseph Kosinski', 'Tom Cruise, Miles Teller, Jennifer Connelly', 'English', 'Chinese, Korean', 'https://example.com/topgun2.jpg', 'https://youtube.com/topgun2'),
('Black Panther: Wakanda Forever', 'The nation of Wakanda is pitted against intervening world powers as they mourn the loss of their king T''Challa.', 'Action', 161, '2022-11-11', 'M', 'Ryan Coogler', 'Letitia Wright, Lupita Nyong''o, Danai Gurira', 'English', 'Chinese, Korean', 'https://example.com/blackpanther2.jpg', 'https://youtube.com/blackpanther2'),
('The Batman', 'When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate.', 'Action', 176, '2022-03-04', 'M', 'Matt Reeves', 'Robert Pattinson, Zoë Kravitz, Paul Dano', 'English', 'Chinese, Korean', 'https://example.com/batman.jpg', 'https://youtube.com/batman'),
('Jurassic World Dominion', 'Four years after the destruction of Isla Nublar, dinosaurs now live and hunt alongside humans all over the world.', 'Action', 147, '2022-06-10', 'M', 'Colin Trevorrow', 'Chris Pratt, Bryce Dallas Howard, Laura Dern', 'English', 'Chinese, Korean', 'https://example.com/jurassic3.jpg', 'https://youtube.com/jurassic3'),
('Minions: The Rise of Gru', 'In the 1970s, young Gru tries to join a group of supervillains called the Vicious 6 after they oust their leader.', 'Animation', 87, '2022-07-01', 'PG', 'Kyle Balda', 'Steve Carell, Pierre Coffin, Russell Brand', 'English', 'Chinese, Korean', 'https://example.com/minions2.jpg', 'https://youtube.com/minions2'),
('Doctor Strange in the Multiverse of Madness', 'Dr. Stephen Strange casts a forbidden spell that opens the doorway to the multiverse.', 'Action', 126, '2022-05-06', 'M', 'Sam Raimi', 'Benedict Cumberbatch, Elizabeth Olsen, Chiwetel Ejiofor', 'English', 'Chinese, Korean', 'https://example.com/doctorstrange2.jpg', 'https://youtube.com/doctorstrange2'),
('Thor: Love and Thunder', 'Thor enlists the help of Valkyrie, Korg and ex-girlfriend Jane Foster to fight Gorr the God Butcher.', 'Action', 119, '2022-07-08', 'M', 'Taika Waititi', 'Chris Hemsworth, Natalie Portman, Christian Bale', 'English', 'Chinese, Korean', 'https://example.com/thor4.jpg', 'https://youtube.com/thor4'),
('Lightyear', 'While working to fix his ship, Buzz Lightyear accidentally launches himself into space and must find his way back home.', 'Animation', 105, '2022-06-17', 'PG', 'Angus MacLane', 'Chris Evans, Keke Palmer, Peter Sohn', 'English', 'Chinese, Korean', 'https://example.com/lightyear.jpg', 'https://youtube.com/lightyear'),
('Elvis', 'The life of American music icon Elvis Presley, from his childhood to becoming a rock and movie star.', 'Biography', 159, '2022-06-24', 'M', 'Baz Luhrmann', 'Austin Butler, Tom Hanks, Olivia DeJong', 'English', 'Chinese, Korean', 'https://example.com/elvis.jpg', 'https://youtube.com/elvis');

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

-- Insert sample seats - 插入示例座位
INSERT INTO seats (hall_id, row_number, seat_number, seat_type, price_multiplier) VALUES
-- Hall 1 (IMAX) seats
(1, 1, 1, 'premium', 1.5), (1, 1, 2, 'premium', 1.5), (1, 1, 3, 'premium', 1.5), (1, 1, 4, 'premium', 1.5), (1, 1, 5, 'premium', 1.5),
(1, 1, 6, 'premium', 1.5), (1, 1, 7, 'premium', 1.5), (1, 1, 8, 'premium', 1.5), (1, 1, 9, 'premium', 1.5), (1, 1, 10, 'premium', 1.5),
(1, 1, 11, 'premium', 1.5), (1, 1, 12, 'premium', 1.5), (1, 1, 13, 'premium', 1.5), (1, 1, 14, 'premium', 1.5), (1, 1, 15, 'premium', 1.5),
(1, 1, 16, 'premium', 1.5), (1, 1, 17, 'premium', 1.5), (1, 1, 18, 'premium', 1.5), (1, 1, 19, 'premium', 1.5), (1, 1, 20, 'premium', 1.5),
-- Hall 1 rows 2-12 (standard seats)
(1, 2, 1, 'standard', 1.0), (1, 2, 2, 'standard', 1.0), (1, 2, 3, 'standard', 1.0), (1, 2, 4, 'standard', 1.0), (1, 2, 5, 'standard', 1.0),
(1, 2, 6, 'standard', 1.0), (1, 2, 7, 'standard', 1.0), (1, 2, 8, 'standard', 1.0), (1, 2, 9, 'standard', 1.0), (1, 2, 10, 'standard', 1.0),
(1, 2, 11, 'standard', 1.0), (1, 2, 12, 'standard', 1.0), (1, 2, 13, 'standard', 1.0), (1, 2, 14, 'standard', 1.0), (1, 2, 15, 'standard', 1.0),
(1, 2, 16, 'standard', 1.0), (1, 2, 17, 'standard', 1.0), (1, 2, 18, 'standard', 1.0), (1, 2, 19, 'standard', 1.0), (1, 2, 20, 'standard', 1.0);

-- Insert sample screenings - 插入示例放映场次
INSERT INTO screenings (movie_id, cinema_id, hall_id, screening_date, start_time, end_time, ticket_price, screening_type, language, subtitles) VALUES
-- Event Cinemas George Street screenings
(1, 1, 1, '2025-10-26', '10:00:00', '13:12:00', 25.00, 150, 200, 'IMAX', 'English', 'Chinese'),
(1, 1, 1, '2025-10-26', '14:00:00', '17:12:00', 25.00, 180, 200, 'IMAX', 'English', 'Chinese'),
(1, 1, 1, '2025-10-26', '18:00:00', '21:12:00', 30.00, 120, 200, 'IMAX', 'English', 'Chinese'),
(2, 1, 2, '2025-10-26', '11:00:00', '13:11:00', 22.00, 100, 150, 'standard', 'English', 'Chinese'),
(2, 1, 2, '2025-10-26', '15:00:00', '17:11:00', 22.00, 120, 150, 'standard', 'English', 'Chinese'),
(2, 1, 2, '2025-10-26', '19:00:00', '21:11:00', 27.00, 80, 150, 'standard', 'English', 'Chinese'),

-- Hoyts Broadway screenings
(3, 2, 1, '2025-10-26', '10:30:00', '13:11:00', 24.00, 200, 250, 'IMAX', 'English', 'Chinese'),
(3, 2, 1, '2025-10-26', '14:30:00', '17:11:00', 24.00, 220, 250, 'IMAX', 'English', 'Chinese'),
(3, 2, 1, '2025-10-26', '18:30:00', '21:11:00', 29.00, 150, 250, 'IMAX', 'English', 'Chinese'),
(4, 2, 2, '2025-10-26', '12:00:00', '14:56:00', 23.00, 80, 120, 'standard', 'English', 'Chinese'),
(4, 2, 2, '2025-10-26', '16:00:00', '18:56:00', 23.00, 100, 120, 'standard', 'English', 'Chinese'),
(4, 2, 2, '2025-10-26', '20:00:00', '22:56:00', 28.00, 60, 120, 'standard', 'English', 'Chinese'),

-- Village Cinemas Bondi Junction screenings
(5, 3, 1, '2025-10-26', '11:30:00', '13:57:00', 26.00, 90, 120, 'Gold Class', 'English', 'Chinese'),
(5, 3, 1, '2025-10-26', '15:30:00', '17:57:00', 26.00, 110, 120, 'Gold Class', 'English', 'Chinese'),
(5, 3, 1, '2025-10-26', '19:30:00', '21:57:00', 31.00, 70, 120, 'Gold Class', 'English', 'Chinese'),
(6, 3, 2, '2025-10-26', '10:00:00', '11:27:00', 18.00, 150, 180, 'standard', 'English', 'Chinese'),
(6, 3, 2, '2025-10-26', '13:00:00', '14:27:00', 18.00, 160, 180, 'standard', 'English', 'Chinese'),
(6, 3, 2, '2025-10-26', '16:00:00', '17:27:00', 18.00, 140, 180, 'standard', 'English', 'Chinese'),

-- Palace Cinemas Norton Street screenings
(7, 4, 1, '2025-10-26', '14:00:00', '16:06:00', 20.00, 60, 80, 'standard', 'English', 'Chinese'),
(7, 4, 1, '2025-10-26', '18:00:00', '20:06:00', 25.00, 50, 80, 'standard', 'English', 'Chinese'),
(8, 4, 2, '2025-10-26', '15:00:00', '16:59:00', 22.00, 70, 90, 'standard', 'English', 'Chinese'),
(8, 4, 2, '2025-10-26', '19:00:00', '20:59:00', 27.00, 60, 90, 'standard', 'English', 'Chinese'),

-- Reading Cinemas Newtown screenings
(9, 5, 1, '2025-10-26', '12:00:00', '13:45:00', 19.00, 100, 130, 'standard', 'English', 'Chinese'),
(9, 5, 1, '2025-10-26', '16:00:00', '17:45:00', 19.00, 110, 130, 'standard', 'English', 'Chinese'),
(9, 5, 1, '2025-10-26', '20:00:00', '21:45:00', 24.00, 80, 130, 'standard', 'English', 'Chinese'),
(10, 5, 2, '2025-10-26', '13:00:00', '15:39:00', 21.00, 85, 110, 'standard', 'English', 'Chinese'),
(10, 5, 2, '2025-10-26', '17:00:00', '19:39:00', 21.00, 95, 110, 'standard', 'English', 'Chinese'),
(10, 5, 2, '2025-10-26', '21:00:00', '23:39:00', 26.00, 70, 110, 'standard', 'English', 'Chinese');

-- Insert sample bookings - 插入示例预订
INSERT INTO bookings (user_id, screening_id, booking_number, num_tickets, total_amount, booking_status, payment_method, payment_status, payment_date) VALUES
(3, 1, 'CIN-2025-001', 2, 50.00, 'confirmed', 'credit_card', 'paid', '2025-10-25 10:30:00'),
(4, 2, 'CIN-2025-002', 1, 25.00, 'confirmed', 'credit_card', 'paid', '2025-10-25 14:20:00'),
(5, 3, 'CIN-2025-003', 3, 90.00, 'confirmed', 'debit_card', 'paid', '2025-10-25 16:45:00'),
(3, 4, 'CIN-2025-004', 2, 44.00, 'confirmed', 'credit_card', 'paid', '2025-10-25 11:15:00'),
(4, 5, 'CIN-2025-005', 1, 22.00, 'pending', 'credit_card', 'pending', NULL);

-- Create views for common queries - 创建常用查询视图
CREATE VIEW movie_screenings_view AS
SELECT 
    m.movie_id,
    m.title,
    m.title_chinese,
    m.genre,
    m.duration_minutes,
    m.rating,
    s.screening_id,
    s.screening_date,
    s.start_time,
    s.end_time,
    s.ticket_price,
    s.available_seats,
    s.total_seats,
    s.screening_type,
    c.cinema_name,
    c.suburb,
    c.address
FROM movies m
JOIN screenings s ON m.movie_id = s.movie_id
JOIN cinemas c ON s.cinema_id = c.cinema_id
WHERE s.is_active = TRUE AND m.is_active = TRUE AND c.is_active = TRUE;

CREATE VIEW cinema_movies_view AS
SELECT 
    c.cinema_id,
    c.cinema_name,
    c.suburb,
    COUNT(DISTINCT s.movie_id) as movie_count,
    COUNT(s.screening_id) as total_screenings
FROM cinemas c
LEFT JOIN screenings s ON c.cinema_id = s.cinema_id AND s.is_active = TRUE
WHERE c.is_active = TRUE
GROUP BY c.cinema_id, c.cinema_name, c.suburb;

-- Grant permissions - 授予权限
-- Note: Adjust permissions based on your security requirements
-- 注意：根据您的安全要求调整权限

COMMIT;