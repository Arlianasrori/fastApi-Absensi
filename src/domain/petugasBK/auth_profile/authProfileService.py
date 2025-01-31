from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload,subqueryload
from fastapi import UploadFile

# models 
from ....models.petugas_BK_model import PetugasBK, DistribusiPetugasBK
# schemas
from ...schemas.petugasBK_schema import PetugasBkBase,PetugasBKDetailWithSekolah,PetugasBKWithAlamat
from .authProfileSchema import UpdateProfileRequest
from ...schemas.alamat_schema import UpdateAlamatBody
# common
from ....error.errorHandling import HttpException
import os
from copy import deepcopy
from ....utils.updateTable_util import updateTable
from python_random_strings import random_strings
import aiofiles

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

async def updateProfile(id_petugasBK : int,body : UpdateProfileRequest,alamat : UpdateAlamatBody,session : AsyncSession) -> PetugasBKWithAlamat :
    findPetugasBK = (await session.execute(select(PetugasBK).options(joinedload(PetugasBK.alamat)).where(PetugasBK.id == id_petugasBK))).scalar_one_or_none()

    if findPetugasBK is None :
        raise HttpException(404,f"petugas BK tidak ditemukan")
    
    if body.model_dump(exclude_unset=True):
        updateTable(body,findPetugasBK)

    if alamat.model_dump(exclude_unset=True):
        updateTable(alamat,findPetugasBK.alamat)

    petugasBKDictCopy = deepcopy(findPetugasBK.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : petugasBKDictCopy
    }

PROFILE_STORE = os.getenv("DEV_FOTO_PROFILE_SISWA_STORE")
PROFILE_BASE_URL = os.getenv("DEV_FOTO_PROFILE_SISWA_BASE_URL")

async def add_update_foto_profile(id : int,foto_profile : UploadFile,session : AsyncSession) -> PetugasBkBase :
    findPetugasBK = (await session.execute(select(PetugasBK).where(PetugasBK.id == id))).scalar_one_or_none()
    if not findPetugasBK :
        raise HttpException(404,f"petugas BK tidak ditemukan")

    ext_file = foto_profile.filename.split(".")

    if ext_file[-1] not in ["jpg","png","jpeg"] :
        raise HttpException(400,f"file harus berupa gambar")

    file_name = f"{random_strings.random_digits(12)}-{foto_profile.filename.split(' ')[0]}.{ext_file[-1]}"
    file_name_save = f"{PROFILE_STORE}{file_name}"
        
    fotoProfileBefore = findPetugasBK.foto_profile

    async with aiofiles.open(file_name_save, "wb") as f:
        await f.write(foto_profile.file.read())
        print(PROFILE_BASE_URL)
        findPetugasBK.foto_profile = f"{PROFILE_BASE_URL}/{file_name}"
    
    if fotoProfileBefore :
        print(fotoProfileBefore)
        file_nama_db_split = fotoProfileBefore.split("/")
        file_name_db = file_nama_db_split[-1]
        os.remove(f"{PROFILE_STORE}/{file_name_db}")
    
    petugasBKDictCopy = deepcopy(findPetugasBK.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : petugasBKDictCopy
    }