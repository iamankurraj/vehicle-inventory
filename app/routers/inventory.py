from fastapi import APIRouter
from app.db import get_connection

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/countries")
def get_countries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM country ORDER BY name;")
    data = [r[0] for r in cur.fetchall()]
    cur.close(); conn.close()
    return data

@router.get("/regions")
def get_regions(country: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.name
        FROM region r
        JOIN country c ON r.country_id = c.id
        WHERE c.name = %s
        ORDER BY r.name;
    """, (country,))
    data = [r[0] for r in cur.fetchall()]
    cur.close(); conn.close()
    return data

@router.get("/parts")
def get_parts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT part_name FROM inventory ORDER BY part_name;")
    data = [r[0] for r in cur.fetchall()]
    cur.close(); conn.close()
    return data

@router.get("/search")
def search(country: str, region: str, part: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name, i.part_name, i.quantity
        FROM inventory i
        JOIN provider p ON i.provider_id = p.id
        JOIN region r ON p.region_id = r.id
        JOIN country c ON r.country_id = c.id
        WHERE c.name=%s AND r.name=%s AND i.part_name=%s;
    """, (country, region, part))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return [
        {"provider": r[0], "part": r[1], "quantity": r[2]}
        for r in rows
    ]




@router.get("/available-parts")
def available_parts():
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

    rows = cur.fetchall()
    cur.close(); conn.close()

    return [
        {
            "part_name": r[0],
            "total_quantity": r[1]
        }
        for r in rows
    ]


@router.get("/part-detail")
def part_detail(part_name: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.name AS provider,
            r.name AS region,
            c.name AS country,
            i.quantity
        FROM inventory i
        JOIN provider p ON i.provider_id = p.id
        JOIN region r ON p.region_id = r.id
        JOIN country c ON r.country_id = c.id
        WHERE i.part_name = %s
          AND i.quantity > 0
        ORDER BY c.name, r.name, p.name;
    """, (part_name,))

    rows = cur.fetchall()
    cur.close(); conn.close()

    if not rows:
        return {"part_name": part_name, "inventory": []}

    return {
        "part_name": part_name,
        "inventory": [
            {
                "provider": r[0],
                "region": r[1],
                "country": r[2],
                "quantity": r[3]
            }
            for r in rows
        ]
    }
