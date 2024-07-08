from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from Comments.queries import (
    insert_comment,
    select_comments_by_blog_id,
    update_comment,
    delete_comment,
)
from repo import AbstractRepository


class CommentEndpoint(HTTPEndpoint, AbstractRepository):
    async def post(self, request: Request):
        data = await request.json()
        blog_id = request.path_params.get("blog_id")
        comment_text = data.get("comment_text")
        if not blog_id or not comment_text:
            return JSONResponse(
                {"message": "Blog ID and comment text are required", "data": None},
                status_code=400,
            )

        comment_id = await insert_comment(blog_id, comment_text)
        return JSONResponse(
            {
                "message": "Comment added successfully",
                "data": {"comment_id": comment_id},
            },
            status_code=201,
        )

    async def get(self, request: Request):
        blog_id = request.path_params.get("blog_id")
        if not blog_id:
            return JSONResponse(
                {"message": "Blog ID path parameter is required", "data": None},
                status_code=400,
            )

        fetched_comments = await select_comments_by_blog_id(blog_id)
        comments_data = [dict(comment) for comment in fetched_comments]
        return JSONResponse(
            {"message": "Comments retrieved successfully", "data": comments_data},
            status_code=200,
        )

    async def put(self, request: Request):
        comment_id = request.path_params.get("comment_id")
        if not comment_id:
            return JSONResponse(
                {"message": "Comment ID path parameter is required", "data": None},
                status_code=400,
            )

        data = await request.json()
        comment_text = data.get("comment_text")
        if not comment_text:
            return JSONResponse(
                {"message": "Comment text is required", "data": None}, status_code=400
            )

        await update_comment(comment_id, comment_text)
        return JSONResponse(
            {
                "message": f"Comment with ID {comment_id} updated successfully",
                "data": {"comment_id": comment_id},
            },
            status_code=200,
        )

    async def delete(self, request: Request):
        comment_id = request.path_params.get("comment_id")
        if not comment_id:
            return JSONResponse(
                {"message": "Comment ID path parameter is required", "data": None},
                status_code=400,
            )

        await delete_comment(comment_id)
        return JSONResponse(
            {
                "message": f"Comment with ID {comment_id} deleted successfully",
                "data": {"comment_id": comment_id},
            },
            status_code=200,
        )
