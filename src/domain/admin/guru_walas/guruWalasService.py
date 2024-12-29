from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models
from ....models.guru_walas_model import GuruWalas,AlamatGuruWalas
from ....models.sekolah_model import TahunSekolah
from ....models.siswa_model import Kelas

# schemas
from ...schemas.guruWalas_schema import GuruWalasBase,GuruWalasDetail
from ...schemas.alamat_schema import AlamatBody,UpdateAlamatBody
from .guruWalasSchema import AddGuruWalasRequest,UpdateGuruWalasRequest,ResponseGuruWalasPag

# common
from ....auth.bcrypt import bcrypt
import math
import os
from copy import deepcopy
from ....utils.generateId_util import generate_id
from ....error.errorHandling import HttpException
from ....utils.updateTable_util import updateTable
import aiofiles
from multiprocessing import Process
from ....utils.removeFile_util import removeFile

async def AddGuruWalas(id_sekolah : int,guruWalas : AddGuruWalasRequest,alamat : AlamatBody,session : AsyncSession) -> GuruWalasDetail:
    findGuruWalasByNirp = (await session.execute(select(GuruWalas).where(GuruWalas.nip == GuruWalas.nip))).scalar_one_or_none()
    if findGuruWalasByNirp :
        raise HttpException(400,f"Guru walas dengan nip {guruWalas.nip} telah ditambahkan")

    
    findGuruWalasByEmail = (await session.execute(select(GuruWalas).where(GuruWalas.email == GuruWalas.email))).scalar_one_or_none()
    if findGuruWalasByEmail :
        raise HttpException(400,f"Guru walas dengan email {guruWalas.email} telah ditambahkan")
    
    findKelas = (await session.execute(select(Kelas).where(Kelas.id == guruWalas.id_kelas))).scalar_one_or_none()
    if not findKelas :
        raise HttpException(400,f"Kelas dengan id {guruWalas.id_kelas} tidak ditemukan")

    findGuruWalasByNoTelepon = (await session.execute(select(GuruWalas).where(GuruWalas.no_telepon == GuruWalas.no_telepon))).scalar_one_or_none()

    if findGuruWalasByNoTelepon :
        raise HttpException(400,f"nomor telepon {guruWalas.no_telepon} sudah ditambahkan")
    
    findTahun = (await session.execute(select(TahunSekolah).where(TahunSekolah.id == guruWalas.id_tahun))).scalar_one_or_none()
    if not findTahun :
        raise HttpException(400,f"Tahun dengan id {guruWalas.id_tahun} tidak ditemukan")
    
    guruWalasMapping = guruWalas.model_dump()
    guruWalasMapping.update({"id" : generate_id(),"id_sekolah" : id_sekolah,"password" : bcrypt.create_hash_password(guruWalas.password)})
    alamatMapping = alamat.model_dump()
    alamatMapping.update({"id_guru_walas" : guruWalasMapping["id"]})
    session.add(GuruWalas(**guruWalasMapping,alamat = AlamatGuruWalas(**alamatMapping)))
    await session.commit()
    
    return {
        "msg" : "success",
        "data" : {
            **guruWalasMapping,
            "foto_profile" : None,
            "token_FCM" : None,
            "alamat" : alamatMapping
        }
    }

PROFILE_STORE = os.getenv("DEV_FOTO_PROFILE_GURU_WALAS_STORE")
PROFILE_BASE_URL = os.getenv("DEV_FOTO_PROFILE_GURU_WALAS_BASE_URL")

