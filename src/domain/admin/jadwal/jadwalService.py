from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_
from sqlalchemy.orm import joinedload

# models
from ....models.jadwal_model import Jadwal,HariEnum,Mapel
from ....models.siswa_model import Kelas, Jurusan
# schemas
from ...schemas.jadwal_schema import JadwalBase,JadwalDetail
from .jadwalSchema import AddJadwalRequest,UpdateJadwalRequest,ResponseJadwalPag,FilterJadwalQuery

# common
from ...common.validation_jadwal import validateJadwal
import math
from copy import deepcopy
from ....utils.generateId_util import generate_id
from ....error.errorHandling import HttpException
from ....utils.updateTable_util import updateTable

async def addJadwal(id_sekolah : int,id_tahun : int,jadwal : AddJadwalRequest,session : AsyncSession) -> JadwalDetail:
    findKelas = (await session.execute(select(Kelas).where(and_(Kelas.id == jadwal.id_kelas,Kelas.jurusan.and_(Jurusan.id_sekolah == id_sekolah),Kelas.jurusan.and_(Jurusan.id_tahun == id_tahun))))).scalar_one_or_none()
    if not findKelas :
        raise HttpException(404,f"Kelas dengan id {jadwal.id_kelas} tidak ditemukan")
    
    findMapel = (await session.execute(select(Mapel).where(and_(Mapel.id == jadwal.id_mapel,Mapel.id_sekolah == id_sekolah,Mapel.id_tahun == id_tahun)))).scalar_one_or_none()
    if not findMapel :
        raise HttpException(404,f"Mapel dengan id {jadwal.id_mapel} tidak ditemukan")
    
    await validateJadwal(jadwal.jam_mulai,jadwal.jam_selesai,jadwal.id_kelas,jadwal.hari,id_sekolah,id_tahun,session)
    
    jadwalMapping = jadwal.model_dump()
    jadwalMapping.update({"id" : generate_id(),"id_sekolah" : id_sekolah,"id_tahun" : id_tahun})
    kelasDictCopy = deepcopy(findKelas.__dict__)
    mapelDictCopy = deepcopy(findMapel.__dict__)
    session.add(Jadwal(**jadwalMapping))
    await session.commit()
    
    return {
        "msg" : "success",
        "data" : {
            **jadwalMapping,
            "kelas" : kelasDictCopy,
            "mapel" : mapelDictCopy
        }
    }

async def getAllJadwal(page : int | None,id_sekolah : int,id_tahun : int,query : FilterJadwalQuery,session : AsyncSession) -> list[JadwalDetail] | ResponseJadwalPag:
    statementGetJadwal = select(Jadwal).options(joinedload(Jadwal.kelas),joinedload(Jadwal.mapel)).where(and_(Jadwal.id_sekolah == id_sekolah,Jadwal.id_tahun == id_tahun,Jadwal.id_kelas == query.id_kelas if query.id_kelas else True,Jadwal.id_mapel == query.id_mapel if query.id_mapel else True,Jadwal.hari == query.hari if query.hari else True)).order_by(Jadwal.jam_mulai)

    if page :
        findJadwal = (await session.execute(statementGetJadwal.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(Jadwal.id))).scalar_one()
        countPage = math.ceil(conntData / 10)
        return {
            "msg" : "success",
            "data" : {
                "data" : findJadwal,
                "count_data" : len(findJadwal),
                "count_page" : countPage
            }
        }
    else :
        findJadwal = (await session.execute(statementGetJadwal)).scalars().all()
        return {
            "msg" : "success",
            "data" : findJadwal
        }

async def getJadwalId(id : int,id_sekolah : int,session : AsyncSession) -> JadwalDetail:
    findJadwal = (await session.execute(select(Jadwal).options(joinedload(Jadwal.kelas),joinedload(Jadwal.mapel)).where(and_(Jadwal.id == id,Jadwal.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if not findJadwal :
        raise HttpException(404,f"Jadwal dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findJadwal
    }

async def updateJadwal(id : int,id_sekolah : int,id_tahun : int,jadwal : UpdateJadwalRequest,session : AsyncSession) -> JadwalDetail:
    findJadwal = (await session.execute(select(Jadwal).options(joinedload(Jadwal.kelas),joinedload(Jadwal.mapel)).where(and_(Jadwal.id == id,Jadwal.id_sekolah == id_sekolah, Jadwal.id_tahun == id_tahun)))).scalar_one_or_none()
    if not findJadwal :
        raise HttpException(404,f"Jadwal dengan id {id} tidak ditemukan")
    
    if jadwal.jam_mulai and jadwal.jam_selesai :
        if jadwal.jam_mulai >= jadwal.jam_selesai :
            raise HttpException(400,f"Jam mulai tidak boleh lebih besar atau sama dengan jam selesai")
    
    if jadwal.jam_mulai and not jadwal.jam_selesai :
        if jadwal.jam_mulai >= findJadwal.jam_selesai :
            raise HttpException(400,f"Jam mulai tidak boleh lebih besar atau sama dengan jam selesai")
        
    if jadwal.jam_selesai and not jadwal.jam_mulai :
        if jadwal.jam_selesai <= findJadwal.jam_mulai :
            raise HttpException(400,f"Jam selesai tidak boleh lebih kecil atau sama dengan jam mulai")
        
    await validateJadwal(jadwal.jam_mulai if jadwal.jam_mulai else findJadwal.jam_mulai,jadwal.jam_selesai if jadwal.jam_selesai else findJadwal.jam_selesai,findJadwal.id_kelas,jadwal.hari if jadwal.hari else findJadwal.hari,id_sekolah,id_tahun,session)

        

    if jadwal.model_dump(exclude_unset=True) :
        updateTable(jadwal,findJadwal)

    jadwalDictCopy = deepcopy(findJadwal.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : jadwalDictCopy
    }

async def deleteJadwal(id : int,id_sekolah : int,session : AsyncSession) -> JadwalBase:
    findJadwal = (await session.execute(select(Jadwal).where(and_(Jadwal.id == id,Jadwal.id_sekolah == id_sekolah)))).scalar_one_or_none()
    if not findJadwal :
        raise HttpException(404,f"Jadwal dengan id {id} tidak ditemukan")
    
    jadwalDictCopy = deepcopy(findJadwal.__dict__)
    await session.delete(findJadwal)
    await session.commit()
    
    return {
        "msg" : "success",
        "data" : jadwalDictCopy
    }
