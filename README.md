# Sydney Cinema Booking System

## Quick Start

### Configuration

First, edit the configuration file to match your environment:

```bash
# Edit config.ini
nano config.ini
```

Update the database settings if needed:
```ini
[database]
host = localhost
port = 5432
user = postgres
password = your_password
dbname = booking_system
```

### Start the Application

```bash
# Initialize database (first time only)
python3 database/init_db.py

# Start web server
python3 backend/app.py
```

## Access the Application

- **Web Interface**: http://localhost:5001
- **API Endpoints**: http://localhost:5001/api/

## Default Login Credentials

- **Admin**: `admin` / `admin123`
- **Staff**: `staff1` / `staff123`
- **Customer**: `john_doe` / `customer123`

## Features

- 🎬 Movie browsing and search
- 🎭 Cinema location management
- 🎫 Online ticket booking
- 👤 User registration and authentication
- 📊 Booking management
- 🎨 Dark theme UI with animations

## Technical Stack

- **Backend**: Python 3.x, Flask
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Models**: Object-Oriented Database Models

## Project Structure

```
Comp9001_finalproject/
├── main.py              # Main interface (START HERE!)
├── backend/             # Flask application and models
│   ├── app.py          # Main Flask application
│   └── models/         # Database model classes
├── database/            # Database scripts
│   ├── schema.sql      # Database schema
│   └── init_db.py      # Database initialization
└── web/                 # Frontend
    ├── templates/      # HTML templates
    └── static/         # CSS, JS, images
```

## Course Information

- **University**: University of Sydney (USYD)
- **Course**: COMP9001
- **Author**: Zhou Li
- **Project**: Final Project - Sydney Cinema Booking System