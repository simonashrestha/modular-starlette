from typing import List
from Database.db import database, blog
from sqlalchemy import select, insert, update, delete

async def insert_blog(blog_description: str, self_description: str, images: str):
    query = insert(blog).values(
        blog_description=blog_description,
        self_description=self_description,
        images=images
    ).returning(blog.c.blog_id)
    
    blog_id = await database.execute(query=query)
    return blog_id

async def select_blog_by_id(blog_id: int):
    query = select(blog.c.blog_description, blog.c.self_description, blog.c.images).where(blog.c.blog_id == blog_id)
    return await database.fetch_one(query=query)

async def update_blog(blog_id: int, blog_description: str, self_description: str, images: str):
    query = update(blog).where(blog.c.blog_id == blog_id).values(
        blog_description=blog_description,
        self_description=self_description,
        images=images
    )
    await database.execute(query=query)

async def delete_blog_and_images(blog_id: int):
    query_delete_blog = delete(blog).where(blog.c.blog_id == blog_id)
    await database.execute(query=query_delete_blog)





