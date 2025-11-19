# Flask RESTful API with Constraints and Validations

## Description
This project demonstrates a simple RESTful API built with Flask and SQLAlchemy. 
It includes database constraints and Python-level validations to ensure data integrity.

## Features
- CRUD operations on a `User` resource
- Database constraints: unique email, non-null fields, age >= 0
- Validations: name length, email format, age check
- JSON-based API responses

## Setup Instructions
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
pip install -r requirements.txt

4. Run the Flask app:
export FLASK_APP=app.py        # Linux/macOS
export FLASK_ENV=development   # optional, enables debug mode
flask run



5. Test API routes using Postman, curl, or your browser.

## Folder Structure
- `app.py` – Flask routes and API logic
- `models.py` – Database models with constraints and validations
- `config.py` – Database configuration
- `tests/` – Placeholder for test scripts

