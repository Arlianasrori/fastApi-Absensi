from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, and_
from sqlalchemy.orm import joinedload

# models 
from ....models.absen_model import KoordinatAbsenKelas
from ....models.jadwal_model import Jadwal
# schemas
from .koordinatAbsenSchema import CekRadiusKoordinatRequest, CekRadiusKoordinatResponse
from ...schemas.koordinatAbsen_schema import KoordinatAbsenKelasBase, KoordinatAbsenDetail
# common
from ....error.errorHandling import HttpException
from ...common.get_distance_koordinat import calculate_radius
from ...common.get_day_today import get_day

async def getAllKoordinat(siswa : dict,session : AsyncSession) -> KoordinatAbsenKelasBase :
    findKoordinatAbsen = (await session.execute(select(KoordinatAbsenKelas).where(and_(KoordinatAbsenKelas.id_kelas == siswa["id_kelas"])))).scalars().all()

    return {
        "msg" : "success",
        "data" : findKoordinatAbsen
    }

async def getKoordinatById(id : int,session : AsyncSession) -> KoordinatAbsenDetail :
    findKoordinat = (await session.execute(select(KoordinatAbsenKelas).options(joinedload(KoordinatAbsenKelas.kelas)).where(KoordinatAbsenKelas.id == id))).scalar_one_or_none()
    if not findKoordinat :
        raise HttpException(404,f"koordinat tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findKoordinat
    }

async def cekRadiusKoordinat(siswa : dict,body : CekRadiusKoordinatRequest,session : AsyncSession) -> CekRadiusKoordinatResponse :
    dayToday : dict = await get_day()
    findJadwal = (await session.execute(select(Jadwal).options(joinedload(Jadwal.koordinat)).where(and_(Jadwal.id_kelas == siswa["id_kelas"],Jadwal.hari == dayToday["day_name"])))).scalars().all()

    for jadwalItem in findJadwal :
        if await calculate_radius(body.latitude,body.longitude,jadwalItem.koordinat.latitude,jadwalItem.koordinat.longitude) <= jadwalItem.koordinat.radius_absen_meter :
            return {
                "msg" : "anda berada didalam radius absen",
                "data" : {
                    "insideRadius" : True
                }
            }
        
    return {
        "msg" : "anda berada diluar radius absen",
        "data" : {
            "insideRadius" : False
        }
    }