from pydantic import BaseModel
from ....domain.schemas.koordinatAbsen_schema import KoordinatAbsenKelasBase
from ....domain.schemas.pagination_schema import PaginationBase

class FilterKoordinatAbsenKelasQuery(BaseModel) :
    id_kelas : int | None = None
    nama_kelas : str | None = None
class ResponseKoordinatAbsenKelasPag(PaginationBase) :
    data : list[KoordinatAbsenKelasBase] = []

class AddKoordinatAbsenKelasRequest(BaseModel) :
    id_kelas : int
    nama_tempat : str
    latitude : float
    longitude : float
    radius_absen_meter : float
    id_tahun : int

class UpdateKoordinatAbsenKelasRequest(BaseModel) :
    id_kelas : int | None = None
    nama_tempat : str | None = None
    latitude : float | None = None
    longitude : float | None = None
    radius_absen_meter : float | None = None
    id_tahun : int | None = None