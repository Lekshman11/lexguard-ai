"""
Legal Advisor Module
Provides general legal information based on user queries.
Integrated from lawyer.py Streamlit module into Flask architecture.
"""
import re

# =========================================================
#  LEGAL KNOWLEDGE BASE (Merged Dataset)
# =========================================================

LEGAL_KB = {

    "rent": {
        "title": "Rental Agreement & Tenant Rights",
        "keywords": ["rent", "tenant", "landlord", "eviction", "lease"],
        "points": [
            "Tenants have the right to peaceful possession of the property.",
            "Landlords cannot evict tenants without due legal process.",
            "Security deposit must be returned after valid deductions.",
            "Eviction must follow proper notice as per agreement or law."
        ],
        "laws": [
            {"name": "Transfer of Property Act, 1882", "section": "Section 105", "description": "Defines lease of immovable property."},
            {"name": "Constitution of India", "section": "Article 300A", "description": "Protects against unlawful deprivation of property."}
        ],
        "what_next": [
            "Review your rental agreement terms.",
            "Request written notice from landlord.",
            "Challenge illegal eviction in civil court."
        ]
    },

    "employment": {
        "title": "Employment Rights & Labor Laws",
        "keywords": ["job", "employment", "salary", "fired", "termination", "labor"],
        "points": [
            "Employees are entitled to minimum wages.",
            "Termination must follow due process.",
            "Unlawful dismissal can be legally challenged.",
            "Equality in public employment is guaranteed."
        ],
        "laws": [
            {"name": "Industrial Disputes Act, 1947", "section": "Section 25F", "description": "Requires notice before termination."},
            {"name": "Constitution of India", "section": "Article 16", "description": "Equality in public employment."}
        ],
        "what_next": [
            "Review employment contract.",
            "Approach labor commissioner.",
            "File complaint before labor court."
        ]
    },

    "defamation": {
        "title": "Defamation & Reputation Rights",
        "keywords": [
            "defame", "defamation", "slander",
            "false accusation", "false allegations",
            "false rumor", "false rumors",
            "rumor", "rumors",
            "spread rumor", "spread rumors",
            "reputation", "character assassination",
            "online defamation"
        ],
        "points": [
            "Defamation involves false statements harming reputation.",
            "Can be civil or criminal.",
            "Freedom of speech has reasonable restrictions.",
            "Truth is a valid defense."
        ],
        "laws": [
            {"name": "Indian Penal Code, 1860", "section": "Section 499", "description": "Defines defamation."},
            {"name": "Constitution of India", "section": "Article 19", "description": "Freedom of speech restrictions."}
        ],
        "what_next": [
            "Send legal notice demanding retraction.",
            "File civil suit for damages.",
            "File criminal complaint if necessary."
        ]
    },

    "police": {
        "title": "Rights During Arrest & Police Action",
        "keywords": ["police", "arrest", "custody", "detained", "fir"],
        "points": [
            "Right to be informed of grounds of arrest.",
            "Right to consult a lawyer.",
            "Must be produced before magistrate within 24 hours.",
            "No forced confession allowed."
        ],
        "laws": [
            {"name": "Constitution of India", "section": "Article 20", "description": "Protection in criminal cases."},
            {"name": "Constitution of India", "section": "Article 21", "description": "Right to life and liberty."},
            {"name": "Constitution of India", "section": "Article 22", "description": "Protection against arrest."}
        ],
        "what_next": [
            "Demand legal representation.",
            "Ensure production before magistrate.",
            "Challenge illegal detention in court."
        ]
    }

}

# =========================================================
#  SYNONYM MAP (maps common synonyms to canonical keywords)
# =========================================================

SYNONYM_MAP = {
    # Rent synonyms
    "renting": "rent", "rental": "rent", "tenancy": "tenant",
    "renter": "tenant", "lessee": "tenant", "lessor": "landlord",
    "kicked out": "eviction", "thrown out": "eviction", "vacate": "eviction",
    "deposit": "rent", "paying guest": "tenant", "pg": "tenant",
    # Employment synonyms
    "work": "job", "working": "job", "employer": "employment",
    "employee": "employment", "wages": "salary", "pay": "salary",
    "sacked": "fired", "dismissed": "fired", "laid off": "fired",
    "retrenchment": "termination", "notice period": "termination",
    "workplace": "employment", "office": "employment",
    # Defamation synonyms
    "defaming": "defame", "slandered": "slander", "libel": "defamation",
    "character assassination": "defamation", "false statement": "false accusation",
    "trolling": "defamation", "spreading lies": "false accusation",
    "fake news": "false accusation", "honour": "reputation", "honor": "reputation",
    # Police synonyms
    "cop": "police", "cops": "police", "constable": "police",
    "arrested": "arrest", "arresting": "arrest", "jail": "custody",
    "lockup": "custody", "detained": "detained", "detain": "detained",
    "complaint": "fir", "first information report": "fir",
}


# =========================================================
#  MATCHING LOGIC
# =========================================================

def legal_advice(question):
    """
    Matches a user question to a legal topic using multi-keyword,
    partial matching, and synonym expansion.

    Returns the same API contract as before:
    - success, matched, title, answer, law_reference, what_next, disclaimer, keyword
    """
    if not question or not question.strip():
        return {
            "success": True,
            "matched": False,
            "message": "Please enter a question to get legal information.",
            "available_topics": ", ".join(sorted(set(d["title"] for d in LEGAL_KB.values()))),
            "disclaimer": "For specific legal advice, please consult a licensed lawyer."
        }

    question_lower = question.lower().strip()

    # --- Step 1: Expand question with synonyms ---
    expanded = question_lower
    for synonym, canonical in SYNONYM_MAP.items():
        if synonym in question_lower:
            expanded += " " + canonical

    # --- Step 2: Match using keywords list (supports partial matching) ---
    matched_topic = None
    matched_keyword = None

    for key, data in LEGAL_KB.items():
        for word in data["keywords"]:
            if word in expanded:
                matched_topic = data
                matched_keyword = word
                break
        if matched_topic:
            break

    # --- Step 3: Build response ---
    if matched_topic:
        # Format answer as HTML bullet points
        answer_html = "<ul class='legal-points'>"
        for point in matched_topic['points']:
            # Convert markdown bold to HTML (if any)
            point_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', point)
            answer_html += f"<li>{point_html}</li>"
        answer_html += "</ul>"

        return {
            "success": True,
            "matched": True,
            "title": matched_topic['title'],
            "answer": answer_html,
            "law_reference": matched_topic['laws'],
            "what_next": matched_topic.get('what_next', []),
            "disclaimer": "DISCLAIMER: This information is for educational purposes only and does not constitute legal advice. Consult a licensed lawyer for your specific situation.",
            "keyword": matched_keyword
        }
    else:
        # No match found
        available_topics = ", ".join(sorted(set(d['title'] for d in LEGAL_KB.values())))
        return {
            "success": True,
            "matched": False,
            "message": "The topic you're asking about is not currently in our knowledge base.",
            "available_topics": available_topics,
            "disclaimer": "For specific legal advice, please consult a licensed lawyer."
        }
