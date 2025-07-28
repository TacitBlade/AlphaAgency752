# Alpha Agency 752

A Streamlit-based user registration application for Alpha Agency 752.

## Features

- User registration with form validation
- Secure password hashing using SHA-256
- Email format validation
- Username format validation (3-30 chars, alphanumeric + underscore)
- Strong password requirements (8+ chars, uppercase, lowercase, number)
- SQLite database for user storage
- Professional styling with custom CSS

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Database

The application automatically creates a SQLite database (`users.db`) to store user registrations with the following schema:

- `id` - Auto-incrementing primary key
- `username` - Unique username
- `email` - Unique email address
- `password` - Hashed password
- `first_name` - User's first name
- `last_name` - User's last name
- `created_at` - Registration timestamp

## Security Features

- Passwords are hashed using SHA-256 before storage
- SQL injection protection through parameterized queries
- Input validation and sanitization
- Maximum character limits on form fields

## License

See LICENSE file for details.