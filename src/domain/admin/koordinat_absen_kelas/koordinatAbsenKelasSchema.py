from pydantic import BaseModel
from ....domain.schemas.absen_schema import KoordinatAbsenKelasBase
from ....domain.schemas.pagination_schema import PaginationBase

class FilterKoordinatAbsenKelasQuery(BaseModel) :
    id_kelas : int | None = None
    nama_kelas : str | None = None
class ResponseKoordinatAbsenKelasPag(PaginationBase) :
    data : list[KoordinatAbsenKelasBase] = []