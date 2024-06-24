from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from db import database
from middleware import JWTAuthenticationMiddleware
from userroutes import register, login, protected_route, get_user, update_user, delete_user
from blogroutes import blog_routes

public_routes = [
    Route("/register", register, methods=["POST"]),
    Route("/login", login, methods=["POST"]),
]

protected_routes = [
    Route("/protected", protected_route, methods=["GET"]),
    Route("/{username}", get_user, methods=["GET"]),
    Route("/{username}", update_user, methods=["PUT"]),
    Route("/{username}", delete_user, methods=["DELETE"]),
    Route("/blog", blog_routes.create_blog, methods=["POST"]),
    Route("/blog/{blog_id}", blog_routes.get_blog, methods=["GET"]),
    Route("/blog/{blog_id}", blog_routes.update_blog, methods=["PUT"]),
    Route("/blog/{blog_id}", blog_routes.delete_blog, methods=["DELETE"]),
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
