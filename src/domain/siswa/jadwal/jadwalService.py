from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

# models 
from ....models.siswa_model import Siswa
from ....models.jadwal_model import Jadwal, HariEnum
# schemas
from .jadwalSchema import GetHariContainsJadwalResponse, FilterJadwalQuery
from ...schemas.jadwal_schema import JadwalWithMapelGuruMapel
# common
from ....error.errorHandling import HttpException

async def getHariContainsJadwal(siswa : dict,session : AsyncSession) -> list[GetHariContainsJadwalResponse] :
    hariList = [
        HariEnum.senin.value,
        HariEnum.selasa.value,
        HariEnum.rabu.value,
        HariEnum.kamis.value,
        HariEnum.jumat.value,
        HariEnum.sabtu.value,
        HariEnum.minggu.value
    ]

    listStatistikHariForResponse = []

    for hariItem in hariList :
        findStatistikJadwal = (await session.execute(select(func.min(Jadwal.jam_mulai).label("min_jam_mulai"),func.max(Jadwal.jam_selesai).label("max_jam_selesai")).where(Jadwal.id_kelas == siswa["id_kelas"],Jadwal.id_tahun == siswa["id_tahun"], Jadwal.hari == hariItem))).one()

        statistikJadwalDict = findStatistikJadwal._asdict()

        if statistikJadwalDict.get("min_jam_mulai") and statistikJadwalDict.get("max_jam_selesai") :
            listStatistikHariForResponse.append({"hari" : hariItem,**statistikJadwalDict})
    print(listStatistikHariForResponse)
    return {
        "msg" : "success",
        "data" : listStatistikHariForResponse
    }

async def getAllJadwal(siswa : dict,query : FilterJadwalQuery,session : AsyncSession) -> list[JadwalWithMapelGuruMapel] :
    findStatistikJadwal = (await session.execute(select(Jadwal).options(joinedload(Jadwal.mapel),joinedload(Jadwal.guru_mapel)).where(Jadwal.id_kelas == siswa["id_kelas"],Jadwal.id_tahun == siswa["id_tahun"],Jadwal.hari == query.hari if query.hari else True))).scalars().all()

    return {
        "msg" : "success",
        "data" : findStatistikJadwal
    }