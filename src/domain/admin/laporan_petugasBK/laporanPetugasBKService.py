from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models
from ....models.laporan_model import LaporanPetugasBK
from ....models.petugas_BK_model import PetugasBK
# schemas
from .laporanPetugasBKSchema import FilterLaporanPetugasBKQuery,ResponseLaporanPetugasBKPag
from ...schemas.laporanPetugasBK_schema import LaporanPetugasBKDetail
# common
import math
from ....error.errorHandling import HttpException

async def getAllLaporanPetugasBK(page : int | None,id_sekolah : int,id_tahun : int,query : FilterLaporanPetugasBKQuery,session : AsyncSession) -> list[LaporanPetugasBKDetail] | ResponseLaporanPetugasBKPag:
    statementGetLaporan = select(LaporanPetugasBK).options(joinedload(LaporanPetugasBK.file),joinedload(LaporanPetugasBK.petugas_BK)).where(and_(LaporanPetugasBK.petugas_BK.and_(PetugasBK.id_sekolah == id_sekolah),LaporanPetugasBK.petugas_BK.and_(PetugasBK.id_tahun == id_tahun),LaporanPetugasBK.id_petugas_BK == query.id_petugas_BK if query.id_petugas_BK else True,LaporanPetugasBK.petugas_BK.and_(PetugasBK.nama == query.nama_petugas_BK) if query.nama_petugas_BK else True))

    if page :
        findLaporan = (await session.execute(statementGetLaporan.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(LaporanPetugasBK.id))).scalar_one()
        countPage = math.ceil(conntData / 10)
        return {
            "msg" : "success",
            "data" : {
                "data" : findLaporan,
                "count_data" : len(findLaporan),
                "count_page" : countPage
            }
        }
    else :
        findLaporan = (await session.execute(statementGetLaporan)).scalars().all()
        return {
            "msg" : "success",
            "data" : findLaporan
        }

async def getLaporanById(id : int,id_sekolah : int,session : AsyncSession) -> LaporanPetugasBKDetail:
    findLaporan = (await session.execute(select(LaporanPetugasBK).options(joinedload(LaporanPetugasBK.file),joinedload(LaporanPetugasBK.petugas_BK)).where(and_(LaporanPetugasBK.petugas_BK.and_(PetugasBK.id_sekolah == id_sekolah),LaporanPetugasBK.id == id)))).scalar_one_or_none()

    if not findLaporan :
        raise HttpException(404,f"Laporan petugas BK dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findLaporan
    }
