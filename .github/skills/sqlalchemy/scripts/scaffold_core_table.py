from __future__ import annotations

import argparse
from textwrap import dedent
from typing import Dict


PY_TO_SQLA_TYPE: Dict[str, str] = {
    "int": "Integer",
    "str": "String",
    "bool": "Boolean",
    "datetime": "DateTime",
    "date": "Date",
    "float": "Float",
}


def parse_columns(raw: str) -> str:
    """Convert comma-separated specs into Column declarations.

    Example input: "id:int, email:str, created_at:datetime"
    """
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    lines = []
    for part in parts:
        name, _, type_name = part.partition(":")
        name = name.strip()
        type_name = type_name.strip() or "str"
        sa_type = PY_TO_SQLA_TYPE.get(type_name, "String")
        if name == "id":
            line = f'    Column("{name}", {sa_type}, primary_key=True)'
        else:
            line = f'    Column("{name}", {sa_type})'
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a SQLAlchemy Core Table.")
    parser.add_argument("table_name", help="Name of the table, e.g. user")
    parser.add_argument(
        "--columns",
        help='Comma-separated column list, e.g. "id:int, email:str, created_at:datetime"',
        required=True,
    )
    args = parser.parse_args()

    columns_block = parse_columns(args.columns)

    template = f"""
from sqlalchemy import Table, Column, MetaData, Integer, String, Boolean, DateTime, Date, Float

metadata = MetaData()

{args.table_name} = Table(
    "{args.table_name}",
    metadata,
{columns_block},
)
"""

    print(dedent(template))


if __name__ == "__main__":
    main()
