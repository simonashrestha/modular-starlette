from starlette.requests import Request
from starlette.responses import JSONResponse
from Users.Auth.auth import hash_password, create_access_token, verify_password
from Users.queries import find_user_by_username, create_user, update_user_password, update_user_email, update_user_gender, delete_user_by_username
from starlette.endpoints import HTTPEndpoint

from pydantic import EmailStr, BaseModel, ValidationError # type: ignore
import re

class UserRegistrationRequest(BaseModel):
    username:str
    password:str
    email: EmailStr
    gender: str

class UserEndpoint (HTTPEndpoint):
    async def register(request: Request):
        try:
            data = await request.json()
            user_data= UserRegistrationRequest(**data)
        except ValidationError as e:
            return JSONResponse(
                {"message": f"validation error: {e.errors()}", "data": None},
                status_code=400
            )

        username = user_data.username
        password = user_data.password
        email = user_data.email
        gender = user_data.gender

        password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
        
        if not re.match(password_regex, password):
            return JSONResponse(
                {"message": "Password must be at least 8 characters long, and include uppercase letters, lowercase letters, digits, and special characters.", "data": None},
                status_code=400
            )

        existing_user = await find_user_by_username(username)
        if existing_user:
            return JSONResponse(
                {"message": "User already exists", "data": None},
                status_code=400
            )

        hashed_password = hash_password(password)
        await create_user(username, hashed_password, email, gender)
        return JSONResponse(
            {"message": "User created successfully", "data": {"username": username}},
            status_code=201
    )


    async def login(request: Request):
        data = await request.json()
        username = data.get("username")
        password = data.get("password")

        user = await find_user_by_username(username)
        if not user or not verify_password(password, user["hashed_password"]):
            return JSONResponse(
                {"message": "Invalid credentials", "data": None},
                status_code=401
            )

        access_token = create_access_token(data={"sub": username})
        return JSONResponse(
            {"message": "Login successful", "data": {"access_token": access_token, "token_type": "bearer"}},
            status_code=200
        )

    async def get_user(request: Request):
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

        user_data = {
            "username": user["username"],
            "email": user["email"],
            "gender": user["gender"]
        }
        return JSONResponse(
            {"message": "User retrieved successfully", "data": user_data},
            status_code=200
        )

    async def update_user(request: Request):
        username = request.path_params.get("username")
        if not username:
            return JSONResponse(
                {"message": "Username path parameter is required", "data": None},
                status_code=400
            )

        data = await request.json()
        new_password = data.get("password")
        email = data.get("email")
        gender = data.get("gender")

        user = await find_user_by_username(username)
        if not user:
            return JSONResponse(
                {"message": "User not found", "data": None},
                status_code=404
            )

        password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
    
        if new_password:
            if not re.match(password_regex, new_password):
                return JSONResponse(
                {"message": "Password must be at least 8 characters long, and include uppercase letters, lowercase letters, digits, and special characters.", "data": None},
                status_code=400
            )
        
        
            hashed_password = hash_password(new_password)
            await update_user_password(username, hashed_password)

        if email:
            await update_user_email(username, email)

        if gender:
            await update_user_gender(username, gender)

        return JSONResponse(
            {"message": f"User {username} updated successfully", "data": {"username": username}},
            status_code=200
        )

    async def delete_user(request: Request):
        username = request.path_params.get("username")
        if not username:
            return JSONResponse(
                {"message": "Username path parameter is required", "data": None},
                status_code=400
            )

        await delete_user_by_username(username)
        return JSONResponse(
            {"message": f"User {username} deleted successfully", "data": {"username": username}},
            status_code=200
        )

    async def protected_route(request: Request):
        user = request.state.user
        return JSONResponse(
            {"message": f"Hello {user['sub']}", "data": {"username": user["sub"]}},
            status_code=200
        )

# from arq import ArqRedis
# from arq.connections import RedisSettings
# from Email_Verification.arq_config import Settings
# from Email_Verification.tasks import send_verification_email
# import smtplib



# arq_redis= ArqRedis(Settings.redis_settings)

# class UserRegistrationRequest(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     gender: str

# class UserEndpoint(HTTPEndpoint):
#     async def register(self, request: Request):
#         try:
#             data = await request.json()
#             user_data = UserRegistrationRequest(**data)
#         except ValidationError as e:
#             return JSONResponse(
#                 {"message": f"Validation error: {e.errors()}", "data": None},
#                 status_code=400
#             )

