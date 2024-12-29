from pydantic import BaseModel
from ...types.user_types import GenderType
from datetime import date
from .alamat_schema import AlamatBase
from .kelasJurusan_schema import KelasBase
class PetugasBkBase(BaseModel) :
    id : int
    nip : str
    nama : str
    no_telepon : str
    email : str
    jenis_kelamin : GenderType
    tempat_lahir : str
    tanggal_lahir : date
    agama : str
    foto_profile : str | None = None
    id_sekolah : int
    id_tahun : int
    token_FCM : str | None = None

class PetugasBKWithAlamat(PetugasBkBase) :
    alamat : AlamatBase

class DistribusiPetugasBKBase(BaseModel) :
    id : int
    kelas : KelasBase

class PetugasBKWithAlamatAndDistribusi(PetugasBKWithAlamat) :
    distribusi_petugas_BK : list[DistribusiPetugasBKBase] | None = None