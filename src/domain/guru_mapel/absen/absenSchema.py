from pydantic import BaseModel
from ...schemas.pagination_schema import PaginationBase
from ...schemas.absen_schema import AbsenBase
from ...schemas.kelasJurusan_schema import KelasWithGuruWalas, KelasBase
from ...schemas.siswa_schema import SiswaBase
# from ....models.absen_model import StatusAbsenEnum , StatusTinjauanEnum
# from ...schemas.guruWalas_schema import GuruWalasBase
# from ...schemas.absen_schema import AbsenWithSiswaKelas,AbsenBase
# from ...schemas.kelasJurusan_schema import KelasWithGuruWalas
from datetime import date
# from ...schemas.petugasBK_schema import PetugasBkBase

class GetStatistikKelasAbsenResponse(BaseModel) :
    jumlah_siswa : int
    kelas : KelasWithGuruWalas

class GetAbsenFilterQuery(BaseModel) :
    tanggal : date 
    id_kelas : int
    limit : int = 10
    offset : int = 1

class HistoriAbsenResponse(BaseModel) :
    siswa : SiswaBase
    absen : AbsenBase | None

class GetHistoriAbsenKelasResponse(PaginationBase) :
    waktu_belajar : int
    absen : list[HistoriAbsenResponse]
    jumlah_hadir : int

class GetAbsenAbsenInKelasResponse(PaginationBase) :
    absen : list[HistoriAbsenResponse]
    jumlah_siswa : int

class GetHistoriKelasAjarResponse(BaseModel) :
    kelas : KelasBase
    jumlah_hadir : int
    tanggal : date
# class GetAbsenInKelasResponse(PaginationBase) :
#     absen : dict[str,dict[int , AbsenBase]]
    
    
# class GetAbsenBySiswaFilterQuery(BaseModel) :
#     tanggal : date 
#     id_siswa : int 

# class GetAbsenByJadwalResponse(PaginationBase) :
#     absen : list[AbsenBase | None]
#     siswa_hadir : int
#     waktu_belajar : int

# class GetStatistikAbsenResponse(BaseModel) :
#     jumlah_siswa : int
#     jumlah_absen_hadir : int
#     jumlah_absen_tanpa_keterangan : int
