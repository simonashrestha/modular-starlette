from starlette.requests import Request
from starlette.responses import JSONResponse
from Database.db import database, users
from Auth.auth import hash_password, verify_password, create_access_token

async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    gender = data.get("gender")
    query = users.select().where(users.c.username == username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        return JSONResponse(
            {"message": "User already exists", "data": None},
            status_code=400
        )
    hashed_password = hash_password(password)
    query = users.insert().values(username=username, hashed_password=hashed_password, email=email, gender=gender)
    await database.execute(query)
    return JSONResponse(
        {"message": "User created successfully", "data": {"username": username}},
        status_code=201
    )

async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
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
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
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

    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    if not user:
        return JSONResponse(
            {"message": "User not found", "data": None},
            status_code=404
        )

    # Update hashed_password if new_password is provided
    if new_password:
        hashed_password = hash_password(new_password)
        query = users.update().where(users.c.username == username).values(hashed_password=hashed_password)
        await database.execute(query)

    # Update email if provided
    if email:
        query = users.update().where(users.c.username == username).values(email=email)
        await database.execute(query)

    # Update gender if provided
    if gender:
        query = users.update().where(users.c.username == username).values(gender=gender)
        await database.execute(query)

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
    query = users.delete().where(users.c.username == username)
    await database.execute(query)
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
