from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models
from ....models.laporan_model import LaporanGuruWalas
from ....models.guru_walas_model import GuruWalas
# schemas
from .laporanGuruWalasSchema import FilterLaporanGuruWalasQuery,ResponseLaporanGuruWalasPag
from ...schemas.laporanGuruWalas_schema import LaporanGuruWalasDetail
# common
import math
from ....error.errorHandling import HttpException

async def getAllLaporanGuruWalas(page : int | None,id_sekolah : int,id_tahun : int,query : FilterLaporanGuruWalasQuery,session : AsyncSession) -> list[LaporanGuruWalasDetail] | ResponseLaporanGuruWalasPag:
    statementGetLaporan = select(LaporanGuruWalas).options(joinedload(LaporanGuruWalas.file),joinedload(LaporanGuruWalas.guru_walas)).where(and_(LaporanGuruWalas.guru_walas.and_(GuruWalas.id_sekolah == id_sekolah),LaporanGuruWalas.guru_walas.and_(GuruWalas.id_tahun == id_tahun),LaporanGuruWalas.id_guru_walas == query.id_guru_walas if query.id_guru_walas else True,LaporanGuruWalas.guru_walas.and_(GuruWalas.nama == query.nama_guru_walas) if query.nama_guru_walas else True))

    if page :
        findLaporan = (await session.execute(statementGetLaporan.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(LaporanGuruWalas.id))).scalar_one()
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

async def getLaporanById(id : int,id_sekolah : int,session : AsyncSession) -> LaporanGuruWalasDetail:
    findLaporan = (await session.execute(select(LaporanGuruWalas).options(joinedload(LaporanGuruWalas.file),joinedload(LaporanGuruWalas.guru_walas)).where(and_(LaporanGuruWalas.guru_walas.and_(GuruWalas.id_sekolah == id_sekolah),LaporanGuruWalas.id == id)))).scalar_one_or_none()

    if not findLaporan :
        raise HttpException(404,f"Laporan guru walas dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findLaporan
    }
