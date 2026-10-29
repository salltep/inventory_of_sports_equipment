from database.database import get_connection
from models.damage import Damage


def _map(row) -> Damage:
    return Damage(*row)


def create(inventory_id: int, description: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Damage(InventoryID, description)
        VALUES (?, ?)
    """, (inventory_id, description))
    conn.commit()
    conn.close()


def get_by_id(damage_id: int) -> Damage | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DamageID, InventoryID, description, date
        FROM Damage
        WHERE DamageID = ?
    """, (damage_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Damage]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DamageID, InventoryID, description, date
        FROM Damage
        ORDER BY date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update_description(damage_id: int, description: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Damage
        SET description = ?
        WHERE DamageID = ?
    """, (description, damage_id))
    conn.commit()
    conn.close()


def delete(damage_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Damage
        WHERE DamageID = ?
    """, (damage_id,))
    conn.commit()
    conn.close()
