from pydantic import BaseModel
from ...types.user_types import UserType
from ..schemas.passwordValidation_schema import PasswordValidation

class LoginRequest(PasswordValidation) :
    textBody : str
    password : str

class LoginResponse(BaseModel) :
    access_token : str
    refresh_token : str
    role : UserType

class RefreshTokenResponse(BaseModel) :
    access_token : str
    refresh_token : str

class ForgotPasswordResponse(BaseModel) :
    id : int
    role : UserType
    email : str
    
class ForgotPasswordIdentifyRequest(BaseModel) :
    textBody : str

class SendOtpAgainRequest(BaseModel) :
    id : int
    role : UserType

class ValidationOTPRequest(BaseModel) :
    role : UserType
    otp : int

class UpdatePasswordRequest(BaseModel) :
    id : int
    OTP : int
    role : UserType
    password : str