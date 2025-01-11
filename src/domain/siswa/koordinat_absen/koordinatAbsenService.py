from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_
from sqlalchemy.orm import joinedload

# models 
from ....models.absen_model import KoordinatAbsenKelas
# schemas
from ...schemas.absen_schema import KoordinatAbsenKelasBase, KoordinatAbsenDetail
# common
from ....error.errorHandling import HttpException

async def getAllKoordinat(siswa : dict,session : AsyncSession) -> KoordinatAbsenKelasBase :
    findKoordinatAbsen = (await session.execute(select(KoordinatAbsenKelas).where(and_(KoordinatAbsenKelas.id_kelas == siswa["id_kelas"])))).scalar_one_or_none()
    if not findKoordinatAbsen :
        raise HttpException(404,f"siswa tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findKoordinatAbsen
    }

async def getKoordinatById(id : int,session : AsyncSession) -> KoordinatAbsenDetail :
    findKoordinat = (await session.execute(select(KoordinatAbsenKelas).options(joinedload(KoordinatAbsenKelas.kelas)).where(KoordinatAbsenKelas.id == id))).scalar_one_or_none()
    if not findKoordinat :
        raise HttpException(404,f"siswa tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findKoordinat
    }
