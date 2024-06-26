from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from Database.db import database, blog, comments
from sqlalchemy import select, update, delete


class BlogEndpoint(HTTPEndpoint):
    async def post(self, request: Request):
        data = await request.json()
        blog_description = data.get("blog_description")
        self_description = data.get("self_description")
        query = blog.insert().values(
            blog_description=blog_description, self_description=self_description
        )
        await database.execute(query)
        return JSONResponse({"message": "Blog created successfully"}, status_code=201)

    async def get(self, request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"error": "Blog ID path parameter is required"}, status_code=400
            )
        query = select(blog).where(blog.c.blog_id == blog_id)
        fetched_blog = await database.fetch_one(query)
        if not fetched_blog:
            return JSONResponse({"error": "Blog not found"}, status_code=404)
        blog_data = {
            "blog_description": fetched_blog["blog_description"],
            "self_description": fetched_blog["self_description"],
            # Add more fields as needed
        }
        return JSONResponse(blog_data)

    async def put(self, request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"error": "Blog ID path parameter is required"}, status_code=400
            )
        data = await request.json()
        blog_description = data.get("blog_description")
        self_description = data.get("self_description")
        query = (
            update(blog)
            .where(blog.c.blog_id == blog_id)
            .values(
                blog_description=blog_description, self_description=self_description
            )
        )
        await database.execute(query)
        return JSONResponse({"message": f"Blog with ID {blog_id} updated successfully"})

    async def delete(self, request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"error": "Blog ID path parameter is required"}, status_code=400
            )

        query_delete_comments = delete(comments).where(comments.c.blog_id == blog_id)
        await database.execute(query_delete_comments)

        query_delete_blog = delete(blog).where(blog.c.blog_id == blog_id)
        await database.execute(query_delete_blog)
        return JSONResponse({"message": f"Blog with ID {blog_id} deleted successfully"})


# class CommentEndpoint(HTTPEndpoint):
#     async def post(self, request: Request):
#         data = await request.json()
#         blog_id = request.path_params.get("blog_id")
#         comment_text = data.get("comment_text")
#         if not blog_id or not comment_text:
#             return JSONResponse(
#                 {"error": "Blog ID and comment text are required"}, status_code=400
#             )
#         query = comments.insert().values(
#             blog_id=blog_id,
#             comment_text=comment_text,
#             timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         )
#         await database.execute(query)
#         return JSONResponse({"message": "Comment added successfully"}, status_code=201)

#     async def get(self, request: Request):
#         blog_id = request.path_params.get("blog_id")
#         if not blog_id:
#             return JSONResponse(
#                 {"error": "Blog ID path parameter is required"}, status_code=400
#             )
#         query = (
#             select(comments)
#             .where(comments.c.blog_id == blog_id)
#             .order_by(comments.c.timestamp.desc())
#         )
#         fetched_comments = await database.fetch_all(query)
#         return JSONResponse([dict(comment) for comment in fetched_comments])

#     async def put(self, request: Request):
#         comment_id = request.path_params.get("comment_id")
#         if not comment_id:
#             return JSONResponse(
#                 {"error": "Comment ID path parameter is required"}, status_code=400
#             )
#         data = await request.json()
#         comment_text = data.get("comment_text")
#         if not comment_text:
#             return JSONResponse({"error": "Comment text is required"}, status_code=400)
#         query = (
#             update(comments)
#             .where(comments.c.comment_id == comment_id)
#             .values(comment_text=comment_text)
#         )
#         await database.execute(query)
#         return JSONResponse(
#             {"message": f"Comment with ID {comment_id} updated successfully"}
#         )

#     async def delete(self, request: Request):
#         comment_id = request.path_params.get("comment_id")
#         if not comment_id:
#             return JSONResponse(
#                 {"error": "Comment ID path parameter is required"}, status_code=400
#             )
#         query = delete(comments).where(comments.c.comment_id == comment_id)
#         await database.execute(query)
#         return JSONResponse(
#             {"message": f"Comment with ID {comment_id} deleted successfully"}
#         )
