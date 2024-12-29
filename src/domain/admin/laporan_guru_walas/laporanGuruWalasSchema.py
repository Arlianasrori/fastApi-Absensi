from pydantic import BaseModel
from ....domain.schemas.laporanGuruWalas_schema import LaporanGuruWalasDetail
from ....domain.schemas.pagination_schema import PaginationBase

class FilterLaporanGuruWalasQuery(BaseModel) :
    id_guru_walas : int | None = None
    nama_guru_walas : str | None = None

class ResponseLaporanGuruWalasPag(PaginationBase) :
    data : list[LaporanGuruWalasDetail] = []