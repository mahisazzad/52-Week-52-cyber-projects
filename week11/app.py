import os
import sqlite3
from datetime import datetime
from flask import Flask, g, render_template_string, request, redirect, url_for, session, flash
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

# --- Config ---
DATABASE = os.environ.get("AUTH_DB_PATH", "auth.db")
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", os.urandom(32))
PEPPER = os.environ.get("AUTH_PEPPER", "")  # Optional app-level secret

ph = PasswordHasher(
    time_cost=3,
    memory_cost=64_000,  # ~64MB
    parallelism=2,
)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# --- DB helpers ---
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(_=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)
        db.commit()

# --- Security helpers ---
def hash_password(password: str) -> str:
    pwd = password if not PEPPER else f"{password}{PEPPER}"
    return ph.hash(pwd)

def verify_password(stored_hash: str, provided_password: str) -> bool:
    pwd = provided_password if not PEPPER else f"{provided_password}{PEPPER}"
    try:
        return ph.verify(stored_hash, pwd)
    except (VerifyMismatchError, InvalidHash):
        return False

FAILED_LOGINS = {}

def login_rate_limited(key: str, window=300, max_attempts=5) -> bool:
    from time import time
    now = time()
    bucket = FAILED_LOGINS.get(key, [])
    bucket = [ts for ts in bucket if now - ts <= window]
    FAILED_LOGINS[key] = bucket
    return len(bucket) >= max_attempts

def record_failed_login(key: str):
    from time import time
    FAILED_LOGINS.setdefault(key, []).append(time())

# --- Inline templates ---
TPL_BASE = """
<!doctype html>
<title>{{ title }}</title>
<style>
  body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; }
  form { max-width: 400px; display: grid; gap: 0.75rem; }
  input { padding: 0.5rem; font-size: 1rem; }
  .btn { padding: 0.5rem 0.75rem; }
  .nav { margin-bottom: 1rem; }
  .nav a { margin-right: 1rem; }
  .flash { background: #ffe8a1; padding: 0.5rem; margin-bottom: 1rem; }
</style>
<div class="nav">
  <a href="{{ url_for('index') }}">Home</a>
  {% if 'user_id' in session %}
    <a href="{{ url_for('logout') }}">Logout</a>
  {% else %}
    <a href="{{ url_for('register') }}">Register</a>
    <a href="{{ url_for('login') }}">Login</a>
  {% endif %}
</div>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    {% for m in messages %}
      <div class="flash">{{ m }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
{{ body|safe }}
"""

TPL_INDEX = """
{% set title='Home' %}
{% set body %}
  <h1>Welcome</h1>
  {% if 'user_id' in session %}
    <p>Logged in as: <strong>{{ session['email'] }}</strong></p>
  {% else %}
    <p>You are not logged in.</p>
  {% endif %}
{% endset %}
""" + TPL_BASE

TPL_REGISTER = """
{% set title='Register' %}
{% set body %}
  <h1>Create account</h1>
  <form method="post" action="{{ url_for('register') }}">
    <label>Email</label>
    <input type="email" name="email" required>
    <label>Password</label>
    <input type="password" name="password" required minlength="8">
    <button class="btn" type="submit">Register</button>
  </form>
{% endset %}
""" + TPL_BASE

TPL_LOGIN = """
{% set title='Login' %}
{% set body %}
  <h1>Login</h1>
  <form method="post" action="{{ url_for('login') }}">
    <label>Email</label>
    <input type="email" name="email" required>
    <label>Password</label>
    <input type="password" name="password" required>
    <button class="btn" type="submit">Login</button>
  </form>
{% endset %}
""" + TPL_BASE

# --- Routes ---
@app.route("/")
def index():
    return render_template_string(TPL_INDEX)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("register"))

        db = get_db()
        cur = db.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            flash("Email already registered.")
            return redirect(url_for("register"))

        pw_hash = hash_password(password)
        db.execute(
            "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
            (email, pw_hash, datetime.utcnow().isoformat()),
        )
        db.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template_string(TPL_REGISTER)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        ip_key = f"{request.remote_addr}:{email}"

        if login_rate_limited(ip_key):
            flash("Too many attempts. Try again later.")
            return redirect(url_for("login"))

        db = get_db()
        user = db.execute("SELECT id, email, password_hash FROM users WHERE email = ?", (email,)).fetchone()
        if user and verify_password(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["email"] = user["email"]
            flash("Logged in successfully.")
            return redirect(url_for("index"))
        else:
            record_failed_login(ip_key)
            flash("Invalid credentials.")
            return redirect(url_for("login"))

    return render_template_string(TPL_LOGIN)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)