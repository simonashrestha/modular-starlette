from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware import Middleware
from db import database
from middleware import JWTAuthenticationMiddleware
from routes import register, login, protected_route

routes = [
    Route("/register", register, methods=["POST"]),
    Route("/login", login, methods=["POST"]),
    Route("/protected", protected_route, methods=["GET"]),
]

middleware = [
    Middleware(JWTAuthenticationMiddleware)
]

app = Starlette(routes=routes, middleware=middleware)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
