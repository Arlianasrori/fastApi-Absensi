from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_,or_, extract
from sqlalchemy.orm import joinedload
from fastapi import UploadFile

# models 
from ....models.absen_model import Absen, AbsenDetail, StatusAbsenEnum, StatusTinjauanEnum
from ....models.jadwal_model import Jadwal
# schemas
from .absenSchema import RekapAbsenMingguanResponse, StatusRekapAbsenMIngguanEnum, CekAbsenSiswaTodayResponse, AbsenSiswaRequest, GetAllLaporanAbsenSiswaResponse, GetDetailAbsenSiswaResponse
from ...schemas.absen_schema import AbsenWithDetail
from ..koordinat_absen.koordinatAbsenSchema import CekRadiusKoordinatRequest
# service
from ..koordinat_absen.koordinatAbsenService import cekRadiusKoordinat
# common
from ....error.errorHandling import HttpException
from ...common.get_day_today import get_day
from datetime import datetime, timedelta, date
import holidays
import os
from ....utils.generateId_util import generate_id
import aiofiles
from babel import Locale
from babel.dates import format_date

async def getRekapAbsenMingguan(siswa : dict,session : AsyncSession) -> RekapAbsenMingguanResponse :
    day_code_today : dict = await get_day()

    endDate = datetime.now().date()
    startDate = endDate - timedelta(days=day_code_today["day_code"])

    print(startDate,endDate,day_code_today["day_code"])

    allAbsenMIngguan = (await session.execute(select(Absen).where(and_(Absen.id_siswa == siswa["id"],Absen.tanggal >= startDate,Absen.tanggal <= endDate)))).scalars().all()

    statistikAbsenMingguan = (await session.execute(select(func.count(Absen.id).filter(and_(Absen.status == StatusAbsenEnum.hadir)).label("total_hadir"),func.count(Absen.id).filter(or_(Absen.status == StatusAbsenEnum.izin,Absen.status == StatusAbsenEnum.sakit,Absen.status == StatusAbsenEnum.dispen)).label("total_izin_sakit_dispensasi")).where(and_(Absen.id_siswa == siswa["id"],Absen.tanggal >= startDate,Absen.tanggal <= endDate)))).one()._asdict()

    id_holidays = holidays.ID()
    locale_id = Locale('id', 'ID')
    progresAbsenMingguanResponse = []
    for i in range(day_code_today["day_code"],-1,-1) :
        print(i)
        dateFilter = endDate - timedelta(days=i)

        if dateFilter in id_holidays:
            progresAbsenMingguanResponse.append({"status" : StatusRekapAbsenMIngguanEnum.LIBUR,"hari" : format_date(dateFilter, format="EEEE", locale=locale_id).lower()})
        elif dateFilter.weekday() >= 6:  # Cek weekend
            progresAbsenMingguanResponse.append({"status" : StatusRekapAbsenMIngguanEnum.LIBUR,"hari" : format_date(dateFilter, format="EEEE", locale=locale_id).lower()})
        else :
            absenFilter = list(filter(lambda x: x.tanggal == dateFilter, allAbsenMIngguan))
            if len(absenFilter) == 0 :
                
                progresAbsenMingguanResponse.append({"status" : StatusRekapAbsenMIngguanEnum.ALPA,"hari" : format_date(dateFilter, format="EEEE", locale=locale_id).lower()})
            elif any(absen.status == StatusAbsenEnum.hadir for absen in absenFilter) :
                progresAbsenMingguanResponse.append({"status" : StatusRekapAbsenMIngguanEnum.HADIR,"hari" : format_date(dateFilter, format="EEEE", locale=locale_id).lower()})
            elif any(absen.status == StatusAbsenEnum.izin for absen in absenFilter) :
                progresAbsenMingguanResponse.append({"status" : StatusRekapAbsenMIngguanEnum.IZIN,"hari" : format_date(dateFilter, format="EEEE", locale=locale_id).lower()})
            elif any(absen.status == "sakit" for absen in absenFilter) :
                progresAbsenMingguanResponse.append({"status" : StatusRekapAbsenMIngguanEnum.SAKIT,"hari" : format_date(dateFilter, format="EEEE", locale=locale_id).lower()})
            elif any(absen.status == "dispen" for absen in absenFilter) :
                progresAbsenMingguanResponse.append({"status" : StatusRekapAbsenMIngguanEnum.DISPENSASI,"hari" : format_date(dateFilter, format="EEEE", locale=locale_id).lower()})
 
    return {
        "msg" : "success",
        "data" : {
            "progress" : progresAbsenMingguanResponse,
            "total_hadir" : statistikAbsenMingguan["total_hadir"],
            "total_izin_sakit_dispensasi" : statistikAbsenMingguan["total_izin_sakit_dispensasi"]
        }
    }

