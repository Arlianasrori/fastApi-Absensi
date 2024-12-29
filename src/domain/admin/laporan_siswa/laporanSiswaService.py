from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models
from ....models.laporan_model import LaporanSiswa
from ....models.siswa_model import Siswa
# schemas
from .laporanSiswaSchema import FilterLaporanSiswaQuery,ResponseLaporanSiswaPag
from ...schemas.laporanSiswa_schema import LaporanSiswaDetail
# common
import math
from ....error.errorHandling import HttpException

async def getAllLaporanSiswa(page : int | None,id_sekolah : int,id_tahun : int,query : FilterLaporanSiswaQuery,session : AsyncSession) -> list[LaporanSiswaDetail] | ResponseLaporanSiswaPag:
    statementGetLaporan = select(LaporanSiswa).options(joinedload(LaporanSiswa.file),joinedload(LaporanSiswa.siswa)).where(and_(LaporanSiswa.siswa.and_(Siswa.id_sekolah == id_sekolah),LaporanSiswa.siswa.and_(Siswa.id_tahun == id_tahun),LaporanSiswa.id_siswa == query.id_siswa if query.id_siswa else True,LaporanSiswa.siswa.and_(Siswa.nama == query.nama_siswa) if query.nama_siswa else True))

    if page :
        findLaporan = (await session.execute(statementGetLaporan.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(LaporanSiswa.id))).scalar_one()
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

async def getLaporanById(id : int,id_sekolah : int,session : AsyncSession) -> LaporanSiswaDetail:
    findLaporan = (await session.execute(select(LaporanSiswa).options(joinedload(LaporanSiswa.file),joinedload(LaporanSiswa.siswa)).where(and_(LaporanSiswa.id == id,LaporanSiswa.siswa.and_(Siswa.id_sekolah == id_sekolah))))).scalar_one_or_none()

    if not findLaporan :
        raise HttpException(404,f"Laporan siswa dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findLaporan
    }
