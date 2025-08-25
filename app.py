import streamlit as st
from auth import login_form, logout_form, register_form
from data_processing import process_excel
from ui_dashboard import show_dashboard
from db_utils import get_user
from datetime import datetime

def main():
    st.set_page_config(page_title="DSA Progress Tracker", layout="wide")
    if 'username' not in st.session_state:
        st.sidebar.title("Authentication")
        auth_choice = st.sidebar.radio("Select action", ["Login", "Register"])
        if auth_choice == "Register":
            register_form()
        elif auth_choice == "Login":
            logged_in = login_form()
            if not logged_in:
                st.stop()
    else:
        logout_form()
        username = st.session_state['username']
        st.subheader("Upload your Excel plan")
        uploaded_file = st.file_uploader("Choose Excel file", type=["xlsx"])
        if uploaded_file and not st.session_state.get("excel_processed"):
            process_excel(uploaded_file, username, datetime.now(), None)
            st.session_state["excel_processed"] = True
        show_dashboard(username)

if __name__ == "__main__":
    main()
