from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# schemas
from .authSchema import LoginRequest,LoginResponse,RefreshTokenResponse,ForgotPasswordResponse

# models
from ...models.developer_model import Developer
from ...models.sekolah_model import Admin
from ...models.siswa_model import Siswa
from ...models.guru_mapel_model import GuruMapel
from ...models.guru_walas_model import GuruWalas
from ...models.petugas_BK_model import PetugasBK

# types
from ...types.user_types import UserType,EnvSecretTokenType

# common
from ...error.errorHandling import HttpException
from ...auth.bcrypt.bcrypt import verify_hash_password
from ...auth.token.create_token import create_token
from ...utils.sendOtp_util import sendOtp
# admin developer
async def adminDeveloperLogin(auth : LoginRequest,Res : Response,session : AsyncSession) -> LoginResponse :
    """
    Authenticate admin or developer login.

    Args:
        auth (LoginBody): Login credentials.
        Res (Response): FastAPI response object.
        session (AsyncSession): Database session.

    Returns:
        ResponseAuthToken: Authentication token and role.

    Raises:
        HttpException: If authentication fails.
    """
    # find developer and check developer
    findDeveloper = (await session.execute(select(Developer).where(Developer.username == auth.textBody))).scalar_one_or_none()

    if findDeveloper :
        isPassword = auth.password == findDeveloper.password

        if isPassword :
            token_payload = {"id" : findDeveloper.id}

            token = create_token(token_payload,EnvSecretTokenType.DEVELOPER)
            Res.set_cookie("access_token",token["access_token"])
            Res.set_cookie("refresh_token",token["refresh_token"])

            return {
                "msg" : "login success",              
                "data" : {
                    **token,
                    "role" : UserType.DEVELOPER
                }
            }

    # find admin and check admin
    findAdmin = (await session.execute(select(Admin).where(Admin.username == auth.textBody))).scalar_one_or_none()

    if findAdmin :
        isPassword = verify_hash_password(auth.password,findAdmin.password)

        if isPassword :
            token_payload = {"id" : findAdmin.id}

            token = create_token(token_payload,EnvSecretTokenType.ADMIN)
            Res.set_cookie("access_token",token["access_token"])
            Res.set_cookie("refresh_token",token["refresh_token"])

            return {
                "msg" : "login success",              
                "data" : {
                    **token,
                    "role" : UserType.ADMIN
                }
            }
            
    raise HttpException(status=400,message="username atau password salah")


async def publicLogin(auth : LoginRequest,Res : Response,session : AsyncSession) -> LoginResponse :
    # find siswa and check siswa
    findSiswa = (await session.execute(select(Siswa).where(Siswa.nis == auth.textBody))).scalar_one_or_none()

    if findSiswa :
        isPassword = verify_hash_password(auth.password,findSiswa.password)

        if isPassword :
            token_payload = {"id" : findSiswa.id}

            token = create_token(token_payload,EnvSecretTokenType.SISWA)
            Res.set_cookie("access_token",token["access_token"])
            Res.set_cookie("refresh_token",token["refresh_token"])

            return {
                "msg" : "login success",              
                "data" : {
                    **token,
                    "role" : UserType.SISWA
                }
            }
        
    # find guru walas and check guru walas
    findGuruWalas = (await session.execute(select(GuruWalas).where(GuruWalas.nip == auth.textBody))).scalar_one_or_none()

    if findGuruWalas :
        isPassword = verify_hash_password(auth.password,findGuruWalas.password)

        if isPassword :
            token_payload = {"id" : findGuruWalas.id}

            token = create_token(token_payload,EnvSecretTokenType.GURU_WALAS)
            Res.set_cookie("access_token",token["access_token"])
            Res.set_cookie("refresh_token",token["refresh_token"])

            return {
                "msg" : "login success",              
                "data" : {
                    **token,
                    "role" : UserType.GURU_WALAS
                }
            }
        
    # find guru mapel and check guru mapel
    findGuruMapel = (await session.execute(select(GuruMapel).where(GuruMapel.nip == auth.textBody))).scalar_one_or_none()

    if findGuruMapel :
        isPassword = verify_hash_password(auth.password,findGuruMapel.password)

        if isPassword :
            token_payload = {"id" : findGuruMapel.id}

            token = create_token(token_payload,EnvSecretTokenType.GURU_MAPEL)
            Res.set_cookie("access_token",token["access_token"])
            Res.set_cookie("refresh_token",token["refresh_token"])

            return {
                "msg" : "login success",              
                "data" : {
                    **token,
                    "role" : UserType.GURU_MAPEL
                }
            }
        
    # find petugas BK and check petugas BK
    findPetugasBK = (await session.execute(select(PetugasBK).where(PetugasBK.nip == auth.textBody))).scalar_one_or_none()

    if findPetugasBK :
        isPassword = verify_hash_password(auth.password,findPetugasBK.password)

        if isPassword :
            token_payload = {"id" : findGuruMapel.id}

            token = create_token(token_payload,EnvSecretTokenType.PETUGAS_BK)
            Res.set_cookie("access_token",token["access_token"])
            Res.set_cookie("refresh_token",token["refresh_token"])

            return {
                "msg" : "login success",              
                "data" : {
                    **token,
                    "role" : UserType.PETUGAS_BK
                }
            }
    raise HttpException(status=400,message="nis/nip atau password salah")


