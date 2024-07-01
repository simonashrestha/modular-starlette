from Database.db import database, blog, reaction
from sqlalchemy import func, update, select, delete


async def increment_likes(user_id: int, blog_id: int):
    query= reaction.insert().values(user_id= user_id, blog_id=blog_id, type='like')
    await database.execute(query)

    update_query = (
        update(blog)
        .where(blog.c.blog_id == blog_id)
        .values(likes=func.coalesce(blog.c.likes, 0) + 1)
    )
    return await database.execute(update_query)

async def increment_dislikes(user_id: int, blog_id: int):
    query= reaction.insert().values(user_id=user_id, blog_id=blog_id, type= 'dislike')
    await database.execute(query)
    
    id = (
        update(blog)
        .where(blog.c.blog_id == blog_id)
        .values(dislikes=func.coalesce(blog.c.dislikes, 0) + 1)
    )
    return await database.execute(id)

async def check_reaction(user_id: int, blog_id: int):
    query = select([reaction.c.type]). where(
        (reaction.c.user_id==user_id) & (reaction.c.blog_id== blog_id)
    )
    result = await database.fetch_one(query)
    return result['type'] if result else None

async def remove_reaction(user_id: int, blog_id: int):
    query= delete(reaction).where(
        (reaction.c.user_id==user_id)& (reaction.c.blog_id== blog_id)
    )
    return await database.execute(query)
