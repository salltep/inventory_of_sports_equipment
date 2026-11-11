import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

from repositories import export_repository

CSV_DELIMITER = ","


def _nest(rows: list[dict], relations: list[dict]) -> list[dict]:
    """Превращает плоские строки в записи со вложенными объектами."""
    fk_columns = {rel["fk"] for rel in relations}
    result = []

    for row in rows:
        item = {}
        nested = {rel["name"]: {} for rel in relations}

        for key, value in row.items():
            prefix, _, column = key.partition("__")
            if column and prefix in nested:
                nested[prefix][column] = value
            elif key not in fk_columns:
                item[key] = value

        for name, fields in nested.items():
            has_data = any(v is not None for v in fields.values())
            item[name] = fields if has_data else None

        result.append(item)

    return result


def _flatten(item: dict, prefix: str = "") -> dict:
    """Для CSV: вложенные объекты объединяются в одну строку (address_city и т.д.)."""
    flat = {}
    for key, value in item.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict):
            flat.update(_flatten(value, name + "_"))
        else:
            flat[name] = "" if value is None else value
    return flat


def _add_element(parent, tag: str, value):
    element = ET.SubElement(parent, tag)
    if isinstance(value, dict):
        for key, inner in value.items():
            _add_element(element, key, inner)
    elif value is not None:
        element.text = str(value)


def _write_json(data: list[dict], path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _write_yaml(data: list[dict], path: Path):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def _write_csv(data: list[dict], path: Path):
    rows = [_flatten(item) for item in data]

    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    # utf-8-sig, чтобы Excel правильно показал русские буквы
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=CSV_DELIMITER)
        writer.writeheader()
        writer.writerows(rows)


def _write_xml(data: list[dict], path: Path, item_tag: str):
    root = ET.Element("data")
    for item in data:
        _add_element(root, item_tag, item)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def export_all(table: str, relations: list[dict], out_dir) -> int:
    """Выгружает таблицу в data.json, data.csv, data.xml и data.yaml. Возвращает число записей."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = export_repository.get_rows(table, relations)
    data = _nest(rows, relations)

    _write_json(data, out_dir / "data.json")
    _write_csv(data, out_dir / "data.csv")
    _write_xml(data, out_dir / "data.xml", table.lower())
    _write_yaml(data, out_dir / "data.yaml")

    return len(data)
