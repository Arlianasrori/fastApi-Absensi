from pydantic import BaseModel
from .mapel_schema import MapelBase
from .kelasJurusan_schema import KelasBase
from ...models.jadwal_model import HariEnum
from datetime import time

class JadwalBase(BaseModel):
    id : int
    hari : HariEnum
    jam_mulai : time
    jam_selesai : time

class JadwalDetail(JadwalBase):
    mapel : MapelBase
    kelas : KelasBase
