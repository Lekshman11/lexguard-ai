import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cases.db")

def find_cases(query, year=None, court=None):
    """
    INPUT:
        query (str)
        year (str or None)
        court (str or None)

    OUTPUT:
        {
            "success": True/False,
            "cases": [
                {
                    "title": str,
                    "summary": str,
                    "outcome": str
                }
            ]
        }
    """
    if not os.path.exists(DB_PATH):
        return {"success": False, "error": "Cases database not found. Please set up cases.db first.", "cases": []}

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        sql = """SELECT case_name, narrative, judgement 
                 FROM cases 
                 WHERE (case_name LIKE ? OR narrative LIKE ? OR key_people LIKE ? OR judgement LIKE ?)"""
        params = [f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"]

        if year and year != "Any":
            sql += " AND year = ?"
            params.append(year)

        if court and court != "Any":
            sql += " AND court = ?"
            params.append(court)

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"success": True, "cases": []}

        cases = []
        for row in rows:
            cases.append({
                "title": row[0],
                "summary": row[1],
                "outcome": row[2]
            })

        return {"success": True, "cases": cases}

    except Exception as e:
        return {"success": False, "error": str(e), "cases": []}