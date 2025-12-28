# Constrained Types Quick Reference

| Purpose            | Pydantic Type or Pattern                     |
|--------------------|-----------------------------------------------|
| min/max length     | `Field(min_length=..., max_length=...)`       |
| numeric ranges     | `Field(ge=..., le=...)`                       |
| strict validation  | `StrictStr`, `StrictInt` (v1 legacy), or v2 `strict=True` |
| regex matching     | `Field(pattern=r"...")`                       |
| repeated fields    | `list[<type>]` with optional `TypeAdapter`    |
| enums              | `Literal[...]` or Python Enum classes         |