async def cekAbsenSiswaToday(siswa : dict,latitude : float,longitude : float, session : AsyncSession) -> CekAbsenSiswaTodayResponse :
    dayNow = await get_day()

    findJadwal = (await session.execute(select(Jadwal).where(and_(Jadwal.id_kelas == siswa["id_kelas"],Jadwal.id_tahun == siswa["id_tahun"],Jadwal.hari == dayNow["day_name"])))).scalars().all()

    if len(findJadwal) == 0 :
        return {
            "msg" : "Tidak ada jadwal hari ini",
            "data" : {
                "avaliableAbsen" : False
            }
        }
    
    dateNow = datetime.now().date()

    id_holidays = holidays.ID()
    if dateNow in id_holidays:
        return {
            "msg" : "Hari ini adalah hari libur nasional",
            "data" : {
                "avaliableAbsen" : False
            }
        }
    elif dateNow.weekday() >= 6:
        return {
            "msg" : "Hari ini adalah hari libur",
            "data" : {
                "avaliableAbsen" : False
            }
        }
    else :
        timeNow = datetime.now().time()
        jadwalNow = list(filter(lambda jadwalItem: timeNow >= jadwalItem.jam_mulai and timeNow <= jadwalItem.jam_selesai, findJadwal))  
        
        
        if len(jadwalNow) == 0 :
            return {
                    "msg" : "Tidak ada jadwal tersedia sekarang",
                    "data" : {
                        "avaliableAbsen" : False
                    }
                }
        else :
            findAbsenNow = (await session.execute(select(Absen).where(and_(Absen.id_siswa == siswa["id"],Absen.tanggal == datetime.now().date(),Absen.jam >= jadwalNow[0].jam_mulai,Absen.jam <= jadwalNow[0].jam_selesai)))).scalar_one_or_none()
        
            if findAbsenNow :
                return {
                        "msg" : "Kamu sudah melakukan absen",
                        "data" : {
                            "avaliableAbsen" : False
                        }
                    }
            cekRadius = await cekRadiusKoordinat(siswa,CekRadiusKoordinatRequest(latitude=latitude,longitude=longitude),session)

            if not cekRadius["data"]["insideRadius"] :
                return {
                    "msg" : "Anda berada di luar radius, silahkan melakukan absen izin atau sakit",
                    "data" : {
                        "avaliableAbsen" : True
                    },
                    "jadwal" : jadwalNow[0]
                }
            return {
                    "msg" : "Tidak ada hari libur hari ini",
                    "data" : {
                        "avaliableAbsen" : True
                    },
                    "jadwal" : jadwalNow[0]
                }

