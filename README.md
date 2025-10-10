# COMP9001 Final Project - Ticket Booking System

English Version | [中文版](./README_CN.md)

## Project Overview

This is the final project for COMP9001 course at the University of Sydney (USYD). The project is a **Ticket Booking System** with both desktop GUI and web interface, using MySQL database for data management.

## Course Information

- **University**: University of Sydney (USYD)
- **Course Code**: COMP9001
- **Project Type**: Final Project
- **Project Name**: Ticket Booking System

## Project Features

### Core Functions
- 🎫 **Ticket Management**: Browse and search events/shows
- 👤 **User System**: User registration, login, and profile management
- 🛒 **Booking System**: Select seats and purchase tickets
- 📋 **Order Management**: View order history and ticket details
- 🔐 **Admin Panel**: Event management and order statistics

### Technical Highlights
- 🖥️ **Desktop Application**: Built with PyQt5 (Modern and beautiful GUI)
- 🌐 **Web Application**: Flask-based lightweight web application
- 💾 **Database**: MySQL for data persistence
- 🎨 **Modern UI**: Professional and user-friendly interface design

## Project Structure

```
Comp9001_finalproject/
├── README.md              # Project documentation (English)
├── README_CN.md           # Project documentation (Chinese)
├── backend/               # Flask backend application
│   └── routes/           # API routes and blueprints
├── database/              # Database scripts and schema
├── desktop/               # Desktop GUI application (PyQt5)
└── web/                   # Web frontend
    ├── static/           # Static resources (CSS, JS)
    │   ├── css/         # Stylesheets
    │   └── js/          # JavaScript files
    └── templates/        # HTML templates
```

## Tech Stack

- **Programming Language**: Python 3.x
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
python desktop/main.py
```

#### Web Application
```bash
python backend/app.py
```
Then open your browser and visit: `http://localhost:5000`

## Development Guide

### Branch Management

- `main`: Main branch, stable production code
- `dev`: Development branch for daily development
- `feature/*`: Feature branches for new features
- `bugfix/*`: Bug fix branches

### Commit Convention

Follow the conventional commit format:

```
<type>: <subject>

<body>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation update
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Build/tool changes

### Coding Standards

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write docstrings for functions and classes

## Project Progress

- [x] Project initialization and repository setup
- [x] Project structure design
- [ ] Database schema design
- [ ] Backend API development
- [ ] Desktop GUI implementation
- [ ] Web frontend development
- [ ] Testing and debugging
- [ ] Documentation completion
- [ ] Final deployment

## Team Members

- [Your Name](GitHub link)

## Database Schema

The system uses the following main tables:

- **users**: User accounts and authentication
- **events**: Event/show information
- **orders**: Ticket orders and transactions
- **seats**: Seat availability and pricing

For detailed schema, see `database/schema.sql`

## API Documentation

(To be added as development progresses)

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=backend tests/
```

## Troubleshooting

### Common Issues

1. **Database connection error**: Check MySQL service status and credentials
2. **Module not found**: Ensure all dependencies are installed via `pip install -r requirements.txt`
3. **Port already in use**: Change the port number in configuration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is for academic purposes only and is part of the COMP9001 course requirements at the University of Sydney.

## Contact

- **GitHub Issues**: [Project Issues](https://github.com/Sumile-leo/Comp9001_finalproject/issues)
- **Email**: your.email@university.edu.au

## Acknowledgments

Special thanks to:
- COMP9001 course instructors and tutors
- University of Sydney for providing learning resources
- Open-source community for various tools and libraries

## Screenshots

(To be added upon completion)

---

**Academic Integrity Notice**: This project is submitted as original work for COMP9001. All code is written by the project team. Please maintain academic integrity and do not plagiarize.

**Last Updated**: October 10, 2025
