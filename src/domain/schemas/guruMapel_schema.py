from pydantic import BaseModel
from ...types.user_types import GenderType
from datetime import date
from .mapel_schema import MapelBase
from .alamat_schema import AlamatBase
from .sekolah_schema import SekolahBase

class GuruMapelBase(BaseModel) :
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
    id_mapel : int
    token_FCM : str | None = None

class GuruMapelWithMapel(GuruMapelBase) :
    mapel : MapelBase

class GuruMapelWithAlamat(GuruMapelBase) :
    alamat : AlamatBase

class GuruMapeldetail(GuruMapelBase) :
    alamat : AlamatBase
    mapel : MapelBase

class GuruMapelDetailWithSekolah(GuruMapeldetail) :
    sekolah : SekolahBase