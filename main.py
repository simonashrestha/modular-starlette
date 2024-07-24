from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from Blogs.endpoint import BlogEndpoint, get_file
from Database.db import database
from middleware import JWTAuthenticationMiddleware
from Users.endpoint import UserEndpoint
from Comments.endpoint import CommentEndpoint
from Blogs.Like.likeroutes import LikeEndpoint

public_routes = [
    Route("/register", UserEndpoint.register, methods=["POST"]),
    Route("/login", UserEndpoint.login, methods=["POST"]),
]

protected_routes = [
    Route("/protected", UserEndpoint.protected_route, methods=["GET"]),
    Route("/{username}", UserEndpoint.get_user, methods=["GET"]),
    Route("/{username}", UserEndpoint.update_user, methods=["PUT"]),
    Route("/{username}", UserEndpoint.delete_user, methods=["DELETE"]),
    Route("/blogs", BlogEndpoint, methods=["POST"]),
    Route("/blogs/{blog_id:int}", BlogEndpoint, methods=["GET", "PUT", "DELETE"]),
    Route("/blogs/{blog_id:int}/like", LikeEndpoint.post_like, methods=["POST"]),
    Route("/blogs/{blog_id:int}/dislike", LikeEndpoint.post_dislikes, methods=["POST"]),
    Route("/comments/{blog_id:int}", CommentEndpoint, methods=["POST"]),
    Route("/blogs/{blog_id:int}/comments", CommentEndpoint, methods=["GET"]),
    Route("/comments/{comment_id:int}", CommentEndpoint, methods=["PUT", "DELETE"]),
    Route("/files/{filename}", get_file, methods=["GET"]),
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




# from starlette.applications import Starlette
# from starlette.routing import Route, Mount
# from starlette.middleware import Middleware
# from Blogs.Like.likeroutes import LikeEndpoint
# from Database.db import database
# from middleware import JWTAuthenticationMiddleware
# from Users.endpoint import UserEndpoint
# from Blogs.endpoint import BlogEndpoint
# from Comments.endpoint import CommentEndpoint



# public_routes = [
#     Route("/register", UserEndpoint.register, methods=["POST"]),
#     Route("/login", UserEndpoint.login, methods=["POST"]),
# ]

# protected_routes = [
#     Route("/protected", UserEndpoint.protected_route, methods=["GET"]),
#     Route("/{username}", UserEndpoint.get_user, methods=["GET"]),
#     Route("/{username}", UserEndpoint.update_user, methods=["PUT"]),
#     Route("/{username}", UserEndpoint.delete_user, methods=["DELETE"]),
#     Route("/blogs", BlogEndpoint, methods=["POST"]),
#     Route("/blogs/{blog_id:int}", BlogEndpoint, methods=["GET", "PUT", "DELETE"]),
#     Route("/blogs/{blog_id:int}/like", LikeEndpoint.post_like, methods=["POST"]),
#     Route("/blogs/{blog_id:int}/dislike", LikeEndpoint.post_dislikes, methods=["POST"]),
#     Route("/comments/{blog_id:int}", CommentEndpoint, methods=["POST"]),
#     Route("/blogs/{blog_id:int}/comments", CommentEndpoint, methods=["GET"]),
#     Route("/comments/{comment_id:int}", CommentEndpoint, methods=["PUT","DELETE"]),
# ]

# middleware = [
#     Middleware(JWTAuthenticationMiddleware)
# ]

# protected_app = Starlette(routes=protected_routes, middleware=middleware)

# app = Starlette(
#     routes=[
#         *public_routes,
#         Mount("/", app=protected_app),
#     ]
# )

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


