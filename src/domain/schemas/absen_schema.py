from pydantic import BaseModel
from .siswa_schema import SiswaBase, SiswaWithKelasWalas, SiswaWithKelas
from .jadwal_schema import JadwalWithKoordinatGuruMapel, JadwalWithKoordinat, JadwalWithMapel
from datetime import date,time
from ...models.absen_model import StatusAbsenEnum, StatusTinjauanEnum
from ..schemas.petugasBK_schema import PetugasBkBase

class AbsenDetailBase(BaseModel) :
    id : int
    id_absen : int
    catatan : str
    status_tinjauan : StatusTinjauanEnum
    id_peninjau : int | None
    tanggal_tinjauan : date | None

class AbsenDetailWithPetugasBK(AbsenDetailBase) :
    petugas_bk : PetugasBkBase | None

class AbsenBase(BaseModel) :
    id : int
    id_jadwal : int
    id_siswa : int
    tanggal : date
    jam : time
    file : str
    status : StatusAbsenEnum

class AbsenWithSiswa(AbsenBase) :
    siswa : SiswaBase

class AbsenWithJadwalMapel(AbsenBase) :
    jadwal : JadwalWithMapel

class AbsenWithDetail(AbsenBase) :
    detail : AbsenDetailBase | None = None
    
class AbsenWithSiswaKelas(AbsenBase) :
    siswa : SiswaWithKelas

class AbsenWithSiswaKelasWalasDetail(AbsenBase) :
    siswa : SiswaWithKelasWalas
    detail : AbsenDetailWithPetugasBK | None = None

class AbsenWithSiswaDetail(AbsenBase) :
    siswa : SiswaBase
    detail : AbsenDetailBase | None = None

class AbsenWithJadwalMapel(AbsenBase) :
    jadwal : JadwalWithMapel

# response
class GetAbsenTinjauanResponse(AbsenWithSiswaKelasWalasDetail) :
    jadwal : JadwalWithKoordinatGuruMapel
    
class GetAbsenHarianResponse(AbsenWithSiswa) :
    detail : AbsenDetailWithPetugasBK | None
    jadwal : JadwalWithKoordinat
