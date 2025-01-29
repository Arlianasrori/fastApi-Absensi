from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

# models 
from ...schemas.sekolah_schema import AdminBase,AdminWithSekolah
from ....models.sekolah_model import Admin

# common
from ....error.errorHandling import HttpException

async def getAdmin(id_admin : int,session : AsyncSession) -> AdminBase :
    findAdmin = (await session.execute(select(Admin).where(Admin.id == id_admin))).scalar_one_or_none()
    if not findAdmin :
        raise HttpException(404,f"admin tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findAdmin
    }

async def getProfile(id_admin : int,session : AsyncSession) -> AdminWithSekolah :
    findAdmin = (await session.execute(select(Admin).options(joinedload(Admin.sekolah)).where(Admin.id == id_admin))).scalar_one_or_none()
    if not findAdmin :
        raise HttpException(404,f"admin tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findAdmin
    }
