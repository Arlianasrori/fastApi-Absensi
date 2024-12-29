# Import necessary modules
from fastapi import Cookie, Request, Header
from ....models.guru_mapel_model import GuruMapel
from ....error.errorHandling import HttpException
from ....db.sessionDepedency import sessionDepedency
from jose import JWTError, jwt
from sqlalchemy import select
import os

# Get the secret key for refresh token from environment variables
SECRET_KEY = os.getenv("GURU_MAPEL_SECRET_REFRESH_TOKEN")

async def guruMapelRefreshAuth(refresh_token: str | None = Cookie(None), Authorization: str = Header(default=None, example="jwt access token"), req: Request = None, Session: sessionDepedency = None):
    """
    Authenticate a guru mapel using refresh token.

    Args:
        refresh_token (str | None): The JWT refresh token from cookies.
        Authorization (str): The JWT refresh token from the Authorization header.
        req (Request): The FastAPI request object.
        Session (sessionDepedency): The database session dependency.

    Raises:
        HttpException: If authentication fails.

    Returns:
        None
    """
    try:
        # Determine the token source (cookie or Authorization header)
        if refresh_token:
            token = refresh_token
        elif Authorization:
            token = Authorization.split(" ")[1]
        
        # Check if a token is present
        if not token:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Decode and verify the JWT refresh token
        mapel = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        # Check if guru mapel information exists in the decoded token
        if not mapel:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Create a select query to find the guru walas in the database
        findGuruMapel = (await Session.execute(select(GuruMapel).where(GuruMapel.id == mapel["id"]))).scalar_one_or_none()

        # Check if the guru walas exists in the database
        if not findGuruMapel:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Add guru walas information to the request object
        req.guruMapel = findGuruMapel.__dict__
    except JWTError as error:
        # Handle JWT decoding errors
        raise HttpException(status=401, message=str(error.args[0]))
