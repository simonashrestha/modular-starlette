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

# PostgreSQL database URL
DATABASE_URL = "postgresql://postgre:admin123@localhost/database"
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


# from sqlalchemy import (
#     JSON,
#     create_engine,
#     MetaData,
#     Table,
#     Column,
#     Integer,
#     String,
#     Text,
#     ForeignKey,
# )
# from databases import Database
# from datetime import datetime
# from sqlalchemy import event

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/database"
# # database = Database(DATABASE_URL)
# # metadata = MetaData()


# # Ensure foreign key support in SQLite
# # def _fk_pragma_on_connect(dbapi_con, con_record):
# #     dbapi_con.execute("PRAGMA foreign_keys = ON")


# # Create the database engine with foreign key support
# engine = create_engine(
#     "postgresql://postgres:admin123@localhost:5432/database"
# )
# connection= engine.connect()
# Base= declarative_base()

# # event.listen(engine, "connect", _fk_pragma_on_connect)

# class User(Base):
#     __tablename__="users"
#     id= Column(Integer, primary_key=True)
#     username= Column(String(50), unique=True)
#     hashed_password= Column(String(255))
#     email= Column(String(50))
#     gender= Column(String(50))

# class Blog(Base):
#     __tablename__="blogs"
#     blog_id= Column(Integer, primary_key=True)
#     blog_description= Column(Text)
#     self_description=Column(String(50))
#     likes= Column(Integer, default=0)
#     dislikes= Column(Integer, default=0)
    
#     reactions= Column(JSON, default={})

# class Comment(Base):
#     __tablename__="comments"
#     comment_id= Column(Integer, primary_key=True)
#     blog_id= Column(Integer, ForeignKey("blog.blog_id", ondelete="CASCADE"))
#     comment_text= Column(Text)
#     timestamp= Column(
#        String(50), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     )

# Base.metadata.create_all(engine)
# Session= sessionmaker(bind=engine)
# session= Session()
