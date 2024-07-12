from sqlalchemy import (
    JSON,
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)
from databases import Database
from datetime import datetime
from sqlalchemy.orm import sessionmaker


# PostgreSQL database URL
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/database"
database = Database(DATABASE_URL)
metadata = MetaData()

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True),
    Column("hashed_password", String(255)),
    Column("email", String(50)),
    Column("gender", String(50)),
)

blog = Table(
    "blog",
    metadata,
    Column("blog_id", Integer, primary_key=True),
    Column("blog_description", Text),
    Column("self_description", String(50)),
    Column("likes", Integer, default=0),
    Column("dislikes", Integer, default=0),
    Column("reactions", JSON, default={})
)

comments = Table(
    "comments",
    metadata,
    Column("comment_id", Integer, primary_key=True),
    Column("blog_id", Integer, ForeignKey("blog.blog_id", ondelete="CASCADE")),
    Column("comment_text", Text),
    Column(
        "timestamp", String(50), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ),
)

metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


