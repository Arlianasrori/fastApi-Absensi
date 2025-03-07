from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_

# models
from ....models.absen_model import KoordinatAbsenKelas
from ....models.siswa_model import Kelas, Jurusan
# schemas
from .koordinatAbsenKelasSchema import FilterKoordinatAbsenKelasQuery,ResponseKoordinatAbsenKelasPag
from ...schemas.absen_schema import KoordinatAbsenKelasBase
# common
import math
from ....error.errorHandling import HttpException

async def getAllKoordinatAbsen(page : int | None,id_sekolah : int,id_tahun : int,query : FilterKoordinatAbsenKelasQuery,session : AsyncSession) -> list[KoordinatAbsenKelasBase] | ResponseKoordinatAbsenKelasPag:
    statementGetKoordinatAbsen = select(KoordinatAbsenKelas).join(KoordinatAbsenKelas.kelas).join(Kelas.jurusan).where(and_(Jurusan.id_sekolah == id_sekolah,Jurusan.id_tahun == id_tahun,KoordinatAbsenKelas.id_kelas == query.id_kelas if query.id_kelas else True,KoordinatAbsenKelas.kelas.and_(Kelas.nama == query.nama_kelas) if query.nama_kelas else True))

    if page :
        findKoordinat = (await session.execute(statementGetKoordinatAbsen.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(KoordinatAbsenKelas.id))).scalar_one()
        countPage = math.ceil(conntData / 10)
        return {
            "msg" : "success",
            "data" : {
                "data" : findKoordinat,
                "count_data" : len(findKoordinat),
                "count_page" : countPage
            }
        }
    else :
        findKoordinat = (await session.execute(statementGetKoordinatAbsen)).scalars().all()
        return {
            "msg" : "success",
            "data" : findKoordinat
        }

async def getKoordinatById(id : int,id_sekolah : int,session : AsyncSession) -> KoordinatAbsenKelasBase:
    findKoordinat = (await session.execute(select(KoordinatAbsenKelas).join(KoordinatAbsenKelas.kelas).join(Kelas.jurusan).where(and_(Jurusan.id_sekolah == id_sekolah,KoordinatAbsenKelas.id == id)))).scalar_one_or_none()

    if not findKoordinat :
        raise HttpException(404,f"Koordinat absen dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findKoordinat
    }
