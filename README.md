# Fitness Tracker (Python + MySQL)

**What**: An intermediate-level Fitness Tracker REST API built with Flask and MySQL.

**Features**
- User registration/login (lightweight, no external auth)
- CRUD for workout logs and meal logs
- Daily summary endpoint (calories in vs calories out)
- Weight history tracking and simple progress report endpoint
- SQL schema + sample data
- Docker + docker-compose for quick local setup

**Requirements**
- Python 3.9+
- MySQL server (or MariaDB)
- `mysql-connector-python`

**Quick start (local)**
1. Create and activate a virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate       # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Create a MySQL database and user (example):
   ```sql
   CREATE DATABASE fitness_tracker;
   CREATE USER 'ft_user'@'localhost' IDENTIFIED BY 'ft_pass';
   GRANT ALL PRIVILEGES ON fitness_tracker.* TO 'ft_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
3. Initialize schema and sample data:
   ```bash
   mysql -u ft_user -p fitness_tracker < db_init.sql
   ```
4. Copy `.env.example` to `.env` and update credentials.
5. Run the app:
   ```bash
   export FLASK_APP=app.py
   flask run
   ```
   Or `python app.py`

**API endpoints (examples)**
- `POST /users` - create user
- `GET /users/<id>` - get user profile
- `POST /workouts` - add workout log
- `GET /workouts?user_id=&date=` - list workouts
- `POST /meals` - add meal log
- `GET /summary?user_id=&date=` - daily summary (calories in/out)

**Notes**
- This project uses explicit SQL via `mysql-connector-python` (no ORM) to keep it instructional.
- Tests and docker setup included.
