from Database.db import database, blog
from sqlalchemy import func, update, select

async def update_reactions(user_id: int, blog_id: int, new_reaction: str):
    # Fetch current reactions
    query = select(blog.c.reactions).where(blog.c.blog_id == blog_id)
    current_reactions = await database.fetch_one(query)

    if not current_reactions:
        return "Blog not found"

    reactions = current_reactions["reactions"]
    if reactions is None:
        reactions = {}

    current_reaction = reactions.get(user_id)

    if current_reaction == new_reaction:
        # Reaction is the same as the new one, so do nothing
        return "No change in reaction"

    # Remove previous reaction if it exists
    if current_reaction:
        if current_reaction == "like":
            update_query = (
                update(blog)
                .where(blog.c.blog_id == blog_id)
                .values(
                    likes=func.coalesce(blog.c.likes, 0) - 1,
                    reactions={k: v for k, v in reactions.items() if k != user_id}
                )
            )
        elif current_reaction == "dislike":
            update_query = (
                update(blog)
                .where(blog.c.blog_id == blog_id)
                .values(
                    dislikes=func.coalesce(blog.c.dislikes, 0) - 1,
                    reactions={k: v for k, v in reactions.items() if k != user_id}
                )
            )
        await database.execute(update_query)

    # Add or update new reaction
    reactions[user_id] = new_reaction
    update_query = (
        update(blog)
        .where(blog.c.blog_id == blog_id)
        .values(
            likes=func.coalesce(blog.c.likes, 0) + (1 if new_reaction == "like" else 0),
            dislikes=func.coalesce(blog.c.dislikes, 0) + (1 if new_reaction == "dislike" else 0),
            reactions=reactions
        )
    )
    await database.execute(update_query)

    return f"Blog {new_reaction}d successfully"






