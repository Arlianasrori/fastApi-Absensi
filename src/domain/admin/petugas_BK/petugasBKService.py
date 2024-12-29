from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload, subqueryload

# models
from ....models.petugas_BK_model import PetugasBK,AlamatPetugasBK,DistribusiPetugasBK
from ....models.sekolah_model import TahunSekolah
from ....models.siswa_model import Kelas, Jurusan

# schemas
from ...schemas.petugasBK_schema import PetugasBkBase,PetugasBKWithAlamatAndDistribusi
from ...schemas.alamat_schema import AlamatBody,UpdateAlamatBody
from .petugasBkSchema import AddPetugasBKRequest,UpdatePetugasBKRequest,ResponsePetugasBKPag,AddDistribusiPetugasBKRequest

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

async def AddPetugasBK(id_sekolah : int,petugasBK : AddPetugasBKRequest,alamat : AlamatBody,session : AsyncSession) -> PetugasBKWithAlamatAndDistribusi:
    findPetugasBKWithNirp = (await session.execute(select(PetugasBK).where(PetugasBK.nip == PetugasBK.nip))).scalar_one_or_none()
    if findPetugasBKWithNirp :
        raise HttpException(400,f"Petugas BK dengan nip {petugasBK.nip} telah ditambahkan")
    
    findPetugasBKWithEmail = (await session.execute(select(PetugasBK).where(PetugasBK.email == PetugasBK.email))).scalar_one_or_none()
    if findPetugasBKWithEmail :
        raise HttpException(400,f"Petugas BK dengan email {petugasBK.email} telah ditambahkan")

    findPetugasBkByNomorTelepon = (await session.execute(select(PetugasBK).where(PetugasBK.no_telepon == PetugasBK.no_telepon))).scalar_one_or_none()

    if findPetugasBkByNomorTelepon :
        raise HttpException(400,f"nomor telepon {petugasBK.no_telepon} sudah ditambahkan")
    
    findTahun = (await session.execute(select(TahunSekolah).where(TahunSekolah.id == petugasBK.id_tahun))).scalar_one_or_none()
    if not findTahun :
        raise HttpException(400,f"Tahun dengan id {petugasBK.id_tahun} tidak ditemukan")
    
    listDistribusiKelasForDb = []
    listDistribusiForResponse = []
    id_petugas_BK = generate_id()
    print("hhh")
    if petugasBK.distribusi_kelas :
        for distribusi in petugasBK.distribusi_kelas :
            findKelas = (await session.execute(select(Kelas).where(and_(Kelas.id == distribusi.id_kelas,Kelas.jurusan.and_(Jurusan.id_sekolah == id_sekolah))))).scalar_one_or_none()
            if not findKelas :
                raise HttpException(400,f"Kelas dengan id {distribusi.id_kelas} tidak ditemukan")
            
            distribusiMapping = {"id" : generate_id(),"id_petugas_BK" : id_petugas_BK,"id_kelas" : distribusi.id_kelas}
            listDistribusiKelasForDb.append(DistribusiPetugasBK(**distribusiMapping))
            listDistribusiForResponse.append({"id" : distribusiMapping["id"],"kelas" : deepcopy(findKelas.__dict__)})

    
    petugasBKMapping = petugasBK.model_dump(exclude={"distribusi_kelas"})
    petugasBKMapping.update({"id" : id_petugas_BK ,"password" : bcrypt.create_hash_password(petugasBK.password),"id_sekolah" : id_sekolah})
    alamatMapping = alamat.model_dump()
    alamatMapping.update({"id_petugas_BK" : petugasBKMapping["id"]})
    session.add(PetugasBK(**petugasBKMapping,alamat = AlamatPetugasBK(**alamatMapping)))
    session.add_all(listDistribusiKelasForDb)
    await session.commit()
    return {
        "msg" : "success",
        "data" : {
            **petugasBKMapping,
            "foto_profile" : None,
            "token_FCM" : None,
            "alamat" : alamatMapping,
            "distribusi_petugas_BK" : listDistribusiForResponse
        }
    }

