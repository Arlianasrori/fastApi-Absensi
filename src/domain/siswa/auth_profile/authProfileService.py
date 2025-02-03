from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

# models 
from ....models.siswa_model import Siswa
from ....models.siswa_model import Kelas
# schemas
from ...schemas.siswa_schema import SiswaBase, SiswaDetailWithSekolahJumlahSiswa
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

async def getProfile(id_siswa : int,session : AsyncSession) -> SiswaDetailWithSekolahJumlahSiswa :
    findSiswa = (await session.execute(select(Siswa).options(joinedload(Siswa.jurusan),joinedload(Siswa.kelas).subqueryload(Kelas.siswa),joinedload(Siswa.alamat),joinedload(Siswa.sekolah)).where(Siswa.id == id_siswa))).scalar_one_or_none()
    if not findSiswa :
        raise HttpException(404,f"siswa tidak ditemukan")
    
    jumlah_anggota = len(findSiswa.kelas.siswa)
    
    kelasDict = findSiswa.kelas.__dict__
    kelasDict.update({"jumlah_siswa" : jumlah_anggota})
    
    siswaDictCopy = findSiswa.__dict__
    siswaDictCopy.update({"kelas" : kelasDict})
    

    return {
        "msg" : "success",
        "data" : siswaDictCopy
    }
