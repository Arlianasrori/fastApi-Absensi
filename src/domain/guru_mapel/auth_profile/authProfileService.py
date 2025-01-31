from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload
from fastapi import UploadFile

# models 
from ...schemas.guruMapel_schema import GuruMapelBase, GuruMapelDetailWithSekolah, GuruMapelWithAlamat
from ....models.guru_mapel_model import GuruMapel
from ...schemas.alamat_schema import UpdateAlamatBody
from .authprofileSchema import UpdateProfileRequest

# common
from ....error.errorHandling import HttpException
from ....utils.updateTable_util import updateTable
from python_random_strings import random_strings
import aiofiles
import os
from copy import deepcopy

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

async def updateProfile(id_guru_mapel : int,body : UpdateProfileRequest,alamat : UpdateAlamatBody,session : AsyncSession) -> GuruMapelWithAlamat :
    findGuruMapel = (await session.execute(select(GuruMapel).options(joinedload(GuruMapel.alamat)).where(GuruMapel.id == id_guru_mapel))).scalar_one_or_none()

    if findGuruMapel is None :
        raise HttpException(404,f"guru mapel tidak ditemukan")
    
    if body.model_dump(exclude_unset=True):
        updateTable(body,findGuruMapel)

    if alamat.model_dump(exclude_unset=True):
        updateTable(alamat,findGuruMapel.alamat)

    guruMapelDictCopy = deepcopy(findGuruMapel.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : guruMapelDictCopy
    }

PROFILE_STORE = os.getenv("DEV_FOTO_PROFILE_GURU_MAPEL_STORE")
PROFILE_BASE_URL = os.getenv("DEV_FOTO_PROFILE_GURU_MAPEL_BASE_URL")

async def add_update_foto_profile(id : int,foto_profile : UploadFile,session : AsyncSession) -> GuruMapelBase :
    findGuruMapel = (await session.execute(select(GuruMapel).where(GuruMapel.id == id))).scalar_one_or_none()
    if not findGuruMapel :
        raise HttpException(404,f"guru mapel tidak ditemukan")

    ext_file = foto_profile.filename.split(".")

    if ext_file[-1] not in ["jpg","png","jpeg"] :
        raise HttpException(400,f"file harus berupa gambar")

    file_name = f"{random_strings.random_digits(12)}-{foto_profile.filename.split(' ')[0]}.{ext_file[-1]}"
    file_name_save = f"{PROFILE_STORE}{file_name}"
        
    fotoProfileBefore = findGuruMapel.foto_profile

    async with aiofiles.open(file_name_save, "wb") as f:
        await f.write(foto_profile.file.read())
        print(PROFILE_BASE_URL)
        findGuruMapel.foto_profile = f"{PROFILE_BASE_URL}/{file_name}"
    
    if fotoProfileBefore :
        print(fotoProfileBefore)
        file_nama_db_split = fotoProfileBefore.split("/")
        file_name_db = file_nama_db_split[-1]
        os.remove(f"{PROFILE_STORE}/{file_name_db}")
    
    guruMapelDictCopy = deepcopy(findGuruMapel.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : guruMapelDictCopy
    }