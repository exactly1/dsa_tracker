import bcrypt
from db_utils import get_user, record_login, record_logout, create_user
import streamlit as st

# Password hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Streamlit login/logout logic

def login_form():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = get_user(username)
        if user and check_password(password, user['password_hash']):
            record_login(username)
            st.session_state['username'] = username
            st.success("Logged in!")
            return True
        else:
            st.error("Invalid credentials")
    return False

def logout_form():
    if st.button("Logout"):
        logout_user(st.session_state.get('username'))
        st.session_state.pop('username', None)
        st.success("Logged out!")

def register_form():
    st.subheader("Register")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    if st.button("Register"):
        if get_user(username):
            st.error("Username already exists")
        else:
            password_hash = hash_password(password)
            create_user(username, password_hash)
            st.success("User registered. Please login.")

def logout_user(username):
    record_logout(username)
