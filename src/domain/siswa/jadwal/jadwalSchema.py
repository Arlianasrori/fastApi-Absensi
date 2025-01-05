from pydantic import BaseModel
from ....models.jadwal_model import HariEnum
from datetime import time

class GetHariContainsJadwalResponse(BaseModel) :
    hari : HariEnum
    min_jam_mulai : time
    max_jam_selesai : time

class FilterJadwalQuery(BaseModel) :
    hari : HariEnum | None = None