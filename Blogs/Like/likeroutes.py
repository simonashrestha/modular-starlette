from starlette.requests import Request
from starlette.responses import JSONResponse
from Blogs.Like.likequeries import increment_likes, increment_dislikes

async def post_like(request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"message": "Blog ID path parameter is required", "data": None},
                status_code=400,
            )

        try:
            blog_id = int(blog_id)
        except ValueError:
            return JSONResponse(
            {"message": "Blog ID must be an integer", "data": None}, status_code=400
        )

        await increment_likes(blog_id)
        return JSONResponse(
        {
            "message": f"Blog with ID {blog_id} liked successfully",
            "data": {"blog_id": blog_id},
        },
        status_code=200,
    )

async def post_dislikes(request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"message": "Blog ID path parameter is required", "data": None},
                status_code=400,
            )

        try:
            blog_id = int(blog_id)
        except ValueError:
            return JSONResponse(
            {"message": "Blog ID must be an integer", "data": None}, status_code=400
        )

        await increment_dislikes(blog_id)
        return JSONResponse(
        {
            "message": f"Blog with ID {blog_id} disliked successfully",
            "data": {"blog_id": blog_id},
        },
        status_code=200,
    )