ABSEN_DOKUMEN_STORE = os.getenv("DEV_LAPORAN_SISWA_STORE")
ABSEN_DOKUMEN_BASE_URL = os.getenv("DEV_LAPORAN_SISWA_BASE_URL")
async def absenSiswa(siswa : dict,body : AbsenSiswaRequest,session : AsyncSession) -> AbsenWithDetail :
    cekRadius = await cekRadiusKoordinat(siswa,CekRadiusKoordinatRequest(latitude=body.latitude,longitude=body.longitude),session)

    if not cekRadius["data"]["insideRadius"] and body.status not in [StatusAbsenEnum.izin,StatusAbsenEnum.sakit,StatusAbsenEnum.dispen,StatusAbsenEnum.izin_telat]:
        raise HttpException(400,"anda berada diluar radius absen")
    
    cekAbsenToday = await cekAbsenSiswaToday(siswa,body.latitude,body.longitude,session)

    if not cekAbsenToday["data"]["avaliableAbsen"] :
        raise HttpException(400,cekAbsenToday["msg"])
    
    if body.status != StatusAbsenEnum.hadir and not body.catatan:
        raise HttpException(400,"catatan wajib diisi")
    
    findAbsenNow = (await session.execute(select(Absen).where(and_(Absen.id_siswa == siswa["id"],Absen.tanggal == datetime.now().date(),Absen.jam >= cekAbsenToday["jadwal"].jam_mulai,Absen.jam <= cekAbsenToday["jadwal"].jam_selesai)))).scalar_one_or_none()

    if findAbsenNow :
        raise HttpException(400,"anda sudah absen hari ini")
    
    print(body.dokumenFile.filename)
    ext_file = body.dokumenFile.filename.split(".")
    print(ext_file[-1])
    if body.status == StatusAbsenEnum.hadir and ext_file[-1].lower() not in ["jpg","png","jpeg"] :
        raise HttpException(400,f"format file tidak di dukung")
    elif body.status != StatusAbsenEnum.hadir and ext_file[-1].lower()  not in ["jpg","png","jpeg","pdf","docx","doc"] :
        raise HttpException(400,f"format file tidak di dukung")

    file_name = f"{generate_id()}-{body.dokumenFile.filename.split(' ')[0].split(".")[0]}.{ext_file[-1]}"
    
    file_name_save = f"{ABSEN_DOKUMEN_STORE}{file_name}"

    async with aiofiles.open(file_name_save, "wb") as f:
        await f.write(body.dokumenFile.file.read())
        absenMapping = {"id" : generate_id(),"id_jadwal" : cekAbsenToday["jadwal"].id,"id_siswa" : siswa["id"],"tanggal" : datetime.now().date(),"jam" : datetime.now().time(),"file" : f"{ABSEN_DOKUMEN_BASE_URL}/{file_name}","status" : body.status}
        session.add(Absen(**absenMapping))


        absenDetailMapping = None
        if body.status != StatusAbsenEnum.hadir:
            if not body.catatan:
                raise HttpException(400,"catatan wajib diisi")
            else :
                absenDetailMapping = {"id" : generate_id(),"id_absen" : absenMapping["id"],"catatan" : body.catatan,"status_tinjauan" : StatusTinjauanEnum.belum_ditinjau.value,"id_peninjau" : None, "tanggal_tinjauan" : None}
                session.add(AbsenDetail(**absenDetailMapping))

        await session.commit()
        return {
            "msg" : "success",
            "data" : {
                **absenMapping,
                "detail" : absenDetailMapping
            }
        }
    
async def getAllLaporanAbsenSiswa(siswa : dict,month : int,year : int,session : AsyncSession) -> dict[date,list[GetAllLaporanAbsenSiswaResponse] | None] :
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.jadwal).joinedload(Jadwal.mapel)).where(and_(Absen.id_siswa == siswa["id"],extract("month",Absen.tanggal) == month,extract("year",Absen.tanggal) == year)).order_by(Absen.tanggal.desc()))).scalars().all()

    absenResponse = defaultdict(list)

    for absen in findAbsen :
        absenResponse[absen.tanggal].append({
            "absen" : absen,
            "mapel" : absen.jadwal.mapel
        })

    print(absenResponse)
    return {
        "msg" : "success",
        "data" : absenResponse
    }

async def getDetailAbsenSiswa(siswa : dict,id_absen : int,session : AsyncSession) -> GetDetailAbsenSiswaResponse :
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.detail),joinedload(Absen.siswa),joinedload(Absen.jadwal).options(joinedload(Jadwal.koordinat),joinedload(Jadwal.mapel),joinedload(Jadwal.guru_mapel))).where(and_(Absen.id_siswa == siswa["id"],Absen.id == id_absen)))).scalar_one_or_none()

    if findAbsen is None :
        raise HttpException(404,"Absen tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findAbsen
    }