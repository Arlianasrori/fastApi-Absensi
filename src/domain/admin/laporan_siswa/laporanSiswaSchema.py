from pydantic import BaseModel
from ....domain.schemas.laporanSiswa_schema import LaporanSiswaDetail
from ....domain.schemas.pagination_schema import PaginationBase

class FilterLaporanSiswaQuery(BaseModel) :
    id_siswa : int | None = None
    nama_siswa : str | None = None
class ResponseLaporanSiswaPag(PaginationBase) :
    data : list[LaporanSiswaDetail] = []