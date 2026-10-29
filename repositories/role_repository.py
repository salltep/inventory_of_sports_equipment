from database.database import get_connection
from models.role import Role


def _map(row) -> Role:
    return Role(*row)


def create(name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Role(name)
        VALUES (?)
    """, (name,))
    conn.commit()
    conn.close()


def get_by_id(role_id: int) -> Role | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT RoleID, name
        FROM Role
        WHERE RoleID = ?
    """, (role_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Role]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT RoleID, name
        FROM Role
        ORDER BY RoleID
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(role_id: int, name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Role
        SET name = ?
        WHERE RoleID = ?
    """, (name, role_id))
    conn.commit()
    conn.close()


def delete(role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Role
        WHERE RoleID = ?
    """, (role_id,))
    conn.commit()
    conn.close()
