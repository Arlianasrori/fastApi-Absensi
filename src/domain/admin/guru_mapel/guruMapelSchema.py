from pydantic import BaseModel,EmailStr,Field
from ....types.user_types import GenderType
from datetime import date
from ...schemas.guruMapel_schema import GuruMapeldetail
from ...schemas.pagination_schema import PaginationBase
from ...schemas.passwordValidation_schema import PasswordValidation

class AddGuruMapelRequest(PasswordValidation) :
    nip : str
    nama : str
    no_telepon : str
    email : EmailStr
    jenis_kelamin : GenderType
    tempat_lahir : str
    tanggal_lahir : date
    agama : str
    password : str
    id_mapel : int
    id_tahun : int | None = None

class UpdateGuruMapelRequest(PasswordValidation) :
    nip : str | None = None
    nama : str | None = None
    no_telepon : str | None = None
    email : EmailStr | None = None
    jenis_kelamin : GenderType | None = None
    tempat_lahir : str | None = None
    tanggal_lahir : date | None = None
    agama : str | None = None
    password : str | None = None
    id_mapel : int | None = None
    id_tahun : int | None = None

class ResponseGuruMapelPag(PaginationBase) :
    data : list[GuruMapeldetail] = []