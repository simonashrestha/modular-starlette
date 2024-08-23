from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from Users.Auth.auth import decode_access_token

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "Authorization" not in request.headers:
            return JSONResponse({"error": "Not Authorized"}, status_code=401)
        
        auth_header = request.headers["Authorization"]
        if not auth_header.startswith("Bearer "):
            return JSONResponse({"error": "Invalid authorization header"}, status_code=401)

        token = auth_header.split(" ")[1]
        payload = decode_access_token(token)
        if payload is None:
            return JSONResponse({"error": "Invalid token"}, status_code=401)

        request.state.user = payload
        response = await call_next(request)
        return response



# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import JSONResponse
# from Users.Auth.auth import decode_access_token

# class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # List of paths that should not require authentication
#         public_paths = ["/request-reset-password"]

#         if request.url.path in public_paths and request.method == "POST":
#             return await call_next(request)

#         if "Authorization" not in request.headers:
#             return JSONResponse({"error": "Not Authorized"}, status_code=401)
        
#         auth_header = request.headers["Authorization"]
#         if not auth_header.startswith("Bearer "):
#             return JSONResponse({"error": "Invalid authorization header"}, status_code=401)

#         token = auth_header.split(" ")[1]
#         payload = decode_access_token(token)
#         if payload is None:
#             return JSONResponse({"error": "Invalid token"}, status_code=401)

#         request.state.user = payload
#         response = await call_next(request)
#         return response





