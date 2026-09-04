# ReservaFlow - CS50x Final Project
# AI assistance disclosure:
# ChatGPT was used as a programming tutor to help explain concepts,
# review code, suggest structure, and assist with debugging.

import os
from datetime import date as dt_date
from functools import wraps

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.environ.get("SECRET_KEY", "reservaflow-development-key")

Session(app)

db = SQL("sqlite:///project.db")


def login_required(f):
    """Require user to be logged in."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def index():
    """Show dashboard."""

    total = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM reservations
        WHERE user_id = ?
        """,
        session["user_id"]
    )[0]["count"]

    confirmed = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM reservations
        WHERE user_id = ? AND status = 'Confirmed'
        """,
        session["user_id"]
    )[0]["count"]

    pending = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM reservations
        WHERE user_id = ? AND status = 'Pending'
        """,
        session["user_id"]
    )[0]["count"]

    completed = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM reservations
        WHERE user_id = ? AND status = 'Completed'
        """,
        session["user_id"]
    )[0]["count"]

    cancelled = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM reservations
        WHERE user_id = ? AND status = 'Cancelled'
        """,
        session["user_id"]
    )[0]["count"]

    recent = db.execute(
        """
        SELECT client_name, service, date, time, status
        FROM reservations
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 5
        """,
        session["user_id"]
    )

    return render_template(
        "index.html",
        total=total,
        confirmed=confirmed,
        pending=pending,
        completed=completed,
        cancelled=cancelled,
        recent=recent
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        if not username:
            return render_template(
                "register.html",
                error="Please enter a username."
            )

        if not password:
            return render_template(
                "register.html",
                error="Please enter a password."
            )

        if password != confirmation:
            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        password_hash = generate_password_hash(password)

        try:
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                password_hash
            )
        except ValueError:
            return render_template(
                "register.html",
                error="Username already exists."
            )

        session["user_id"] = user_id
        session["username"] = username

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in an existing user."""

    session.clear()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username:
            return render_template(
                "login.html",
                error="Please enter your username."
            )

        if not password:
            return render_template(
                "login.html",
                error="Please enter your password."
            )

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"],
            password
        ):
            return render_template(
                "login.html",
                error="Invalid username or password."
            )

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log out current user."""

    session.clear()

    return redirect("/login")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_reservation():
    """Create a new reservation."""

    if request.method == "POST":
        client_name = request.form.get("client_name", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        date = request.form.get("date", "")
        time = request.form.get("time", "")
        status = request.form.get("status", "Pending")
        notes = request.form.get("notes", "").strip()

        if not client_name:
            return render_template(
                "add_reservation.html",
                error="Please enter the client's name."
            )

        if not service:
            return render_template(
                "add_reservation.html",
                error="Please select a service."
            )

        if not date:
            return render_template(
                "add_reservation.html",
                error="Please select a date."
            )

        try:
            reservation_date = dt_date.fromisoformat(date)
        except ValueError:
            return render_template(
                "add_reservation.html",
                error="Invalid reservation date."
            )

        if reservation_date < dt_date.today():
            return render_template(
                "add_reservation.html",
                error="Reservations cannot be created in the past."
            )

        if not time:
            return render_template(
                "add_reservation.html",
                error="Please select a time."
            )

        allowed_statuses = [
            "Pending",
            "Confirmed",
            "Completed",
            "Cancelled"
        ]

        if status not in allowed_statuses:
            status = "Pending"

        if status != "Cancelled":
            conflict = db.execute(
                """
                SELECT id
                FROM reservations
                WHERE user_id = ?
                  AND date = ?
                  AND time = ?
                  AND status != 'Cancelled'
                """,
                session["user_id"],
                date,
                time
            )

            if conflict:
                return render_template(
                    "add_reservation.html",
                    error="There is already a reservation at this date and time."
                )

        db.execute(
            """
            INSERT INTO reservations
            (user_id, client_name, phone, service, date, time, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            session["user_id"],
            client_name,
            phone,
            service,
            date,
            time,
            status,
            notes
        )

        return redirect("/reservations")

    return render_template("add_reservation.html")


@app.route("/reservations")
@login_required
def reservations():
    """Show and filter reservations for the current user."""

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()

    query = """
        SELECT id, client_name, phone, service, date, time, status, notes
        FROM reservations
        WHERE user_id = ?
    """

    values = [session["user_id"]]

    if search:
        query += """
            AND (
                client_name LIKE ?
                OR service LIKE ?
                OR phone LIKE ?
            )
        """
        term = f"%{search}%"
        values.extend([term, term, term])

    if status:
        query += " AND status = ?"
        values.append(status)

    query += " ORDER BY date ASC, time ASC"

    rows = db.execute(query, *values)

    return render_template(
        "reservations.html",
        reservations=rows,
        search=search,
        selected_status=status
    )


@app.route("/edit/<int:reservation_id>", methods=["GET", "POST"])
@login_required
def edit_reservation(reservation_id):
    """Edit an existing reservation."""

    rows = db.execute(
        """
        SELECT *
        FROM reservations
        WHERE id = ? AND user_id = ?
        """,
        reservation_id,
        session["user_id"]
    )

    if len(rows) != 1:
        return redirect("/reservations")

    reservation = rows[0]

    if request.method == "POST":
        client_name = request.form.get("client_name", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        date = request.form.get("date", "")
        time = request.form.get("time", "")
        status = request.form.get("status", "Pending")
        notes = request.form.get("notes", "").strip()

        if not client_name or not service or not date or not time:
            return render_template(
                "edit_reservation.html",
                reservation=reservation,
                error="Please complete all required fields."
            )

        allowed_statuses = [
            "Pending",
            "Confirmed",
            "Completed",
            "Cancelled"
        ]

        if status not in allowed_statuses:
            status = "Pending"

        if status != "Cancelled":
            conflict = db.execute(
                """
                SELECT id
                FROM reservations
                WHERE user_id = ?
                  AND date = ?
                  AND time = ?
                  AND status != 'Cancelled'
                  AND id != ?
                """,
                session["user_id"],
                date,
                time,
                reservation_id
            )

            if conflict:
                return render_template(
                    "edit_reservation.html",
                    reservation=reservation,
                    error="There is already another reservation at this date and time."
                )

        db.execute(
            """
            UPDATE reservations
            SET client_name = ?,
                phone = ?,
                service = ?,
                date = ?,
                time = ?,
                status = ?,
                notes = ?
            WHERE id = ? AND user_id = ?
            """,
            client_name,
            phone,
            service,
            date,
            time,
            status,
            notes,
            reservation_id,
            session["user_id"]
        )

        return redirect("/reservations")

    return render_template(
        "edit_reservation.html",
        reservation=reservation
    )


@app.route("/delete/<int:reservation_id>", methods=["POST"])
@login_required
def delete_reservation(reservation_id):
    """Delete a reservation."""

    db.execute(
        """
        DELETE FROM reservations
        WHERE id = ? AND user_id = ?
        """,
        reservation_id,
        session["user_id"]
    )

    return redirect("/reservations")
