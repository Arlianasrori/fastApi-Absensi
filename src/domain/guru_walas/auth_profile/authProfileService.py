from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models 
from ...schemas.guruWalas_schema import GuruWalasBase, GuruWalasDetailWithSekolah
from ....models.guru_walas_model import GuruWalas

# common
from ....error.errorHandling import HttpException

async def getGuruWalas(id_walas : int,session : AsyncSession) -> GuruWalasBase :
    findWalas = (await session.execute(select(GuruWalas).where(GuruWalas.id == id_walas))).scalar_one_or_none()
    if not findWalas :
        raise HttpException(404,f"Guru Walas tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findWalas
    }

async def getGuruWalasProfile(id_walas : int,session : AsyncSession) -> GuruWalasDetailWithSekolah :
    findWalas = (await session.execute(select(GuruWalas).options(joinedload(GuruWalas.sekolah),joinedload(GuruWalas.alamat),joinedload(GuruWalas.kelas)).where(GuruWalas.id == id_walas))).scalar_one_or_none()
    if not findWalas :
        raise HttpException(404,f"Guru Walas tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findWalas
    }
