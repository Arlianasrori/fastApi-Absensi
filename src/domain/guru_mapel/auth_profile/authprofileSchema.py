from pydantic import BaseModel
from pydantic import EmailStr
from ....types.user_types import GenderType 

class UpdateProfileRequest(BaseModel):
    nama : str | None = None 
    jenis_kelamin : GenderType | None = None
    no_telepon : str | None = None 
    email : EmailStr | None = None
    token_FCM : str | None = None