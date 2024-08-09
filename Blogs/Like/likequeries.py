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

async def increment_dislikes(user_id: int, blog_id: int, reaction: str):
    query= select(blog.c.reactions).where(blog.c.blog_id==blog_id)
    current_reactions= await database.fetch_one(query)

    if not current_reactions:
        return "Blog not found"
    
    reactions= current_reactions["reactions"]
    if reactions is None:
        reactions= {}

    if reactions.get(user_id)==reaction:
        return "Already disliked"
    
    reactions[user_id]= reaction

    update_query= (
        update(blog)
        .where(blog.c.blog_id== blog_id)
        .values(
            dislikes=  func.coalesce(blog.c.dislikes, 0)+1,
            reactions= reactions,
        )
    )
    
    await database.execute(update_query)

    return "Disliked"




