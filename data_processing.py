import pandas as pd
from db_utils import insert_plan_progress
import streamlit as st
from datetime import datetime

def process_excel(file, username, user_login_time, user_logout_time):
    df = pd.read_excel(file)
    for _, row in df.iterrows():
        week = row.get('Week', None)
        date_str = row.get('Date', None)
        # Parse date string in 'yyyy-MM-dd' format to date object
        date_obj = None
        if pd.notnull(date_str):
            try:
                date_obj = pd.to_datetime(date_str, format='%Y-%m-%d').date()
            except Exception:
                date_obj = pd.to_datetime(date_str).date()
        day = pd.to_datetime(date_str).strftime('%A') if pd.notnull(date_str) else None
        task = row.get('Task', None)
        import ast
        problems_raw = row['Problem and URL(s)']
        try:
            problems_list = ast.literal_eval(problems_raw)
        except Exception:
            problems_list = [str(problems_raw)]
        import re
        for item in problems_list:
            # Extract first URL from string
            url_match = re.search(r'(https?://\S+)', item)
            url = url_match.group(1) if url_match else ''
            problem = item.replace(url, '').replace('-', '').strip() if url else item.strip()
            insert_plan_progress(
                user=username,
                week=week,
                date=date_obj,
                day=day,
                task=task,
                problem=url,
                url=problems_raw,
                user_login_time=user_login_time,
                user_logout_time=user_logout_time,
                time_taken_to_solve=None,
                passed_test_cases=None,
                solution_developed=False,
                hints_used=False
            )
    st.success("Excel processed and tasks added!")
