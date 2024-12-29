from pydantic import BaseModel
from ....domain.schemas.laporanPetugasBK_schema import LaporanPetugasBKDetail
from ....domain.schemas.pagination_schema import PaginationBase

class FilterLaporanPetugasBKQuery(BaseModel) :
    id_petugas_BK : int | None = None
    nama_petugas_BK : str | None = None

class ResponseLaporanPetugasBKPag(PaginationBase) :
    data : list[LaporanPetugasBKDetail] = []