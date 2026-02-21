import os
import io
import re as re_module
import requests  # 🔴 REQUIRED: Run 'pip install requests'
import sqlite3
import resend
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from datetime import datetime
from googletrans import Translator
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

# --- IMPORT YOUR MODULES ---
# Ensure these files exist in your 'modules' folder.
# If you don't have them yet, comment them out to run the server.
try:
    from modules.scanner import scan_and_analyze
    from modules.legal_advisor import legal_advice
    from modules.cases import find_cases
    from modules.connect import get_lawyers
    from modules.protect import protect_me
except ImportError as e:
    print(f"[WARNING] Some modules could not be imported: {e}")
    # Dummy functions to prevent crash if modules are missing
    def scan_and_analyze(path): return {"error": "Module missing"}
    def legal_advice(q): return {"answer": "Module missing"}
    def find_cases(q): return []
    def get_lawyers(c, s): return []
    def protect_me(k): return {"response": "Module missing"}

app = Flask(__name__)
app.secret_key = "lexguard_super_secret_key_2024"

# --- AUTH & REVIEWS MODULES ---
try:
    from modules.auth import init_auth_db, register_user, login_user, role_required, login_required
    from modules.reviews import init_reviews_db, submit_for_review, get_pending_reviews, get_approved_reviews, get_user_reviews, approve_review
    init_auth_db()
    init_reviews_db()
except ImportError as e:
    print(f"[WARNING] Auth/Reviews modules could not be imported: {e}")

# --- CONFIGURATION ---
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- DEMO CASE STATUS ENGINE ---
# This is a demo dataset. In production, integrate with authorized judicial APIs.
DEMO_CASES = {
    "1234": {"status": "Pending", "next_hearing": "15-Aug-2026"},
    "5678": {"status": "Disposed", "next_hearing": None},
    "9999": {"status": "Adjourned", "next_hearing": "01-Sep-2026"}
}

# --- CASE REQUESTS DB ---
CASE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lexguard_auth.db")

