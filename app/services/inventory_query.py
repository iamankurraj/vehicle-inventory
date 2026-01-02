from app.db import get_connection

def find_part(part: str, region: str | None):
    conn = get_connection()
    cur = conn.cursor()

    if region:
        cur.execute("""
            SELECT p.name, i.part_name, i.quantity
            FROM inventory i
            JOIN provider p ON i.provider_id = p.id
            JOIN region r ON p.region_id = r.id
            WHERE i.part_name ILIKE %s
              AND r.name ILIKE %s
              AND i.quantity > 0
        """, (f"%{part}%", f"%{region}%"))
    else:
        cur.execute("""
            SELECT p.name, i.part_name, i.quantity
            FROM inventory i
            JOIN provider p ON i.provider_id = p.id
            WHERE i.part_name ILIKE %s
              AND i.quantity > 0
        """, (f"%{part}%",))

    return cur.fetchall()



def list_available_parts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            i.part_name,
            SUM(i.quantity) AS total_quantity
        FROM inventory i
        WHERE i.quantity > 0
        GROUP BY i.part_name
        ORDER BY i.part_name;
    """)

    return [
        {
            "part_name": row[0],
            "total_quantity": row[1]
        }
        for row in cur.fetchall()
    ]


def get_part_inventory(part_name: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.name AS provider,
            r.name AS region,
            i.quantity
        FROM inventory i
        JOIN provider p ON i.provider_id = p.id
        JOIN region r ON p.region_id = r.id
        WHERE i.part_name = %s
          AND i.quantity > 0
        ORDER BY r.name, p.name;
    """, (part_name,))

    rows = cur.fetchall()
    if not rows:
        return None

    return {
        "part_name": part_name,
        "inventory": [
            {
                "provider": r[0],
                "region": r[1],
                "quantity": r[2]
            }
            for r in rows
        ]
    }
