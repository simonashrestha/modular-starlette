import os
import shutil
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse
from starlette.endpoints import HTTPEndpoint
from starlette.datastructures import UploadFile
from Blogs.queries import (
    insert_blog,
    select_blog_by_id,
    update_blog,
    delete_blog_and_comments,
)
from repo import AbstractRepository

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class BlogEndpoint(HTTPEndpoint, AbstractRepository):
    async def post(self, request: Request):
        form = await request.form()
        blog_description = form.get("blog_description")
        self_description = form.get("self_description")
        image: UploadFile = form.get("image")

        if not blog_description or not self_description:
            return JSONResponse(
                {"message": "Both blog_description and self_description are required", "data": None},
                status_code=400,
            )

        image_filename = None
        if image:
            image_filename = os.path.join(UPLOAD_DIR, image.filename)
            with open(image_filename, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

        blog_id = await insert_blog(blog_description, self_description, image_filename)
        return JSONResponse(
            {"message": "Blog created successfully", "data": {"blog_id": blog_id}},
            status_code=201,
        )

    async def get(self, request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"message": "Blog ID path parameter is required", "data": None},
                status_code=400,
            )

        fetched_blog = await select_blog_by_id(blog_id)
        if not fetched_blog:
            return JSONResponse(
                {"message": "Blog not found", "data": None}, status_code=404
            )

        blog_data = {
            "blog_description": fetched_blog["blog_description"],
            "self_description": fetched_blog["self_description"],
            "image": fetched_blog["image"]
        }
        return JSONResponse(
            {"message": "Blog retrieved successfully", "data": blog_data},
            status_code=200,
        )

    async def put(self, request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"message": "Blog ID path parameter is required", "data": None},
                status_code=400,
            )

        form = await request.form()
        blog_description = form.get("blog_description")
        self_description = form.get("self_description")
        image: UploadFile = form.get("image")

        if not blog_description or not self_description:
            return JSONResponse(
                {
                    "message": "Both blog_description and self_description are required",
                    "data": None,
                },
                status_code=400,
            )

        image_filename = None
        if image:
            image_filename = os.path.join(UPLOAD_DIR, image.filename)
            with open(image_filename, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

        await update_blog(blog_id, blog_description, self_description, image_filename)
        return JSONResponse(
            {
                "message": f"Blog with ID {blog_id} updated successfully",
                "data": {"blog_id": blog_id},
            },
            status_code=200,
        )

    async def delete(self, request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"message": "Blog ID path parameter is required", "data": None},
                status_code=400,
            )

        await delete_blog_and_comments(blog_id)
        return JSONResponse(
            {
                "message": f"Blog with ID {blog_id} deleted successfully",
                "data": {"blog_id": blog_id},
            },
            status_code=200,
        )

async def get_file(request: Request):
    filename = request.path_params["filename"]
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse({"detail": "File not found"}, status_code=404)
    return FileResponse(file_path)



# class BlogEndpoint(HTTPEndpoint, AbstractRepository):
#     async def post(self, request: Request):
#         data = await request.json()

#         blog_description = data.get("blog_description")
#         self_description = data.get("self_description")
       
#         if not blog_description or not self_description:
#             return JSONResponse(
#                 {
#                     "message": "Both blog_description and self_description are required",
#                     "data": None,
#                 },
#                 status_code=400,
#             )

#         blog_id = await insert_blog(blog_description, self_description)
#         return JSONResponse(
#             {"message": "Blog created successfully", "data": {"blog_id": blog_id}},
#             status_code=201,
#         )

#     async def get(self, request: Request):
#         blog_id = request.path_params.get("blog_id")
#         if not blog_id:
#             return JSONResponse(
#                 {"message": "Blog ID path parameter is required", "data": None},
#                 status_code=400,
#             )

#         fetched_blog = await select_blog_by_id(blog_id)
#         if not fetched_blog:
#             return JSONResponse(
#                 {"message": "Blog not found", "data": None}, status_code=404
#             )

#         blog_data = {
#             "blog_description": fetched_blog["blog_description"],
#             "self_description": fetched_blog["self_description"],
#         }
#         return JSONResponse(
#             {"message": "Blog retrieved successfully", "data": blog_data},
#             status_code=200,
#         )

#     async def put(self, request: Request):
#         blog_id = request.path_params.get("blog_id")
#         if not blog_id:
#             return JSONResponse(
#                 {"message": "Blog ID path parameter is required", "data": None},
#                 status_code=400,
#             )

#         data = await request.json()
#         blog_description = data.get("blog_description")
#         self_description = data.get("self_description")

#         if not blog_description or not self_description:
#             return JSONResponse(
#                 {
#                     "message": "Both blog_description and self_description are required",
#                     "data": None,
#                 },
#                 status_code=400,
#             )

#         await update_blog(blog_id, blog_description, self_description)
#         return JSONResponse(
#             {
#                 "message": f"Blog with ID {blog_id} updated successfully",
#                 "data": {"blog_id": blog_id},
#             },
#             status_code=200,
#         )

#     async def delete(self, request: Request):
#         blog_id = request.path_params.get("blog_id")
#         if not blog_id:
#             return JSONResponse(
#                 {"message": "Blog ID path parameter is required", "data": None},
#                 status_code=400,
#             )

#         await delete_blog_and_comments(blog_id)
#         return JSONResponse(
#             {
#                 "message": f"Blog with ID {blog_id} deleted successfully",
#                 "data": {"blog_id": blog_id},
#             },
#             status_code=200,
#         )


   