def init_case_requests_db():
    """Create case_requests table if it doesn't exist. Does NOT alter other tables."""
    conn = sqlite3.connect(CASE_DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS case_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            case_number TEXT,
            year TEXT,
            court_type TEXT,
            status TEXT,
            next_hearing TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("[CASE-LOOKUP] case_requests table initialized")

init_case_requests_db()

# --- EMAIL NOTIFICATION (Resend SDK) ---
# ============================================================
# Set RESEND_API_KEY env var before running:
#   PowerShell: $env:RESEND_API_KEY="re_xxxxxxxxxxxx"
#   CMD:        set RESEND_API_KEY=re_xxxxxxxxxxxx
#   Linux/Mac:  export RESEND_API_KEY=re_xxxxxxxxxxxx
# GLOBAL key — one key for all users. Do NOT generate per user.
# ============================================================
resend.api_key = os.getenv("RESEND_API_KEY", "re_ak4V8RHc_6nGGpW3BQ48NwuMRLk9Sj4ZE")

SENDER_EMAIL = "LexGuard AI <onboarding@resend.dev>"

def send_case_email(to_email, case_number, status, next_hearing):
    """Send case status email via Resend SDK. Uses global API key."""
    if not resend.api_key:
        print("[EMAIL] Resend API key not configured")
        return False

    print(f"[EMAIL] Attempting to send email to: {to_email}")
    try:
        response = resend.Emails.send({
            "from": SENDER_EMAIL,
            "to": [to_email],
            "subject": "LexGuard Case Status Update",
            "html": f"""
                <h2>⚖️ Case Status Update</h2>
                <p><strong>Case Number:</strong> {case_number}</p>
                <p><strong>Status:</strong> {status}</p>
                <p><strong>Next Hearing:</strong> {next_hearing or 'Not Scheduled'}</p>
                <br>
                <p style="color: #666;">- LexGuard AI</p>
            """
        })
        print(f"[EMAIL] ✅ Sent successfully to {to_email} — ID: {response}")
        return True
    except Exception as e:
        print(f"[EMAIL] ❌ Failed to send to {to_email}: {e}")
        return False

# 🟢 TWILIO CONFIGURATION (Verified Credentials)
TWILIO_SID = "AC84e896c393cfa3d25482e0d3a95d7c53"
TWILIO_AUTH = "97c21844db8ec9444003523562d4a9c5"


# 🟢 FROM Number (Must match your curl command)
TWILIO_PHONE = "+17622093495"

# 🟢 TO Number (Your Verified Indian Number)
MY_PHONE = "+919176200584"


# =========================================================
#  1. UI ROUTES (HTML PAGES)
# =========================================================

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login_page"))
    return render_template("dashboard.html")

@app.route("/scanner")
def scanner_page():
    return render_template("scanner.html")

@app.route("/legal-advisor")
def legal_advisor_page():
    return render_template("legal_advisor.html")

@app.route("/cases")
def cases_page():
    return render_template("cases.html")

@app.route("/lawyers")
def lawyers_page():
    return render_template("lawyers.html")

@app.route("/protect")
def protect_page():
    return render_template("protect.html")


# =========================================================
#  2. CORE API ROUTES (FUNCTIONALITY)
# =========================================================

@app.route("/api/scan", methods=["POST"])
def api_scan():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"})
    
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        result = scan_and_analyze(file_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/legal", methods=["POST"])
def api_legal():
    """Legal advice endpoint — translates output if session lang != en."""
    data = request.get_json() or {}
    result = legal_advice(data.get("question", ""))

    # Translate text fields if non-English language selected
    lang = session.get("lang", "en")
    if lang != "en" and result.get("matched"):
        result["title"] = translate_text(result.get("title", ""), lang)
        # Translate answer (HTML) — strip tags, translate, rebuild
        if result.get("answer"):
            result["answer"] = translate_text(result["answer"], lang)
        if result.get("what_next"):
            result["what_next"] = [translate_text(item, lang) for item in result["what_next"]]
        if result.get("disclaimer"):
            result["disclaimer"] = translate_text(result["disclaimer"], lang)

    return jsonify(result)

@app.route("/api/cases", methods=["POST"])
def api_cases():
    data = request.get_json() or {}
    query = data.get("query", "")
    year = data.get("year", "Any")
    court = data.get("court", "Any")
    return jsonify(find_cases(query, year, court))

@app.route("/api/lawyers", methods=["POST"])
def api_lawyers():
    data = request.get_json() or {}
    return jsonify(get_lawyers(data.get("city", ""), data.get("specialization", "")))

@app.route("/api/protect", methods=["POST"])
def api_protect():
    data = request.get_json() or {}
    return jsonify(protect_me(data.get("keyword", "")))

@app.route("/save-audio", methods=["POST"])
def save_audio():
    if "audio" not in request.files:
        return jsonify({"status": "error", "message": "No audio file"})
        
    audio = request.files["audio"]
    # Save with specific timestamp for evidence
    filename = datetime.now().strftime("Evidence_%Y%m%d%H%M%S") + ".webm"
    path = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(path)
    return jsonify({"status": "saved", "filename": filename})


# =========================================================
#  3. SOS API (THE FIX)
# =========================================================

@app.route('/api/send-sos', methods=['POST'])
def send_sos():
    """
    Sends an SOS SMS using Direct HTTP Request (Imitates Curl).
    This bypasses library issues.
    """
    # 1. Get Coordinates from Frontend
    data = request.json
    lat = data.get('lat', '0')
    lng = data.get('lng', '0')
    
    # 🔴 FIX: Correct Google Maps URL format
    maps_url = f"https://maps.google.com/?q={lat},{lng}"
    
    message_body = f"LEXGUARD EMERGENCY!\nI feel unsafe.\nTracking Location: {maps_url}"

    # 3. Construct the API URL
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    
    # 4. Define Payload (Same as your Curl command)
    payload = {
        "To": MY_PHONE,
        "From": TWILIO_PHONE,
        "Body": message_body
    }

    try:
        print(f"[SOS] Sending SOS Request to {MY_PHONE}...")
        
        # 5. Send Request
        response = requests.post(
            url, 
            data=payload, 
            auth=(TWILIO_SID, TWILIO_AUTH) # Basic Auth using SID/Token
        )
        
        # 6. Handle Response
        if response.status_code == 201: # HTTP 201 = Created (Success)
            print(f"[OK] SMS Sent! SID: {response.json().get('sid')}")
            return jsonify({"status": "success", "response": response.json()})
        else:
            print(f"[ERROR] Twilio Refused: {response.text}")
            return jsonify({"status": "error", "message": response.text}), 500

    except Exception as e:
        print(f"[ERROR] Connection Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# =========================================================
#  4. AUTH ROUTES (NEW — does NOT modify existing routes)
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        result = login_user(request.form.get("email"), request.form.get("password"))
        if result["success"]:
            user = result["user"]
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["name"] = user["name"]
            if user["role"] == "lawyer":
                return redirect(url_for("lawyer_dashboard"))
            return redirect(url_for("user_dashboard"))
        return render_template("login.html", error=result["message"])
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        result = register_user(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password"),
            request.form.get("role", "user")
        )
        if result["success"]:
            return render_template("register.html", success="Account created! You can now login.")
        return render_template("register.html", error=result["message"])
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# =========================================================
#  5. DASHBOARD ROUTES (NEW — role-protected)
# =========================================================

@app.route("/lawyer-dashboard")
@role_required("lawyer")
def lawyer_dashboard():
    pending = get_pending_reviews()
    approved = get_approved_reviews()
    return render_template("lawyer_dashboard.html", pending=pending, approved=approved)

@app.route("/user-dashboard")
@role_required("user")
def user_dashboard():
    reviews = get_user_reviews(session["user_id"])
    return render_template("user_dashboard.html", reviews=reviews)


# =========================================================
#  6. REVIEW WORKFLOW ROUTES (NEW — does NOT touch /api/legal)
# =========================================================

@app.route("/api/review-advice", methods=["POST"])
@login_required
def review_advice():
    """User submits a question. AI generates response, stored for lawyer review."""
    question = (request.form.get("question") or "").strip()
    if not question:
        return redirect(url_for("user_dashboard"))
    # Get AI response (reuses existing legal_advice function)
    ai_result = legal_advice(question)
    ai_response = ai_result.get("answer", "No AI response generated.")
    # Store for lawyer review
    result = submit_for_review(session["user_id"], question, ai_response)
    return redirect(url_for("user_dashboard"))

@app.route("/api/approve-advice", methods=["POST"])
@role_required("lawyer")
def approve_advice():
    """Lawyer approves or edits AI-generated advice."""
    review_id = request.form.get("review_id")
    final_response = request.form.get("final_response", "")
    lawyer_notes = request.form.get("lawyer_notes", "")
    if review_id:
        approve_review(int(review_id), final_response, lawyer_notes)
    return redirect(url_for("lawyer_dashboard"))


# =========================================================
#  7. DEMO CASE LOOKUP ENGINE (NEW — does NOT modify existing routes)
# =========================================================

@app.route("/submit-case", methods=["POST"])
def submit_case():
    """
    Demo case status lookup.
    - Checks case_number against DEMO_CASES dataset
    - Saves record in case_requests table
    - Sends email notification to logged-in user
    - Returns JSON with status info
    """
    # Require login
    if not session.get("user_id"):
        return jsonify({"success": False, "error": "Please login to use case lookup."}), 401

    data = request.get_json() or {}
    case_number = (data.get("case_number") or "").strip()
    year = (data.get("year") or "").strip()
    court_type = (data.get("court_type") or "").strip()

    if not case_number:
        return jsonify({"success": False, "error": "Case number is required."}), 400

    # Determine status from demo dataset
    if case_number in DEMO_CASES:
        status = DEMO_CASES[case_number]["status"]
        next_hearing = DEMO_CASES[case_number]["next_hearing"]
    else:
        status = "Under Review"
        next_hearing = "To Be Announced"

    # Save to database
    try:
        conn = sqlite3.connect(CASE_DB_PATH)
        conn.execute(
            "INSERT INTO case_requests (user_id, case_number, year, court_type, status, next_hearing) VALUES (?, ?, ?, ?, ?, ?)",
            (session["user_id"], case_number, year, court_type, status, next_hearing)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[CASE-LOOKUP ERROR] DB save failed: {e}")

    # Send email notification to logged-in user
    email_sent = False
    try:
        from modules.auth import get_db
        conn = get_db()
        user = conn.execute("SELECT email FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        conn.close()
        if user:
            email_sent = send_case_email(user["email"], case_number, status, next_hearing)
    except Exception as e:
        print(f"[CASE-LOOKUP ERROR] Email lookup failed: {e}")

    return jsonify({
        "success": True,
        "status": status,
        "next_hearing": next_hearing or "Not Scheduled",
        "email_sent": email_sent
    })


# =========================================================
#  8. SETTINGS / PROFILE MANAGEMENT (NEW — does NOT modify existing routes)
# =========================================================

@app.route("/settings", methods=["GET", "POST"])
def settings():
    """
    Profile management page.
    - GET: show current user details
    - POST: update username, email, and optionally password
    """
    # Require login
    if not session.get("user_id"):
        return redirect(url_for("login_page"))

    from modules.auth import get_db
    from werkzeug.security import generate_password_hash

    if request.method == "GET":
        # Fetch current user details (never expose password_hash)
        conn = get_db()
        user = conn.execute("SELECT id, name, email, role FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        conn.close()
        if not user:
            return redirect(url_for("login_page"))
        return render_template("settings.html", user=user)

    # --- POST: Update profile ---
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    new_password = (request.form.get("new_password") or "").strip()
    confirm_password = (request.form.get("confirm_password") or "").strip()

    # Validation
    if not name or not email:
        return _render_settings_with_error("Username and email are required.")

    # Password confirmation check
    if new_password and new_password != confirm_password:
        return _render_settings_with_error("Passwords do not match.")

    conn = get_db()

    # Email uniqueness check (exclude current user)
    existing = conn.execute(
        "SELECT id FROM users WHERE email = ? AND id != ?", (email, session["user_id"])
    ).fetchone()
    if existing:
        conn.close()
        return _render_settings_with_error("This email is already in use by another account.")

    # Update user details
    try:
        if new_password:
            conn.execute(
                "UPDATE users SET name = ?, email = ?, password_hash = ? WHERE id = ?",
                (name, email, generate_password_hash(new_password), session["user_id"])
            )
        else:
            conn.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (name, email, session["user_id"])
            )
        conn.commit()
        conn.close()

        # Update session if username changed
        session["name"] = name

        # Re-fetch user for display
        conn = get_db()
        user = conn.execute("SELECT id, name, email, role FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        conn.close()
        return render_template("settings.html", user=user, success="Profile updated successfully!")

    except Exception as e:
        conn.close()
        return _render_settings_with_error(f"Update failed: {str(e)}")


def _render_settings_with_error(error_msg):
    """Helper to re-render settings page with error and current user data."""
    from modules.auth import get_db
    conn = get_db()
    user = conn.execute("SELECT id, name, email, role FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    conn.close()
    return render_template("settings.html", user=user, error=error_msg)


# =========================================================
#  9. MULTI-LANGUAGE SUPPORT (NEW — does NOT modify existing routes)
# =========================================================

# Translation utility
translator = Translator()

def translate_text(text, target_lang):
    """Translate text to target language. Returns original on failure."""
    if target_lang == "en":
        return text
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except:
        return text


@app.route("/set-language", methods=["POST"])
def set_language():
    """Store selected language in session."""
    data = request.get_json() or {}
    lang = data.get("lang", "en")
    if lang in ("en", "hi", "ta"):
        session["lang"] = lang
    return jsonify({"success": True, "lang": session.get("lang", "en")})


@app.route("/get-lang")
def get_lang():
    """Return current session language for JS."""
    return jsonify({"lang": session.get("lang", "en")})


@app.route("/translate-batch", methods=["POST"])
def translate_batch():
    """Translate an array of text strings to the session language."""
    data = request.get_json() or {}
    texts = data.get("texts", [])
    lang = session.get("lang", "en")

    if lang == "en" or not texts:
        return jsonify({"translations": texts})

    translated = []
    for text in texts:
        if text and text.strip():
            translated.append(translate_text(text, lang))
        else:
            translated.append(text)

    return jsonify({"translations": translated})


# =========================================================
#  10. PDF EXPORT (NEW — does NOT modify existing routes)
# =========================================================

@app.route("/export-pdf", methods=["POST"])
def export_pdf():
    """
    Generate and return a PDF of legal advice.
    Expects JSON: { title, answer, what_next, disclaimer }
    """
    data = request.get_json() or {}
    title = data.get("title", "Legal Advice")
    answer = data.get("answer", "")
    what_next = data.get("what_next", [])
    disclaimer = data.get("disclaimer", "")
    law_reference = data.get("law_reference", [])

    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            topMargin=0.75*inch, bottomMargin=0.75*inch,
                            leftMargin=0.75*inch, rightMargin=0.75*inch)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'],
                                  fontSize=18, spaceAfter=12, textColor=colors.HexColor('#1a365d'))
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'],
                                    fontSize=14, spaceAfter=8, textColor=colors.HexColor('#2d3748'))
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'],
                                 fontSize=11, spaceAfter=6, leading=16)
    disclaimer_style = ParagraphStyle('Disclaimer', parent=styles['Normal'],
                                       fontSize=9, textColor=colors.grey, spaceAfter=6,
                                       leading=13, borderColor=colors.grey,
                                       borderWidth=0.5, borderPadding=8)

    elements = []

    # Header
    elements.append(Paragraph("LexGuard AI — Legal Advisor Report", title_style))
    elements.append(Spacer(1, 8))

    # Topic title
    elements.append(Paragraph(f"Topic: {title}", heading_style))
    elements.append(Spacer(1, 6))

    # Key Information
    elements.append(Paragraph("Key Information:", heading_style))
    # Strip HTML tags for PDF
    clean_answer = re_module.sub(r'<[^>]+>', '', answer)
    for line in clean_answer.split('\n'):
        line = line.strip()
        if line:
            elements.append(Paragraph(f"• {line}", body_style))
    elements.append(Spacer(1, 8))

    # Law References
    if law_reference:
        elements.append(Paragraph("Relevant Laws / Acts:", heading_style))
        for law in law_reference:
            name = law.get('name', '')
            section = law.get('section', '')
            desc = law.get('description', '')
            elements.append(Paragraph(f"<b>{name}</b> — {section}", body_style))
            elements.append(Paragraph(f"   {desc}", body_style))
        elements.append(Spacer(1, 8))

    # What Next
    if what_next:
        elements.append(Paragraph("What Can You Do Next?", heading_style))
        for idx, item in enumerate(what_next, 1):
            elements.append(Paragraph(f"{idx}. {item}", body_style))
        elements.append(Spacer(1, 8))

    # Disclaimer
    if disclaimer:
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(disclaimer, disclaimer_style))

    # Footer
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Generated by LexGuard AI on {datetime.now().strftime('%d-%b-%Y %H:%M')}",
                               ParagraphStyle('Footer', parent=styles['Normal'],
                                              fontSize=8, textColor=colors.grey)))

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name=f"LexGuard_Advice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                     mimetype='application/pdf')


if __name__ == "__main__":
    print("LexGuard AI is running on http://127.0.0.1:5000")
    app.run(debug=True)