import psycopg2
import os
from datetime import datetime

def get_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT", 5432)
    )

def get_user(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username, password_hash FROM login WHERE username=%s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {'username': row[0], 'password_hash': row[1]}
    return None

def create_user(username, password_hash):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO login (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    conn.commit()
    cur.close()
    conn.close()

def record_login(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE login SET login_datetime=%s WHERE username=%s", (datetime.now(), username))
    conn.commit()
    cur.close()
    conn.close()

def record_logout(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE login SET logout_datetime=%s WHERE username=%s", (datetime.now(), username))
    conn.commit()
    cur.close()
    conn.close()

def insert_plan_progress(user, week, date, day, task, problem, url, user_login_time, user_logout_time, time_taken_to_solve, passed_test_cases, solution_developed, hints_used):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO plan_progress ("user", week, date, day, task, problem, url, user_login_time, user_logout_time, time_taken_to_solve, passed_test_cases, solution_developed, hints_used)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user, week, date, day, task, problem, url, user_login_time, user_logout_time, time_taken_to_solve, passed_test_cases, solution_developed, hints_used))
    conn.commit()
    cur.close()
    conn.close()

def get_tasks_for_date(user, date):
    conn = get_conn()
    cur = conn.cursor()
    # Debug: print all dates
    cur.execute("SELECT date FROM plan_progress")
    all_dates = cur.fetchall()
    # print(f"Dates in DB: {[str(d[0]) for d in all_dates]}", flush=True)
    query = "SELECT * FROM plan_progress WHERE date=%s"
    params = (date,)
    print(f"Actual query sent to DB: {query % params}", flush=True)
    print(f"Query: {query}")
    print(f"Parameters: {params}")
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def update_task(task_id, time_taken_to_solve, passed_test_cases, solution_developed, hints_used):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE plan_progress SET time_taken_to_solve=%s, passed_test_cases=%s, solution_developed=%s, hints_used=%s WHERE id=%s
    """, (time_taken_to_solve, passed_test_cases, solution_developed, hints_used, task_id))
    conn.commit()
    cur.close()
    conn.close()

def get_weekly_stats(user):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT week, COUNT(*) as total, SUM(CASE WHEN solution_developed THEN 1 ELSE 0 END) as completed
        FROM plan_progress WHERE user=%s GROUP BY week ORDER BY week
    """, (user,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    stats = []
    for week, total, completed in rows:
        percent_completed = 100 * completed / total if total else 0
        stats.append({'week': week, 'percent_completed': percent_completed, 'total': total, 'completed': completed})
    return stats
