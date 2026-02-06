import os
import requests  # 🔴 REQUIRED: Run 'pip install requests'
from flask import Flask, render_template, request, jsonify
from datetime import datetime

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
    print(f"⚠️ Warning: Some modules could not be imported: {e}")
    # Dummy functions to prevent crash if modules are missing
    def scan_and_analyze(path): return {"error": "Module missing"}
    def legal_advice(q): return {"answer": "Module missing"}
    def find_cases(q): return []
    def get_lawyers(c, s): return []
    def protect_me(k): return {"response": "Module missing"}

app = Flask(__name__)

# --- CONFIGURATION ---
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🟢 TWILIO CONFIGURATION (Verified Credentials)
TWILIO_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 🟢 FROM Number (Must match your curl command)
TWILIO_PHONE = "+xxxxxxxxx"

# 🟢 TO Number (Your Verified Indian Number)
MY_PHONE = "+XXXXXXXXXXXX"


# =========================================================
#  1. UI ROUTES (HTML PAGES)
# =========================================================

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():
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
    data = request.get_json()
    return jsonify(legal_advice(data.get("question", "")))

@app.route("/api/cases", methods=["POST"])
def api_cases():
    data = request.get_json()
    return jsonify(find_cases(data.get("query", "")))

@app.route("/api/lawyers", methods=["POST"])
def api_lawyers():
    data = request.get_json()
    return jsonify(get_lawyers(data.get("city", ""), data.get("specialization", "")))

@app.route("/api/protect", methods=["POST"])
def api_protect():
    data = request.get_json()
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
    
    message_body = f"🚨 LEXGUARD EMERGENCY!\nI feel unsafe.\nTracking Location: {maps_url}"

    # 3. Construct the API URL
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    
    # 4. Define Payload (Same as your Curl command)
    payload = {
        "To": MY_PHONE,
        "From": TWILIO_PHONE,
        "Body": message_body
    }

    try:
        print(f"📡 Sending SOS Request to {MY_PHONE}...")
        
        # 5. Send Request
        response = requests.post(
            url, 
            data=payload, 
            auth=(TWILIO_SID, TWILIO_AUTH) # Basic Auth using SID/Token
        )
        
        # 6. Handle Response
        if response.status_code == 201: # HTTP 201 = Created (Success)
            print(f"✅ SMS Sent! SID: {response.json().get('sid')}")
            return jsonify({"status": "success", "response": response.json()})
        else:
            print(f"❌ Twilio Refused: {response.text}")
            return jsonify({"status": "error", "message": response.text}), 500

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# =========================================================
#  4. START SERVER
# =========================================================

if __name__ == "__main__":
    print("🚀 LexGuard AI is running on http://127.0.0.1:5000")
    app.run(debug=True)