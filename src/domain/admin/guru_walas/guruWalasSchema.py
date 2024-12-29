from pydantic import BaseModel,Field,EmailStr
from ....types.user_types import GenderType
from datetime import date
from ...schemas.guruWalas_schema import GuruWalasDetail
from ...schemas.pagination_schema import PaginationBase
from ...schemas.passwordValidation_schema import PasswordValidation

class AddGuruWalasRequest(PasswordValidation) :
    nip : str
    nama : str
    no_telepon : str 
    email : EmailStr
    jenis_kelamin : GenderType
    tempat_lahir : str
    tanggal_lahir : date
    agama : str
    password : str
    id_kelas : int
    id_tahun : int | None = None

class UpdateGuruWalasRequest(PasswordValidation) :
    nip : str | None = None
    nama : str | None = None
    no_telepon : str | None = None
    email : EmailStr | None = None
    jenis_kelamin : GenderType | None = None
    tempat_lahir : str | None = None
    tanggal_lahir : date | None = None
    agama : str | None = None
    foto_profile : str | None = None
    password : str | None = None
    id_kelas : int | None = None
    id_tahun : int | None = None

class ResponseGuruWalasPag(PaginationBase) :
    data : list[GuruWalasDetail] = []