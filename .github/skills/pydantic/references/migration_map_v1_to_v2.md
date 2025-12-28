# Migration Map: Pydantic v1 → Pydantic v2

| v1 Feature                      | v2 Equivalent                          |
|--------------------------------|----------------------------------------|
| `parse_obj(...)`              | `model_validate(...)`                  |
| `dict()`                      | `model_dump()`                         |
| `json()`                      | `model_dump_json()`                    |
| `schema()`                    | `model_json_schema()`                  |
| `class Config:`              | `model_config = ConfigDict(...)`       |
| `orm_mode = True`             | `from_attributes=True`                 |
| `@validator`                  | `@field_validator` / functional validators |
