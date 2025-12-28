# SQLAlchemy Performance Patterns

Key techniques for keeping ORM-heavy applications responsive.

## Avoid N+1 queries

- Use `selectinload()` or `joinedload()` when loading collections or related objects.
- Prefer bulk-loading over per-row queries inside loops.

## Use indexes wisely

- Create indexes on frequently filtered columns (e.g. email, created_at).
- Avoid unnecessary multi-column indexes.

## Paginate results

- Use `limit` / `offset`, cursor-based pagination, or ID-based pagination for large datasets.

## Profile and observe

- Enable SQL echo during debugging (`echo=True`).
- Use application-level profiling tools to locate slow queries.