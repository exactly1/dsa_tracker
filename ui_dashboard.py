import streamlit as st
import plotly.express as px
import pandas as pd
from db_utils import get_tasks_for_date, update_task, get_weekly_stats
from datetime import datetime

def show_dashboard(username):
    st.header(f"Welcome, {username}")
    today = datetime.today().date()
    date = st.date_input("Select date", value=today)
    # Dynamic week dates starting from selected date
    week_dates = [date + pd.Timedelta(days=i) for i in range(7)]

    # Main panel: select date and show tasks for that date
    tasks = get_tasks_for_date(username, date)
    if not tasks:
        st.info("No tasks for selected date.")
    else:
        for task in tasks:
            st.subheader(task[6])  # problem
            st.write(f"URL: {task[7]}")
            with st.form(key=f"form_{task[0]}"):
                time_taken = st.text_input("Time Taken (e.g. 00:30:00)", value=str(task[10]) if task[10] else "")
                passed_cases = st.number_input("Passed Test Cases", value=task[11] or 0)
                solution_developed = st.checkbox("Solution Developed", value=task[12])
                hints_used = st.checkbox("Hints Used", value=task[13])
                submitted = st.form_submit_button("Submit Update")
                if submitted:
                    update_task(task[0], time_taken, passed_cases, solution_developed, hints_used)
                    st.success("Task updated!")

    # Sidebar panel: calendar and week tasks
    with st.sidebar:
        st.markdown("## 📅 Calendar & Week's Tasks")
        for d in week_dates:
            day_tasks = get_tasks_for_date(username, d)
            st.markdown(f"**{d.strftime('%A, %Y-%m-%d')}**")
            if day_tasks:
                for t in day_tasks:
                    st.write(f"- {t[6]} [{t[7]}]")
            else:
                st.write("_No tasks_")

    stats = get_weekly_stats(username)
    if stats:
        fig = px.bar(stats, x='week', y='percent_completed', title='% Completed per Week')
        st.plotly_chart(fig)
