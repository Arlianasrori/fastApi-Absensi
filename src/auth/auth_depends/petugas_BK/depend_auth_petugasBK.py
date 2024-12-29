# Import necessary modules
from fastapi import Cookie, Request, Header
from ....models.petugas_BK_model import PetugasBK
from ....error.errorHandling import HttpException
from ....db.sessionDepedency import sessionDepedency
from jose import JWTError, jwt
from sqlalchemy import select
import os

# Get the secret key for JWT token verification from environment variables
SECRET_KEY = os.getenv("PETUGAS_BK_SECRET_ACCESS_TOKEN")

async def petugasBKDependAuth(access_token: str | None = Cookie(None), Authorization: str = Header(default=None, example="jwt access token"), req: Request = None, Session: sessionDepedency = None):
    """
    Authenticate a petugas bk (school counselor) using JWT token.

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
        petugasBK = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        # Check if petugas BK information exists in the decoded token
        if not petugasBK:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Create a select query to find the petugas BK in the database
        findPetugasBK = (await Session.execute(select(PetugasBK).where(PetugasBK.id == petugasBK["id"]))).scalar_one_or_none()

        # Check if the petugas BK exists in the database
        if not findPetugasBK:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Add petugas BK information to the request object
        req.petugasBK = findPetugasBK.__dict__
    except JWTError as error:
        # Handle JWT decoding errors
        raise HttpException(status=401, message=str(error.args[0]))
