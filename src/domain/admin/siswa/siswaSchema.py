from pydantic import BaseModel,field_validator,EmailStr
from ...schemas.passwordValidation_schema import PasswordValidation
from ...schemas.pagination_schema import PaginationBase
from ...schemas.siswa_schema import SiswaWithJurusanKelasAlamat

class AddSiswaRequest(PasswordValidation) :
    nis : str
    nama : str
    jenis_kelamin : str
    no_telepon : str
    email : EmailStr
    id_kelas : int
    id_jurusan : int
    id_tahun : int
    password : str | None = None

class UpdateSiswaRequest(PasswordValidation) :
    nis : str | None = None
    nama : str | None = None
    jenis_kelamin : str | None = None
    no_telepon : str | None = None
    email : EmailStr | None = None
    id_kelas : int | None = None
    id_jurusan : int | None = None
    password : str | None = None

class ResponseSiswaPag(PaginationBase) :
    data : list[SiswaWithJurusanKelasAlamat] = []