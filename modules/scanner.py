def scan_and_analyze(file_path):
    """
    INPUT:
        file_path (str) - Path to uploaded PDF/Image

    OUTPUT:
        {
            "success": True,
            "full_text": str,
            "clauses": [
                {
                    "id": int,
                    "text": str,
                    "risk": "HIGH" | "MEDIUM" | "LOW",
                    "confidence": float,
                    "explanation": str,
                    "alternate_solution": str
                }
            ],
            "heatmap": {
                "high": int,
                "medium": int,
                "low": int
            }
        }
    """

    # DEMO DATA (Replace with real logic later)
    return {
        "success": True,
        "full_text": "Demo contract text extracted from document.",
        "clauses": [
            {
                "id": 1,
                "text": "The company may terminate this agreement without notice.",
                "risk": "HIGH",
                "confidence": 0.93,
                "explanation": "One-sided termination clause that may disadvantage the employee.",
                "alternate_solution": "Add a 30-day notice period for both parties."
            }
        ],
        "heatmap": {
            "high": 1,
            "medium": 0,
            "low": 0
        }
    }
