"""
Reviews Module — AI + Lawyer review workflow.
Stores AI-generated advice for lawyer review before delivering to users.

Tables: advice_reviews (id, user_id, question, ai_response, status, lawyer_notes, final_response, created_at)
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lexguard_auth.db")


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
#  DATABASE INIT
# =========================================================

def init_reviews_db():
    """Create advice_reviews table if it doesn't exist."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS advice_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            lawyer_notes TEXT DEFAULT '',
            final_response TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()
    print("[REVIEWS] Database initialized")


# =========================================================
#  REVIEW OPERATIONS
# =========================================================

def submit_for_review(user_id, question, ai_response):
    """
    Store AI-generated advice for lawyer review.
    Returns: {"success": True, "review_id": int}
    """
    try:
        conn = get_db()
        cursor = conn.execute(
            "INSERT INTO advice_reviews (user_id, question, ai_response, status, created_at) VALUES (?, ?, ?, 'pending', ?)",
            (user_id, question, ai_response, datetime.now().isoformat())
        )
        review_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {"success": True, "review_id": review_id, "message": "Your query is being reviewed by a legal professional."}
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_pending_reviews():
    """Get all pending reviews for lawyers to review."""
    conn = get_db()
    rows = conn.execute("""
        SELECT r.*, u.name as user_name, u.email as user_email
        FROM advice_reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.status = 'pending'
        ORDER BY r.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_approved_reviews():
    """Get all approved reviews."""
    conn = get_db()
    rows = conn.execute("""
        SELECT r.*, u.name as user_name
        FROM advice_reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.status = 'approved'
        ORDER BY r.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_user_reviews(user_id):
    """Get all reviews for a specific user."""
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM advice_reviews
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_review_by_id(review_id):
    """Get a single review by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM advice_reviews WHERE id = ?", (review_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def approve_review(review_id, final_response, lawyer_notes=""):
    """
    Lawyer approves (or edits) a review.
    Sets status to 'approved' and stores final response.
    """
    try:
        conn = get_db()
        conn.execute("""
            UPDATE advice_reviews
            SET status = 'approved', final_response = ?, lawyer_notes = ?
            WHERE id = ?
        """, (final_response, lawyer_notes, review_id))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Review approved successfully."}
    except Exception as e:
        return {"success": False, "message": str(e)}
