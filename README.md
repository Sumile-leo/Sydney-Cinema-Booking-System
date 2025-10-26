# Sydney Cinema Booking System

A comprehensive cinema booking system for managing movies, cinemas, screenings, and user bookings.

**Author**: Zhou Li  
**Email**: lizhouxx0126@gmail.com  
**Date**: October 10-29, 2025  
**Course**: COMP9001 - The University of Sydney

## Important Notice

This project acknowledges the use of AI assistance in its development:

- **Frontend Pages & README**: The HTML templates, CSS styling, and README documentation were generated with the assistance of ChatGPT.
- **Python Business Logic**: All Python backend code including routes, services, database functions, and models were written by the author (Zhou Li).
- **Database Schema**: Designed by the author.

For any inquiries or questions, please contact the author via email.

## Features

- 🎬 **Movie Management**: Browse movies with posters, details, and genres
- 🏛️ **Cinema Management**: View cinema locations, facilities, and hall layouts
- 🎫 **Ticket Booking**: Select seats with real-time availability and pricing
- 👤 **User Dashboard**: Track bookings, past screenings, and account status
- 🔧 **Admin Panel**: Manage cinemas, movies, screenings, and cinema halls
- 🎨 **Modern UI**: Dark theme with smooth animations and responsive design

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/Comp9001_finalproject.git
cd Comp9001_finalproject
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure database**

Edit `config.ini` with your database credentials:

```ini
[database]
host = localhost
port = 5432
dbname = cinema_db
user = your_username
password = your_password
```

4. **Initialize database**

Create the database and schema:

```bash
psql -U your_username -d cinema_db -f database/schema.sql
```

5. **Populate sample data**

Run the initialization script:

```bash
python init_database.py
```

6. **Start the application**

```bash
python app.py
```

7. **Access the application**

- Web Interface: http://localhost:5000
- Default demo credentials:
  - Admin: `admin` / `admin123`
  - User: `john_doe` / `customer123`

## Project Structure

```
Comp9001_finalproject/
├── app.py                      # Main Flask application
├── init_database.py           # Database initialization script
├── config.ini                 # Database configuration
├── requirements.txt           # Python dependencies
├── backend/                   # Backend business logic
│   ├── models/               # Database model classes
│   │   ├── user.py
│   │   ├── cinema.py
│   │   ├── movie.py
│   │   ├── screening.py
│   │   ├── cinema_hall.py
│   │   ├── seat.py
│   │   └── booking.py
│   └── services.py           # Business logic services
├── routes/                    # Flask route handlers
│   ├── main.py              # Main routes (index, bookings)
│   ├── auth.py              # Authentication routes
│   ├── cinemas.py           # Cinema routes
│   ├── movies.py            # Movie routes
│   ├── screenings.py        # Screening routes
│   ├── dashboard.py         # User dashboard routes
│   └── admin.py             # Admin panel routes
├── database/                # Database scripts
│   ├── schema.sql           # Database schema
│   └── db.py               # Database connection and queries
└── web/                     # Frontend
    ├── templates/           # HTML templates
    │   ├── admin/          # Admin panel templates
    │   └── errors/         # Error pages
    └── static/             # CSS and JavaScript
```

## Technical Stack

- **Backend**: Python 3.10+, Flask 2.3.3
- **Database**: PostgreSQL with psycopg 3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Architecture**: MVC pattern with service layer

## Key Features

### User Features

- Browse active movies with posters and details
- View cinema locations and facilities
- Select seats with real-time availability
- Track booking history and cancellation status
- Personal dashboard with statistics

### Admin Features

- Manage cinema activation/deactivation
- Add new cinemas and halls
- Manage movie library and activation
- Schedule screenings with filtering
- View all bookings and system statistics

## Database Schema

- **users**: User accounts and authentication
- **cinemas**: Cinema locations and facilities
- **movies**: Movie information and metadata
- **cinema_halls**: Hall configurations per cinema
- **seats**: Seat layout and pricing by seat type
- **screenings**: Movie showtimes and scheduling
- **bookings**: User ticket purchases
- **seat_bookings**: Junction table for booking-seat relationships

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Database Management

- **Schema**: See `database/schema.sql`
- **Sample Data**: Run `python init_database.py`
- **Connection**: Configure in `config.ini`

## License

This project is developed for educational purposes as part of COMP9001 coursework at the University of Sydney.

## Contact

**Author**: Zhou Li  
**Email**: your.email@example.com  
**Institution**: The University of Sydney
