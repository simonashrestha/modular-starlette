from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from Auth.auth import decode_access_token

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header= request.headers.get("Authorization")
        # if "Authorization" not in request.headers:
        #     return JSONResponse({"error": "Not Authorized"}, status_code=401)
        # auth_header = request.headers["Authorization"]
        auth_header= request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse({"error": "Invalid authorization header"}, status_code=401)

        token = auth_header.split("Bearer ", "")
        payload = decode_access_token(token)
        if payload is None:
            return JSONResponse({"error": "Invalid token"}, status_code=401)

        request.state.user = payload
        response = await call_next(request)
        return response
