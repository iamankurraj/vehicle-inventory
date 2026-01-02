from fastapi import APIRouter, HTTPException
from app.db import get_connection
import re

router = APIRouter(prefix="/reserve", tags=["Reservation"])

@router.get("/verify-vin")
def verify_vin(vin: str):
    if not re.fullmatch(r"[A-Za-z0-9]{17}", vin):
        return {"valid": False}

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM vehicle WHERE vin=%s;", (vin,))
    exists = cur.fetchone() is not None
    cur.close(); conn.close()

    return {"valid": exists}

@router.post("")
def reserve(vin: str, provider: str, part: str):
    if not re.fullmatch(r"[A-Za-z0-9]{17}", vin):
        raise HTTPException(400, "Invalid VIN format")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM vehicle WHERE vin=%s;", (vin,))
    if not cur.fetchone():
        raise HTTPException(403, "VIN not recognized")

    cur.execute("""
        SELECT i.id, i.quantity
        FROM inventory i
        JOIN provider p ON i.provider_id = p.id
        WHERE p.name=%s AND i.part_name=%s;
    """, (provider, part))

    row = cur.fetchone()
    if not row or row[1] <= 0:
        raise HTTPException(400, "Out of stock")

    cur.execute(
        "UPDATE inventory SET quantity = quantity - 1 WHERE id=%s;",
        (row[0],)
    )

    conn.commit()
    cur.close(); conn.close()

    return {"status": "reserved"}
