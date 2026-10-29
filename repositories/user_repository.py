from database.database import get_connection
from models.user import User


def _map(row) -> User:
    return User(*row)


def create(login: str, password_hash: str, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO User(login, passwordHash, RoleID)
        VALUES (?, ?, ?)
    """, (login, password_hash, role_id))
    conn.commit()
    conn.close()


def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT UserID, login, passwordHash, RoleID
        FROM User
        WHERE UserID = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT UserID, login, passwordHash, RoleID
        FROM User
        WHERE login = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT UserID, login, passwordHash, RoleID
        FROM User
        ORDER BY UserID
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update_role(user_id: int, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE User
        SET RoleID = ?
        WHERE UserID = ?
    """, (role_id, user_id))
    conn.commit()
    conn.close()


def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM User
        WHERE UserID = ?
    """, (user_id,))
    conn.commit()
    conn.close()
