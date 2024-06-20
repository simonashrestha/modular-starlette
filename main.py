from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from db import database
from middleware import JWTAuthenticationMiddleware
from routes import register, login, protected_route

public_routes = [
    Route("/register", register, methods=["POST"]),
    Route("/login", login, methods=["POST"]),
]
protected_routes = [
    Route("/protected", protected_route, methods=["GET"]),
]

middleware = [
    Middleware(JWTAuthenticationMiddleware)
]

protected_app = Starlette(routes=protected_routes, middleware=middleware)

app = Starlette(
    routes = [
        *public_routes,
        Mount("/", app=protected_app),
    ]
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
