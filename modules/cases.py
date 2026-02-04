def find_cases(query):
    """
    INPUT:
        query (str)

    OUTPUT:
        {
            "success": True,
            "cases": [
                {
                    "title": str,
                    "summary": str,
                    "outcome": str
                }
            ]
        }
    """

    return {
        "success": True,
        "cases": [
            {
                "title": "ABC vs XYZ (2019)",
                "summary": "Court ruled termination without notice violated labor protections.",
                "outcome": "In favor of employee"
            }
        ]
    }
