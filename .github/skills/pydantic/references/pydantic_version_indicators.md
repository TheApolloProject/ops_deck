# Pydantic Version Indicators

## Pydantic v2 markers
- Usage of `model_config = ConfigDict(...)`
- `model_validate`, `model_dump`, `model_dump_json`
- `field_validator`, `model_validator`
- `TypeAdapter`
- `from_attributes=True` replacement for `orm_mode`

## Pydantic v1 markers
- Inner class `Config`
- `@validator`
- `parse_obj`, `dict`, `json`
- `schema()` and legacy metadata fields
