from pydantic import BaseModel
from ....models.absen_model import StatusAbsenEnum , StatusTinjauanEnum
from ...schemas.guruWalas_schema import GuruWalasBase
from ...schemas.absen_schema import AbsenWithSiswaKelas,AbsenBase
from ...schemas.kelasJurusan_schema import  KelasBase, KelasWithGuruWalas
from datetime import date
from ...schemas.petugasBK_schema import PetugasBkBase
from ...schemas.pagination_schema import PaginationBase

class StatistikAbsenResponse(BaseModel) :
    diterima : int
    ditolak : int
    belum_ditinjau : int

class GetHistoriTinjauanAbsenResponse(BaseModel) :
    belum_ditinjau : list[AbsenWithSiswaKelas] | None = None
    diterima : list[AbsenWithSiswaKelas] | None = None
    ditolak : list[AbsenWithSiswaKelas] | None = None

class GetAbsenByKelasFilterQuery(BaseModel) :
    tanggal : date 
    id_kelas : int
    page : int = 1
    take : int = 10

class GetAbsenBySiswaFilterQuery(BaseModel) :
    tanggal : date 
    id_siswa : int 

class TinjauAbsenRequest(BaseModel) :
    status_tinjauan : StatusTinjauanEnum

class TinjauAbsenResponse(BaseModel) :
    status : StatusTinjauanEnum
    petugasBK : PetugasBkBase
    absen : AbsenBase

class GetAbsenByKelasResponse(PaginationBase) :
    jumlah_siswa : int
    absen : dict[str,dict[int , AbsenBase]]
    
class KelasWithWalas(KelasBase) :
    guru_walas : GuruWalasBase | None = None
    
class GetAllKelasTinjauanResponse(BaseModel) :
    kelas : list[KelasWithGuruWalas]
