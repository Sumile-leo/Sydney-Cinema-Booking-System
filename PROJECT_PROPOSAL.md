# COMP9001 Final Project Proposal
# Ticket Booking System (购票系统)

## Project Overview

### Project Name
**Ticket Booking System (购票系统)**

### Course Information
- **University**: University of Sydney (USYD)
- **Course Code**: COMP9001
- **Project Type**: Final Project
- **Submission Deadline**: November 2, 2025
- **Student**: Zhou Li

### Project Description
A comprehensive ticket booking and management system that provides both desktop GUI and web interface for purchasing event tickets. The system allows users to browse events, select seats, purchase tickets, and manage their orders through an intuitive interface.

## Motivation

### Why This Project?
1. **Real-world Application**: Ticket booking systems are widely used in entertainment, sports, and event industries
2. **Technical Diversity**: Combines desktop GUI development, web development, and database management
3. **User Experience Focus**: Emphasizes modern UI/UX design principles
4. **Scalability**: Can be extended for different types of events and venues

### Learning Objectives
- Master Python GUI development with PyQt5
- Learn web development with Flask framework
- Understand database design and management
- Implement user authentication and session management
- Practice software engineering principles

## Technical Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Desktop GUI   │    │   Web Frontend  │    │   Mobile App    │
│   (PyQt5)       │    │   (HTML/CSS/JS) │    │   (Future)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Flask API     │
                    │   (Backend)     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   MySQL DB      │
                    │   (Database)    │
                    └─────────────────┘
