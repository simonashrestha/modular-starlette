from Database.db import database, blog
from sqlalchemy import func, update


async def increment_likes(blog_id: int):
    query = (
        update(blog)
        .where(blog.c.blog_id == blog_id)
        .values(likes=func.coalesce(blog.c.likes, 0) + 1)
    )
    return await database.execute(query)


async def increment_dislikes(blog_id: int):
    query = (
        update(blog)
        .where(blog.c.blog_id == blog_id)
        .values(dislikes=func.coalesce(blog.c.dislikes, 0) + 1)
    )
    return await database.execute(query)
