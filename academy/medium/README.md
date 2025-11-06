# Medium Level 🚀

Welcome to the intermediate section of the TCB Trading Card Brain Academy! This section is for developers who understand the basics and want to learn more advanced concepts used in real-world applications.

## What You'll Learn

This section covers intermediate concepts and patterns used throughout this project:

### Application Architecture

#### Flask Blueprints and Modular Design
- **What it is**: A way to organize Flask applications into reusable components
- **Why we use it**: Makes large applications more maintainable and organized
- **In this project**: The `src/api/routes/` directory contains organized blueprints
- **Key concepts**:
  - Separating concerns (routes, services, models)
  - Blueprint registration and URL prefixes
  - Organizing code by feature or domain
- **Resources to add**:
  - Creating and registering blueprints
  - Organizing routes by functionality
  - Inter-blueprint communication
  - Best practices for project structure

#### Service Layer Pattern
- **What it is**: Separating business logic from route handlers
- **Why we use it**: Makes code more testable, reusable, and maintainable
- **In this project**: The `src/services/` directory contains business logic
- **Key files**: `src/services/deck_service.py`, `src/services/auth_service.py`
- **Resources to add**:
  - Separating API routes from business logic
  - Creating service classes
  - Dependency injection basics
  - Testing services independently

### Database Design

#### SQLAlchemy ORM
- **What it is**: Object-Relational Mapping - work with databases using Python objects
- **Why we use it**: Write database code in Python instead of SQL, making it more maintainable
- **In this project**: Models in `src/models/` define database structure
- **Key concepts**:
  - Defining models and relationships
  - Querying with SQLAlchemy
  - Migrations and schema changes
  - Understanding the session lifecycle
- **Resources to add**:
  - Creating models and relationships (one-to-many, many-to-many)
  - Writing efficient queries
  - Understanding eager vs lazy loading
  - Transaction management

#### Database Relationships
- **What they are**: How tables connect to each other
- **In this project**: 
  - Users have many decks (one-to-many)
  - Users have many cards in collection (one-to-many)
  - Decks contain card references
- **Resources to add**:
  - One-to-many relationships
  - Many-to-many relationships
  - Foreign keys and referential integrity
  - Designing normalized databases

### RESTful API Design

#### REST Principles
- **What it is**: A standard way to design web APIs using HTTP methods
- **Why we use it**: Industry standard that makes APIs predictable and easy to use
- **In this project**: All `/api/` endpoints follow REST conventions
- **Key concepts**:
  - HTTP methods (GET, POST, PUT, DELETE)
  - Resource-oriented design
  - Status codes and error handling
  - JSON request/response format
- **Resources to add**:
  - Designing RESTful endpoints
  - Proper use of HTTP methods
  - Status codes (200, 201, 400, 404, 500)
  - Request validation and error responses

#### Authentication and Authorization
- **What it is**: Verifying who users are (authentication) and what they can do (authorization)
- **Why we use it**: Protect user data and restrict access to certain features
- **In this project**: Flask-Login handles session-based authentication
- **Key files**: `src/services/auth_service.py`, models with `UserMixin`
- **Resources to add**:
  - Session-based authentication
  - Password hashing with werkzeug
  - Login/logout flows
  - Protecting routes with `@login_required`
  - Current user context

### Frontend-Backend Integration

#### AJAX and Fetch API
- **What it is**: Making HTTP requests from JavaScript without page reloads
- **Why we use it**: Create smooth, app-like user experiences
- **In this project**: JavaScript in `static/` makes API calls to Flask backend
- **Resources to add**:
  - Making GET and POST requests with fetch
  - Handling JSON responses
  - Error handling in async code
  - Updating the DOM with response data

#### Form Handling and Validation
- **What it is**: Processing user input from forms
- **In this project**: Both server-side (Flask) and client-side (JavaScript) validation
- **Resources to add**:
  - Server-side validation
  - Client-side validation
  - CSRF protection
  - Form submission with AJAX

### Containerization

#### Docker Basics
- **What it is**: Packaging applications with all their dependencies
- **Why we use it**: Ensures the app runs the same way everywhere (dev, staging, production)
- **In this project**: `Dockerfile` and `docker-compose.yml`
- **Key concepts**:
  - Understanding images and containers
  - Writing Dockerfiles
  - Multi-stage builds for optimization
  - Docker Compose for multi-container apps
- **Resources to add**:
  - Creating Docker images
  - Running containers
  - Volume mounting for development
  - Container networking
  - Best practices for Python Docker images

### Configuration Management

#### Environment Variables
- **What they are**: External configuration values
- **Why we use them**: Keep secrets out of code and configure apps for different environments
- **In this project**: `src/config/config.py` manages configuration
- **Resources to add**:
  - Using environment variables
  - Configuration for different environments (dev, staging, prod)
  - Managing secrets securely
  - Default values and validation

### Testing

#### Unit and Integration Testing
- **What they are**: Automated tests to verify code works correctly
- **Why we use them**: Catch bugs early and enable confident refactoring
- **In this project**: `tests/` directory with unit and system tests
- **Resources to add**:
  - Writing unit tests for services
  - Testing Flask routes
  - Mocking dependencies
  - Test fixtures and setup
  - Running tests with pytest

## Suggested Learning Path

1. **Understand the architecture**: Explore the `src/` directory structure
2. **Study the service layer**: Look at how `deck_service.py` encapsulates business logic
3. **Examine database models**: See how SQLAlchemy models define relationships
4. **Trace API requests**: Follow a request from frontend JavaScript through routes to services
5. **Explore authentication**: Understand the login flow and session management
6. **Experiment with Docker**: Build and run the container locally

## Hands-On Exercises

### Exercise Ideas (To be added)
- Create a new API endpoint with proper REST design
- Add a new database model with relationships
- Implement a new service class for additional functionality
- Write unit tests for an existing service
- Add client-side form validation
- Create a new blueprint for a feature domain

## Real-World Patterns in This Project

### 1. Repository Pattern (Implicit)
The service layer acts as a repository, abstracting database access from the API layer.

### 2. Dependency Injection
Services receive dependencies (like database sessions) from calling code rather than creating them.

### 3. MVC-like Pattern
- **Models**: SQLAlchemy models in `src/models/`
- **Views**: Flask routes in `src/api/routes/` (though these are more like controllers)
- **Templates**: Jinja2 templates in `templates/`

### 4. Factory Pattern
The application factory pattern allows creating multiple app instances with different configurations.

## Common Challenges and Solutions

### Challenge: Understanding the Request Flow
**Solution**: Trace a single request from browser → route → service → database and back

### Challenge: Database Query Performance
**Solution**: Learn about eager loading, query optimization, and indexing

### Challenge: Managing State in JavaScript
**Solution**: Understand when to fetch fresh data vs. maintain client-side state

### Challenge: Debugging API Issues
**Solution**: Use browser DevTools Network tab, server logs, and Postman/curl for testing

## Architecture Decisions

To understand why certain architectural decisions were made, see:
- [Architecture Documentation](../../docs/architecture/ARCHITECTURE.md)
- [API Documentation](../../docs/api/CARD_DATABASE.md)

## Next Steps

Once you're comfortable with these intermediate concepts, move on to the [Advanced](../advanced/) section to learn about:
- Infrastructure as Code
- Cloud deployment strategies
- Advanced security patterns
- Performance optimization
- CI/CD pipelines

## Contributing

Have experience with these topics? Share your knowledge! Intermediate developers often provide the best explanations because they remember what it was like to learn these concepts.

---

*Intermediate skills are where you start building real-world applications. Keep practicing and experimenting!*
