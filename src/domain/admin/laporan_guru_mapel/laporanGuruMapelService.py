from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models
from ....models.laporan_model import LaporanGuruMapel
from ....models.guru_mapel_model import GuruMapel
# schemas
from .laporanGuruMapelSchema import FilterLaporanGuruMapelQuery,ResponseLaporanGuruMapelPag
from ...schemas.laporanGuruMapel_schema import LaporanGuruMapelDetail
# common
import math
from ....error.errorHandling import HttpException

async def getAllLaporanGuruMapel(page : int | None,id_sekolah : int,id_tahun : int,query : FilterLaporanGuruMapelQuery,session : AsyncSession) -> list[LaporanGuruMapelDetail] | ResponseLaporanGuruMapelPag:
    statementGetLaporan = select(LaporanGuruMapel).options(joinedload(LaporanGuruMapel.file),joinedload(LaporanGuruMapel.guru_mapel)).where(and_(LaporanGuruMapel.guru_mapel.and_(GuruMapel.id_sekolah == id_sekolah),LaporanGuruMapel.guru_mapel.and_(GuruMapel.id_tahun == id_tahun),LaporanGuruMapel.id_guru_mapel == query.id_guru_mapel if query.id_guru_mapel else True,LaporanGuruMapel.guru_mapel.and_(GuruMapel.nama == query.nama_guru_mapel) if query.nama_guru_mapel else True))

    if page :
        findLaporan = (await session.execute(statementGetLaporan.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(LaporanGuruMapel.id))).scalar_one()
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

async def getLaporanById(id : int,id_sekolah : int,session : AsyncSession) -> LaporanGuruMapelDetail:
    findLaporan = (await session.execute(select(LaporanGuruMapel).options(joinedload(LaporanGuruMapel.file),joinedload(LaporanGuruMapel.guru_mapel)).where(and_(LaporanGuruMapel.guru_mapel.and_(GuruMapel.id_sekolah == id_sekolah),LaporanGuruMapel.id == id)))).scalar_one_or_none()

    if not findLaporan :
        raise HttpException(404,f"Laporan guru mapel dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findLaporan
    }
