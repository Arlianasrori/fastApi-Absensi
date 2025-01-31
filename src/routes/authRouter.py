from fastapi import APIRouter,Depends, Request,Response

# model and service
from ..domain.auth import authService
from ..domain.auth.authSchema import LoginRequest,ForgotPasswordResponse,ForgotPasswordIdentifyRequest,SendOtpAgainRequest,UpdatePasswordRequest,LoginResponse,RefreshTokenResponse,ValidationOTPRequest
from ..db.sessionDepedency import sessionDepedency

# schema
from ..domain.schemas.response_schema import ApiResponse,MessageOnlyResponse
from ..types.user_types import EnvSecretTokenType

# depends
from ..auth.auth_depends.developer.depend_refresh_auth_developer import developerRefreshAuth
from ..auth.auth_depends.admin.depend_refresh_auth_admin import adminrefreshAuth
from ..auth.auth_depends.siswa.depend_refresh_siswa_auth import siswaRefreshAuth
from ..auth.auth_depends.guru_mapel.depend_refresh_guru_mapel_auth import guruMapelRefreshAuth
from ..auth.auth_depends.guru_walas.depend_refresh_guru_walas_auth import guruWalasRefreshAuth
from ..auth.auth_depends.petugas_BK.depend_refresh_petugasBK_auth import petugasBKRefreshAuth


authRouter = APIRouter(prefix="/auth")


# admin developer auth
@authRouter.post("/adminDeveloper/login",response_model=ApiResponse[LoginResponse],tags=["AUTH/DEVELOPERADMIN"])
async def admin_developer_login(auth : LoginRequest,Res : Response,session : sessionDepedency) :
    return await authService.adminDeveloperLogin(auth,Res,session)

@authRouter.post("/developer/refreshToken",dependencies=[Depends(developerRefreshAuth)],response_model=ApiResponse[RefreshTokenResponse],tags=["AUTH/DEVELOPERADMIN"])
async def developer_refresh_token(Req : Request,Res : Response) :
    return await authService.refresh_token(Req.developer,EnvSecretTokenType.DEVELOPER,Res)

@authRouter.post("/admin/refreshToken",dependencies=[Depends(adminrefreshAuth)],response_model=ApiResponse[RefreshTokenResponse],tags=["AUTH/DEVELOPERADMIN"])
async def admin_refresh_token(Req : Request,Res : Response) :
    return await authService.refresh_token(Req.admin,EnvSecretTokenType.ADMIN,Res)


# public login
@authRouter.post("/public/login",response_model=ApiResponse[LoginResponse],tags=["AUTH/PUBLIC"])
async def public_login(auth : LoginRequest,Res : Response,session : sessionDepedency) :
    return await authService.publicLogin(auth,Res,session)

# siswa
@authRouter.post("/siswa/refreshToken",dependencies=[Depends(siswaRefreshAuth)],response_model=ApiResponse[RefreshTokenResponse],tags=["AUTH/SISWA"])
async def siswa_refresh_token(Req : Request,Res : Response) :
    return await authService.refresh_token(Req.siswa,EnvSecretTokenType.SISWA,Res)

# guru walas
@authRouter.post("/guruWalas/refreshToken",dependencies=[Depends(guruWalasRefreshAuth)],response_model=ApiResponse[RefreshTokenResponse],tags=["AUTH/GURUWALAS"])
async def guru_walas_refresh_token(Req : Request,Res : Response) :
    return await authService.refresh_token(Req.guruPembimbing,EnvSecretTokenType.GURU_WALAS,Res)

# guru mapel
@authRouter.post("/guruMapel/refreshToken",dependencies=[Depends(guruMapelRefreshAuth)],response_model=ApiResponse[RefreshTokenResponse],tags=["AUTH/GURUMAPEL"])
async def guru_mapel_refresh_token(Req : Request,Res : Response) :
    return await authService.refresh_token(Req.pembimbingDudi,EnvSecretTokenType.GURU_MAPEL,Res)

# guru petugas BK
@authRouter.post("/petugasBK/refreshToken",dependencies=[Depends(petugasBKRefreshAuth)],response_model=ApiResponse[RefreshTokenResponse],tags=["AUTH/PETUGASBK"])
async def petugas_BK_refresh_token(Req : Request,Res : Response) :
    return await authService.refresh_token(Req.pembimbingDudi,EnvSecretTokenType.PETUGAS_BK,Res)

# all logout
@authRouter.post("/logout",responses={"200" : {"content": {
                "application/json": {
                    "example" : {
                        "msg" : "logout success"
                    }
                }
            }}},tags=["AUTH"])
async def logout(Res : Response) :
    return await authService.logout(Res)

# reset password
@authRouter.post("/checkAccountAndSendOtp",response_model=ApiResponse[ForgotPasswordResponse],tags=["AUTH/RESET_PASSWORD"])
async def cek_akun_and_send_otp(textBody : ForgotPasswordIdentifyRequest,session : sessionDepedency = None) :
    return await authService.cekAkunAndSendOtp(textBody.textBody,session)

@authRouter.post("/sendOTPAgain",response_model=MessageOnlyResponse,tags=["AUTH/RESET_PASSWORD"])
async def sendUlangOTP(body : SendOtpAgainRequest,session : sessionDepedency) :
    return await authService.send_otp_again(body.id,body.role,session)

@authRouter.post("/validationOTP",response_model=MessageOnlyResponse,tags=["AUTH/RESET_PASSWORD"])
async def validationOTP(body : ValidationOTPRequest,session : sessionDepedency) :
    return await authService.check_otp(body.otp,body.role,session)

@authRouter.patch("/updatePassword",response_model=MessageOnlyResponse,tags=["AUTH/RESET_PASSWORD"])
async def update_password(body : UpdatePasswordRequest,session : sessionDepedency) :
    return await authService.update_password(body.id,body.role,body.password,body.OTP,session)

