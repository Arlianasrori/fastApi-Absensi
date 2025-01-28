from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models 
from ...schemas.guruMapel_schema import GuruMapelBase, GuruMapelDetailWithSekolah
from ....models.guru_mapel_model import GuruMapel

# common
from ....error.errorHandling import HttpException

async def getGuruMapel(id_guru_mapel : int,session : AsyncSession) -> GuruMapelBase :
    findGuruMapel = (await session.execute(select(GuruMapel).where(GuruMapel.id == id_guru_mapel))).scalar_one_or_none()
    if not findGuruMapel :
        raise HttpException(404,f"Guru Mapel tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findGuruMapel
    }

async def getGuruMapelProfile(id_guru_mapel : int,session : AsyncSession) -> GuruMapelDetailWithSekolah :
    findGuruMapel = (await session.execute(select(GuruMapel).options(joinedload(GuruMapel.sekolah),joinedload(GuruMapel.alamat),joinedload(GuruMapel.mapel)).where(GuruMapel.id == id_guru_mapel))).scalar_one_or_none()
    print(findGuruMapel.__dict__)
    if not findGuruMapel :
        raise HttpException(404,f"Guru Mapel tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findGuruMapel
    }
