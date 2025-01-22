from pydantic import BaseModel
from ....models.jadwal_model import HariEnum
from datetime import time
from ...schemas.jadwal_schema import JadwalWithMapel

class GetHariContainsJadwalResponse(BaseModel) :
    hari : HariEnum
    min_jam_mulai : time
    max_jam_selesai : time

class FilterJadwalQuery(BaseModel) :
    hari : HariEnum | None = None

class JadwalToday(BaseModel) :
    jadwal : JadwalWithMapel
    isAbsen : bool

class JadwalTodayResponse(BaseModel) :
    dataJadwal : list[JadwalToday]
    countMapel : int