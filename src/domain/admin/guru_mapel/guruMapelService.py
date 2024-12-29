from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models
from ....models.guru_mapel_model import GuruMapel,AlamatGuruMapel
from ....models.sekolah_model import TahunSekolah
from ....models.jadwal_model import Mapel

# schemas
from ...schemas.guruMapel_schema import GuruMapelBase,GuruMapeldetail
from ...schemas.alamat_schema import AlamatBody,UpdateAlamatBody
from .guruMapelSchema import AddGuruMapelRequest,UpdateGuruMapelRequest,ResponseGuruMapelPag

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

async def addGuruMapel(id_sekolah : int,guruMapel : AddGuruMapelRequest,alamat : AlamatBody,session : AsyncSession) -> GuruMapeldetail:
    findGuruMapelByNirp = (await session.execute(select(GuruMapel).where(GuruMapel.nip == GuruMapel.nip))).scalar_one_or_none()
    if findGuruMapelByNirp :
        raise HttpException(400,f"Guru Mapel dengan nip {guruMapel.nip} telah ditambahkan")

    
    findGuruMapelByEmail = (await session.execute(select(GuruMapel).where(GuruMapel.email == GuruMapel.email))).scalar_one_or_none()
    if findGuruMapelByEmail :
        raise HttpException(400,f"Guru Mapel dengan email {guruMapel.email} telah ditambahkan")
    
    findMapel = (await session.execute(select(Mapel).where(Mapel.id == guruMapel.id_mapel))).scalar_one_or_none()
    if not findMapel :
        raise HttpException(400,f"Mapel dengan id {guruMapel.id_mapel} tidak ditemukan")

    findGuruMapelByNoTelepon = (await session.execute(select(GuruMapel).where(GuruMapel.no_telepon == GuruMapel.no_telepon))).scalar_one_or_none()

    if findGuruMapelByNoTelepon :
        raise HttpException(400,f"nomor telepon {guruMapel.no_telepon} sudah ditambahkan")
    
    findTahun = (await session.execute(select(TahunSekolah).where(TahunSekolah.id == guruMapel.id_tahun))).scalar_one_or_none()
    if not findTahun :
        raise HttpException(400,f"Tahun dengan id {guruMapel.id_tahun} tidak ditemukan")
    
    guruMapelMapping = guruMapel.model_dump()
    guruMapelMapping.update({"id" : generate_id(),"id_sekolah" : id_sekolah,"password" : bcrypt.create_hash_password(guruMapel.password)})
    alamatMapping = alamat.model_dump()
    alamatMapping.update({"id_guru_mapel" : guruMapelMapping["id"]})
    session.add(GuruMapel(**guruMapelMapping,alamat = AlamatGuruMapel(**alamatMapping)))
    await session.commit()
    
    return {
        "msg" : "success",
        "data" : {
            **guruMapelMapping,
            "foto_profile" : None,
            "token_FCM" : None,
            "mapel" : findMapel.__dict__,
            "alamat" : alamatMapping
        }
    }

PROFILE_STORE = os.getenv("DEV_FOTO_PROFILE_GURU_MAPEL_STORE")
PROFILE_BASE_URL = os.getenv("DEV_FOTO_PROFILE_GURU_MAPEL_BASE_URL")

