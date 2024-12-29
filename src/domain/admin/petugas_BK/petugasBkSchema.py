from pydantic import BaseModel
from ....types.user_types import GenderType
from datetime import date
from ...schemas.petugasBK_schema import PetugasBKWithAlamatAndDistribusi
from ...schemas.pagination_schema import PaginationBase
from ...schemas.passwordValidation_schema import PasswordValidation

class AddDistribusiPetugasBKRequest(BaseModel) :
    id_kelas : int

class AddPetugasBKRequest(PasswordValidation) :
    nip : str
    nama : str
    no_telepon : str
    email : str
    jenis_kelamin : GenderType
    tempat_lahir : str
    tanggal_lahir : date
    agama : str
    password : str
    id_tahun : int | None = None
    distribusi_kelas : list[AddDistribusiPetugasBKRequest] | None = None

class UpdatePetugasBKRequest(PasswordValidation) :
    nip : str | None = None
    nama : str | None = None
    no_telepon : str | None = None
    email : str | None = None
    jenis_kelamin : GenderType | None = None
    tempat_lahir : str | None = None
    tanggal_lahir : date | None = None
    agama : str | None = None
    password : str | None = None
    id_tahun : int | None = None

class AddDistribusiPetugasBKRequest(BaseModel) :
    id_kelas : int

class ResponsePetugasBKPag(PaginationBase) :
    data : list[PetugasBKWithAlamatAndDistribusi] = []