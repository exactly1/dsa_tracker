-- SQL schema for DSA Planner

CREATE TABLE IF NOT EXISTS login (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    login_datetime TIMESTAMP,
    logout_datetime TIMESTAMP
);

CREATE TABLE IF NOT EXISTS plan_progress (
    id SERIAL PRIMARY KEY,
    "user" VARCHAR(50) NOT NULL,
    week VARCHAR(100),
    date DATE,
    day VARCHAR(20),
    task VARCHAR(255),
    problem VARCHAR(255),
    url TEXT,
    user_login_time TIMESTAMP,
    user_logout_time TIMESTAMP,
    time_taken_to_solve INTERVAL,
    passed_test_cases INT,
    solution_developed BOOLEAN,
    hints_used BOOLEAN
);
