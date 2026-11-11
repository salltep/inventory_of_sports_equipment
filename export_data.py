from pathlib import Path

from services.export_service import export_all

# Какую таблицу выгружать и какие связанные таблицы вкладывать.
# Чтобы выгрузить другую таблицу, достаточно изменить только эти настройки.
TABLE = "Operation"

RELATIONS = [
    {
        "name": "inventory",          # имя вложенного объекта
        "table": "Inventory",         # связанная таблица
        "fk": "InventoryID",          # внешний ключ в выгружаемой таблице
        "pk": "InventoryID",          # первичный ключ связанной таблицы
        "columns": ["name", "type", "status", "quantity"],
    },
    {
        "name": "user",
        "table": "User",
        "fk": "UserID",
        "pk": "UserID",
        "columns": ["login"],         # хеш пароля в выгрузку не попадает
    },
]

OUT_DIR = Path(__file__).resolve().parent / "out"


def main():
    try:
        count = export_all(TABLE, RELATIONS, OUT_DIR)
        print(f"Выгружено записей: {count}")
        print(f"Файлы сохранены в папку: {OUT_DIR}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
