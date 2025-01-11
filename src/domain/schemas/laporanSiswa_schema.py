from pydantic import BaseModel
from .siswa_schema import SiswaBase
from datetime import datetime
from .fileLaporan_schema import FileLaporanBase

class LaporanSiswaBase(BaseModel):
    id : int
    catatan : str
    datetime : datetime

class LaporanSiswaWithFile(LaporanSiswaBase) :
    file : list[FileLaporanBase] | None = None
class LaporanSiswaDetail(LaporanSiswaBase):
    siswa : SiswaBase
    file : list[FileLaporanBase] | None = None
