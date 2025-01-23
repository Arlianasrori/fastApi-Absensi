from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,and_

# models
from ....models.jadwal_model import Mapel

# schemas
from .mapelSchema import AddMapelRequest,UpdateMapelRequest
from ...schemas.mapel_schema import MapelBase

# common
from copy import deepcopy
from ....utils.generateId_util import generate_id
from ....error.errorHandling import HttpException

async def addMapel(id_sekolah : int,mapel : AddMapelRequest,session : AsyncSession) -> MapelBase :
    findMapelByName = (await session.execute(select(Mapel).where(and_(Mapel.id_sekolah == id_sekolah,Mapel.nama == mapel.nama)))).scalar_one_or_none()

    if findMapelByName :
        raise HttpException(400,f"mapel {mapel.nama} sudah ada")
    
    mapelMapping = mapel.model_dump()
    mapelMapping.update({"id" : generate_id(),"id_sekolah" : id_sekolah})
    
    session.add(Mapel(**mapelMapping))
    await session.commit()

    return {
        "msg" : "success",
        "data" : {
            **mapelMapping,
            "id_sekolah" : id_sekolah
        }
    }

async def getAllMapel(id_sekolah : int,id_tahun : int,session : AsyncSession) -> list[MapelBase] :
    findMapel = (await session.execute(select(Mapel).where(and_(Mapel.id_sekolah == id_sekolah,Mapel.id_tahun == id_tahun)))).scalars().all()

    return {
        "msg" : "success",
        "data" : findMapel
    }

async def updateMapel(id_sekolah : int,id_mapel : int,mapel : UpdateMapelRequest,session : AsyncSession) -> MapelBase :
    findMapelById = (await session.execute(select(Mapel).where(and_(Mapel.id_sekolah == id_sekolah,Mapel.id == id_mapel)))).scalar_one_or_none()

    if not findMapelById :
        raise HttpException(404,f"mapel dengan mapel {id_mapel} tidak ditemukan")
    
    mapelDictCopy = findMapelById.__dict__
    if mapel.nama :
        findMapelByNama = (await session.execute(select(Mapel).where(and_(Mapel.id_sekolah == id_sekolah,Mapel.nama == mapel.nama)))).scalar_one_or_none()

        if findMapelByNama :
            raise HttpException(400,f"mapel {mapel.nama} telah ditambahkan")

        findMapelById.nama = mapel.nama
        mapelDictCopy = deepcopy(findMapelById.__dict__)
        await session.commit()

    return {
        "msg" : "success",
        "data" : mapelDictCopy
    }
    
async def deleteMapel(id_sekolah : int,id_mapel : int,session : AsyncSession) -> MapelBase :
    findMapelById = (await session.execute(select(Mapel).where(and_(Mapel.id_sekolah == id_sekolah,Mapel.id == id_mapel)))).scalar_one_or_none()

    if not findMapelById :
        raise HttpException(404,f"mapel dengan id {id_mapel} tidak ditemukan")
    
    mapelDictCopy = deepcopy(findMapelById.__dict__)
    await session.delete(findMapelById)
    await session.commit()
    
    return {
        "msg" : "success",
        "data" : mapelDictCopy
    }