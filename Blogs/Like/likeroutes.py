from starlette.requests import Request
from starlette.responses import JSONResponse
from Blogs.Like.likequeries import increment_likes, increment_dislikes, check_reaction, remove_reaction

async def post_like(request: Request):
        blog_id = request.path_params.get("blog_id")
        user_id= request.user['id']

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

        current_reaction= await check_reaction(user_id, blog_id)

        if current_reaction=="dislike":
             await remove_reaction(user_id, blog_id)
        
        if current_reaction !="like":
             await increment_likes(user_id, blog_id)
        
        return JSONResponse(
        {
            "message": f"Blog with ID {blog_id} liked successfully",
            "data": {"blog_id": blog_id},
        },
        status_code=200,
    )

async def post_dislikes(request: Request):
        blog_id = request.path_params.get("blog_id")
        user_id= request.user['id']

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

        current_reaction= await check_reaction(user_id, blog_id)

        if current_reaction=="like":
             await remove_reaction(user_id, blog_id)

        if current_reaction !="dislike":
            await increment_dislikes(user_id, blog_id)
        return JSONResponse(
        {
            "message": f"Blog with ID {blog_id} disliked successfully",
            "data": {"blog_id": blog_id},
        },
        status_code=200,
    )


