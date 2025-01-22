from pydantic import BaseModel
from ....models.absen_model import StatusAbsenEnum 
from ...schemas.absen_schema import AbsenWithSiswa
from datetime import date

class StatistikAbsenResponse(BaseModel) :
    diterima : int
    ditolak : int
    belum_ditinjau : int

class GetHistoriTinjauanAbsenResponse(BaseModel) :
    belum_ditinjau : list[AbsenWithSiswa] | None = None
    diterima : list[AbsenWithSiswa] | None = None
    ditolak : list[AbsenWithSiswa] | None = None

class GetAbsenByKelasFilterQuery(BaseModel) :
    tanggal : date 
    id_kelas : int

class GetAbsenBySiswaFilterQuery(BaseModel) :
    tanggal : date 
    id_siswa : int 
    