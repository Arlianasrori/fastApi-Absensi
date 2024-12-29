# Import necessary modules
from fastapi import Cookie, Request, Header
from ....models.guru_mapel_model import GuruMapel
from ....error.errorHandling import HttpException
from ....db.sessionDepedency import sessionDepedency
from jose import JWTError, jwt
from sqlalchemy import select
import os

# Get the secret key for JWT token verification from environment variables
SECRET_KEY = os.getenv("GURU_MAPEL_SECRET_ACCESS_TOKEN")

async def guruMapelDependAuth(access_token: str | None = Cookie(None), Authorization: str = Header(default=None, example="jwt access token"), req: Request = None, Session: sessionDepedency = None):
    """
    Authenticate a guru mapel (teacher) using JWT token.

    Args:
        access_token (str | None): The JWT token from cookies.
        Authorization (str): The JWT token from the Authorization header.
        req (Request): The FastAPI request object.
        Session (sessionDepedency): The database session dependency.

    Raises:
        HttpException: If authentication fails.

    Returns:
        None
    """
    try:
        # Determine the token source (cookie or Authorization header)
        token = None
        if access_token:
            token = access_token
        elif Authorization:
            token = Authorization.split(" ")[1]
        
        # Check if a token is present
        if not token:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Decode and verify the JWT token
        guruMapel = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        # Check if guru mapel information exists in the decoded token
        if not guruMapel:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Create a select query to find the guru mapel in the database
        findGuruMapel = (await Session.execute(select(GuruMapel).where(GuruMapel.id == guruMapel["id"]))).scalar_one_or_none()

        # Check if the guru mapel exists in the database
        if not findGuruMapel:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Add guru mapel information to the request object
        req.guruMapel = findGuruMapel.__dict__
    except JWTError as error:
        # Handle JWT decoding errors
        raise HttpException(status=401, message=str(error.args[0]))
