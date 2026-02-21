"""
Auth Module — Session-based authentication & role-based access control.
Uses SQLite for user storage. Passwords hashed with werkzeug.

Tables: users (id, name, email, password_hash, role)
"""
import sqlite3
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, jsonify, redirect, url_for

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lexguard_auth.db")


# =========================================================
#  DATABASE INIT
# =========================================================

def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db():
    """Create users table if it doesn't exist."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()
    print("[AUTH] Database initialized")


# =========================================================
#  USER OPERATIONS
# =========================================================

def register_user(name, email, password, role="user"):
    """
    Register a new user.
    Returns: {"success": True/False, "message": str}
    """
    if not name or not email or not password:
        return {"success": False, "message": "All fields are required."}

    if role not in ("user", "lawyer"):
        return {"success": False, "message": "Invalid role. Must be 'user' or 'lawyer'."}

    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name.strip(), email.strip().lower(), generate_password_hash(password), role)
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": "Registration successful."}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "Email already registered."}
    except Exception as e:
        return {"success": False, "message": str(e)}


def login_user(email, password):
    """
    Validate credentials and return user dict.
    Returns: {"success": True/False, "user": {...}} or {"success": False, "message": str}
    """
    if not email or not password:
        return {"success": False, "message": "Email and password are required."}

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email.strip().lower(),)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }
    return {"success": False, "message": "Invalid email or password."}


# =========================================================
#  ROLE-BASED ACCESS DECORATOR
# =========================================================

def role_required(role):
    """
    Decorator to restrict routes by role.
    Usage: @role_required("lawyer")
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login_page"))
            if session.get("role") != role:
                return jsonify({"success": False, "error": "Access denied. Requires role: " + role}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def login_required(f):
    """Decorator to require any authenticated user."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated_function
