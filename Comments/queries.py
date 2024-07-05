from Database.db import database, comments
from sqlalchemy import select, update, delete, insert
from datetime import datetime

async def insert_comment(blog_id: int, comment_text: str):
    query = comments.insert().values(
        blog_id=blog_id,
        comment_text=comment_text,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    return await database.execute(query)

async def select_comments_by_blog_id(blog_id: int):
    query = (
        select(comments)
        .where(comments.c.blog_id == blog_id)
        .order_by(comments.c.timestamp.desc())
    )
    return await database.fetch_all(query)

async def update_comment(comment_id: int, comment_text: str):
    query = (
        update(comments)
        .where(comments.c.comment_id == comment_id)
        .values(comment_text=comment_text)
    )
    return await database.execute(query)

async def delete_comment(comment_id: int):
    query = delete(comments).where(comments.c.comment_id == comment_id)
    return await database.execute(query)
