from pydantic import BaseModel
from .petugasBK_schema import PetugasBkBase
from datetime import datetime
from .fileLaporan_schema import FileLaporanBase

class LaporanPetugasBKBase(BaseModel):
    id : int
    id_petugas_BK : int
    id_guru_walas : int | None = None
    id_guru_mapel : int | None = None
    catatan : str
    datetime : datetime

class LaporanPetugasBKDetail(LaporanPetugasBKBase):
    petugas_BK : PetugasBkBase
    file : list[FileLaporanBase] | None = None