from pydantic import BaseModel
from ....domain.schemas.laporanGuruMapel_schema import LaporanGuruMapelDetail
from ....domain.schemas.pagination_schema import PaginationBase

class FilterLaporanGuruMapelQuery(BaseModel) :
    id_guru_mapel : int | None = None
    nama_guru_mapel : str | None = None
class ResponseLaporanGuruMapelPag(PaginationBase) :
    data : list[LaporanGuruMapelDetail] = []