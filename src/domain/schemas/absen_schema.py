from pydantic import BaseModel
from .siswa_schema import SiswaBase, SiswaWithKelasWalas
from .jadwal_schema import JadwalWithKoordinatGuruMapel, JadwalWithKoordinat, JadwalWithMapel
from datetime import date,time
from ...models.absen_model import StatusAbsenEnum, StatusTinjauanEnum
from ..schemas.petugasBK_schema import PetugasBkBase

class AbsenDetailBase(BaseModel) :
    id : int
    id_absen : int
    catatan : str
    diterima : StatusTinjauanEnum
    id_peninjau : int | None
    tanggal_peninjau : date | None

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

class AbsenWithSiswaKelas(AbsenBase) :
    siswa : SiswaBase

class AbsenWithSiswaKelasWalasDetail(AbsenBase) :
    siswa : SiswaWithKelasWalas
    detail : AbsenDetailWithPetugasBK

class AbsenWithSiswaDetail(AbsenBase) :
    siswa : SiswaBase
    detail : AbsenDetailBase

class GetAbsenTinjauanResponse(AbsenWithSiswaKelasWalasDetail) :
    jadwal : JadwalWithKoordinatGuruMapel
    
class GetAbsenHarianResponse(AbsenWithSiswa) :
    detail : AbsenDetailWithPetugasBK
    jadwal : JadwalWithKoordinat
