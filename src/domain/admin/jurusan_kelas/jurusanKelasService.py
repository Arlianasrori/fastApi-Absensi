from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,and_
from sqlalchemy.orm import joinedload,subqueryload

# models
from .jurusanKelasSchema import AddJurusanRequest, AddKelasRequest,UpdateJurusanRequest,UpdateKelasRequest
from ....models.siswa_model import Jurusan, Kelas
from ....models.sekolah_model import TahunSekolah
from ...schemas.kelasJurusan_schema import JurusanBase,KelasBase,JurusanWithKelas,KelasWithJurusan

# common
from copy import deepcopy
from ....utils.generateId_util import generate_id
from ....error.errorHandling import HttpException
from ....utils.updateTable_util import updateTable

# jurusan
async def addJurusan(id_sekolah : int,jurusan : AddJurusanRequest, session : AsyncSession) -> JurusanBase :
    """
    Add a new Jurusan (major) to the database.

    Args:
        id_sekolah (int): The school ID.
        jurusan (AddJurusanBody): The Jurusan data to be added.
        session (AsyncSession): The database session.

    Returns:
        JurusanBase: The newly added Jurusan.

    Raises:
        HttpException: If the specified school year is not found or if a Jurusan with the same name already exists.
    """
    findTahunById = (await session.execute(select(TahunSekolah).where(TahunSekolah.id == jurusan.id_tahun))).scalar_one_or_none()

    if not findTahunById :
        raise HttpException(404,f"tahun sekolah dengan id {jurusan.id_tahun} tidak ditemukan")


    findJurusanByName = (await session.execute(select(Jurusan).where(and_(Jurusan.nama == jurusan.nama,Jurusan.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if findJurusanByName :
        raise HttpException(400,f"jurusan dengan nama {jurusan.nama} telah ditambahkan")
    
    jurusanMapping = jurusan.model_dump()
    jurusanMapping.update({"id" : generate_id(),"id_sekolah" : id_sekolah})

    session.add(Jurusan(**jurusanMapping))
    await session.commit()

    return {
        "msg" : "success",
        "data" : jurusanMapping
    }

async def getAllJurusan(id_sekolah : int,id_tahun : int,session : AsyncSession) -> list[JurusanBase] :
    """
    Retrieve all Jurusan entries for a specific school and year.

    Args:
        id_sekolah (int): The school ID.
        id_tahun (int): The year ID.
        session (AsyncSession): The database session.

    Returns:
        list[JurusanBase]: A list of all Jurusan entries.
    """
    findAllJurusan = (await session.execute(select(Jurusan).where(and_(Jurusan.id_sekolah == id_sekolah,Jurusan.id_tahun == id_tahun)))).scalars().all()
    return {
        "msg" : "success",
        "data" : findAllJurusan
    }

async def getJurusanById(id : int,id_sekolah : int, session : AsyncSession) -> JurusanWithKelas :
    """
    Retrieve a specific Jurusan entry by its ID.

    Args:
        id (int): The Jurusan ID.
        id_sekolah (int): The school ID.
        session (AsyncSession): The database session.

    Returns:
        MoreJurusanBase: The Jurusan entry with additional details.

    Raises:
        HttpException: If the Jurusan entry is not found.
    """
    findJurusanById = (await session.execute(select(Jurusan).options(subqueryload(Jurusan.kelas)).where(and_(Jurusan.id == id,Jurusan.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if not findJurusanById :
        raise HttpException(404,f"jurusan dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findJurusanById
    }

async def updateJurusan(id : int,jurusan : UpdateJurusanRequest,id_sekolah : int, session : AsyncSession) -> JurusanBase :
    """
    Update a Jurusan entry.

    Args:
        id (int): The Jurusan ID.
        jurusan (UpdateJurusanBody): The updated Jurusan data.
        id_sekolah (int): The school ID.
        session (AsyncSession): The database session.

    Returns:
        JurusanBase: The updated Jurusan entry.

    Raises:
        HttpException: If the Jurusan entry is not found or if a Jurusan with the same name already exists.
    """
    findJurusanById = (await session.execute(select(Jurusan).where(and_(Jurusan.id == id,Jurusan.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if not findJurusanById :
        raise HttpException(404,f"jurusan dengan id {id} tidak ditemukan")
    
    jurusanDictCopy = findJurusanById.__dict__
    if jurusan.nama :
        findJurusanByName = (await session.execute(select(Jurusan).where(and_(Jurusan.nama == jurusan.nama,Jurusan.id_sekolah == findJurusanById.id_sekolah,Jurusan.id != id)))).scalar_one_or_none()

        if findJurusanByName :
            raise HttpException(400,f"jurusan dengan nama {jurusan.nama} telah ditambahkan")

        findJurusanById.nama = jurusan.nama
        jurusanDictCopy = deepcopy(findJurusanById.__dict__)
        await session.commit()  

    return {
        "msg" : "success",
        "data" : jurusanDictCopy
    } 

async def deleteJurusan(id : int,id_sekolah : int, session : AsyncSession) -> JurusanBase :
    """
    Delete a Jurusan entry.

    Args:
        id (int): The Jurusan ID.
        id_sekolah (int): The school ID.
        session (AsyncSession): The database session.

    Returns:
        JurusanBase: The deleted Jurusan entry.

    Raises:
        HttpException: If the Jurusan entry is not found.
    """
    findJurusanById = (await session.execute(select(Jurusan).where(and_(Jurusan.id == id,Jurusan.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if not findJurusanById :
        raise HttpException(404,f"jurusan dengan id {id} tidak ditemukan")
    
    jurusanDictCopy = deepcopy(findJurusanById.__dict__)
    await session.delete(findJurusanById)
    await session.commit()
    
    return {
        "msg" : "success",
        "data" : jurusanDictCopy
    }

#  kelas
async def addKelas(id_sekolah : int,kelas : AddKelasRequest, session : AsyncSession) -> KelasBase :
    """
    Add a new Kelas (class) to the database.

    Args:
        id_sekolah (int): The school ID.
        kelas (AddKelasBody): The Kelas data to be added.
        session (AsyncSession): The database session.

    Returns:
        KelasBase: The newly added Kelas.

    Raises:
        HttpException: If the specified Jurusan is not found.
    """
    findJurusanById = (await session.execute(select(Jurusan).where(and_(Jurusan.id == kelas.id_jurusan,Jurusan.id_sekolah == id_sekolah)))).scalar_one_or_none()

    if not findJurusanById :
        raise HttpException(404,f"jurusan dengan id {kelas.id_jurusan} tidak ditemukan")
    
    kelasMapping = kelas.model_dump()
    kelasMapping.update({"id" : generate_id()})
    session.add(Kelas(**kelasMapping))
    await session.commit()

    return {
        "msg" : "success",
        "data" : kelasMapping
    }
    
async def getAllKelas(id_sekolah : int,id_tahun : int,session : AsyncSession) -> list[KelasBase] :
    """
    Retrieve all Kelas entries for a specific school and year.

    Args:
        id_sekolah (int): The school ID.
        id_tahun (int): The year ID.
        session (AsyncSession): The database session.

    Returns:
        list[KelasBase]: A list of all Kelas entries.
    """
    findAllKelas = (await session.execute(select(Kelas).where(and_(Kelas.jurusan.has(Jurusan.id_sekolah == id_sekolah),Kelas.jurusan.has(Jurusan.id_tahun == id_tahun))))).scalars().all()
    return {
        "msg" : "success",
        "data" : findAllKelas
    }

async def getKelasById(id : int,id_sekolah : int, session : AsyncSession) -> KelasWithJurusan :
    """
    Retrieve a specific Kelas entry by its ID.

    Args:
        id (int): The Kelas ID.
        id_sekolah (int): The school ID.
        session (AsyncSession): The database session.

    Returns:
        KelasWithJurusan: The Kelas entry with its associated Jurusan.

    Raises:
        HttpException: If the Kelas entry is not found.
    """
    findKelasById = (await session.execute(select(Kelas).options(joinedload(Kelas.jurusan)).where(and_(Kelas.id == id,Kelas.jurusan.has(Jurusan.id_sekolah == id_sekolah)) ))).scalar_one_or_none()

    if not findKelasById :
        raise HttpException(404,f"kelas dengan id {id} tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findKelasById
    }

async def updateKelas(id : int,id_sekolah : int,kelas : UpdateKelasRequest, session : AsyncSession) -> KelasBase :
    """
    Update a Kelas entry.

    Args:
        id (int): The Kelas ID.
        id_sekolah (int): The school ID.
        kelas (UpdateKelasBody): The updated Kelas data.
        session (AsyncSession): The database session.

    Returns:
        KelasBase: The updated Kelas entry.

    Raises:
        HttpException: If the Kelas entry or the specified Jurusan is not found.
    """
    findKelasById = (await session.execute(select(Kelas).where(and_(Kelas.id == id,Kelas.jurusan.has(Jurusan.id_sekolah == id_sekolah))))).scalar_one_or_none()

    if not findKelasById :
        raise HttpException(404,f"kelas dengan id {id} tidak ditemukan")
    
    if kelas.id_jurusan :
        findJurusanById = (await session.execute(select(Jurusan).where(and_(Jurusan.id == kelas.id_jurusan,Jurusan.id_sekolah == id_sekolah)))).scalar_one_or_none()

        if not findJurusanById :
            raise HttpException(404,f"jurusan dengan id {kelas.id_jurusan} tidak ditemukan")

    kelasDictCopy = findKelasById.__dict__

    if kelas.model_dump(exclude_unset=True) :
        updateTable(kelas,findKelasById)
        kelasDictCopy = deepcopy(findKelasById.__dict__)
        await session.commit()

    return {
        "msg" : "success",
        "data" : kelasDictCopy
    }

async def deleteKelas(id : int,id_sekolah : int, session : AsyncSession) -> KelasBase :
    """
    Delete a Kelas entry.

    Args:
        id (int): The Kelas ID.
        id_sekolah (int): The school ID.
        session (AsyncSession): The database session.

    Returns:
        KelasBase: The deleted Kelas entry.

    Raises:
        HttpException: If the Kelas entry is not found.
    """
    findKelasById = (await session.execute(select(Kelas).where(and_(Kelas.id == id,Kelas.jurusan.has(Jurusan.id_sekolah == id_sekolah))))).scalar_one_or_none()

    if not findKelasById :
        raise HttpException(404,f"kelas dengan id {id} tidak ditemukan")
    
    kelasDictCopy = deepcopy(findKelasById.__dict__)
    await session.delete(findKelasById)
    await session.commit()

    return {
        "msg" : "success",
        "data" : kelasDictCopy
    }

