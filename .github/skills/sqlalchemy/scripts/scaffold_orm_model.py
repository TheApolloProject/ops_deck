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


def parse_fields(raw: str) -> str:
    """Convert a comma-separated field spec into mapped_column declarations.

    Example input: "id:int, email:str, is_active:bool"
    """
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    lines = []
    for part in parts:
        name, _, type_name = part.partition(":")
        name = name.strip()
        type_name = type_name.strip() or "str"
        sa_type = PY_TO_SQLA_TYPE.get(type_name, "String")
        if name == "id":
            line = f"    {name}: Mapped[int] = mapped_column({sa_type}, primary_key=True)"
        else:
            line = f"    {name}: Mapped[{type_name}] = mapped_column({sa_type})"
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a SQLAlchemy 2.x ORM model.")
    parser.add_argument("model_name", help="Name of the ORM model class, e.g. User")
    parser.add_argument(
        "--fields",
        help='Comma-separated field list, e.g. "id:int, email:str, created_at:datetime"',
        required=True,
    )
    args = parser.parse_args()

    fields_block = parse_fields(args.fields)

    template = f"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, Date, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class {args.model_name}(Base):
    __tablename__ = "{args.model_name.lower()}"

{fields_block}
"""

    print(dedent(template))


if __name__ == "__main__":
    main()
