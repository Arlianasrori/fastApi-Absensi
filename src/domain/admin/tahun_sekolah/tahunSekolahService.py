from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,and_
from sqlalchemy.orm import joinedload

# models
from .tahunSekolahSchema import AddTahunSekolahRequest,UpdateTahunSekolahRequest
from ...schemas.sekolah_schema import TahunSekolahBase
from ....models.sekolah_model import TahunSekolah

# common
from copy import deepcopy
from ....utils.generateId_util import generate_id
from ....error.errorHandling import HttpException

async def addTahunSekolah(id_sekolah : int,tahun : AddTahunSekolahRequest,session : AsyncSession) -> TahunSekolahBase :
    """
    Add a new school year to the database.

    Args:
        id_sekolah (int): The ID of the school.
        tahun (AddTahunSekolahBody): The school year data to be added.
        session (AsyncSession): The database session.

    Returns:
        TahunSekolahBase: The newly added school year data.

    Raises:
        HttpException: If the school year already exists.
    """
    findTahunById = (await session.execute(select(TahunSekolah).where(and_(TahunSekolah.id_sekolah == id_sekolah,TahunSekolah.tahun == tahun.tahun)))).scalar_one_or_none()

    if findTahunById :
        raise HttpException(400,f"tahun {tahun.tahun} sudah ada")
    
    tahunMapping = tahun.model_dump()
    tahunMapping.update({"id" : generate_id(),"id_sekolah" : id_sekolah})
    
    session.add(TahunSekolah(**tahunMapping))
    await session.commit()

    return {
        "msg" : "success",
        "data" : {
            **tahunMapping,
            "id_sekolah" : id_sekolah
        }
    }

async def getAllTahunSekolah(id_sekolah : int,session : AsyncSession) -> list[TahunSekolahBase] :
    """
    Retrieve all school years for a specific school.

    Args:
        id_sekolah (int): The ID of the school.
        session (AsyncSession): The database session.

    Returns:
        list[TahunSekolahBase]: A list of all school years for the specified school.
    """
    findTahunById = (await session.execute(select(TahunSekolah).where(TahunSekolah.id_sekolah == id_sekolah))).scalars().all()

    return {
        "msg" : "success",
        "data" : findTahunById
    }

async def updateTahunSekolah(id_sekolah : int,id_tahun : int,tahun : UpdateTahunSekolahRequest,session : AsyncSession) -> TahunSekolahBase :
    """
    Update an existing school year.

    Args:
        id_sekolah (int): The ID of the school.
        id_tahun (int): The ID of the school year to update.
        tahun (UpdateTahunSekolahBody): The updated school year data.
        session (AsyncSession): The database session.

    Returns:
        TahunSekolahBase: The updated school year data.

    Raises:
        HttpException: If the school year is not found or if the new year already exists.
    """
    findTahunById = (await session.execute(select(TahunSekolah).where(and_(TahunSekolah.id_sekolah == id_sekolah,TahunSekolah.id == id_tahun)))).scalar_one_or_none()

    if not findTahunById :
        raise HttpException(404,f"tahun dengan id {id_tahun} tidak ditemukan")
    
    tahunDictCopy = findTahunById.__dict__
    if tahun.tahun :
        findTahunByTahun = (await session.execute(select(TahunSekolah).where(and_(TahunSekolah.id_sekolah == id_sekolah,TahunSekolah.tahun == tahun.tahun)))).scalar_one_or_none()

        if findTahunByTahun :
            raise HttpException(400,f"tahun {tahun.tahun} telah ditambahkan")

        findTahunById.tahun = tahun.tahun
        tahunDictCopy = deepcopy(findTahunById.__dict__)
        await session.commit()

    return {
        "msg" : "success",
        "data" : tahunDictCopy
    }
    
async def deleteTahunSekolah(id_sekolah : int,id_tahun : int,session : AsyncSession) -> TahunSekolahBase :
    """
    Delete a school year.

    Args:
        id_sekolah (int): The ID of the school.
        id_tahun (int): The ID of the school year to delete.
        session (AsyncSession): The database session.

    Returns:
        TahunSekolahBase: The deleted school year data.

    Raises:
        HttpException: If the school year is not found.
    """
    findTahunById = (await session.execute(select(TahunSekolah).where(and_(TahunSekolah.id_sekolah == id_sekolah,TahunSekolah.id == id_tahun)))).scalar_one_or_none()

    if not findTahunById :
        raise HttpException(404,f"tahun dengan id {id_tahun} tidak ditemukan")
    
    tahunDictCopy = deepcopy(findTahunById.__dict__)
    await session.delete(findTahunById)
    await session.commit()
    
    return {
        "msg" : "success",
        "data" : tahunDictCopy
    }