async def refresh_token(data,envSecretType : EnvSecretTokenType,Res : Response) -> RefreshTokenResponse :
    """
    Refresh authentication token for user.

    Args:
        data: User data.
        Res (Response): FastAPI response object.

    Returns:
        ResponseRefreshToken: New authentication token.
    """
    token_payload = {"id" : data["id"]}

    token = create_token(token_payload,envSecretType)
    Res.set_cookie("access_token",token["access_token"],httponly=True,max_age="24 * 60 * 60 * 60")
    Res.set_cookie("refresh_token",token["refresh_token"],httponly=True,max_age="24 * 60 * 60 * 60 * 60")
    return {
        "msg" : "succes",
        "data" : token
    }

#logout
async def logout(Res : Response) :
    """
    Log out user by deleting authentication cookies.

    Args:
        Res (Response): FastAPI response object.

    Returns:
        dict: Success message.
    """
    Res.delete_cookie("access_token")
    Res.delete_cookie("refresh_token")
    return {
        "msg" : "logout success"
    }

async def cekAkunAndSendOtp(textBody : str,session : AsyncSession) -> ForgotPasswordResponse :
    # find developer and check developer
    findDeveloper = (await session.execute(select(Developer).where(Developer.username == textBody))).scalar_one_or_none()

    if findDeveloper :
        otp = await sendOtp(findDeveloper.email)
        findDeveloper.OTP_code = otp
        await session.commit()
        await session.refresh(findDeveloper)
        return {       
            "msg" : "OTP berhasil dikirim",   
            "data" : {
                "id" : findDeveloper.id,
                "role" : UserType.DEVELOPER,
                "email" : findDeveloper.email
            }
        }

    # find admin and check admin
    findAdmin = (await session.execute(select(Admin).where(Admin.username == textBody))).scalar_one_or_none()

    if findAdmin :
        otp = await sendOtp(findAdmin.email)
        findAdmin.OTP_code = otp
        await session.commit()
        await session.refresh(findAdmin)
        return {
            "msg" : "OTP berhasil dikirim",              
            "data" : {
                "id" : findAdmin.id,
                "role" : UserType.ADMIN,
                "email" : findAdmin.email
            }
        }

    # find siswa and check siswa
    findSiswa = (await session.execute(select(Siswa).where(Siswa.nis == textBody))).scalar_one_or_none()

    if findSiswa :
        otp = await sendOtp(findSiswa.email)
        findSiswa.OTP_code = otp
        await session.commit()
        await session.refresh(findSiswa)
        return {
            "msg" : "OTP berhasil dikirim",              
            "data" : {
                "id" : findSiswa.id,
                "role" : UserType.SISWA,
                "email" : findSiswa.email
            }
        }
        
    # find guru walas and check guru walas
    findGuruWalas = (await session.execute(select(GuruWalas).where(GuruWalas.nip == textBody))).scalar_one_or_none()

    if findGuruWalas :
        otp = await sendOtp(findGuruWalas.email)
        findGuruWalas.OTP_code = otp
        await session.commit()
        await session.refresh(findGuruWalas)
        return {
            "msg" : "OTP berhasil dikirim",              
            "data" : {
                "id" : findGuruWalas.id,
                "role" : UserType.GURU_WALAS,
                "email" : findGuruWalas.email
            }
        }
        
    # find guru mapel and check guru mapel
    findGuruMapel = (await session.execute(select(GuruMapel).where(GuruMapel.nip == textBody))).scalar_one_or_none()

    if findGuruMapel :
        otp = await sendOtp(findGuruMapel.email)
        findGuruMapel.OTP_code = otp
        await session.commit()
        await session.refresh(findGuruMapel)
        return {
            "msg" : "send message success",              
            "data" : {
                "id" : findGuruMapel.id,
                "role" : UserType.GURU_MAPEL,

                "email" : findGuruMapel.email,
            }
        }
    
    raise HttpException(status=400,message="akun tidak ditemukan")