#         username = user_data.username
#         password = user_data.password
#         email = user_data.email
#         gender = user_data.gender

#         password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
        
#         if not re.match(password_regex, password):
#             return JSONResponse(
#                 {"message": "Password must be at least 8 characters long, and include uppercase letters, lowercase letters, digits, and special characters.", "data": None},
#                 status_code=400
#             )

#         existing_user = await find_user_by_username(username)
#         if existing_user:
#             return JSONResponse(
#                 {"message": "User already exists", "data": None},
#                 status_code=400
#             )

#         hashed_password = hash_password(password)
#         await create_user(username, hashed_password, email, gender)
        
#         # Generate a verification link
#         verification_link = f"http://yourdomain.com/verify-email/{username}"  # Adjust according to your verification link structure
        
#         # Enqueue the email verification task
#         await arq_redis.enqueue_job('send_verification_email', email, verification_link)

#         return JSONResponse(
#             {"message": "User created successfully, verification email sent", "data": {"username": username}},
#             status_code=201
#         )
    
#     async def verify_email(self, request:Request):
#         username= request.path_params['username']
#         user= await find_user_by_username(username)
#         if user is None:
#             return JSONResponse(
#                 {"message": "User not found", "data": None},
#                 status_code=404
#             )
        
#         if not user['need_verification']:
#             return JSONResponse(
#                 {"message": "Email already verified", "data": None},
#                 status_code=400
#             )
        
#         await update_user_verification_status(username, True)
#         return JSONResponse(
#             {"message": "Email successfully verified", "data": {"username": username}},
#             status_code=200
#         )
    
#     async def login(request: Request):
#         data = await request.json()
#         username = data.get("username")
#         password = data.get("password")

#         user = await find_user_by_username(username)
#         if not user or not verify_password(password, user["hashed_password"]):
#             return JSONResponse(
#                 {"message": "Invalid credentials", "data": None},
#                 status_code=401
#             )

#         access_token = create_access_token(data={"sub": username})
#         return JSONResponse(
#             {"message": "Login successful", "data": {"access_token": access_token, "token_type": "bearer"}},
#             status_code=200
#         )

#     async def get_user(request: Request):
#         username = request.path_params.get("username")
#         if not username:
#             return JSONResponse(
#                 {"message": "Username path parameter is required", "data": None},
#                 status_code=400
#             )

#         user = await find_user_by_username(username)
#         if not user:
#             return JSONResponse(
#                 {"message": "User not found", "data": None},
#                 status_code=404
#             )

#         user_data = {
#             "username": user["username"],
#             "email": user["email"],
#             "gender": user["gender"]
#         }
#         return JSONResponse(
#             {"message": "User retrieved successfully", "data": user_data},
#             status_code=200
#         )

#     async def update_user(request: Request):
#         username = request.path_params.get("username")
#         if not username:
#             return JSONResponse(
#                 {"message": "Username path parameter is required", "data": None},
#                 status_code=400
#             )

#         data = await request.json()
#         new_password = data.get("password")
#         email = data.get("email")
#         gender = data.get("gender")

#         user = await find_user_by_username(username)
#         if not user:
#             return JSONResponse(
#                 {"message": "User not found", "data": None},
#                 status_code=404
#             )

#         password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
    
#         if new_password:
#             if not re.match(password_regex, new_password):
#                 return JSONResponse(
#                 {"message": "Password must be at least 8 characters long, and include uppercase letters, lowercase letters, digits, and special characters.", "data": None},
#                 status_code=400
#             )
        
        
#             hashed_password = hash_password(new_password)
#             await update_user_password(username, hashed_password)

#         if email:
#             await update_user_email(username, email)

#         if gender:
#             await update_user_gender(username, gender)

#         return JSONResponse(
#             {"message": f"User {username} updated successfully", "data": {"username": username}},
#             status_code=200
#         )

#     async def delete_user(request: Request):
#         username = request.path_params.get("username")
#         if not username:
#             return JSONResponse(
#                 {"message": "Username path parameter is required", "data": None},
#                 status_code=400
#             )

#         await delete_user_by_username(username)
#         return JSONResponse(
#             {"message": f"User {username} deleted successfully", "data": {"username": username}},
#             status_code=200
#         )

#     async def protected_route(request: Request):
#         user = request.state.user
#         return JSONResponse(
#             {"message": f"Hello {user['sub']}", "data": {"username": user["sub"]}},
#             status_code=200
#         )













