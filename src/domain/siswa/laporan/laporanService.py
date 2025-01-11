from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from fastapi import UploadFile

# models 
from ....models.laporan_model import LaporanSiswa, FileLaporanSiswa
# schemas
from .laporanSchema import FilterQueryLaporan, AddLaporanSiswaRequest,UpdateLaporanSiswaRequest
from ...schemas.laporanSiswa_schema import LaporanSiswaBase,LaporanSiswaDetail
# common
from ....error.errorHandling import HttpException
from datetime import datetime
from ....utils.generateId_util import generate_id
import os
import aiofiles
from copy import deepcopy
from multiprocessing import Process
from ...common.delete_image_laporan_list import deleteImageList
from ...common.delete_image_laporan import deleteImage
from ...schemas.response_schema import MessageOnlyResponse
from ....utils.updateTable_util import updateTable

async def getAllLaporan(siswa : dict,query : FilterQueryLaporan,session : AsyncSession) -> list[LaporanSiswaBase] :
    now = datetime.now()
    startQuery = datetime(query.year if query.year else now.year, query.month if query.month else 1, 1,00,00,00)
    endQuery = datetime(query.year if query.year else now.year, query.month if query.month else 12, 31,12,60,60)
    findLaporan = (await session.execute(select(LaporanSiswa).where(and_(LaporanSiswa.id_siswa == siswa["id"],LaporanSiswa.datetime >= startQuery,LaporanSiswa.datetime <= endQuery)))).scalars().all()

    return {
        "msg" : "success",
        "data" : findLaporan
    }

async def getLaporanById(id : int,session : AsyncSession) -> LaporanSiswaDetail :
    findLaporan = (await session.execute(select(LaporanSiswa).options(joinedload(LaporanSiswa.siswa),joinedload(LaporanSiswa.file)).where(LaporanSiswa.id == id))).scalar_one_or_none()
    if not findLaporan :
        raise HttpException(404,f"laporan tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findLaporan
    }

async def addLaporan(id_siswa : int,laporan : AddLaporanSiswaRequest,session : AsyncSession) -> LaporanSiswaBase :
    laporanMapping = laporan.model_dump()
    laporanMapping.update({"id" : generate_id(),"id_siswa" : id_siswa,"datetime" : datetime.now()})

    session.add(LaporanSiswa(**laporanMapping))
    await session.commit()

    return {
        "msg" : "success",
        "data" : laporanMapping
    }

FILE_LAPORAN_STORE = os.getenv("DEV_PKL_SISWA")
FILE_LAPORAN_BASE_URL = os.getenv("DEV_SISWA_BASE_URL")
async def addFileLaporan(id_siswa : int,id_laporan : int,file : UploadFile,session : AsyncSession) -> LaporanSiswaDetail :
    findLaporanPkl = (await session.execute(select(LaporanSiswa).where(and_(LaporanSiswa.id == id_laporan,LaporanSiswa.id_siswa == id_siswa)))).scalar_one_or_none()

    if not findLaporanPkl :
        raise HttpException(404,f"laporan tidak ditemukan")

    ext_file = file.filename.split(".")

    if ext_file[-1] not in ["jpg","png","jpeg","pdf","docx","doc","xls","xlsx"] :
        raise HttpException(400,f"format file tidak di dukung")

    file_name = f"{generate_id()}-{file.filename.split(' ')[0].split(".")[0]}.{ext_file[-1]}"
    
    file_name_save = f"{FILE_LAPORAN_STORE}{file_name}"

    async with aiofiles.open(file_name_save, "wb") as f:
        await f.write(file.file.read())
        fileMapping = {"id" : generate_id(),"id_laporan" : id_laporan,"file" : f"{FILE_LAPORAN_BASE_URL}/{file_name}"}
        await session.add(FileLaporanSiswa(**fileMapping))
    
    laporanPklDictCopy = deepcopy(findLaporanPkl.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : {**laporanPklDictCopy,file : [fileMapping]}
    }

async def deleteFileLaporan(id_siswa : int,id_file : int,session : AsyncSession) -> MessageOnlyResponse :
    findFileLaporan = (await session.execute(select(FileLaporanSiswa).where(and_(FileLaporanSiswa.id == id_file,FileLaporanSiswa.laporan.and_(LaporanSiswa.id_siswa == id_siswa))))).scalar_one_or_none()

    if not findFileLaporan :
        raise HttpException(404,f"file laporan tidak ditemukan")
    
    fileUrlCopy = findFileLaporan.file
    session.delete(findFileLaporan)
    await session.commit()
    proccess = Process(target=deleteImage,args=(fileUrlCopy,FILE_LAPORAN_STORE))
    proccess.start()

    return {
        "msg" : "success"
    }

async def deleteLaporan(id_siswa : int,id_laporan : int,session : AsyncSession) -> LaporanSiswaDetail :
    findLaporan = (await session.execute(select(LaporanSiswa).options(joinedload(LaporanSiswa.file)).where(and_(LaporanSiswa.id == id_laporan,LaporanSiswa.id_siswa == id_siswa)))).scalar_one_or_none()

    if not findLaporan :
        raise HttpException(404,f"laporan tidak ditemukan")
    
    fileLaporanCopy = deepcopy(findLaporan.file)

    proccess = Process(target=deleteImageList,args=(fileLaporanCopy,FILE_LAPORAN_STORE))
    proccess.start()
    laporanDictCopy = deepcopy(findLaporan.__dict__)
    await session.delete(findLaporan)
    await session.commit()

    return {
        "msg" : "success",
        "data" : laporanDictCopy
    }


async def updateLaporan(id_siswa : int,id_laporan : int,laporan : UpdateLaporanSiswaRequest,session : AsyncSession) -> LaporanSiswaBase :
    findLaporan = (await session.execute(select(LaporanSiswa).where(and_(LaporanSiswa.id == id_laporan,LaporanSiswa.id_siswa == id_siswa)))).scalar_one_or_none()

    if not findLaporan :
        raise HttpException(404,f"laporan tidak ditemukan")

    if laporan :
        updateTable(findLaporan,laporan)
        await session.commit()

    laporanDictCopy = deepcopy(findLaporan.__dict__)
    return {
        "msg" : "success",
        "data" : laporanDictCopy
    }