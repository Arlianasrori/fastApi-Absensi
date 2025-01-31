from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,and_

# models
from ....models.absen_model import KoordinatAbsenKelas
from ....models.siswa_model import Kelas, Jurusan
# schemas
from .koordinatAbsenKelasSchema import FilterKoordinatAbsenKelasQuery,ResponseKoordinatAbsenKelasPag,AddKoordinatAbsenKelasRequest,UpdateKoordinatAbsenKelasRequest
from ...schemas.koordinatAbsen_schema import KoordinatAbsenKelasBase
# common
import math
from ....error.errorHandling import HttpException
from ....utils.generateId_util import generate_id
from ....utils.updateTable_util import updateTable
from copy import deepcopy

async def getAllKoordinatAbsen(page : int | None,id_sekolah : int,id_tahun : int,query : FilterKoordinatAbsenKelasQuery,session : AsyncSession) -> list[KoordinatAbsenKelasBase] | ResponseKoordinatAbsenKelasPag:
    statementGetKoordinatAbsen = select(KoordinatAbsenKelas).join(KoordinatAbsenKelas.kelas).join(Kelas.jurusan).where(and_(Jurusan.id_sekolah == id_sekolah,Jurusan.id_tahun == id_tahun,KoordinatAbsenKelas.id_kelas == query.id_kelas if query.id_kelas else True,KoordinatAbsenKelas.kelas.and_(Kelas.nama == query.nama_kelas) if query.nama_kelas else True))

    if page :
        findKoordinat = (await session.execute(statementGetKoordinatAbsen.limit(10).offset(10 * (page - 1)))).scalars().all()
        conntData = (await session.execute(func.count(KoordinatAbsenKelas.id))).scalar_one()
        countPage = math.ceil(conntData / 10)
        return {
            "msg" : "success",
            "data" : {
                "data" : findKoordinat,
                "count_data" : len(findKoordinat),
                "count_page" : countPage
            }
        }
    else :
        findKoordinat = (await session.execute(statementGetKoordinatAbsen)).scalars().all()
        return {
            "msg" : "success",
            "data" : findKoordinat
        }

async def getKoordinatById(id : int,id_sekolah : int,session : AsyncSession) -> KoordinatAbsenKelasBase:
    findKoordinat = (await session.execute(select(KoordinatAbsenKelas).join(KoordinatAbsenKelas.kelas).join(Kelas.jurusan).where(and_(Jurusan.id_sekolah == id_sekolah,KoordinatAbsenKelas.id == id)))).scalar_one_or_none()

    if not findKoordinat :
        raise HttpException(404,f"Koordinat absen dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findKoordinat
    }

async def addKoordinatAbsenKelas(id_sekolah : int,body : AddKoordinatAbsenKelasRequest,session : AsyncSession) -> KoordinatAbsenKelasBase :
    findKelas = (await session.execute(select(Kelas).where(and_(Kelas.id == body.id_kelas,Kelas.jurusan.and_(Jurusan.id_sekolah == id_sekolah,Jurusan.id_tahun == body.id_tahun))))).scalar_one_or_none()

    if not findKelas :
        raise HttpException(404,f"Kelas dengan id {body.id_kelas} tidak ditemukan")
    
    koordinatMapping = body.model_dump()
    koordinatMapping.update({"id" : generate_id(),"id_sekolah" : id_sekolah})
    session.add(KoordinatAbsenKelas(**koordinatMapping))
    await session.commit()
    return {
        "msg" : "success",
        "data" : koordinatMapping
    }

async def updateKoordinatAbsenKelas(id : int,id_sekolah : int,body : UpdateKoordinatAbsenKelasRequest,session : AsyncSession) -> KoordinatAbsenKelasBase :
    findKoordinat = (await session.execute(select(KoordinatAbsenKelas).where(and_(KoordinatAbsenKelas.id == id,KoordinatAbsenKelas.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if not findKoordinat :
        raise HttpException(404,f"Koordinat absen dengan id {id} tidak ditemukan")
    
    if body.model_dump(exclude_unset=True):
        updateTable(body,findKoordinat)

    koordinatDictCopy = deepcopy(findKoordinat.__dict__)
    await session.commit()
    return {
        "msg" : "success",
        "data" : koordinatDictCopy
    }