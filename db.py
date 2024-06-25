from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, ForeignKey
from databases import Database
from datetime import datetime

DATABASE_URL = "sqlite:///./database.db"
database = Database(DATABASE_URL)
metadata = MetaData()

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
)

comments = Table(
    "comments",
    metadata,
    Column("comment_id", Integer, primary_key=True),
    Column("blog_id", Integer, ForeignKey("blog.blog_id", ondelete="CASCADE")),
    Column("comment_text", Text),
    Column("timestamp", String(50), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

from sqlalchemy import event

def enable_foreign_keys(dbapi_connection, connection_record):
    cursor= dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()