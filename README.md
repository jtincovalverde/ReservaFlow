# ReservaFlow

A full-stack reservation management web application built as my **CS50x Final Project**.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/docs/Web/JavaScript)
[![Python CI](https://github.com/jtincovalverde/ReservaFlow/actions/workflows/ci.yml/badge.svg)](https://github.com/jtincovalverde/ReservaFlow/actions/workflows/ci.yml)
[![CS50x](https://img.shields.io/badge/CS50x-Completed-A51C30)](https://cs50.harvard.edu/certificates/33971312-603f-44b5-ae8c-69c073080305)

**Video demo:** https://www.youtube.com/watch?v=mBzinlOeNAw  
**Verified CS50x certificate:** https://cs50.harvard.edu/certificates/33971312-603f-44b5-ae8c-69c073080305

## Preview

![ReservaFlow reservations interface](assets/reservations.png)

## Overview

ReservaFlow is a web application for managing reservations in a simple, structured workflow. It was designed around a common operational problem: bookings become difficult to control when they are spread across messages, notes, or spreadsheets.

The application combines authentication, reservation management, search, filtering, dashboard metrics, scheduling validation, and user-level data separation in a single Flask application.

## Architecture

![ReservaFlow architecture](assets/architecture.svg)

The browser sends requests to the Flask backend, which manages authentication, business rules, validation, reservation workflows, and persistence in SQLite.

## Main features

- User registration, login, and logout
- Secure password hashing
- Reservation creation, editing, and deletion
- Dashboard metrics for Total, Pending, Confirmed, Completed, and Cancelled reservations
- Recent reservations overview
- Search by client, phone number, or service
- Filter by reservation status
- Prevention of conflicting active reservations at the same date and time
- Validation that prevents reservations in the past
- User-level authorization so one account cannot edit another account's reservations
- Responsive Bootstrap interface with custom CSS
- Browser confirmation before destructive delete actions

## Reservation workflow

Each reservation stores:

- Client name
- Phone number
- Service
- Date
- Time
- Status
- Notes

The supported statuses are `Pending`, `Confirmed`, `Completed`, and `Cancelled`.

Cancelled bookings do not block their former time slot. When editing a reservation, the application excludes the current reservation from conflict detection so it does not conflict with itself.

Date validation is performed both in JavaScript and on the Python backend. This means the application does not depend only on browser-side validation.

## Database design

ReservaFlow uses SQLite with two main tables:

- `users` — account information and password hashes
- `reservations` — booking information linked to a `user_id`

Reservation queries are scoped to the authenticated user. The application also verifies `user_id` during edit and delete operations to prevent unauthorized access by URL manipulation.

## Tech stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Flask |
| Database | SQLite, CS50 SQL |
| Templates | HTML, Jinja |
| Frontend | Bootstrap, custom CSS, JavaScript |
| Authentication | Flask Session, Werkzeug password hashing |
| Configuration | Environment variables / python-dotenv |
| Automation | GitHub Actions CI |

## Run locally

1. Clone or download the repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create the SQLite database:

```bash
sqlite3 project.db < schema.sql
```

4. Optional but recommended: copy `.env.example` to `.env` and replace the example secret with your own secure value.
5. Start the app:

```bash
flask run
```

6. Open the local Flask URL and register a new account.

The local database, sessions, environment file, and Python cache files are intentionally excluded from version control.

## Project structure

```text
ReservaFlow/
├── .github/
│   └── workflows/
│       └── ci.yml
├── assets/
│   ├── architecture.svg
│   └── reservations.png
├── static/
│   ├── app.js
│   └── styles.css
├── templates/
│   ├── add_reservation.html
│   ├── edit_reservation.html
│   ├── index.html
│   ├── layout.html
│   ├── login.html
│   ├── register.html
│   └── reservations.html
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── schema.sql
```

## Design decisions

I kept reservation status in the same table rather than splitting bookings into separate tables by state. This makes status transitions simpler and avoids unnecessary duplication.

I also chose to prevent active reservations from sharing the same date and time. That rule goes beyond basic CRUD behavior and makes the application closer to a real booking workflow.

SQLite was appropriate for the scope of the project because it provides persistent relational storage without requiring a separate database server.

## CS50x

ReservaFlow was submitted as my final project for **CS50x: Introduction to Computer Science** in 2026.

- [Verify CS50x certificate](https://cs50.harvard.edu/certificates/33971312-603f-44b5-ae8c-69c073080305)
- [Watch project video](https://www.youtube.com/watch?v=mBzinlOeNAw)

## AI assistance

ChatGPT was used during development as a programming assistant and tutor for explaining concepts, reviewing code, discussing project structure, and debugging. AI assistance is disclosed here and in the source code.

## Possible improvements

Future versions could add a calendar view, configurable working hours, different reservation durations, customer profiles, staff accounts, notifications, exports, analytics, and deployment to a production environment.