```

### Technology Stack
- **Frontend**: PyQt5 (Desktop), HTML5/CSS3/JavaScript (Web)
- **Backend**: Flask (Python web framework)
- **Database**: MySQL
- **Authentication**: Session-based authentication
- **API**: RESTful API design

## Core Features

### 1. User Management
- **User Registration**: Create new user accounts
- **User Login/Logout**: Secure authentication system
- **Profile Management**: Update user information
- **Password Reset**: Email-based password recovery

### 2. Event Management
- **Event Listing**: Browse available events/shows
- **Event Details**: View event information, venue, timing
- **Event Search**: Filter events by category, date, location
- **Event Categories**: Concerts, sports, theater, movies, etc.

### 3. Booking System
- **Seat Selection**: Interactive seat map with availability
- **Ticket Types**: Different pricing tiers (VIP, Standard, Economy)
- **Shopping Cart**: Add multiple tickets before checkout
- **Payment Processing**: Secure payment integration
- **Booking Confirmation**: Email/SMS confirmation

### 4. Order Management
- **Order History**: View past and current bookings
- **Ticket Details**: Download/view digital tickets
- **Order Modification**: Cancel or modify bookings (within policy)
- **Refund Processing**: Handle cancellation requests

### 5. Admin Panel
- **Event Management**: Create, update, delete events
- **User Management**: View user accounts and activity
- **Order Statistics**: Sales reports and analytics
- **Venue Management**: Manage seating arrangements

## Database Design

### Core Tables

#### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### Events Table
```sql
CREATE TABLE events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    venue VARCHAR(100) NOT NULL,
    event_date DATETIME NOT NULL,
    ticket_price DECIMAL(10,2) NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### Orders Table
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    seat_numbers VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    order_status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'refunded') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);
```

#### Seats Table
```sql
CREATE TABLE seats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    seat_type ENUM('VIP', 'Standard', 'Economy') DEFAULT 'Standard',
    price DECIMAL(10,2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (event_id) REFERENCES events(id),
    UNIQUE KEY unique_seat (event_id, seat_number)
);
```

## Implementation Plan

### Phase 1: Backend Development (Week 1)
**Duration**: October 10-16, 2025

#### Database Setup
- [ ] Design and create database schema
- [ ] Set up MySQL database
- [ ] Create database connection module
- [ ] Implement database initialization scripts

#### Flask API Development
- [ ] Set up Flask application structure
- [ ] Implement user authentication endpoints
- [ ] Create event management API
- [ ] Develop booking system API
- [ ] Add order management endpoints

#### Core Backend Features
- [ ] User registration and login
- [ ] Password hashing and security
- [ ] Session management
- [ ] Input validation and error handling
- [ ] API documentation

### Phase 2: Desktop Application (Week 2)
**Duration**: October 17-23, 2025

#### PyQt5 GUI Development
- [ ] Design main application window
- [ ] Create login/registration dialogs
- [ ] Implement event browsing interface
- [ ] Develop seat selection interface
- [ ] Build booking confirmation dialog

#### Desktop Features
- [ ] User authentication integration
- [ ] Event listing and search
- [ ] Interactive seat map
- [ ] Shopping cart functionality
- [ ] Order history viewer
- [ ] Admin panel interface

#### UI/UX Design
- [ ] Modern and intuitive interface
- [ ] Responsive design elements
- [ ] Custom styling and themes
- [ ] Error handling and user feedback
- [ ] Accessibility features

### Phase 3: Web Frontend & Integration (Week 3)
**Duration**: October 24 - November 2, 2025

#### Web Interface Development
- [ ] Create responsive HTML templates
- [ ] Implement CSS styling
- [ ] Add JavaScript functionality
- [ ] Develop user authentication pages
- [ ] Build event browsing interface

#### Frontend-Backend Integration
- [ ] Connect web frontend to Flask API
- [ ] Implement AJAX for dynamic content
- [ ] Add real-time seat availability
- [ ] Integrate payment processing
- [ ] Handle session management

#### Testing and Polish
- [ ] Unit testing for backend
- [ ] Integration testing
- [ ] User acceptance testing
- [ ] Performance optimization
- [ ] Bug fixes and refinements

## Challenges and Solutions

### Technical Challenges

#### 1. Database Concurrency
**Challenge**: Handling simultaneous seat bookings
**Solution**: Implement database transactions and locking mechanisms

#### 2. Real-time Updates
**Challenge**: Keeping seat availability current
**Solution**: Use WebSocket or polling for real-time updates

#### 3. Payment Integration
**Challenge**: Secure payment processing
**Solution**: Integrate with established payment gateways (Stripe, PayPal)

#### 4. Scalability
**Challenge**: Handling high traffic during popular events
**Solution**: Implement caching and database optimization

### Design Challenges

#### 1. User Experience
**Challenge**: Creating intuitive interfaces for both desktop and web
**Solution**: Follow modern UI/UX principles and conduct user testing

#### 2. Cross-platform Compatibility
**Challenge**: Ensuring consistent experience across platforms
**Solution**: Use responsive design and cross-platform testing

## Success Criteria

### Functional Requirements
- [ ] Users can register and login successfully
- [ ] Events can be browsed and searched
- [ ] Seats can be selected and booked
- [ ] Orders can be processed and confirmed
- [ ] Admin can manage events and users
- [ ] System handles concurrent bookings correctly

### Technical Requirements
- [ ] Application runs without crashes
- [ ] Database operations are efficient
- [ ] API responses are fast (< 2 seconds)
- [ ] Code is well-documented and maintainable
- [ ] Security best practices are followed

### User Experience Requirements
- [ ] Interface is intuitive and easy to use
- [ ] Loading times are acceptable
- [ ] Error messages are clear and helpful
- [ ] Application works on different screen sizes

## Testing Strategy

### Unit Testing
- Test individual functions and methods
- Verify database operations
- Test API endpoints
- Validate input handling

### Integration Testing
- Test desktop-backend integration
- Test web-backend integration
- Verify database connections
- Test payment processing

### User Acceptance Testing
- Test complete user workflows
- Verify all features work as expected
- Test error scenarios
- Validate user experience

### Performance Testing
- Test with multiple concurrent users
- Verify database performance
- Test API response times
- Validate memory usage

## Resources and Tools

### Development Tools
- **IDE**: Visual Studio Code / PyCharm
- **Version Control**: Git / GitHub
- **Database**: MySQL Workbench
- **GUI Design**: Qt Designer
- **API Testing**: Postman

### Learning Resources
- PyQt5 Documentation
- Flask Documentation
- MySQL Documentation
- Python Best Practices
- UI/UX Design Principles

### External Services
- **Payment Gateway**: Stripe / PayPal (for future integration)
- **Email Service**: SMTP / SendGrid (for notifications)
- **Cloud Hosting**: AWS / Heroku (for deployment)

## Risk Assessment

### Technical Risks
- **Database Performance**: Risk of slow queries with large datasets
  - *Mitigation*: Implement proper indexing and query optimization
- **Security Vulnerabilities**: Risk of data breaches or unauthorized access
  - *Mitigation*: Follow security best practices and regular security audits
- **Integration Issues**: Risk of problems connecting different components
  - *Mitigation*: Thorough testing and gradual integration

### Timeline Risks
- **Feature Creep**: Risk of adding too many features
  - *Mitigation*: Stick to core requirements and MVP approach
- **Technical Difficulties**: Risk of encountering complex problems
  - *Mitigation*: Start with simpler implementations and iterate
- **Testing Time**: Risk of insufficient testing time
  - *Mitigation*: Test continuously throughout development

### Resource Risks
- **Learning Curve**: Risk of spending too much time learning new technologies
  - *Mitigation*: Use familiar technologies where possible
- **External Dependencies**: Risk of third-party service failures
  - *Mitigation*: Have backup plans and fallback options

## Conclusion

The Ticket Booking System project represents a comprehensive application that demonstrates proficiency in multiple areas of software development. By combining desktop GUI development, web development, and database management, this project showcases the versatility of Python and modern web technologies.

The project's real-world applicability makes it an excellent choice for demonstrating practical software engineering skills. The modular architecture allows for future extensions and improvements, making it a valuable learning experience and portfolio piece.

With careful planning, systematic development, and thorough testing, this project will successfully meet all requirements and provide a solid foundation for understanding full-stack application development.

---

**Project Timeline**: October 10 - November 2, 2025 (3 weeks)
**Total Estimated Hours**: 60-80 hours
**Complexity Level**: Intermediate to Advanced