from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,and_
from sqlalchemy.orm import joinedload
from fastapi import UploadFile

# models 
from ....models.guru_walas_model import GuruWalas
# schemas
from ...schemas.guruWalas_schema import GuruWalasBase, GuruWalasDetailWithSekolah, GuruWalasWithAlamat
from .authProfileSchema import UpdateProfileRequest
from ...schemas.alamat_schema import UpdateAlamatBody

# common
from ....error.errorHandling import HttpException
import aiofiles
from python_random_strings import random_strings
import aiofiles
from ....utils.updateTable_util import updateTable
import os
from copy import deepcopy
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

async def updateProfile(id_walas : int,body : UpdateProfileRequest,alamat : UpdateAlamatBody,session : AsyncSession) -> GuruWalasWithAlamat :
    findWalas = (await session.execute(select(GuruWalas).options(joinedload(GuruWalas.alamat)).where(GuruWalas.id == id_walas))).scalar_one_or_none()

    if findWalas is None :
        raise HttpException(404,f"Guru Walas tidak ditemukan")
    
    if body.model_dump(exclude_unset=True):
        updateTable(body,findWalas)

    if alamat.model_dump(exclude_unset=True):
        updateTable(alamat,findWalas.alamat)

    await session.commit()

    return {
        "msg" : "success",
        "data" : findWalas
    }

PROFILE_STORE = os.getenv("DEV_FOTO_PROFILE_GURU_WALAS_STORE")
PROFILE_BASE_URL = os.getenv("DEV_FOTO_PROFILE_GURU_WALAS_BASE_URL")

async def add_update_foto_profile(id : int,foto_profile : UploadFile,session : AsyncSession) -> GuruWalasBase :
    findWalas = (await session.execute(select(GuruWalas).where(GuruWalas.id == id))).scalar_one_or_none()
    if not findWalas :
        raise HttpException(404,f"Guru Walas tidak ditemukan")

    ext_file = foto_profile.filename.split(".")

    if ext_file[-1] not in ["jpg","png","jpeg"] :
        raise HttpException(400,f"file harus berupa gambar")

    file_name = f"{random_strings.random_digits(12)}-{foto_profile.filename.split(' ')[0]}.{ext_file[-1]}"
    file_name_save = f"{PROFILE_STORE}{file_name}"
        
    fotoProfileBefore = findWalas.foto_profile

    async with aiofiles.open(file_name_save, "wb") as f:
        await f.write(foto_profile.file.read())
        print(PROFILE_BASE_URL)
        findWalas.foto_profile = f"{PROFILE_BASE_URL}/{file_name}"
    
    if fotoProfileBefore :
        print(fotoProfileBefore)
        file_nama_db_split = fotoProfileBefore.split("/")
        file_name_db = file_nama_db_split[-1]
        os.remove(f"{PROFILE_STORE}/{file_name_db}")
    
    guruWalasDictCopy = deepcopy(findWalas.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : guruWalasDictCopy
    }
