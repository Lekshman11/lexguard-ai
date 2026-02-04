def legal_advice(question):
    """
    INPUT:
        question (str)

    OUTPUT:
        {
            "success": True,
            "answer": str,
            "law_reference": str,
            "disclaimer": str
        }
    """

    return {
        "success": True,
        "answer": "Under Indian law, employment termination depends on contract terms and labor regulations.",
        "law_reference": "Industrial Disputes Act, 1947",
        "disclaimer": "This is for educational purposes only. Consult a licensed lawyer for legal advice."
    }
