from pydantic import BaseModel, field_validator,EmailStr
from ..schemas.passwordValidation_schema import PasswordValidation

class Developer(BaseModel) :
    id : int
    username : str
    no_telepon : str
    email : EmailStr

class AddSekolahRequest(BaseModel) :
    npsn : str
    nama : str

class UpdateSekolahRequest(BaseModel) :
    npsn : str | None = None
    nama : str | None = None

# admin
class AddAdminRequest(PasswordValidation) :
    id_sekolah : int
    username : str
    password : str
    no_telepon : str
    email : EmailStr
    
    @field_validator("username")
    def validate_username(cls, v):
        if " " in v:
            raise ValueError("username tidak bisa mengandung spasi")
        return v

class UpdateAdminRequest(PasswordValidation) :
    username : str | None = None
    password : str | None = None
    no_telepon : str | None = None
    email : EmailStr | None = None

    @field_validator("username")
    def validate_username(cls, v):
        if " " in v:
            raise ValueError("username tidak bisa mengandung spasi")
        return v