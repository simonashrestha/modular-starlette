from starlette.responses import JSONResponse
from starlette.requests import Request
from pydantic import BaseModel, ValidationError # type: ignore
import re
from Users.queries import find_user_by_email, update_user_password
from Users.Auth.auth import create_password_reset_token, decode_password_reset_token, hash_password
from Email_Verification.email_tasks import send_password_reset_email

class RequestPasswordResetData(BaseModel):
    email: str

async def request_password_reset(request: Request):
    try:
        data = await request.json()
        reset_data = RequestPasswordResetData(**data)
    except ValidationError as e:
        return JSONResponse(
            {"message": f"Validation error: {e.errors()}", "data": None},
            status_code=400
        )

    email = reset_data.email

    user = await find_user_by_email(email)
    if not user:
        return JSONResponse(
            {"message": "User not found", "data": None},
            status_code=404
        )

    reset_token = create_password_reset_token(email)
    await send_password_reset_email(email, reset_token)

    return JSONResponse(
        {"message": "Password reset email sent successfully", "data": None},
        status_code=200
    )

class PasswordResetData(BaseModel):
    new_password: str
    confirm_new_password: str

async def reset_password(request: Request):
    try:
        data = await request.json()
        reset_data = PasswordResetData(**data)
    except ValidationError as e:
        return JSONResponse(
            {"message": f"Validation error: {e.errors()}", "data": None},
            status_code=400
        )

    new_password = reset_data.new_password
    confirm_new_password = reset_data.confirm_new_password

    if new_password != confirm_new_password:
        return JSONResponse(
            {"message": "Passwords do not match", "data": None},
            status_code=400
        )

    token = request.query_params.get("token")  # Extract the token from the query parameters
    if not token:
        return JSONResponse(
            {"message": "Token is required", "data": None},
            status_code=400
        )

    decoded_token = decode_password_reset_token(token)
    if not decoded_token:
        return JSONResponse(
            {"message": "Invalid or expired token", "data": None},
            status_code=400
        )

    email = decoded_token.get("sub")
    if not email:
        return JSONResponse(
            {"message": "Invalid token data", "data": None},
            status_code=400
        )

    user = await find_user_by_email(email)
    if not user:
        return JSONResponse(
            {"message": "User not found", "data": None},
            status_code=404
        )

    password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"

    if not re.match(password_regex, new_password):
        return JSONResponse(
            {"message": "Password must be at least 8 characters long and include uppercase letters, lowercase letters, digits, and special characters.", "data": None},
            status_code=400
        )

    hashed_password = hash_password(new_password)
    await update_user_password(email, hashed_password)  # Assuming `update_user_password` uses email as identifier

    return JSONResponse(
        {"message": "Password reset successfully", "data": {"email": email}},
        status_code=200
    )
