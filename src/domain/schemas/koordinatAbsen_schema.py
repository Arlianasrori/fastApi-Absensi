from pydantic import BaseModel
from .kelasJurusan_schema import KelasBase
class KoordinatAbsenKelasBase(BaseModel) :
    id : int
    id_kelas : int
    nama_tempat : str
    latitude : float
    longitude : float
    radius_absen_meter : float

class KoordinatAbsenDetail(KoordinatAbsenKelasBase) :
    kelas : KelasBase