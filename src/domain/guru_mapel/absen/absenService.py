from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_, extract, distinct
from sqlalchemy.orm import joinedload, subqueryload

# models 
from ....models.petugas_BK_model import PetugasBK, DistribusiPetugasBK
from ....models.absen_model import Absen, AbsenDetail, StatusAbsenEnum, StatusTinjauanEnum
from ....models.siswa_model import Kelas, Siswa
from ....models.jadwal_model import Jadwal
# schemas
from .absenSchema import GetAbsenFilterQuery, GetAbsenAbsenInKelasResponse, GetHistoriAbsenKelasResponse, GetStatistikKelasAbsenResponse, GetHistoriKelasAjarResponse
from ...schemas.kelasJurusan_schema import KelasBase
# from .absenSchema import GetAbsenFilterQuery, GetAbsenBySiswaFilterQuery, GetAbsenInKelasResponse, GetAbsenByJadwalResponse, GetStatistikAbsenResponse
from ...schemas.absen_schema import AbsenBase, GetAbsenHarianResponse,AbsenWithJadwalMapel
from ...schemas.jadwal_schema import JadwalWithMapelGuruMapel
# common
from ....error.errorHandling import HttpException
import datetime
from collections import defaultdict
from ....utils.generateId_util import generate_id
from ....utils.updateTable_util import updateTable
from copy import deepcopy
from ...common.get_day_today import get_day
import math
from babel import Locale
from babel.dates import format_date

# get statistik kelas diajar saat ini
async def getStatistikKelasAbsen(guruMapel : dict,session : AsyncSession) -> GetStatistikKelasAbsenResponse :
    dayNow : str = (await get_day())["day_name"]
    timeNow : datetime.time = datetime.datetime.now().time()

    findJadwalNow = (await session.execute(select(Jadwal).options(joinedload(Jadwal.kelas)).where(and_(Jadwal.id_guru_mapel == guruMapel["id"],Jadwal.hari == dayNow,and_(Jadwal.jam_mulai <= timeNow,Jadwal.jam_selesai >= timeNow))))).scalars().all()

    if len(findJadwalNow) == 0 :
        raise HttpException(404,f"Tidak jadwal hari ini")

    findKelas = (await session.execute(select(Kelas).options(subqueryload(Kelas.siswa),joinedload(Kelas.guru_walas)).where(Kelas.id == findJadwalNow[0].id_kelas))).scalar_one_or_none()

    return {
        "msg" : "success",
        "data" : {
            "jumlah_siswa" : len(findKelas.siswa),
            "kelas" : findKelas
        }
    }

async def getHistoriKelasAjar(guruMapel : dict,session : AsyncSession) -> list[GetHistoriKelasAjarResponse] :
    countDataKelas = 0
    responseData = []

    locale_id = Locale('id', 'ID')
    dateNow = datetime.datetime.now().date()
    

    for i in range (0,7) :
        if countDataKelas > 3 :
            break
        dateQuery = dateNow - datetime.timedelta(days=i)
        dayName = format_date(dateQuery, format="EEEE", locale=locale_id).lower()
        findJadwal = (await session.execute(select(Jadwal).options(joinedload(Jadwal.kelas)).where(Jadwal.id_guru_mapel == guruMapel["id"],Jadwal.hari == dayName).order_by(Jadwal.hari.asc(),Jadwal.jam_mulai.asc()))).scalars().all()

        if len(findJadwal) > 0 :
            for jadwalItem in findJadwal :
                countSiswaHadir = (await session.execute(select(func.count(Absen.id)).where(Absen.id_jadwal == jadwalItem.id,Absen.status == StatusAbsenEnum.hadir,Absen.tanggal == dateQuery))).scalar_one()
                responseData.append({
                    "kelas" : jadwalItem.kelas,
                    "tanggal" : dateQuery,
                    "jumlah_hadir" : countSiswaHadir
                })
                countDataKelas += 1

    return {
        "msg" : "success",
        "data" : responseData
    }

