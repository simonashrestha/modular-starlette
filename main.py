from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from db import database
from middleware import JWTAuthenticationMiddleware
from userroutes import register, login, protected_route, get_user, update_user, delete_user
from blogroutes import BlogEndpoint,CommentEndpoint

public_routes = [
    Route("/register", register, methods=["POST"]),
    Route("/login", login, methods=["POST"]),
]

protected_routes = [
    Route("/protected", protected_route, methods=["GET"]),
    Route("/{username}", get_user, methods=["GET"]),
    Route("/{username}", update_user, methods=["PUT"]),
    Route("/{username}", delete_user, methods=["DELETE"]),
    Route("/blogs", BlogEndpoint, methods=["POST"]),
    Route("/blogs/{blog_id:int}", BlogEndpoint, methods=["GET", "PUT", "DELETE"]),
    Route("/comments/{blog_id:int}", CommentEndpoint, methods=["POST"]),
    Route("/blogs/{blog_id:int}/comments", CommentEndpoint, methods=["GET"]),
    Route("/comments/{comment_id:int}", CommentEndpoint, methods=["PUT","DELETE"]),
]

middleware = [
    Middleware(JWTAuthenticationMiddleware)
]

protected_app = Starlette(routes=protected_routes, middleware=middleware)

app = Starlette(
    routes=[
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
