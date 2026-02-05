import pdfplumber
import re


# ---------- PDF TEXT EXTRACTION ----------
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


# ---------- CLAUSE SPLITTING ----------
def split_into_clauses(text):
    """
    Robust clause splitter for numbered legal clauses:
    1. , 2.1 , 4.3 etc.
    """

    # Use NON-capturing group (?: ) to avoid None values
    pattern = r'\n\s*(?:\d+(\.\d+)*)\s+'
    raw_parts = re.split(pattern, text)

    clauses = []
    buffer = ""

    for part in raw_parts:
        if not part:
            continue  # skip None or empty parts

        # Detect start of a clause by number pattern at beginning
        if re.match(r'^\d+(\.\d+)*', part.strip()):
            if buffer:
                clauses.append(buffer.strip())
            buffer = "Clause " + part.strip()
        else:
            buffer += " " + part.strip()

    if buffer:
        clauses.append(buffer.strip())

    return clauses



# ---------- RISK DETECTION ----------
def detect_risk(clause_text):
    clause = clause_text.lower()

    if "terminate" in clause and "notice" not in clause:
        return "HIGH", "Termination without notice can be risky for the employee."

    if "non-compete" in clause or "competitor" in clause:
        return "HIGH", "Non-compete restrictions may limit future employment."

    if "arbitration" in clause:
        return "MEDIUM", "Mandatory arbitration may restrict court access."

    if "confidential" in clause:
        return "MEDIUM", "Strict confidentiality obligations may continue after employment."

    if "indemnify" in clause or "indemnification" in clause:
        return "MEDIUM", "Indemnification may create unexpected financial liability."

    return "LOW", "This appears to be a standard contractual clause."


def suggest_alternative(risk_level):
    if risk_level == "HIGH":
        return "Negotiate balanced terms or add employee protections."
    if risk_level == "MEDIUM":
        return "Seek clarification or limit the scope of this clause."
    return "No immediate change required."


# ---------- MAIN FUNCTION ----------
def scan_and_analyze(file_path):
    full_text = extract_text_from_pdf(file_path)
    clauses = split_into_clauses(full_text)

    analyzed_clauses = []

    for i, clause in enumerate(clauses[:10]):  # limit for performance
        risk, explanation = detect_risk(clause)

        analyzed_clauses.append({
            "id": i + 1,
            "text": clause[:700],  # prevent huge payload
            "risk": risk,
            "confidence": 0.85,
            "explanation": explanation,
            "alternate_solution": suggest_alternative(risk)
        })

    heatmap = {
        "high": sum(1 for c in analyzed_clauses if c["risk"] == "HIGH"),
        "medium": sum(1 for c in analyzed_clauses if c["risk"] == "MEDIUM"),
        "low": sum(1 for c in analyzed_clauses if c["risk"] == "LOW")
    }

    return {
        "success": True,
        "full_text": full_text[:2000],
        "clauses": analyzed_clauses,
        "heatmap": heatmap
    }


# ---------- LOCAL TEST ----------
#if __name__ == "__main__":
    #print(scan_and_analyze("uploads/sample_offer_letter.pdf"))
