# Beginner Level 📚

Welcome to the beginner section of the TCB Trading Card Brain Academy! This section is designed for developers who are new to web development, Python, or programming in general.

## What You'll Learn

This section covers the fundamental technologies and concepts used in this project:

### Core Technologies

#### Python Basics
- **What it is**: Python is a high-level, interpreted programming language known for its simplicity and readability
- **Why we use it**: Python's clear syntax makes it perfect for rapid web application development
- **In this project**: All backend logic, API endpoints, and business rules are written in Python
- **Resources to add**:
  - Python syntax and data structures
  - Functions and modules
  - Object-oriented programming basics
  - Working with files and data

#### Flask Framework
- **What it is**: Flask is a lightweight web framework for Python
- **Why we use it**: Flask is simple to learn, flexible, and perfect for building web applications without unnecessary complexity
- **In this project**: Flask handles routing, HTTP requests/responses, and serves our web pages
- **Key files**: `app.py` (main application file)
- **Resources to add**:
  - Flask routing and views
  - Templates with Jinja2
  - Handling forms and user input
  - Working with static files (CSS, JavaScript)

#### HTML, CSS, and JavaScript
- **What they are**: The three core technologies for building web pages
  - HTML: Structure and content
  - CSS: Styling and layout
  - JavaScript: Interactivity and dynamic behavior
- **Why we use them**: Every web application needs these to create the user interface
- **In this project**: Templates (`templates/` directory) and static files (`static/` directory)
- **Resources to add**:
  - HTML structure and common elements
  - CSS selectors and styling
  - JavaScript basics and DOM manipulation
  - Making API calls with fetch

#### Databases with SQLite
- **What it is**: SQLite is a lightweight, file-based database
- **Why we use it**: Perfect for development and small to medium applications without requiring a separate database server
- **In this project**: Stores user accounts, decks, and card collections
- **Resources to add**:
  - What is a database and why do we need one?
  - Tables, rows, and columns
  - Basic SQL queries (SELECT, INSERT, UPDATE, DELETE)
  - Understanding relationships between tables

### Development Tools

#### Git and GitHub
- **What it is**: Git is a version control system; GitHub is a platform for hosting Git repositories
- **Why we use it**: Track changes to code, collaborate with others, and maintain project history
- **Resources to add**:
  - Basic Git commands (clone, commit, push, pull)
  - Understanding branches
  - Reading commit history
  - Creating pull requests

#### Command Line / Terminal
- **What it is**: A text-based interface for interacting with your computer
- **Why we use it**: Many development tools and commands are run from the terminal
- **Resources to add**:
  - Navigating directories (cd, ls, pwd)
  - Running Python scripts
  - Installing packages with pip
  - Understanding file paths

#### Virtual Environments
- **What it is**: Isolated Python environments for projects
- **Why we use it**: Keeps project dependencies separate and avoids conflicts
- **Resources to add**:
  - Creating a virtual environment
  - Activating/deactivating
  - Installing packages with pip
  - Understanding requirements.txt

## Suggested Learning Path

1. **Start with Python basics**: If you're new to programming, learn Python fundamentals first
2. **Understand HTML/CSS**: Learn how web pages are structured and styled
3. **Learn Flask basics**: Understand how Flask serves web pages and handles requests
4. **Explore the code**: Open `app.py` and follow along with simple routes
5. **Try making changes**: Modify HTML templates or add a simple route
6. **Learn about databases**: Understand how data is stored and retrieved

## Hands-On Exercises

### Exercise Ideas (To be added)
- Create a simple "Hello World" Flask application
- Modify an existing HTML template to change the page appearance
- Add a new route that displays static information
- Create a simple database query to fetch cards
- Use Git to commit your changes

## Project-Specific Concepts

### What is a Trading Card Game (TCG)?
Trading Card Games like One Piece TCG are games where players use decks of cards to compete. Each card has attributes like power, cost, and special effects. This application helps players build optimal decks.

### Application Flow
1. User visits the website (frontend)
2. Browser requests pages from Flask (backend)
3. Flask processes the request and queries the database if needed
4. Flask renders HTML templates with data
5. Browser displays the page to the user

## Common Terms

- **Frontend**: The part users see and interact with (HTML, CSS, JavaScript)
- **Backend**: The server-side logic (Python, Flask)
- **API**: Application Programming Interface - how frontend and backend communicate
- **Route**: A URL path that triggers specific code (e.g., `/onepiece`)
- **Template**: HTML file with placeholders for dynamic data
- **Database**: Organized storage for application data

## Next Steps

Once you're comfortable with these basics, move on to the [Medium](../medium/) section to learn about:
- More advanced Flask features
- API design
- Database relationships
- Authentication systems

## Contributing

Have suggestions for beginner-friendly content? Please contribute! Beginners helping beginners is incredibly valuable.

---

*Remember: Everyone starts as a beginner. Take your time, practice, and don't hesitate to ask questions!*
