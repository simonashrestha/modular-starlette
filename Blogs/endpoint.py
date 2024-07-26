import os
import shutil
import json
from typing import List
from starlette.requests import Request
from starlette.responses import JSONResponse, FileResponse
from starlette.endpoints import HTTPEndpoint
from starlette.datastructures import UploadFile
from Blogs.queries import (
    insert_blog,
    select_blog_by_id,
    update_blog,
    delete_blog_and_images,
)
from repo import AbstractRepository

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class BlogEndpoint(HTTPEndpoint, AbstractRepository):
    async def post(self, request: Request):
        form = await request.form()
        blog_description = form.get("blog_description")
        self_description = form.get("self_description")
        images: List[UploadFile] = form.getlist("images")

        if not blog_description or not self_description:
            return JSONResponse(
                {"message": "Both blog_description and self_description are required", "data": None},
                status_code=400,
            )
        
        # Save images
        image_filenames = []
        for image in images:
            image_filename = os.path.join(UPLOAD_DIR, image.filename)
            with open(image_filename, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_filenames.append(image_filename)

        # Convert list of filenames to JSON format
        image_filenames_json = json.dumps(image_filenames)

        # Insert blog entry
        blog_id = await insert_blog(blog_description, self_description, image_filenames_json)
        
        if not blog_id:
            return JSONResponse(
                {"message": "Failed to create blog entry", "data": None},
                status_code=500,
            )

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

        # Convert JSON string to list of image filenames
        image_paths = json.loads(fetched_blog["images"])

        blog_data = {
            "blog_description": fetched_blog["blog_description"],
            "self_description": fetched_blog["self_description"],
            "images": image_paths
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
        images: List[UploadFile] = form.getlist("images")

        if not blog_description or not self_description:
            return JSONResponse(
                {"message": "Both blog_description and self_description are required", "data": None},
                status_code=400,
            )

        image_filenames = []
        if images:
            for image in images:
                image_filename = os.path.join(UPLOAD_DIR, image.filename)
                with open(image_filename, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                image_filenames.append(image_filename)

            # Convert list of filenames to JSON format
            image_filenames_json = json.dumps(image_filenames)
        else:
            image_filenames_json = None

        await update_blog(blog_id, blog_description, self_description, image_filenames_json)

        return JSONResponse(
            {"message": f"Blog with ID {blog_id} updated successfully", "data": {"blog_id": blog_id}},
            status_code=200,
        )

    async def delete(self, request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"message": "Blog ID path parameter is required", "data": None},
                status_code=400,
            )

        await delete_blog_and_images(blog_id)
        return JSONResponse(
            {"message": f"Blog with ID {blog_id} deleted successfully", "data": {"blog_id": blog_id}},
            status_code=200,
        )

    async def get_file(self, request: Request):
        filename = request.path_params["filename"]
        file_path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            return JSONResponse({"detail": "File not found"}, status_code=404)
        return FileResponse(file_path)



#this is the updated one 
# import os
# import shutil
# from typing import List
# from starlette.requests import Request
# from starlette.responses import FileResponse, JSONResponse
# from starlette.endpoints import HTTPEndpoint
# from starlette.datastructures import UploadFile
# from Blogs.queries import (
#     delete_blog_and_images,
#     insert_blog,
#     insert_images,
#     select_blog_by_id,
#     select_images_by_blog_id,
#     update_blog,
# )
# from repo import AbstractRepository

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# class BlogEndpoint(HTTPEndpoint,AbstractRepository):
#     async def post(self, request: Request):
#         form = await request.form()
#         blog_description = form.get("blog_description")
#         self_description = form.get("self_description")
#         images: List[UploadFile] = form.getlist("images")

#         if not blog_description or not self_description:
#             return JSONResponse(
#                 {"message": "Both blog_description and self_description are required", "data": None},
#                 status_code=400,
#             )
#         # Insert blog entry
#         blog_id = await insert_blog(blog_description, self_description)
#         if not blog_id:
#             return JSONResponse(
#                 {"message": "Failed to create blog entry", "data": None},
#                 status_code=500,
#             )
        
#     # Save images
#         image_filenames = []
#         print("images", images)
#         for image in images:
#             image_filename = os.path.join(UPLOAD_DIR, image.filename)
#             print("image", image_filename)
#             with open(image_filename, "wb") as buffer:
#                 shutil.copyfileobj(image.file, buffer)
#             image_filenames.append(image_filename)
#         print ("empty", image_filenames)
#         # Insert images
#         if image_filenames:
#             await insert_images(blog_id, image_filenames)

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

#         fetched_images = await select_images_by_blog_id(blog_id)
#         image_paths = [img["image_path"] for img in fetched_images]

#         blog_data = {
#             "blog_description": fetched_blog["blog_description"],
#             "self_description": fetched_blog["self_description"],
#             "images": image_paths
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

#         form = await request.form()
#         blog_description = form.get("blog_description")
#         self_description = form.get("self_description")
#         images: List[UploadFile] = form.getlist("images")

#         if not blog_description or not self_description:
#             return JSONResponse(
#                 {"message": "Both blog_description and self_description are required", "data": None},
#                 status_code=400,
#             )

#         await update_blog(blog_id, blog_description, self_description)

#         if images:
#             await delete_blog_and_images(blog_id)
#             image_filenames = []
#             for image in images:
#                 image_filename = os.path.join(UPLOAD_DIR, image.filename)
#                 with open(image_filename, "wb") as buffer:
#                     shutil.copyfileobj(image.file, buffer)
#                 image_filenames.append(image_filename)
#             await insert_images(blog_id, image_filenames)

#         return JSONResponse(
#             {"message": f"Blog with ID {blog_id} updated successfully", "data": {"blog_id": blog_id}},
#             status_code=200,
#         )

#     async def delete(self, request: Request):
#         blog_id = request.path_params.get("blog_id")
#         if not blog_id:
#             return JSONResponse(
#                 {"message": "Blog ID path parameter is required", "data": None},
#                 status_code=400,
#             )

#         await delete_blog_and_images(blog_id)
#         return JSONResponse(
#             {"message": f"Blog with ID {blog_id} deleted successfully", "data": {"blog_id": blog_id}},
#             status_code=200,
#         )




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


   