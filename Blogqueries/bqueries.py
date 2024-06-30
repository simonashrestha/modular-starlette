from Database.db import database, blog, comments
from sqlalchemy import func, select, update, delete, insert

async def insert_blog(blog_description: str, self_description: str):
    query = blog.insert().values(
        blog_description=blog_description, self_description=self_description
    )
    return await database.execute(query)

async def select_blog_by_id(blog_id: int):
    query = select(blog).where(blog.c.blog_id == blog_id)
    return await database.fetch_one(query)

async def update_blog(blog_id: int, blog_description: str, self_description: str):
    query = (
        update(blog)
        .where(blog.c.blog_id == blog_id)
        .values(blog_description=blog_description, self_description=self_description)
    )
    return await database.execute(query)

async def delete_blog_and_comments(blog_id: int):
    query_delete_comments = delete(comments).where(comments.c.blog_id == blog_id)
    await database.execute(query_delete_comments)

    query_delete_blog = delete(blog).where(blog.c.blog_id == blog_id)
    await database.execute(query_delete_blog)