async def add_update_foto_profile(id : int,id_sekolah : int,foto_profile : UploadFile,session : AsyncSession) -> GuruMapelBase :
    findGuruMapel = (await session.execute(select(GuruMapel).where(and_(GuruMapel.id == id,GuruMapel.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findGuruMapel :
        raise HttpException(404,f"guru mapel tidak ditemukan")

    ext_file = foto_profile.filename.split(".")

    if ext_file[-1] not in ["jpg","png","jpeg"] :
        raise HttpException(400,f"file harus berupa gambar")

    file_name = f"{generate_id()}-{foto_profile.filename.split(' ')[0]}.{ext_file[-1]}"
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
    
    guruDictCopy = deepcopy(findGuruMapel.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : guruDictCopy
    } 

async def getAllGuruMapel(page : int | None,id_sekolah : int,id_tahun : int,session : AsyncSession) -> GuruMapeldetail | ResponseGuruMapelPag:
    statementGetGuruMapel = select(GuruMapel).options(joinedload(GuruMapel.alamat),joinedload(GuruMapel.mapel)).where(and_(GuruMapel.id_sekolah == id_sekolah,GuruMapel.id_tahun == id_tahun))

    if page :
        findGuruMapel = (await session.execute(statementGetGuruMapel.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(GuruMapel.id))).scalar_one()
        countPage = math.ceil(conntData / 10)
        return {
            "msg" : "success",
            "data" : {
                "data" : findGuruMapel,
                "count_data" : len(findGuruMapel),
                "count_page" : countPage
            }
        }
    else :
        findGuruMapel = (await session.execute(statementGetGuruMapel)).scalars().all()
        return {
            "msg" : "success",
            "data" : findGuruMapel
        }

async def getGuruMapelId(id : int,id_sekolah : int,session : AsyncSession) -> GuruMapeldetail:
    findGuruMapel = (await session.execute(select(GuruMapel).options(joinedload(GuruMapel.alamat),joinedload(GuruMapel.mapel)).where(and_(GuruMapel.id == id,GuruMapel.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if not findGuruMapel :
        raise HttpException(404,f"Guru mapel dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findGuruMapel
    }

async def updateGuruMapel(id : int,id_sekolah : int,guruMapel : UpdateGuruMapelRequest,alamat : UpdateAlamatBody,session : AsyncSession) -> GuruMapeldetail:
    findGuruMapel = (await session.execute(select(GuruMapel).options(joinedload(GuruMapel.alamat),joinedload(GuruMapel.mapel)).where(and_(GuruMapel.id == id,GuruMapel.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findGuruMapel :
        raise HttpException(404,f"Guru mapel dengan id {id} tidak ditemukan")
    
    if guruMapel.id_mapel :
        findMapel = (await session.execute(select(Mapel).where(Mapel.id == guruMapel.id_mapel))).scalar_one_or_none()
        if not findMapel :
            raise HttpException(404,f"Mapel dengan id {guruMapel.id_mapel} tidak ditemukan")
    
    if guruMapel.nip :
        findGuruMapelByNip = (await session.execute(select(GuruMapel).where(and_(GuruMapel.nip == GuruMapel.nip,GuruMapel.id != id)))).scalar_one_or_none()
        if findGuruMapelByNip :
            raise HttpException(400,f"Guru mapel dengan nip {guruMapel.nip} sudah ditambahkan")
    
    if guruMapel.no_telepon :
        findGuruMapelByNoTelepon = (await session.execute(select(guruMapel).where(and_(guruMapel.no_telepon == guruMapel.no_telepon,guruMapel.id != id)))).scalar_one_or_none()
        if findGuruMapelByNoTelepon :
            raise HttpException(400,f"Guru mapel dengan nomor telepon {guruMapel.no_telepon} sudah ditambahkan")
    
    if guruMapel.email :
        findGuruMapelByEmail = (await session.execute(select(guruMapel).where(and_(guruMapel.email == guruMapel.email,guruMapel.id != id)))).scalar_one_or_none()
        if findGuruMapelByEmail :
            raise HttpException(400,f"Guru mapel dengan email {guruMapel.email} sudah ditambahkan")

    if guruMapel.password :
        guruMapel.password = bcrypt.create_hash_password(guruMapel.password)
    if guruMapel.model_dump(exclude_unset=True) :
        updateTable(guruMapel,findGuruMapel)


    if alamat.model_dump(exclude_unset=True):
        updateTable(alamat,findGuruMapel.alamat)

    guruMapelDictCopy = deepcopy(findGuruMapel.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : guruMapelDictCopy
    }

async def deleteGuruMapel(id : int,id_sekolah : int,session : AsyncSession) -> GuruMapelBase:
    findGuruMapel = (await session.execute(select(GuruMapel).where(and_(GuruMapel.id == id,GuruMapel.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findGuruMapel :
        raise HttpException(404,f"Guru mapel dengan id {id} tidak ditemukan")
    
    fotoProfileBefore = deepcopy(findGuruMapel.foto_profile)
    await session.delete(findGuruMapel)
    guruMapelDictCopy = deepcopy(findGuruMapel.__dict__)
    await session.commit()

    if fotoProfileBefore :
        file_nama_db_split = fotoProfileBefore.split("/")
        file_name_db = file_nama_db_split[-1]

        proccess = Process(target=removeFile,args=(f"{PROFILE_STORE}/{file_name_db}",))
        proccess.start()
    
    return {
        "msg" : "success",
        "data" : guruMapelDictCopy
    }
