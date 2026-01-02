from app.db import get_connection

def find_providers(region: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT p.name
        FROM provider p
        JOIN region r ON p.region_id = r.id
        WHERE r.name ILIKE %s
        ORDER BY p.name
    """, (f"%{region}%",))

    return [row[0] for row in cur.fetchall()]
