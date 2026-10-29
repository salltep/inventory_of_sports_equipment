from database.database import get_connection
from models.inventory import Inventory


def _map(row) -> Inventory:
    return Inventory(*row)


def create(name: str, type_: str, quantity: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Inventory(name, type, quantity)
        VALUES (?, ?, ?)
    """, (name, type_, quantity))
    conn.commit()
    conn.close()


def get_by_id(inventory_id: int) -> Inventory | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT InventoryID, name, type, status, quantity
        FROM Inventory
        WHERE InventoryID = ?
    """, (inventory_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Inventory]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT InventoryID, name, type, status, quantity
        FROM Inventory
        ORDER BY InventoryID
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update_status(inventory_id: int, status: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Inventory
        SET status = ?
        WHERE InventoryID = ?
    """, (status, inventory_id))
    conn.commit()
    conn.close()


def update_quantity(inventory_id: int, quantity: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Inventory
        SET quantity = ?
        WHERE InventoryID = ?
    """, (quantity, inventory_id))
    conn.commit()
    conn.close()


def delete(inventory_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Inventory
        WHERE InventoryID = ?
    """, (inventory_id,))
    conn.commit()
    conn.close()
