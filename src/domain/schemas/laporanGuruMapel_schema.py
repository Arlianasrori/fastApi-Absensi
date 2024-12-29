from pydantic import BaseModel
from .guruMapel_schema import GuruMapelBase
from datetime import datetime
from .fileLaporan_schema import FileLaporanBase

class LaporanGuruMapelBase(BaseModel):
    id : int
    catatan : str
    datetime : datetime

class LaporanGuruMapelDetail(LaporanGuruMapelBase):
    guru_mapel : GuruMapelBase
    file : list[FileLaporanBase] | None = None