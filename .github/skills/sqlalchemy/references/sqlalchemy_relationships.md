# SQLAlchemy Relationships

Design relationships explicitly to keep behaviour predictable and queries efficient.

## One-to-many

```python
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")


class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="posts")
````

## Many-to-many via association table

```python
tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
    Column("post_id", ForeignKey("post.id"), primary_key=True),
)
```

```python
class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(primary_key=True)
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        secondary=tag_post,
        back_populates="tags",
    )
```

Choose loading strategies (`selectinload`, `joinedload`) based on query patterns and performance needs.