from starlette.requests import Request
from starlette.responses import JSONResponse
from db import database, users
from auth import hash_password, verify_password, create_access_token

async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    gender = data.get("gender")
    query = users.select().where(users.c.username == username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        return JSONResponse({"error": "User already exists"}, status_code=400)
    hashed_password = hash_password(password)
    query = users.insert().values(username=username, hashed_password=hashed_password, email=email, gender=gender)
    await database.execute(query)
    return JSONResponse({"message": "User created successfully"}, status_code=201)

async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    print(user)
    if not user or not verify_password(password, user["hashed_password"]):
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)
    access_token = create_access_token(data={"sub": username})
    return JSONResponse({"access_token": access_token, "token_type": "bearer"})

async def get_user(request: Request):
    username = request.path_params.get("username")
    if not username:
        return JSONResponse({"error": "Username path parameter is required"}, status_code=400)
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)
    user_data = {
        "username": user["username"],
        "hashed_password": user["hashed_password"],
        "email": user["email"],  
        "gender": user["gender"]
    }
    return JSONResponse(user_data)

async def update_user (request: Request):
    username = request.path_params.get("username")
    if not username:
        return JSONResponse({"error": "Username path parameter is required"}, status_code=400)
    data = await request.json()
    print(data)
    new_password = data.get("password")
    email = data.get("email")
    gender = data.get("gender")

    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)

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

    return JSONResponse({"message": f"User {username} updated successfully"})

async def delete_user(request: Request):
    username = request.path_params.get("username")
    if not username:
        return JSONResponse({"error": "Username path parameter is required"}, status_code=400)
    query = users.delete().where(users.c.username == username)
    await database.execute(query)
    return JSONResponse({"message": f"User {username} deleted successfully"})

async def protected_route(request: Request):
    user = request.state.user
    return JSONResponse({"message": f"Hello {user['sub']}"})