PROFILE_STORE = os.getenv("DEV_FOTO_PROFILE_PETUGAS_BK_STORE")
PROFILE_BASE_URL = os.getenv("DEV_FOTO_PROFILE_PETUGAS_BK_BASE_URL")

async def add_update_foto_profile(id : int,id_sekolah : int,foto_profile : UploadFile,session : AsyncSession) -> PetugasBkBase :
    findPetugasBK = (await session.execute(select(PetugasBK).where(and_(PetugasBK.id == id,PetugasBK.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findPetugasBK :
        raise HttpException(404,f"guru mapel tidak ditemukan")

    ext_file = foto_profile.filename.split(".")

    if ext_file[-1] not in ["jpg","png","jpeg"] :
        raise HttpException(400,f"file harus berupa gambar")

    file_name = f"{generate_id()}-{foto_profile.filename.split(' ')[0]}.{ext_file[-1]}"
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

async def getAllPetugasBK(page : int | None,id_sekolah : int,id_tahun : int,session : AsyncSession) -> PetugasBKWithAlamatAndDistribusi | ResponsePetugasBKPag:
    statementGetPetugasBK = select(PetugasBK).options(joinedload(PetugasBK.alamat),subqueryload(PetugasBK.distribusi_petugas_BK).joinedload(DistribusiPetugasBK.kelas)).where(and_(PetugasBK.id_sekolah == id_sekolah,PetugasBK.id_tahun == id_tahun))

    if page :
        findPetugasBK = (await session.execute(statementGetPetugasBK.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(PetugasBK.id))).scalar_one()
        countPage = math.ceil(conntData / 10)
        return {
            "msg" : "success",
            "data" : {
                "data" : findPetugasBK,
                "count_data" : len(findPetugasBK),
                "count_page" : countPage
            }
        }
    else :
        findPetugasBK = (await session.execute(statementGetPetugasBK)).scalars().all()
        return {
            "msg" : "success",
            "data" : findPetugasBK
        }

async def getPetugasBKId(id : int,id_sekolah : int,session : AsyncSession) -> PetugasBKWithAlamatAndDistribusi:
    findPetugasBK = (await session.execute(select(PetugasBK).options(joinedload(PetugasBK.alamat),subqueryload(PetugasBK.distribusi_petugas_BK).joinedload(DistribusiPetugasBK.kelas)).where(and_(PetugasBK.id == id,PetugasBK.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if not findPetugasBK :
        raise HttpException(404,f"Petugas BK dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findPetugasBK
    }

async def updatePetugasBK(id : int,id_sekolah : int,petugasBK : UpdatePetugasBKRequest,alamat : UpdateAlamatBody,session : AsyncSession) -> PetugasBKWithAlamatAndDistribusi :
    findPetugasBK = (await session.execute(select(PetugasBK).options(joinedload(PetugasBK.alamat),subqueryload(PetugasBK.distribusi_petugas_BK).joinedload(DistribusiPetugasBK.kelas)).where(and_(PetugasBK.id == id,PetugasBK.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findPetugasBK :
        raise HttpException(404,f"Petugas BK dengan id {id} tidak ditemukan")
    
    if petugasBK.nip :
        findPetugasBKByNip = (await session.execute(select(PetugasBK).where(and_(PetugasBK.nip == PetugasBK.nip,PetugasBK.id != id)))).scalar_one_or_none()
        if findPetugasBKByNip :
            raise HttpException(400,f"Petugas BK dengan nip {petugasBK.nip} sudah ditambahkan")
    
    if petugasBK.no_telepon :
        findPetugasBKByNoTelepon = (await session.execute(select(PetugasBK).where(and_(PetugasBK.no_telepon == PetugasBK.no_telepon,PetugasBK.id != id)))).scalar_one_or_none()
        if findPetugasBKByNoTelepon :
            raise HttpException(400,f"Petugas BKs dengan nomor telepon {petugasBK.no_telepon} sudah ditambahkan")
    
    if petugasBK.email :
        findPetugasBKByEmail = (await session.execute(select(PetugasBK).where(and_(PetugasBK.email == PetugasBK.email,PetugasBK.id != id)))).scalar_one_or_none()
        if findPetugasBKByEmail :
            raise HttpException(400,f"Guru walas dengan email {petugasBK.email} sudah ditambahkan")
    
    if petugasBK.password :
        petugasBK.password = bcrypt.create_hash_password(petugasBK.password)

    if petugasBK.model_dump(exclude_unset=True) :
        updateTable(petugasBK,findPetugasBK)


    if alamat.model_dump(exclude_unset=True):
        updateTable(alamat,findPetugasBK.alamat)

    guruWalasDictCopy = deepcopy(findPetugasBK.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : guruWalasDictCopy
    }

async def deletePetugasBK(id : int,id_sekolah : int,session : AsyncSession) -> PetugasBkBase:
    findPetugasBK = (await session.execute(select(PetugasBK).where(and_(PetugasBK.id == id,PetugasBK.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findPetugasBK :
        raise HttpException(404,f"Petugas BK dengan id {id} tidak ditemukan")
    
    fotoProfileBefore = deepcopy(findPetugasBK.foto_profile)
    await session.delete(findPetugasBK)
    petugasBKDictCopy = deepcopy(findPetugasBK.__dict__)
    await session.commit()

    if fotoProfileBefore :
        file_nama_db_split = fotoProfileBefore.split("/")
        file_name_db = file_nama_db_split[-1]

        proccess = Process(target=removeFile,args=(f"{PROFILE_STORE}/{file_name_db}",))
        proccess.start()
    
    return {
        "msg" : "success",
        "data" : petugasBKDictCopy
    }

async def addDistribusiPetugasBK(id_petugas_BK : int,id_sekolah : int,id_tahun : int,distribusi : AddDistribusiPetugasBKRequest,session : AsyncSession) -> PetugasBKWithAlamatAndDistribusi :
    findPetugasBK = (await session.execute(select(PetugasBK).where(and_(PetugasBK.id == id_petugas_BK,PetugasBK.id_sekolah == id_sekolah,PetugasBK.id_tahun == id_tahun)))).scalar_one_or_none()
    if not findPetugasBK :
        raise HttpException(404,f"Petugas BK dengan id {id_petugas_BK} tidak ditemukan")
    
    findKelas = (await session.execute(select(Kelas).where(and_(Kelas.id == distribusi.id_kelas,Kelas.jurusan.and_(Jurusan.id_sekolah == id_sekolah),Kelas.jurusan.and_(Jurusan.id_tahun == id_tahun))))).scalar_one_or_none()
    if not findKelas :
        raise HttpException(404,f"Kelas dengan id {distribusi.id_kelas} tidak ditemukan")
    
    findDistribusi = (await session.execute(select(DistribusiPetugasBK).where(and_(DistribusiPetugasBK.id_petugas_BK == id_petugas_BK,DistribusiPetugasBK.id_kelas == distribusi.id_kelas)))).scalar_one_or_none()
    if findDistribusi :
        raise HttpException(400,f"Distribusi petugas BK dengan id kelas {distribusi.id_kelas} sudah ditambahkan")
    
    session.add(DistribusiPetugasBK(id=generate_id(),id_petugas_BK = id_petugas_BK,id_kelas = distribusi.id_kelas))
    await session.commit()
    return {
        "msg" : "Add success"
    }

async def deleteDistribusiPetugasBK(id : int,id_sekolah : int,session : AsyncSession) -> PetugasBKWithAlamatAndDistribusi :
    findDistribusi = (await session.execute(select(DistribusiPetugasBK).where(and_(DistribusiPetugasBK.id == id)))).scalar_one_or_none()

    if not findDistribusi :
        raise HttpException(404,f"Distribusi petugas BK dengan id {id} tidak ditemukan")
    
    await session.delete(findDistribusi)
    await session.commit()
    return {
        "msg" : "Delete success"
    }