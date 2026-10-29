from database.database import get_connection
from models.operation import Operation


def _map(row) -> Operation:
    return Operation(*row)


def create(inventory_id: int, user_id: int, type_: str, comment: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Operation(InventoryID, UserID, type, comment)
        VALUES (?, ?, ?, ?)
    """, (inventory_id, user_id, type_, comment))
    conn.commit()
    conn.close()


def get_by_id(operation_id: int) -> Operation | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT OperationID, InventoryID, UserID, type, date, comment
        FROM Operation
        WHERE OperationID = ?
    """, (operation_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Operation]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT OperationID, InventoryID, UserID, type, date, comment
        FROM Operation
        ORDER BY date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update_comment(operation_id: int, comment: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Operation
        SET comment = ?
        WHERE OperationID = ?
    """, (comment, operation_id))
    conn.commit()
    conn.close()


def delete(operation_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Operation
        WHERE OperationID = ?
    """, (operation_id,))
    conn.commit()
    conn.close()
