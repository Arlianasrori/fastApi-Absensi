from pydantic import BaseModel
from .mapel_schema import MapelBase
from .kelasJurusan_schema import KelasBase
from .guruMapel_schema import GuruMapelBase
from .koordinatAbsen_schema import KoordinatAbsenKelasBase
from ...models.jadwal_model import HariEnum
from datetime import time

class JadwalBase(BaseModel):
    id : int
    hari : HariEnum
    jam_mulai : time
    jam_selesai : time

class JadwalWithMapel(JadwalBase) :
    mapel : MapelBase

class JadwalWithKoordinat(JadwalBase) :
    koordinat : KoordinatAbsenKelasBase

class JadwalWithMapel(JadwalBase) :
    mapel : MapelBase

class JadwalWithMapelGuruMapel(JadwalBase) :
    mapel : MapelBase
    guru_mapel : GuruMapelBase

class JadwalWithKoordinatGuruMapel(JadwalBase) :
    guru_mapel : GuruMapelBase
    koordinat : KoordinatAbsenKelasBase
    
class JadwalDetail(JadwalBase):
    mapel : MapelBase
    kelas : KelasBase
    guru_mapel : GuruMapelBase
    koordinat : KoordinatAbsenKelasBase
