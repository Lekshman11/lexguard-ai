

from flask import Flask, render_template, request, jsonify
import os

# Import team modules
from modules.scanner import scan_and_analyze
from modules.legal_advisor import legal_advice
from modules.cases import find_cases
from modules.connect import get_lawyers
from modules.protect import protect_me

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ UI ------------------

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/")
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


# ------------------ APIs ------------------

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
    question = data.get("question", "")

    try:
        result = legal_advice(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/cases", methods=["POST"])
def api_cases():
    data = request.get_json()
    query = data.get("query", "")

    try:
        return jsonify(find_cases(query))
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/lawyers", methods=["POST"])
def api_lawyers():
    data = request.get_json()
    city = data.get("city", "")
    specialization = data.get("specialization", "")

    try:
        return jsonify(get_lawyers(city, specialization))
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/protect", methods=["POST"])
def api_protect():
    data = request.get_json()
    keyword = data.get("keyword", "")

    try:
        return jsonify(protect_me(keyword))
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)
