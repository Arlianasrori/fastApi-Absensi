from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from fastapi import UploadFile

# models 
from ....models.siswa_model import Siswa
# schemas
from ...schemas.siswa_schema import SiswaBase, SiswaDetailWithSekolah, SiswaWithAlamat
from .authProfileSchema import UpdateProfileRequest
from ...schemas.alamat_schema import UpdateAlamatBody
# common
from ....error.errorHandling import HttpException
from ....utils.updateTable_util import updateTable
import os
from python_random_strings import random_strings
import aiofiles
from copy import deepcopy

async def getSiswa(id_siswa : int,session : AsyncSession) -> SiswaBase :
    findSiswa = (await session.execute(select(Siswa).where(Siswa.id == id_siswa))).scalar_one_or_none()
    if not findSiswa :
        raise HttpException(404,f"siswa tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findSiswa
    }

async def getProfile(id_siswa : int,session : AsyncSession) -> SiswaDetailWithSekolah :
    findSiswa = (await session.execute(select(Siswa).options(joinedload(Siswa.jurusan),joinedload(Siswa.kelas),joinedload(Siswa.alamat),joinedload(Siswa.sekolah)).where(Siswa.id == id_siswa))).scalar_one_or_none()
    if not findSiswa :
        raise HttpException(404,f"siswa tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findSiswa
    }

async def updateProfile(id_siswa : int,body : UpdateProfileRequest,alamat : UpdateAlamatBody,session : AsyncSession) -> SiswaWithAlamat :
    findSiswa = (await session.execute(select(Siswa).options(joinedload(Siswa.alamat)).where(Siswa.id == id_siswa))).scalar_one_or_none()

    if findSiswa is None :
        raise HttpException(404,f"siswa tidak ditemukan")
    
    if body.model_dump(exclude_unset=True):
        updateTable(body,findSiswa)

    if alamat.model_dump(exclude_unset=True):
        updateTable(alamat,findSiswa.alamat)

    siswaDictCopy = deepcopy(findSiswa.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : siswaDictCopy
    }

PROFILE_STORE = os.getenv("DEV_FOTO_PROFILE_SISWA_STORE")
PROFILE_BASE_URL = os.getenv("DEV_FOTO_PROFILE_SISWA_BASE_URL")

async def add_update_foto_profile(id : int,foto_profile : UploadFile,session : AsyncSession) -> SiswaBase :
    findSiswa = (await session.execute(select(Siswa).where(Siswa.id == id))).scalar_one_or_none()
    if not findSiswa :
        raise HttpException(404,f"siswa tidak ditemukan")

    ext_file = foto_profile.filename.split(".")

    if ext_file[-1] not in ["jpg","png","jpeg"] :
        raise HttpException(400,f"file harus berupa gambar")

    file_name = f"{random_strings.random_digits(12)}-{foto_profile.filename.split(' ')[0]}.{ext_file[-1]}"
    file_name_save = f"{PROFILE_STORE}{file_name}"
        
    fotoProfileBefore = findSiswa.foto_profile

    async with aiofiles.open(file_name_save, "wb") as f:
        await f.write(foto_profile.file.read())
        print(PROFILE_BASE_URL)
        findSiswa.foto_profile = f"{PROFILE_BASE_URL}/{file_name}"
    
    if fotoProfileBefore :
        print(fotoProfileBefore)
        file_nama_db_split = fotoProfileBefore.split("/")
        file_name_db = file_nama_db_split[-1]
        os.remove(f"{PROFILE_STORE}/{file_name_db}")
    
    siswaDictCopy = deepcopy(findSiswa.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : siswaDictCopy
    }