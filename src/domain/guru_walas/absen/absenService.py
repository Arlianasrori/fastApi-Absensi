from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_, extract
from sqlalchemy.orm import joinedload, subqueryload

# models 
from ....models.petugas_BK_model import PetugasBK, DistribusiPetugasBK
from ....models.absen_model import Absen, AbsenDetail, StatusAbsenEnum, StatusTinjauanEnum
from ....models.siswa_model import Kelas, Siswa
from ....models.jadwal_model import Jadwal
# schemas
from .absenSchema import GetAbsenFilterQuery, GetAbsenBySiswaFilterQuery, GetAbsenInKelasResponse, GetAbsenByJadwalResponse
from ...schemas.absen_schema import AbsenBase, GetAbsenHarianResponse,AbsenWithJadwalMapel
from ...schemas.jadwal_schema import JadwalWithMapelGuruMapel
# common
from ....error.errorHandling import HttpException
from datetime import date
from collections import defaultdict
from ....utils.generateId_util import generate_id
from ....utils.updateTable_util import updateTable
from copy import deepcopy
from ...common.get_day_today import get_day
import math
from babel import Locale
from babel.dates import format_date


async def getHistoriAbsen(walas : dict,session : AsyncSession) -> list[AbsenBase]:
    findAbsen = (await session.execute(select(Absen).where(Absen.siswa.and_(Siswa.id_kelas == walas["id_kelas"])).limit(3))).scalars().all()
    
    return {
        "msg" : "success",
        "data" : findAbsen
    }
    
async def getAllAbsenInKelas(walas : dict,query : GetAbsenFilterQuery,session : AsyncSession) -> GetAbsenInKelasResponse :    
    findSiswa = (await session.execute(select(Siswa).where(Siswa.id_kelas == walas["id_kelas"]).order_by(Siswa.nama.asc()).limit(query.limit).offset((query.offset - 1) * query.limit))).scalars().all()

    idSiswaList = [siswa.id for siswa in findSiswa]

    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.siswa)).where(and_(Absen.siswa.and_(Siswa.id_kelas == walas["id_kelas"]),Absen.tanggal == query.tanggal,Absen.id_siswa.in_(idSiswaList))))).scalars().all()
    
    dayNow : dict = await get_day()
    findJadwal = (await session.execute(select(Jadwal).where(and_(Jadwal.id_kelas == walas["id_kelas"],Jadwal.hari == dayNow["day_name"].value)).order_by(Jadwal.jam_mulai.asc()))).scalars().all()

    print(findJadwal,dayNow["day_name"].value)
    
    grouped_absen = {}
    for siswaItem in findSiswa :
        absenSiswa = list(filter(lambda x: x.id_siswa == siswaItem.id, findAbsen))
        dictResponse = {}
        
        for index,jadwalItem in enumerate(findJadwal) :
            absenFilter = list(filter(lambda x: x.id_jadwal == jadwalItem.id, absenSiswa))
            if len(absenFilter) > 0 :
                dictResponse.update({index + 1 : absenFilter[0]})
            else :
                dictResponse.update({index + 1 : None})
        
        grouped_absen[siswaItem.nama] = dictResponse
    
    countDataSiswa = (await session.execute(select(func.count(Siswa.id)).where(Siswa.id_kelas == walas["id_kelas"]))).scalar_one()
    countPage = math.ceil(countDataSiswa / query.limit)

    return {
        "msg" : "success",
        "data" : {
            "absen" : grouped_absen,
            "count_data" : len(findSiswa),
            "count_page" : countPage
        }
    }

async def getAllAbsenBySiswa(query : GetAbsenBySiswaFilterQuery,session : AsyncSession) -> list[AbsenWithJadwalMapel] :
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.jadwal).joinedload(Jadwal.mapel)).where(and_(Absen.id_siswa == query.id_siswa,Absen.tanggal == query.tanggal)))).scalars().all()

    return {
        "msg" : "success",
        "data" : findAbsen
    }


# get detail absen harian
async def getDetailAbsenHarian(id_absen : int,session : AsyncSession) -> GetAbsenHarianResponse :
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.detail).joinedload(AbsenDetail.petugas_bk),joinedload(Absen.siswa),joinedload(Absen.jadwal).joinedload(Jadwal.koordinat)).where(Absen.id == id_absen))).scalar_one_or_none()

    if findAbsen is None :
        raise HttpException(404,"Absen tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findAbsen
    }

async def getAllTanggalContainsAbsen(walas : dict,month : int,session : AsyncSession) -> list[date] :
    findAbsenTanggal = (await session.execute(select(Absen.tanggal).where(Absen.siswa.and_(Siswa.id_kelas == walas["id_kelas"])).where(extract("month",Absen.tanggal) == month))).scalars().all()

    return {
        "msg" : "success",
        "data" : set([tanggal for tanggal in findAbsenTanggal])
    }

async def getJadwalByTanggal(walas : dict,tanggal : date,session : AsyncSession) -> list[JadwalWithMapelGuruMapel] :
    locale_id = Locale('id', 'ID')
    dayName = format_date(tanggal, format="EEEE", locale=locale_id).lower()
    findJadwal = (await session.execute(select(Jadwal).options(joinedload(Jadwal.mapel),joinedload(Jadwal.guru_mapel)).where(and_(Jadwal.hari == dayName,Jadwal.id_kelas == walas["id_kelas"])))).scalars().all()

    return {
        "msg" : "success",
        "data" : findJadwal
    }

async def getAbsenByJadwal(walas : dict,id_jadwal : int,query : GetAbsenFilterQuery,session : AsyncSession) -> GetAbsenByJadwalResponse :
    findJadwal = (await session.execute(select(Jadwal).where(Jadwal.id == id_jadwal))).scalar_one_or_none()

    if findJadwal is None :
        raise HttpException(404,"Jadwal tidak ditemukan")
    
    # Konversi waktu ke datetime dan hitung selisih dalam menit
    jam_mulai = findJadwal.jam_mulai.hour * 60 + findJadwal.jam_mulai.minute
    jam_selesai = findJadwal.jam_selesai.hour * 60 + findJadwal.jam_selesai.minute
    waktuBelajar = jam_selesai - jam_mulai  # hasil dalam menit
    # waktuBelajar = findJadwal.jam_selesai - findJadwal.jam_mulai

    findAbsen = (await session.execute(select(Absen).where(and_(Absen.id_jadwal == id_jadwal,Absen.tanggal == query.tanggal, Absen.siswa.and_(Siswa.id_kelas == walas["id_kelas"]))).order_by(Siswa.nama.asc()).limit(query.limit).offset((query.offset - 1) * query.limit))).scalars().all()

    countDataSiswa = (await session.execute(select(func.count(Absen.id).label("count_data"),func.count(Absen.id).filter(Absen.status == StatusAbsenEnum.hadir.value).label("siswa_hadir")).where(and_(Absen.siswa.and_(Siswa.id_kelas == walas["id_kelas"]),Absen.tanggal == query.tanggal)))).one()._asdict()


    
    countPage = math.ceil(countDataSiswa["count_data"] / query.limit)

    return {
        "msg" : "success",
        "data" : {
            "absen" : findAbsen,
            "siswa_hadir" : countDataSiswa["siswa_hadir"],
            "waktu_belajar" : waktuBelajar,
            "count_data" : len(findAbsen),
            "count_page" : countPage
        }
    }