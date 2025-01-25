from pydantic import BaseModel
from ...schemas.pagination_schema import PaginationBase
from ...schemas.absen_schema import AbsenBase
# from ....models.absen_model import StatusAbsenEnum , StatusTinjauanEnum
# from ...schemas.guruWalas_schema import GuruWalasBase
# from ...schemas.absen_schema import AbsenWithSiswaKelas,AbsenBase
# from ...schemas.kelasJurusan_schema import KelasWithGuruWalas
from datetime import date
# from ...schemas.petugasBK_schema import PetugasBkBase

class GetAbsenFilterQuery(BaseModel) :
    tanggal : date 
    limit : int = 10
    offset : int = 1

class GetAbsenInKelasResponse(PaginationBase) :
    absen : dict[str,dict[int , AbsenBase]]
    
    
class GetAbsenBySiswaFilterQuery(BaseModel) :
    tanggal : date 
    id_siswa : int 

class GetAbsenByJadwalResponse(PaginationBase) :
    absen : list[AbsenBase | None]
    siswa_hadir : int
    waktu_belajar : int

# class TinjauAbsenRequest(BaseModel) :
#     status_tinjauan : StatusTinjauanEnum

# class TinjauAbsenResponse(BaseModel) :
#     status : StatusTinjauanEnum
#     petugasBK : PetugasBkBase
#     absen : AbsenBase

# class GetAbsenByKelasResponse(BaseModel) :
#     jumlah_siswa : int
#     guru_walas : GuruWalasBase
#     absen : dict[str,dict[int,AbsenBase | None]]

# class GetAllKelasTinjauanResponse(BaseModel) :
#     kelas : list[KelasWithGuruWalas]
#     jumlah_siswa : int
