# COMP9001 Final Project - Ticket Booking System

English Version | [中文版](./README_CN.md)

## Project Overview

This is the final project for COMP9001 course at the University of Sydney (USYD). The project is a **Ticket Booking System** with both desktop GUI and web interface, using MySQL database for data management.

## Course Information

- **University**: University of Sydney (USYD)
- **Course Code**: COMP9001
- **Project Type**: Final Project
- **Project Name**: Ticket Booking System (购票系统)
- **Submission Deadline**: November 2, 2025

## Project Features

### 🎫 Core Functions
- **Event Management**: Browse and search events/shows
- **User System**: Registration, login, and profile management
- **Booking System**: Select seats and purchase tickets
- **Order Management**: View order history and ticket details
- **Admin Panel**: Event management and order statistics

### Technical Highlights
- 🖥️ **Desktop Application**: Built with PyQt5 (Modern and beautiful GUI)
- 🌐 **Web Application**: Flask-based lightweight web application
- 💾 **Database**: MySQL for data persistence
- 🎨 **Modern UI**: Professional and user-friendly interface design

## Project Structure

```
Comp9001_finalproject/
├── README.md                  # Project documentation (English)
├── README_CN.md               # Project documentation (Chinese)
├── PROJECT_SUMMARY.md         # Brief project description
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
├── main.py                    # Application entry point
├── backend/                   # Flask backend application
│   ├── __init__.py
│   ├── app.py                 # Flask application
│   ├── models.py              # Database models
│   ├── routes/                # API routes
│   └── config.py             # Configuration
├── desktop/                   # Desktop GUI application (PyQt5)
│   ├── __init__.py
│   ├── main_window.py         # Main GUI window
│   ├── login_dialog.py        # Login dialog
│   ├── booking_window.py      # Booking interface
│   └── admin_panel.py         # Admin interface
├── database/                  # Database scripts and schema
│   ├── schema.sql             # Database schema
│   └── init_db.py             # Database initialization
├── web/                       # Web frontend
│   ├── static/                # Static resources (CSS, JS)
│   │   ├── css/               # Stylesheets
│   │   └── js/                # JavaScript files
│   └── templates/             # HTML templates
├── assets/                    # Game assets (optional)
│   ├── sounds/                # Sound effects
│   └── music/                 # Background music
├── docs/                      # Additional documentation
│   └── particle_demo.py       # Particle demo (reference)
└── tests/                     # Test code
```

## Tech Stack

- **Programming Language**: Python 3.8+
- **Web Framework**: Flask
- **Desktop GUI**: PyQt5
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Additional Libraries**: 
  - PyMySQL / mysql-connector-python (Database driver)
  - Flask-SQLAlchemy (ORM, optional)
  - PyQt5 Designer (GUI design tool)
  - Other Python libraries as needed

## Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sumile-leo/Comp9001_finalproject.git
   cd Comp9001_finalproject
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL database**
   - Start MySQL service
   - Create database and import schema
   - Update database configuration in config file

4. **Initialize the database**
   ```bash
   python database/init_db.py
   ```

### Running the Application

#### Desktop Application
```bash
python desktop/main_window.py
```

#### Web Application
```bash
python backend/app.py
```
Then open your browser and visit: `http://localhost:5000`

## Development Progress

- [x] Project initialization and repository setup
- [x] Project documentation and proposal
- [ ] Week 1: Database design and backend API
- [ ] Week 2: Desktop GUI implementation
- [ ] Week 3: Web frontend and integration

## Development Timeline

### Week 1 (Oct 10-16): Backend Development
- Database schema design
- Flask API development
- User authentication system
- Event and order management

### Week 2 (Oct 17-23): Desktop Application
- PyQt5 GUI design
- User interface implementation
- Booking system integration
- Admin panel development

### Week 3 (Oct 24 - Nov 2): Web Frontend & Polish
- Web interface development
- Frontend-backend integration
- Testing and debugging
- Documentation and presentation

## Database Schema

The system uses the following main tables:

- **users**: User accounts and authentication
- **events**: Event/show information
- **orders**: Ticket orders and transactions
- **seats**: Seat availability and pricing

For detailed schema, see `database/schema.sql`

## Learning Outcomes

This project demonstrates:

**Python Programming:**
- Object-oriented design (classes for users, events, orders)
- Data structures (managing collections of objects)
- Database operations (CRUD operations)
- Web development (Flask framework)

**GUI Development:**
- PyQt5 advanced features
- Custom UI components
- Event handling (user interactions)
- Desktop application architecture

**Database Management:**
- Relational database design
- SQL queries and operations
- Data relationships and constraints
- Database optimization

**Software Engineering:**
- Modular design
- Code organization
- API development
- Documentation

## Team Members

- Zhou Li - [GitHub](https://github.com/Sumile-leo)

## Acknowledgments

Special thanks to:
- COMP9001 course instructors and tutors
- University of Sydney for providing learning resources
- Flask and PyQt5 communities for documentation and support

## License

This project is for academic purposes only and is part of the COMP9001 course requirements at the University of Sydney.

## Contact

- **GitHub Repository**: [Comp9001_finalproject](https://github.com/Sumile-leo/Comp9001_finalproject)
- **GitHub Issues**: [Report Issues](https://github.com/Sumile-leo/Comp9001_finalproject/issues)
- **Email**: your.email@university.edu.au

---

**Academic Integrity Notice**: This project is submitted as original work for COMP9001. All code is written by the project author. Please maintain academic integrity.

**Last Updated**: October 10, 2025