async def getAllAbsenByHistori(guruMapel : dict,query : GetAbsenFilterQuery,session : AsyncSession) -> GetHistoriAbsenKelasResponse :
    locale_id = Locale('id', 'ID')
    dayName = format_date(query.tanggal, format="EEEE", locale=locale_id).lower()

    findJadwal = (await session.execute(select(Jadwal).where(and_(Jadwal.id_guru_mapel == guruMapel["id"],Jadwal.id_kelas == query.id_kelas,Jadwal.hari == dayName)))).scalars().all()

    if len(findJadwal) == 0 :
        raise HttpException(404,f"Tidak ada jadwal pada tanggal yang diberikan")
    
    waktu_belajar = 0

    jam_mulai = findJadwal[0].jam_mulai.hour * 60 + findJadwal[0].jam_mulai.minute
    jam_selesai = findJadwal[0].jam_selesai.hour * 60 + findJadwal[0].jam_selesai.minute
    waktu_belajar += jam_selesai - jam_mulai

    
    findSiswa = (await session.execute(select(Siswa).where(Siswa.id_kelas == query.id_kelas).order_by(Siswa.nama.asc()).limit(query.limit).offset((query.offset - 1) * query.limit))).scalars().all()
    
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.siswa)).where(and_(Absen.siswa.and_(Siswa.id_kelas == query.id_kelas),Absen.tanggal == query.tanggal,Absen.siswa.and_(Siswa.id_kelas == query.id_kelas),Absen.id_jadwal == findJadwal[0].id)))).scalars().all()

    grouped_absen = []
    for siswaItem in findSiswa :
        absenSiswa = list(filter(lambda x: x.id_siswa == siswaItem.id, findAbsen))
        dictResponse = {"siswa" : siswaItem,"absen" : absenSiswa[0] if len(absenSiswa) > 0 else None}
        grouped_absen.append(dictResponse)

    countDataSiswa = (await session.execute(select(func.count(Siswa.id)).where(Siswa.id_kelas == query.id_kelas))).scalar_one()
    countPage = math.ceil(countDataSiswa / query.limit)

    return {
        "msg" : "success",
        "data" : {
            "waktu_belajar" : waktu_belajar,
            "absen" : grouped_absen,
            "jumlah_hadir" : len(list(filter(lambda x: x.status == StatusAbsenEnum.hadir, findAbsen))),
            "count_data" : len(findSiswa),
            "count_page" : countPage
        }
    }

async def getKelasAjar(guruMapel : dict,session : AsyncSession) -> list[KelasBase]:
    findIdKelas = (await session.execute(select(Kelas.id).join(Jadwal).where(Jadwal.id_guru_mapel == guruMapel["id"]))).scalars().all()

    findKelas = (await session.execute(select(Kelas).where(Kelas.id.in_(findIdKelas)))).scalars().all()

    return {
        "msg" : "success",
        "data" : findKelas
    }

async def getAllAbsenInKelas(guruMapel : dict,query : GetAbsenFilterQuery,session : AsyncSession) -> GetAbsenAbsenInKelasResponse :
    locale_id = Locale('id', 'ID')
    dayName = format_date(query.tanggal, format="EEEE", locale=locale_id).lower()

    findJadwal = (await session.execute(select(Jadwal).where(and_(Jadwal.id_guru_mapel == guruMapel["id"],Jadwal.id_kelas == query.id_kelas,Jadwal.hari == dayName)))).scalars().all()

    if len(findJadwal) == 0 :
        raise HttpException(404,f"Tidak ada jadwal pada tanggal yang diberikan")

    findKelas = (await session.execute(select(Kelas).options(subqueryload(Kelas.siswa)).where(Kelas.id == query.id_kelas))).scalar_one_or_none()

    if findKelas is None :
        raise HttpException(404,f"Kelas tidak ditemukan")

    findSiswa = (await session.execute(select(Siswa).where(Siswa.id_kelas == query.id_kelas).order_by(Siswa.nama.asc()).limit(query.limit).offset((query.offset - 1) * query.limit))).scalars().all()
    
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.siswa)).where(and_(Absen.siswa.and_(Siswa.id_kelas == query.id_kelas),Absen.tanggal == query.tanggal,Absen.siswa.and_(Siswa.id_kelas == query.id_kelas),Absen.id_jadwal == findJadwal[0].id)))).scalars().all()

    grouped_absen = []
    for siswaItem in findSiswa :
        absenSiswa = list(filter(lambda x: x.id_siswa == siswaItem.id, findAbsen))
        dictResponse = {"siswa" : siswaItem,"absen" : absenSiswa[0] if len(absenSiswa) > 0 else None}
        grouped_absen.append(dictResponse)

    countDataSiswa = (await session.execute(select(func.count(Siswa.id)).where(Siswa.id_kelas == query.id_kelas))).scalar_one()
    countPage = math.ceil(countDataSiswa / query.limit)

    return {
        "msg" : "success",
        "data" : {
            "absen" : grouped_absen,
            "jumlah_siswa" : len(findKelas.siswa),
            "count_data" : len(findSiswa),
            "count_page" : countPage
        }
    }


async def getDetailAbsenHarian(id_absen : int,session : AsyncSession) -> GetAbsenHarianResponse :
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.detail).joinedload(AbsenDetail.petugas_bk),joinedload(Absen.siswa),joinedload(Absen.jadwal).joinedload(Jadwal.koordinat)).where(Absen.id == id_absen))).scalar_one_or_none()

    if findAbsen is None :
        raise HttpException(404,"Absen tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findAbsen
    }