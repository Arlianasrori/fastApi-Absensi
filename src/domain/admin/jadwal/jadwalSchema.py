from pydantic import BaseModel
from ...schemas.pagination_schema import PaginationBase
from ...schemas.jadwal_schema import JadwalDetail
from datetime import time
from ....models.jadwal_model import HariEnum

class AddJadwalRequest(BaseModel) :
    id_mapel : int
    id_kelas : int
    id_guru_mapel : int
    hari : HariEnum
    jam_mulai : time
    jam_selesai : time
    id_koordinat : int

class UpdateJadwalRequest(BaseModel) :
    hari : HariEnum | None = None
    jam_mulai : time | None = None
    jam_selesai : time | None = None

class FilterJadwalQuery(BaseModel) :
    id_kelas : int | None = None
    id_mapel : int | None = None
    hari : HariEnum | None = None

class ResponseJadwalPag(PaginationBase) :
    data : list[JadwalDetail] = []