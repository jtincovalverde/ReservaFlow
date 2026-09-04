# ReservaFlow

A reservation management web application built as my **CS50x Final Project**.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/docs/Web/JavaScript)
[![CS50x](https://img.shields.io/badge/CS50x-Completed-A51C30)](https://cs50.harvard.edu/certificates/33971312-603f-44b5-ae8c-69c073080305)

**Video Demo:** https://www.youtube.com/watch?v=mBzinlOeNAw  
**CS50x Certificate:** https://cs50.harvard.edu/certificates/33971312-603f-44b5-ae8c-69c073080305

## Preview

![ReservaFlow reservations interface](assets/reservations.png)

## Overview

ReservaFlow is a web application that I created to manage reservations in a simple and organized way.

I chose this idea because reservation management is a real problem that can quickly become disorganized when information is handled through messages, notes, or spreadsheets. My goal was to build something that could be useful for a small business or an independent professional while also allowing me to apply several of the concepts I learned during CS50x.

The project was built with Python and Flask on the backend, SQLite for the database, HTML and Jinja for the templates, Bootstrap and CSS for the interface, and JavaScript for client-side behavior.

## Main features

- User registration, login, and logout
- Password hashing for account security
- Reservation creation, editing, and deletion
- Dashboard statistics by reservation status
- Search by client, phone number, or service
- Filter reservations by status
- Prevention of conflicting active reservations at the same date and time
- Validation to prevent reservations in the past
- User-level data separation so each account only accesses its own reservations
- Responsive interface built with Bootstrap and custom CSS

## How ReservaFlow works

A user first creates an account and then logs into the application. Passwords are not stored as plain text. They are hashed before being saved in the database and checked securely when the user logs in.

Once logged in, the user reaches the Dashboard.

The Dashboard gives a quick overview of the current reservations. It shows five indicators:

- Total
- Pending
- Confirmed
- Completed
- Cancelled

These numbers are calculated from the database every time the dashboard loads.

The dashboard also includes a Recent Reservations section so the user can quickly see the latest bookings without opening the complete reservation list.

## Reservations

A reservation contains:

- Client name
- Phone number
- Service
- Date
- Time
- Status
- Notes

The phone number and notes are optional, while the main booking fields are required.

The available statuses are Pending, Confirmed, Completed, and Cancelled.

After creating a reservation, it appears on the Reservations page. From there, the user can edit or delete it. When editing a reservation, the existing information is loaded automatically into the form.

For deletion, the interface asks for confirmation before the reservation is removed to reduce accidental deletions.

## Preventing scheduling problems

Before creating a new reservation, ReservaFlow checks whether another active reservation already exists for the same date and time. If it does, the new reservation is rejected and an error message is shown.

Cancelled reservations do not block the time slot because once a reservation has been cancelled, that time should become available again.

The same validation is applied when editing reservations. In that case, the system ignores the reservation currently being edited so it does not detect itself as a scheduling conflict.

Another validation prevents reservations from being created in the past. JavaScript sets the minimum selectable date in the form to the current date, and the backend performs the same validation in Python so the application does not rely only on browser-side checks.

## Search and filters

The Reservations page includes a search function that can find reservations using the client name, phone number, or service.

A status filter allows the user to display only Pending, Confirmed, Completed, or Cancelled reservations. The Clear button removes the current filters and returns to the complete list.

## Database design

ReservaFlow uses SQLite and has two main tables: `users` and `reservations`.

The `users` table stores account information. The `reservations` table stores booking information and contains a `user_id` that links each reservation to its owner.

The application checks the `user_id` when reading, editing, or deleting reservations. This prevents one user from accessing another user's bookings simply by modifying a URL.

## Running locally

1. Clone or download this repository.
2. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create the SQLite database:

   ```bash
   sqlite3 project.db < schema.sql
   ```

4. Optionally copy `.env.example` to `.env` and replace the example secret with your own secure value.
5. Start the application:

   ```bash
   flask run
   ```

6. Open the local Flask URL in your browser and register a new account.

The database file is intentionally excluded from this public repository. `schema.sql` contains the structure required to recreate it, while `.gitignore` prevents local database, session, environment, and cache files from being committed.

## Project structure

```text
ReservaFlow/
├── app.py
├── schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── assets/
│   └── reservations.png
├── static/
│   ├── app.js
│   └── styles.css
└── templates/
    ├── add_reservation.html
    ├── edit_reservation.html
    ├── index.html
    ├── layout.html
    ├── login.html
    ├── register.html
    └── reservations.html
```

`app.py` contains the Flask application and backend logic, including authentication, database queries, dashboard calculations, CRUD operations, search, filtering, validation, and conflict detection.

`schema.sql` defines the database tables and indexes.

`templates/` contains the Jinja/HTML views, while `static/` contains the custom CSS and JavaScript.

## Design decisions

At first, a reservation system can look like a simple CRUD application, but while developing it I noticed that several decisions were necessary for it to behave more like a real booking system.

For example, I chose to store reservation status in the same table instead of creating separate tables for pending or completed reservations. This makes changing a reservation from one state to another much simpler.

I also decided not to let active reservations share the same time slot. This was not necessary just to store information in a database, but it made more sense for the real problem the application is trying to solve.

SQLite was enough for the scope of this project because the application is relatively small and does not require an external database server.

For the interface, I used Bootstrap as a base and added custom CSS so the application would have its own visual identity instead of relying only on the default Bootstrap appearance.

## CS50x

ReservaFlow was submitted as my final project for **CS50x: Introduction to Computer Science**.

- Certificate: https://cs50.harvard.edu/certificates/33971312-603f-44b5-ae8c-69c073080305
- Video presentation: https://www.youtube.com/watch?v=mBzinlOeNAw

## AI Assistance

I used ChatGPT during the development of ReservaFlow as a programming assistant and tutor. It helped me review code, understand errors, discuss possible project structures, and debug problems while I developed and tested the application.

The use of AI is also disclosed in the source code as required for the CS50x Final Project.

## Possible improvements

ReservaFlow could be expanded in several ways in the future, including staff accounts, different reservation durations, configurable working hours, a calendar view, customer profiles, email reminders, exporting information, and more detailed reports.

For the scope of my CS50x Final Project, I focused on creating a complete working reservation workflow instead of adding many features that I would not have enough time to implement and test properly.
