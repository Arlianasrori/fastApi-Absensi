from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

# models 
from ....models.siswa_model import Siswa
# schemas
from ...schemas.siswa_schema import SiswaBase, SiswaWithJurusanKelasAlamat
# common
from ....error.errorHandling import HttpException

async def getSiswa(id_siswa : int,session : AsyncSession) -> SiswaBase :
    findSiswa = (await session.execute(select(Siswa).where(Siswa.id == id_siswa))).scalar_one_or_none()
    if not findSiswa :
        raise HttpException(404,f"siswa tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findSiswa
    }

async def getProfile(id_siswa : int,session : AsyncSession) -> SiswaWithJurusanKelasAlamat :
    findSiswa = (await session.execute(select(Siswa).options(joinedload(Siswa.jurusan),joinedload(Siswa.kelas),joinedload(Siswa.alamat)).where(Siswa.id == id_siswa))).scalar_one_or_none()
    if not findSiswa :
        raise HttpException(404,f"siswa tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findSiswa
    }
