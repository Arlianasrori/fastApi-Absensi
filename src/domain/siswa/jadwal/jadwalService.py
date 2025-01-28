from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

# models 
from ....models.siswa_model import Siswa
from ....models.jadwal_model import Jadwal, HariEnum
from ....models.absen_model import Absen
# schemas
from .jadwalSchema import GetHariContainsJadwalResponse, FilterJadwalQuery, JadwalTodayResponse
from ...schemas.jadwal_schema import JadwalDetail
# types
from ....types.hari_list import dayCodeSet 
# common
from ....error.errorHandling import HttpException
from datetime import datetime
from ...common.get_day_today import get_day

async def getHariContainsJadwal(siswa : dict,session : AsyncSession) -> list[GetHariContainsJadwalResponse] :

    listStatistikHariForResponse = []

    for hariItem in dayCodeSet :
        findStatistikJadwal = (await session.execute(select(func.min(Jadwal.jam_mulai).label("min_jam_mulai"),func.max(Jadwal.jam_selesai).label("max_jam_selesai")).where(Jadwal.id_kelas == siswa["id_kelas"],Jadwal.id_tahun == siswa["id_tahun"], Jadwal.hari == hariItem.value))).one()

        statistikJadwalDict = findStatistikJadwal._asdict()

        if statistikJadwalDict.get("min_jam_mulai") and statistikJadwalDict.get("max_jam_selesai") :
            listStatistikHariForResponse.append({"hari" : hariItem,**statistikJadwalDict})
    print(listStatistikHariForResponse)
    return {
        "msg" : "success",
        "data" : listStatistikHariForResponse
    }

async def getAllJadwal(siswa : dict,query : FilterJadwalQuery,session : AsyncSession) -> list[JadwalDetail] :
    findJadwal = (await session.execute(select(Jadwal).options(joinedload(Jadwal.mapel),joinedload(Jadwal.koordinat),joinedload(Jadwal.guru_mapel),joinedload(Jadwal.kelas)).where(Jadwal.id_kelas == siswa["id_kelas"],Jadwal.id_tahun == siswa["id_tahun"],Jadwal.hari == query.hari if query.hari else True))).scalars().all()

    return {
        "msg" : "success",
        "data" : findJadwal
    }

async def getAllJadwalToday(siswa : dict,session : AsyncSession) -> JadwalTodayResponse :
    dayTodaay : dict = await get_day()
    dateToday = datetime.now().date()
    findJadwal = (await session.execute(select(Jadwal).options(joinedload(Jadwal.mapel)).where(Jadwal.id_kelas == siswa["id_kelas"],Jadwal.hari == dayTodaay["day_name"]))).scalars().all()

    findAllAbsenSiswaToday = (await session.execute(select(Absen).where(Absen.id_siswa == siswa["id"],Absen.tanggal == dateToday))).scalars().all()

    listJadwalTodayResponse = []

    for jadwalItem in findJadwal :
        if list(filter(lambda x: x.id_jadwal == jadwalItem.id, findAllAbsenSiswaToday)) :
            listJadwalTodayResponse.append({"jadwal" : jadwalItem,"isAbsen" : True})
        else :
            listJadwalTodayResponse.append({"jadwal" : jadwalItem,"isAbsen" : False})
    return {
        "msg" : "success",
        "data" : {
            "dataJadwal" : listJadwalTodayResponse,
            "countMapel" :  len(set(jadwal.id_mapel for jadwal in findJadwal))
        }    
    }