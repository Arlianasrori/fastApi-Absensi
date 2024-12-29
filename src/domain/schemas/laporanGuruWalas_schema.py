from pydantic import BaseModel
from .guruWalas_schema import GuruWalasBase
from datetime import datetime
from .fileLaporan_schema import FileLaporanBase

class LaporanGuruWalasBase(BaseModel):
    id : int
    catatan : str
    datetime : datetime

class LaporanGuruWalasDetail(LaporanGuruWalasBase):
    guru_walas : GuruWalasBase
    file : list[FileLaporanBase] | None = None