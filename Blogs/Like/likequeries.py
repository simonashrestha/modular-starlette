from Database.db import database, blog
from sqlalchemy import func, update, select

async def increment_likes(user_id: int, blog_id: int, reaction: str):
    # Fetch the current reactions for the blog
    query = select(blog.c.reactions).where(blog.c.blog_id == blog_id)
    current_reactions = await database.fetch_one(query)
    
    if not current_reactions:
        return "Blog not found"
    
    reactions = current_reactions["reactions"]
    if reactions is None:
        reactions = {}

    # Check if the user has already liked the blog
    if reactions.get(user_id) == reaction:
        return "Already liked"

    # Update the reactions
    reactions[user_id] = reaction

    update_query = (
        update(blog)
        .where(blog.c.blog_id == blog_id)
        .values(
            likes=func.coalesce(blog.c.likes, 0) + 1,
            reactions=reactions,
        )
    )
    await database.execute(update_query)

    return "Liked"

#This is working code:
# async def increment_likes(blog_id: int):
#     query = (
#         update(blog)
#         .where(blog.c.blog_id == blog_id)
#         .values(likes=func.coalesce(blog.c.likes, 0) + 1)
#     )
#     return await database.execute(query)

async def increment_dislikes(blog_id: int):
    id = (
        update(blog)
        .where(blog.c.blog_id == blog_id)
        .values(dislikes=func.coalesce(blog.c.dislikes, 0) + 1)
    )
    return await database.execute(id)

