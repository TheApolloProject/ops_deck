from __future__ import annotations

from textwrap import dedent


LEGACY_EXAMPLE = "session.query(User).filter(User.email == email).first()"

MODERN_EXAMPLE = dedent(
    """
    from sqlalchemy import select

    stmt = select(User).where(User.email == email)
    user = session.scalar(stmt)
    """
).strip()


def explain_rewrite() -> str:
    """Return a text explanation of how to modernise a common legacy query."""
    return dedent(
        f"""
        Legacy pattern:

            {LEGACY_EXAMPLE}

        Modern 2.x pattern:

            {MODERN_EXAMPLE}

        Key changes:

        - Use the unified select() construct instead of session.query().
        - Execute the statement via session.scalar() / session.scalars() or session.execute().
        - Keep filter criteria inside where() rather than filter().
        """
    ).strip()


if __name__ == "__main__":
    print(explain_rewrite())
