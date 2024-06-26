from Database.db import database, users
from Auth.auth import hash_password
from sqlalchemy import select, update, delete, insert

async def find_user_by_username(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)

async def create_user(username: str, hashed_password: str, email: str, gender: str):
    query = users.insert().values(username=username, hashed_password=hashed_password, email=email, gender=gender)
    return await database.execute(query)

async def update_user_password(username: str, hashed_password: str):
    query = users.update().where(users.c.username == username).values(hashed_password=hashed_password)
    return await database.execute(query)

async def update_user_email(username: str, email: str):
    query = users.update().where(users.c.username == username).values(email=email)
    return await database.execute(query)

async def update_user_gender(username: str, gender: str):
    query = users.update().where(users.c.username == username).values(gender=gender)
    return await database.execute(query)

async def delete_user_by_username(username: str):
    query = users.delete().where(users.c.username == username)
    return await database.execute(query)
