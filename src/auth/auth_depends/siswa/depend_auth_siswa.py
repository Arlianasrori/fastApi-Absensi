# Import necessary modules
from fastapi import Cookie, Request, Header
from ....models.siswa_model import Siswa
from ....error.errorHandling import HttpException
from ....db.sessionDepedency import sessionDepedency
from jose import JWTError, jwt
from sqlalchemy import select
import os

# Get the secret key for JWT token verification from environment variables
SECRET_KEY = os.getenv("SISWA_SECRET_ACCESS_TOKEN")

async def siswaDependAuth(access_token: str | None = Cookie(None), Authorization: str = Header(default=None, example="jwt access token"), req: Request = None, Session: sessionDepedency = None):
    """
    Authenticate a student (siswa) using JWT token.

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
        siswa = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        # Check if student information exists in the decoded token
        if not siswa:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Create a select query to find the student in the database
        selectQuery = select(Siswa.id, Siswa.nama, Siswa.token_FCM, Siswa.id_sekolah, Siswa.id_kelas, Siswa.id_tahun).where(Siswa.id == siswa["id"])
        exec = await Session.execute(selectQuery)
        findSiswa = exec.first()

        # Check if the student exists in the database
        if not findSiswa:
            raise HttpException(status=401, message="invalid token(unauthorized)")
        
        # Add student information to the request object
        req.siswa = findSiswa._asdict()
    except JWTError as error:
        # Handle JWT decoding errors
        raise HttpException(status=401, message=str(error.args[0]))