async def add_update_foto_profile(id : int,id_sekolah : int,foto_profile : UploadFile,session : AsyncSession) -> GuruWalasBase :
    findGuruWalas = (await session.execute(select(GuruWalas).where(and_(GuruWalas.id == id,GuruWalas.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findGuruWalas :
        raise HttpException(404,f"guru mapel tidak ditemukan")

    ext_file = foto_profile.filename.split(".")

    if ext_file[-1] not in ["jpg","png","jpeg"] :
        raise HttpException(400,f"file harus berupa gambar")

    file_name = f"{generate_id()}-{foto_profile.filename.split(' ')[0]}.{ext_file[-1]}"
    file_name_save = f"{PROFILE_STORE}{file_name}"
        
    fotoProfileBefore = findGuruWalas.foto_profile

    async with aiofiles.open(file_name_save, "wb") as f:
        await f.write(foto_profile.file.read())
        print(PROFILE_BASE_URL)
        findGuruWalas.foto_profile = f"{PROFILE_BASE_URL}/{file_name}"
    
    if fotoProfileBefore :
        print(fotoProfileBefore)
        file_nama_db_split = fotoProfileBefore.split("/")
        file_name_db = file_nama_db_split[-1]
        os.remove(f"{PROFILE_STORE}/{file_name_db}")
    
    walasDictCopy = deepcopy(findGuruWalas.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : walasDictCopy
    } 

async def getAllGuruWalas(page : int | None,id_sekolah : int,id_tahun : int,session : AsyncSession) -> GuruWalasDetail | ResponseGuruWalasPag:
    statementGetGuruWalas = select(GuruWalas).options(joinedload(GuruWalas.alamat),joinedload(GuruWalas.kelas)).where(and_(GuruWalas.id_sekolah == id_sekolah,GuruWalas.id_tahun == id_tahun))

    if page :
        findGuruWalas = (await session.execute(statementGetGuruWalas.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(GuruWalas.id))).scalar_one()
        countPage = math.ceil(conntData / 10)
        return {
            "msg" : "success",
            "data" : {
                "data" : findGuruWalas,
                "count_data" : len(findGuruWalas),
                "count_page" : countPage
            }
        }
    else :
        findGuruWalas = (await session.execute(statementGetGuruWalas)).scalars().all()
        return {
            "msg" : "success",
            "data" : findGuruWalas
        }

async def getGuruWalasId(id : int,id_sekolah : int,session : AsyncSession) -> GuruWalasDetail:
    findGuruWalas = (await session.execute(select(GuruWalas).options(joinedload(GuruWalas.alamat),joinedload(GuruWalas.kelas)).where(and_(GuruWalas.id == id,GuruWalas.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if not findGuruWalas :
        raise HttpException(404,f"Guru walas dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findGuruWalas
    }

async def updateGuruWalas(id : int,id_sekolah : int,guruWalas : UpdateGuruWalasRequest,alamat : UpdateAlamatBody,session : AsyncSession) -> GuruWalasDetail:
    print(guruWalas.model_dump(exclude_unset=True))
    findGuruWalas = (await session.execute(select(GuruWalas).options(joinedload(GuruWalas.alamat),joinedload(GuruWalas.kelas)).where(and_(GuruWalas.id == id,GuruWalas.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findGuruWalas :
        raise HttpException(404,f"Guru walas dengan id {id} tidak ditemukan")
    
    if guruWalas.id_kelas :
        findKelas = (await session.execute(select(Kelas).where(Kelas.id == guruWalas.id_kelas))).scalar_one_or_none()
        if not findKelas :
            raise HttpException(404,f"Kelas dengan id {guruWalas.id_kelas} tidak ditemukan")
    
    if guruWalas.nip :
        findGuruWalasByNip = (await session.execute(select(GuruWalas).where(and_(GuruWalas.nip == GuruWalas.nip,GuruWalas.id != id)))).scalar_one_or_none()
        if findGuruWalasByNip :
            raise HttpException(400,f"Guru mapel dengan nip {guruWalas.nip} sudah ditambahkan")
    
    if guruWalas.no_telepon :
        findGuruWalasByNoTelepon = (await session.execute(select(guruWalas).where(and_(guruWalas.no_telepon == guruWalas.no_telepon,guruWalas.id != id)))).scalar_one_or_none()
        if findGuruWalasByNoTelepon :
            raise HttpException(400,f"Guru walas dengan nomor telepon {guruWalas.no_telepon} sudah ditambahkan")
    
    if guruWalas.email :
        findGuruWalasByEmail = (await session.execute(select(guruWalas).where(and_(guruWalas.email == guruWalas.email,guruWalas.id != id)))).scalar_one_or_none()
        if findGuruWalasByEmail :
            raise HttpException(400,f"Guru walas dengan email {guruWalas.email} sudah ditambahkan")

    if guruWalas.password :
        guruWalas.password = bcrypt.create_hash_password(guruWalas.password)

    if guruWalas.model_dump(exclude_unset=True) :
        updateTable(guruWalas,findGuruWalas)


    if alamat.model_dump(exclude_unset=True):
        updateTable(alamat,findGuruWalas.alamat)

    guruWalasDictCopy = deepcopy(findGuruWalas.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : guruWalasDictCopy
    }

async def deleteGuruWalas(id : int,id_sekolah : int,session : AsyncSession) -> GuruWalasBase:
    findGuruWalas = (await session.execute(select(GuruWalas).where(and_(GuruWalas.id == id,GuruWalas.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findGuruWalas :
        raise HttpException(404,f"Guru walas dengan id {id} tidak ditemukan")
    
    fotoProfileBefore = deepcopy(findGuruWalas.foto_profile)
    await session.delete(findGuruWalas)
    guruWalasDictCopy = deepcopy(findGuruWalas.__dict__)
    await session.commit()

    if fotoProfileBefore :
        file_nama_db_split = fotoProfileBefore.split("/")
        file_name_db = file_nama_db_split[-1]

        proccess = Process(target=removeFile,args=(f"{PROFILE_STORE}/{file_name_db}",))
        proccess.start()
    
    return {
        "msg" : "success",
        "data" : guruWalasDictCopy
    }