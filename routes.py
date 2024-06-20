from starlette.requests import Request
from starlette.responses import JSONResponse
from db import database, users
from auth import hash_password, verify_password, create_access_token

async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    query = users.select().where(users.c.username == username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        return JSONResponse({"error": "User already exists"}, status_code=400)

    hashed_password = hash_password(password)
    query = users.insert().values(username=username, hashed_password=hashed_password)
    await database.execute(query)
    return JSONResponse({"message": "User created successfully"}, status_code=201)

async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    if not user or not verify_password(password, user["hashed_password"]):
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)

    access_token = create_access_token(data={"sub": username})
    return JSONResponse({"access_token": access_token, "token_type": "bearer"})

async def protected_route(request: Request):
    user = request.state.user
    return JSONResponse({"message": f"Hello {user['sub']}"})