async def check_otp(otp : str,role : UserType,session : AsyncSession) -> bool :
    if role == UserType.DEVELOPER :
        findDeveloper = (await session.execute(select(Developer).where(Developer.OTP_code == otp))).scalar_one_or_none()

        if findDeveloper :
            return {
                "msg" : "otp is valid"
            }       
    elif role == UserType.ADMIN :
        findAdmin = (await session.execute(select(Admin).where(Admin.OTP_code == otp))).scalar_one_or_none()

        if findAdmin :
            return {
                "msg" : "otp is valid"
            }
        
    elif role == UserType.SISWA :
        findSiswa = (await session.execute(select(Siswa).where(Siswa.OTP_code == otp))).scalar_one_or_none()
    
        if findSiswa :
            return {
                "msg" : "otp is valid"

            }
        
    elif role == UserType.GURU_WALAS :
        findGuruWalas = (await session.execute(select(GuruWalas).where(GuruWalas.OTP_code == otp))).scalar_one_or_none()

        if findGuruWalas :
            return {
                "msg" : "otp is valid"
            }

    elif role == UserType.GURU_MAPEL :
        findGuruMapel = (await session.execute(select(GuruMapel).where(GuruMapel.OTP_code == otp))).scalar_one_or_none()

        if findGuruMapel :
            return {
                "msg" : "otp is valid"
            }
        
    raise HttpException(status=400,message="otp is not valid")    

async def send_otp_again(id : int,role : UserType,session : AsyncSession) :
    if role == UserType.DEVELOPER :
        findDeveloper = (await session.execute(select(Developer).where(Developer.id == id))).scalar_one_or_none()

        if findDeveloper :
            otp = await sendOtp(findDeveloper.email)
            findDeveloper.OTP_code = otp
            await session.commit()

            return {
                "msg" : "send message success"
            }
    elif role == UserType.ADMIN :
        findAdmin = (await session.execute(select(Admin).where(Admin.id == id))).scalar_one_or_none()

        if findAdmin :
            otp = await sendOtp(findAdmin.email)
            findAdmin.OTP_code = otp
            await session.commit()
            
            return {
                "msg" : "send message success"
            }     
    elif role == UserType.SISWA :
        findSiswa = (await session.execute(select(Siswa).where(Siswa.id == id))).scalar_one_or_none()

        if findSiswa :
            otp = await sendOtp(findSiswa.email)
            findSiswa.OTP_code = otp
            await session.commit()
            
            return {
                "msg" : "send message success"
            }
        
    elif role == UserType.GURU_WALAS :
        findGuruWalas = (await session.execute(select(GuruWalas).where(GuruWalas.id == id))).scalar_one_or_none()

        if findGuruWalas :
            otp = await sendOtp(findGuruWalas.email)
            findGuruWalas.OTP_code = otp
            await session.commit()
            
            return {
                "msg" : "send message success"
            }

    elif role == UserType.GURU_MAPEL :
        findGuruMapel = (await session.execute(select(GuruMapel).where(GuruMapel.id == id))).scalar_one_or_none()

        if findGuruMapel :
            otp = await sendOtp(findGuruMapel.email)
            findGuruMapel.OTP_code = otp
            await session.commit()
            
            return {
                "msg" : "send message success"
            }
        
    raise HttpException(status=400,message="akun tidak ditemukan")

async def update_password(id : int,role : UserType,password : str,OTP : int,session : AsyncSession) :
    if role == UserType.DEVELOPER :
        findDeveloper = (await session.execute(select(Developer).where(Developer.id == id))).scalar_one_or_none()

        if findDeveloper :
            if findDeveloper.OTP_code == OTP :
                findDeveloper.password = password
                await session.commit()

                return {
                    "msg" : "update password success"
                }
            
    elif role == UserType.ADMIN :
        findAdmin = (await session.execute(select(Admin).where(Admin.id == id))).scalar_one_or_none()

        if findAdmin :
            if findAdmin.OTP_code == OTP :
                findAdmin.password = password
                await session.commit()
                
                return {
                    "msg" : "update password success"
                }
        
    elif role == UserType.SISWA :
        findSiswa = (await session.execute(select(Siswa).where(Siswa.id == id))).scalar_one_or_none()

        if findSiswa :
            if findSiswa.OTP_code == OTP :
                findSiswa.password = password
                await session.commit()  
            
                return {
                    "msg" : "update password success"
                }
        
    elif role == UserType.GURU_WALAS :
        findGuruWalas = (await session.execute(select(GuruWalas).where(GuruWalas.id == id))).scalar_one_or_none()

        if findGuruWalas :
            if findGuruWalas.OTP_code == OTP :
                findGuruWalas.password = password
                await session.commit()
                
                return {
                    "msg" : "update password success"
                }

    elif role == UserType.GURU_MAPEL :
        findGuruMapel = (await session.execute(select(GuruMapel).where(GuruMapel.id == id))).scalar_one_or_none()

        if findGuruMapel :
            if findGuruMapel.OTP_code == OTP :
                findGuruMapel.password = password
                await session.commit()
                
                return {
                        "msg" : "update password success"
                    }
        
    raise HttpException(status=400,message="akun tidak ditemukan")
