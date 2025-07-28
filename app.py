import streamlit as st
import sqlite3
import re
import hashlib
from datetime import datetime

# Initialize SQLite database
def init_db() -> None:
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        first_name TEXT,
        last_name TEXT,
        created_at TIMESTAMP
    )''')
    conn.commit()
    conn.close()

# Hash password for security
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Validate email format
def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Validate password strength
def is_valid_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    return True, "Password is valid."

# Validate username
def is_valid_username(username: str) -> tuple[bool, str]:
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 20:
        return False, "Username must be no more than 20 characters long."
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, "Username is valid."

# Initialize database
init_db()

# Streamlit page configuration
st.set_page_config(
    page_title="Alpha Agency 752 - Welcome",
    page_icon="✨",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
    }
    .title {
        font-size: 3em;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 1.5em;
        color: #4b5563;
        text-align: center;
        margin-bottom: 30px;
    }
    .form-container {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        margin: 0 auto;
    }
    .stButton>button {
        background-color: #16a34a;
        color: white;
        width: 100%;
        padding: 10px;
        font-size: 1.2em;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #22c55e;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #6b7280;
    }
    </style>
""", unsafe_allow_html=True)

# Landing page content
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<h1 class="title">Welcome to Alpha Agency 752</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Join our community to unlock exclusive insights and services.</p>', unsafe_allow_html=True)

# Registration form
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.subheader("Register Now")
with st.form(key='registration_form'):
    first_name = st.text_input("First Name", max_chars=50, help="Enter your first name")
    last_name = st.text_input("Last Name", max_chars=50, help="Enter your last name")
    username = st.text_input("Username", max_chars=20, help="3-20 characters, letters, numbers, and underscores only")
    email = st.text_input("Email", help="Enter a valid email address")
    password = st.text_input("Password", type="password", help="Minimum 8 characters with uppercase, lowercase, and numbers")
    confirm_password = st.text_input("Confirm Password", type="password", help="Re-enter your password")
    submit_button = st.form_submit_button("Register")

    if submit_button:
        # Validate all fields are filled
        if not all([first_name, last_name, username, email, password, confirm_password]):
            st.error("All fields are required.")
        else:
            # Validate email format
            if not is_valid_email(email):
                st.error("Please enter a valid email address.")
            # Validate username
            elif not is_valid_username(username)[0]:
                st.error(is_valid_username(username)[1])
            # Validate password strength
            elif not is_valid_password(password)[0]:
                st.error(is_valid_password(password)[1])
            # Check password confirmation
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                # Attempt to register user
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                try:
                    c.execute(
                        "INSERT INTO users (username, email, password, first_name, last_name, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (username, email, hash_password(password), first_name, last_name, datetime.now())
                    )
                    conn.commit()
                    st.success("Registration successful! Welcome aboard!")
                except sqlite3.IntegrityError as e:
                    if "username" in str(e).lower():
                        st.error("Username already exists. Please choose a different username.")
                    elif "email" in str(e).lower():
                        st.error("Email already exists. Please use a different email address.")
                    else:
                        st.error("Registration failed. Please try again.")
                except Exception as e:
                    st.error(f"An error occurred during registration: {str(e)}")
                finally:
                    conn.close()
                    
st.markdown('<h3>Already Registered? Log In</h3>', unsafe_allow_html=True)
with st.form(key='login_form'):
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    login_button = st.form_submit_button("Log In")
    if login_button:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                 (login_username, hash_password(login_password)))
        user = c.fetchone()
        conn.close()
        if user:
            st.success(f"Welcome back, {user[4]} {user[5]}!")
        else:
            st.error("Invalid username or password.")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">© 2025 Alpha Agency 752. All rights reserved.</div>', unsafe_allow_html=True)