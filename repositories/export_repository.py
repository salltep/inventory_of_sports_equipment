import re

from database.database import get_connection

_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _check(name: str) -> str:
    # имена таблиц и столбцов нельзя передать через ?, поэтому проверяем их сами
    if not _NAME.match(name):
        raise Exception(f"Недопустимое имя в запросе: {name}")
    return name


def get_rows(table: str, relations: list[dict]) -> list[dict]:
    """
    Выбирает все записи таблицы вместе со связанными данными (LEFT JOIN).
    Столбцы связанных таблиц получают имена вида <связь>__<столбец>.
    """
    columns = ["m.*"]
    joins = []

    for n, rel in enumerate(relations, start=1):
        alias = f"r{n}"
        name = _check(rel["name"])
        for column in rel["columns"]:
            columns.append(f'{alias}.{_check(column)} AS "{name}__{column}"')
        joins.append(
            f"LEFT JOIN {_check(rel['table'])} {alias} "
            f"ON m.{_check(rel['fk'])} = {alias}.{_check(rel['pk'])}"
        )

    sql = f"SELECT {', '.join(columns)} FROM {_check(table)} m {' '.join(joins)}"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    names = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()

    return [dict(zip(names, row)) for row in rows]
