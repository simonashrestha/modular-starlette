from starlette.requests import Request
from starlette.responses import JSONResponse
from Users.queries import find_user_by_username, update_user_verification_status
from starlette.endpoints import HTTPEndpoint


class EmailVerificationEndpoint(HTTPEndpoint):
    async def get(self, request: Request):
        username = request.path_params.get("username")
        if not username:
            return JSONResponse(
                {"message": "Username path parameter is required", "data": None},
                status_code=400
            )

        user = await find_user_by_username(username)
        if not user:
            return JSONResponse(
                {"message": "User not found", "data": None},
                status_code=404
            )

        # Update the user's verification status
        await update_user_verification_status(username, verified=True)

        return JSONResponse(
            {"message": f"User {username} verified successfully", "data": {"username": username}},
            status_code=200
        )