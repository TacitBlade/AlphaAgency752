import streamlit as st
import sqlite3
import re
import hashlib
from datetime import datetime

# Initialize SQLite database
def init_db():
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
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Validate email format
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

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
        background-color: #1e3a8a;
        color: white;
        width: 100%;
        padding: 10px;
        font-size: 1.2em;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #3b82f6;
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
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit_button = st.form_submit_button("Register")

    if submit_button:
        if not all([first_name, last_name, username, email, password, confirm_password]):
            st.error("All fields are required.")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            try:
                c.execute(
                    "INSERT INTO users (username, email, password, first_name, last_name, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, email, hash_password(password), first_name, last_name, datetime.now())
                )
                conn.commit()
                st.success("Registration successful! Welcome aboard!")
            except sqlite3.IntegrityError:
                st.error("Username or email already exists.")
            finally:
                conn.close()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">© 2025 Alpha Agency 752. All rights reserved.</div>', unsafe_allow_html=True)