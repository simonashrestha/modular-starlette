from starlette.requests import Request
from starlette.responses import JSONResponse
from db import database, blog

async def create_blog(request: Request):
    data = await request.json()
    blog_description = data.get("blog_description")
    self_description = data.get("self_description")
    query = blog.insert().values(blog_description=blog_description, self_description=self_description)
    await database.execute(query)
    return JSONResponse({"message": "Blog created successfully"}, status_code=201)

async def get_blog(request: Request):
    blog_id = request.path_params.get("blog_id")
    if not blog_id:
        return JSONResponse({"error": "Blog ID path parameter is required"}, status_code=400)
    query = blog.select().where(blog.c.blog_id == blog_id)
    fetched_blog = await database.fetch_one(query)
    if not fetched_blog:
        return JSONResponse({"error": "Blog not found"}, status_code=404)
    blog_data = {
        "blog_description": fetched_blog["blog_description"],
        "self_description": fetched_blog["self_description"]
        # Add more fields as needed
    }
    return JSONResponse(blog_data)

async def update_blog(request: Request):
    blog_id = request.path_params.get("blog_id")
    if not blog_id:
        return JSONResponse({"error": "Blog ID path parameter is required"}, status_code=400)
    data = await request.json()
    blog_description = data.get("blog_description")
    self_description = data.get("self_description")
    query = blog.update().where(blog.c.blog_id == blog_id).values(
        blog_description=blog_description,
        self_description=self_description
    )
    await database.execute(query)
    return JSONResponse({"message": f"Blog with ID {blog_id} updated successfully"})

async def delete_blog(request: Request):
    blog_id = request.path_params.get("blog_id")
    if not blog_id:
        return JSONResponse({"error": "Blog ID path parameter is required"}, status_code=400)
    query = blog.delete().where(blog.c.blog_id == blog_id)
    await database.execute(query)
    return JSONResponse({"message": f"Blog with ID {blog_id} deleted successfully"})
