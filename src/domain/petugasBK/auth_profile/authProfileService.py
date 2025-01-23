from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload,subqueryload

# models 
from ....models.petugas_BK_model import PetugasBK, DistribusiPetugasBK
# schemas
from ...schemas.petugasBK_schema import PetugasBkBase,PetugasBKDetailWithSekolah
# common
from ....error.errorHandling import HttpException

async def getPetugasBK(id_petugasBK : int,session : AsyncSession) -> PetugasBkBase :
    findPetugasBK = (await session.execute(select(PetugasBK).where(PetugasBK.id == id_petugasBK))).scalar_one_or_none()
    if not findPetugasBK :
        raise HttpException(404,f"petugas BK tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findPetugasBK
    }

async def getProfile(id_petugasBK : int,session : AsyncSession) -> PetugasBKDetailWithSekolah :
    findPetugasBk = (await session.execute(select(PetugasBK).options(joinedload(PetugasBK.alamat),subqueryload(PetugasBK.distribusi_petugas_BK).joinedload(DistribusiPetugasBK.kelas),joinedload(PetugasBK.sekolah)).where(PetugasBK.id == id_petugasBK))).scalar_one_or_none()
    if not findPetugasBk :
        raise HttpException(404,f"petugas BK tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findPetugasBk
    }
