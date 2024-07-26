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



#This is worked code
# from typing import List
# from Database.db import database, blog
# from sqlalchemy import select, insert, update, delete

# async def insert_blog(blog_description: str, self_description: str, images: str):
#     query = insert(blog).values(
#         blog_description=blog_description,
#         self_description=self_description,
#         images=images
#     ).returning(blog.c.blog_id)
    
#     blog_id = await database.execute(query=query)
#     return blog_id

# async def select_blog_by_id(blog_id: int):
#     query = select([blog.c.blog_description, blog.c.self_description, blog.c.images]).where(blog.c.blog_id == blog_id)
#     return await database.fetch_one(query=query)

# async def update_blog(blog_id: int, blog_description: str, self_description: str, images: str):
#     query = update(blog).where(blog.c.blog_id == blog_id).values(
#         blog_description=blog_description,
#         self_description=self_description,
#         images=images
#     )
#     await database.execute(query=query)

# async def delete_blog_and_images(blog_id: int):
#     query_delete_blog = delete(blog).where(blog.c.blog_id == blog_id)
#     await database.execute(query=query_delete_blog)




#This was the recent one
# from typing import List
# from Database.db import database, blog, comments
# from sqlalchemy import select, update, delete

# async def insert_blog(blog_description: str, self_description: str, images:str):
#     query = """
#     INSERT INTO blog (blog_description, self_description)
#     VALUES (:blog_description, :self_description)
#     RETURNING blog_id;
#     """
#     values = {
#         "blog_description": blog_description,
#         "self_description": self_description
#     }
#     blog_id = await database.execute(query=query, values=values)
#     return blog_id

# async def insert_images(blog_id: int, image_paths: List[str]):
#     try:
#         query = """
#         INSERT INTO image (blog_id, image_path) VALUES (:blog_id, :image_path)
#         """
#         values = [{"blog_id": blog_id, "image_path": path} for path in image_paths]
#         await database.execute_many(query=query, values=values)
#     except Exception as e:
#         print(f"Error inserting images: {e}")

# async def select_blog_by_id(blog_id: int):
#     query = """
#     SELECT blog_description, self_description FROM blog WHERE blog_id = :blog_id
#     """
#     return await database.fetch_one(query=query, values={"blog_id": blog_id})

# async def select_images_by_blog_id(blog_id: int):
#     query = """
#     SELECT image_path FROM image WHERE blog_id = :blog_id
#     """
#     return await database.fetch_all(query=query, values={"blog_id": blog_id})

# async def update_blog(blog_id: int, blog_description: str, self_description: str):
#     query = """
#     UPDATE blog
#     SET blog_description = :blog_description, self_description = :self_description
#     WHERE blog_id = :blog_id
#     """
#     values = {"blog_description": blog_description, "self_description": self_description, "blog_id": blog_id}
#     await database.execute(query=query, values=values)

# async def delete_blog_and_images(blog_id: int):
#     query_delete_images = images.delete().where(images.c.blog_id == blog_id)
#     await database.execute(query_delete_images)

#     query_delete_blog = blog.delete().where(blog.c.blog_id == blog_id)
#     await database.execute(query_delete_blog)





# from Database.db import database, blog, comments
# from sqlalchemy import func, select, update, delete, insert

# async def insert_blog(blog_description: str, self_description: str):
#     query = blog.insert().values(
#         blog_description=blog_description, self_description=self_description
#     )
#     return await database.execute(query)

# async def select_blog_by_id(blog_id: int):
#     query = select(blog).where(blog.c.blog_id == blog_id)
#     return await database.fetch_one(query)

# async def update_blog(blog_id: int, blog_description: str, self_description: str):
#     query = (
#         update(blog)
#         .where(blog.c.blog_id == blog_id)
#         .values(blog_description=blog_description, self_description=self_description)
#     )
#     return await database.execute(query)

# async def delete_blog_and_comments(blog_id: int):
#     query_delete_comments = delete(comments).where(comments.c.blog_id == blog_id)
#     await database.execute(query_delete_comments)

#     query_delete_blog = delete(blog).where(blog.c.blog_id == blog_id)
#     await database.execute(query_delete_blog)

