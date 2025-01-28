from pydantic import BaseModel
from ...types.user_types import GenderType
from datetime import date

class JurusanBase(BaseModel):
    id : int
    nama : str  
    id_sekolah : int
    id_tahun : int

class KelasBase(BaseModel) :
    id : int
    nama : str
    id_jurusan : int

# so that no circular depedency
class GuruWalasBase(BaseModel) :
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
    id_kelas : int
    token_FCM : str | None = None
    
class KelasWithGuruWalas(KelasBase) :
    guru_walas : GuruWalasBase | None

class JurusanWithKelas(JurusanBase) :
    kelas : list[KelasBase] = []

class KelasWithJurusan(KelasBase) :
    jurusan : JurusanBase
