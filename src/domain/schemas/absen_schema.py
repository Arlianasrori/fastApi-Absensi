from pydantic import BaseModel
from .siswa_schema import SiswaBase
from datetime import date,time
from ...models.absen_model import StatusAbsenEnum
class AbsenDetailBase(BaseModel) :
    id : int
    id_absen : int
    catatan : str

class AbsenBase(BaseModel) :
    id : int
    id_jadwal : int
    id_siswa : int
    tanggal : date
    jam : time
    file : str
    status : StatusAbsenEnum

class AbsenWithSiswaDetail(AbsenBase) :
    siswa : SiswaBase
    detail : AbsenDetailBase

class KoordinatAbsenKelasBase(BaseModel) :
    id : int
    id_kelas : int
    nama_tempat : str
    latitude : float
    longitude : float
    radius_absen_meter : float