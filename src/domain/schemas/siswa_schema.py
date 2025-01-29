from pydantic import BaseModel,EmailStr
from .alamat_schema import AlamatBase
from .kelasJurusan_schema import JurusanBase,KelasBase,KelasWithGuruWalas
from .guruWalas_schema import GuruWalasBase
from .sekolah_schema import SekolahBase
class SiswaBase(BaseModel) :
    id : int
    nis : str
    nama : str
    jenis_kelamin : str
    email : EmailStr
    no_telepon : str
    token_FCM : str | None = None
    foto_profile : str | None = None

class SiswaWithKelas(SiswaBase) :
    kelas : KelasBase
    
class SiswaWithKelasWalas(SiswaBase) :
    kelas : KelasWithGuruWalas

class SiswaWithAlamat(SiswaBase) :
    alamat : AlamatBase | None = None

class SiswaWithJurusanKelasAlamat(SiswaBase) :
    jurusan : JurusanBase
    alamat : AlamatBase | None = None
    kelas : KelasBase

class SiswaDetailWithSekolah(SiswaWithJurusanKelasAlamat) :
    sekolah : SekolahBase
