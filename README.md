# ReservaFlow

#### Video Demo: https://www.youtube.com/watch?v=mBzinlOeNAw

#### Description:

ReservaFlow is a web application that I created to manage reservations in a simple and organized way.

I chose this idea because reservation management is a real problem that can quickly become disorganized when information is handled through messages, notes, or spreadsheets. My goal was to build something that could be useful for a small business or an independent professional while also allowing me to apply several of the concepts I learned during CS50x.

The project was built with Python and Flask on the backend, SQLite for the database, HTML and Jinja for the templates, Bootstrap and CSS for the interface, and JavaScript for some client-side behavior.

## How ReservaFlow works

A user first creates an account and then logs into the application. Passwords are not stored as plain text. They are hashed before being saved in the database and checked securely when the user logs in.

Once logged in, the user reaches the Dashboard.

The Dashboard gives a quick overview of the current reservations. I decided to show five indicators:

- Total
- Pending
- Confirmed
- Completed
- Cancelled

These numbers are not fixed values. They are calculated from the database every time the dashboard loads.

I also added a Recent Reservations section that shows the latest reservations created by the logged-in user. This makes the dashboard useful without having to open the complete reservation list every time.

## Reservations

The main part of the project is the reservation system.

A reservation contains:

- Client name
- Phone number
- Service
- Date
- Time
- Status
- Notes

The phone number and notes are optional, while the other important fields are required.

The available statuses are Pending, Confirmed, Completed, and Cancelled.

After creating a reservation, it appears on the Reservations page. From there, the user can edit or delete it.

When editing a reservation, the existing information is loaded automatically into the form. This allows the user to change things such as the time, service, client information, or reservation status.

For deletion, I added a browser confirmation before the reservation is removed. I did this because deleting information is a more destructive action than editing it, and I wanted to reduce accidental deletions.

## Preventing scheduling problems

One of the features I considered important was preventing duplicate reservations.

Before creating a new reservation, ReservaFlow checks whether another active reservation already exists for the same date and time. If it does, the new reservation is rejected and an error message is shown.

Cancelled reservations do not block the time slot because I considered that once a reservation has been cancelled, that time should become available again.

I also implemented this validation when editing reservations. In that case, the system ignores the reservation that is currently being edited so that it does not detect itself as a scheduling conflict.

Another validation prevents reservations from being created in the past.

JavaScript sets the minimum selectable date in the reservation form to the current date. I also added the same validation in Python because browser-side validation alone is not enough. A request could still be modified manually, so the backend should verify the date too.

## Search and filters

As the number of reservations grows, looking through the complete table becomes less convenient.

For that reason, I added a search function that can find reservations using the client name, phone number, or service.

I also added a status filter. This allows the user to show only Pending, Confirmed, Completed, or Cancelled reservations.

The Clear button removes the current filters and returns to the full list.

## Database design

ReservaFlow uses SQLite and currently has two main tables: `users` and `reservations`.

The `users` table stores account information.

The `reservations` table stores the booking information and also contains a `user_id`.

I decided to connect each reservation to a user instead of having one shared list. Because of this, when a user logs in, the application only retrieves reservations belonging to that account.

The application also checks the `user_id` when editing or deleting a reservation. This prevents one user from changing another user's reservations simply by modifying a URL.

## Running locally

1. Install the Python dependencies with `pip install -r requirements.txt`.
2. Create the SQLite database with `sqlite3 project.db < schema.sql`.
3. Start the application with `flask run`.
4. Open the local Flask URL in your browser and register a new account.

The database file is intentionally excluded from the public repository. `schema.sql` contains the structure required to recreate it, while `.gitignore` prevents local database, session, environment, and cache files from being committed.

## Project files

`app.py` contains the Flask application and most of the backend logic. It includes authentication, database queries, dashboard calculations, reservation creation, editing, deletion, searching, filtering, validation, and conflict detection.

`project.db` is the local SQLite database used to store users and reservations. It is generated locally and is not committed to the public repository.

`templates/layout.html` contains the general page structure and navigation bar shared by the rest of the application.

`templates/index.html` contains the Dashboard.

`templates/login.html` and `templates/register.html` contain the authentication forms.

`templates/reservations.html` displays the reservation table, search controls, filters, and available actions.

`templates/add_reservation.html` contains the form used to create a reservation.

`templates/edit_reservation.html` contains the form used to modify an existing reservation.

`static/styles.css` contains my custom styles in addition to Bootstrap. I used it for the cards, spacing, shadows, authentication pages, dashboard indicators, and hover effects.

`static/app.js` contains the JavaScript used to control the minimum date that can be selected when creating a reservation.

`requirements.txt` contains the Python dependencies required to run the application.

`schema.sql` defines the `users` and `reservations` tables and the indexes used by the application.

`.gitignore` keeps local database, session, environment, virtual-environment, and cache files out of version control.

## Design decisions

At first, a reservation system can look like a simple CRUD application, but while developing it I noticed that several decisions were necessary for it to behave more like a real booking system.

For example, I chose to store the reservation status in the same table instead of creating separate tables for pending or completed reservations. This makes changing a reservation from one state to another much simpler.

I also decided not to let active reservations share the same time slot. This was not necessary just to store information in a database, but it made more sense for the actual problem the application is trying to solve.

SQLite was enough for the scope of this project because the application is relatively small and does not require an external database server.

For the interface, I used Bootstrap as a base but added my own CSS because I did not want the entire application to look like the default Bootstrap components.

## AI Assistance

I used ChatGPT during the development of ReservaFlow as a programming assistant and tutor. It helped me review code, understand errors, discuss possible project structures, and debug problems while I developed and tested the application.

The use of AI is also disclosed in the source code as required for the CS50x Final Project.

## Possible improvements

ReservaFlow could be expanded in several ways in the future.

Some features I would consider adding are staff accounts, different reservation durations, configurable working hours, a calendar view, customer profiles, email reminders, exporting information, and more detailed reports.

For the scope of my CS50x Final Project, I focused on creating a complete working reservation workflow instead of adding many features that I would not have enough time to implement and test properly.
