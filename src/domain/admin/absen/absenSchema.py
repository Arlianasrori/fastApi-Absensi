from pydantic import BaseModel
from ....domain.schemas.absen_schema import AbsenWithSiswaDetail
from ....domain.schemas.pagination_schema import PaginationBase
from ....models.jadwal_model import HariEnum
from datetime import date

class FilterAbsenQuery(BaseModel) :
    id_siswa : int | None = None
    hari : HariEnum | None = None
    tanggal_mulai : date | None = None
    tanggal_selesai : date | None = None
    diterima : bool = None

class ResponseAbsenPag(PaginationBase) :
    data : list[AbsenWithSiswaDetail] = []