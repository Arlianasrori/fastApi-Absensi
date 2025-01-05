from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models
from ....models.absen_model import Absen
from ....models.jadwal_model import Jadwal
from ....models.siswa_model import Siswa
# schemas
from .absenSchema import FilterAbsenQuery,ResponseAbsenPag
from ...schemas.absen_schema import AbsenWithSiswaDetail
# common
import math
from ....error.errorHandling import HttpException

async def getAllAbsen(page : int | None,id_sekolah : int,id_tahun : int,query : FilterAbsenQuery,session : AsyncSession) -> list[AbsenWithSiswaDetail] | ResponseAbsenPag:
    statementGetAbsen = select(Absen).options(joinedload(Absen.siswa),joinedload(Absen.detail)).where(and_(Absen.siswa.and_(Siswa.id_sekolah == id_sekolah),Absen.siswa.and_(Siswa.id_tahun == id_tahun),Absen.id_siswa == query.id_siswa if query.id_siswa else True, Absen.jadwal.and_(Jadwal.hari == query.hari) if query.hari else True, Absen.tanggal >= query.tanggal_mulai if query.tanggal_mulai else True, Absen.tanggal <= query.tanggal_selesai if query.tanggal_selesai else True,Absen.diterima == query.diterima if query.diterima else True))

    if page :
        findAbsen = (await session.execute(statementGetAbsen.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(Absen.id))).scalar_one()
        countPage = math.ceil(conntData / 10)
        return {
            "msg" : "success",
            "data" : {
                "data" : findAbsen,
                "count_data" : len(findAbsen),
                "count_page" : countPage
            }
        }
    else :
        findAbsen = (await session.execute(statementGetAbsen)).scalars().all()
        return {
            "msg" : "success",
            "data" : findAbsen
        }

async def getAbsenById(id : int,id_sekolah : int,session : AsyncSession) -> AbsenWithSiswaDetail:
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.siswa),joinedload(Absen.detail)).where(and_(Absen.id == id,Absen.siswa.and_(Siswa.id_sekolah == id_sekolah))))).scalar_one_or_none()

    if not findAbsen :
        raise HttpException(404,f"Absen dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findAbsen
    }