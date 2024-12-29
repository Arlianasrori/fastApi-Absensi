from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload,subqueryload
# model
from ...models.sekolah_model import Sekolah,AlamatSekolah,Admin
from ..schemas.alamat_schema import AlamatBase,AlamatBody,UpdateAlamatBody
from ..schemas.sekolah_schema import SekolahBase,SekolahWithAlamat,SekolahDetail,AdminWithSekolah,AdminBase
from .developerSchema import AddSekolahRequest,AddAdminRequest,UpdateAdminRequest,UpdateSekolahRequest

# common
from ...utils.generateId_util import generate_id
from ...error.errorHandling import HttpException
import os
from copy import deepcopy
from ...utils.updateTable_util import updateTable
from ...auth.bcrypt import bcrypt


# sekolah
async def add_sekolah(sekolah : AddSekolahRequest,alamat : AlamatBody,session : AsyncSession) -> SekolahWithAlamat :
    """
    Add a new school to the database.

    Args:
        sekolah (AddSekolahBody): The school data to be added.
        alamat (AlamatBase): The address data for the school.
        session (AsyncSession): The database session.

    Returns:
        SekolahWithAlamat: The newly added school with its address.

    Raises:
        HttpException: If a school with the same NPSN already exists.
    """
    findSekolahByNpsn = (await session.execute(select(Sekolah).where(Sekolah.npsn == sekolah.npsn))).scalar_one_or_none()
    if findSekolahByNpsn :
        raise HttpException(400,f"sekolah dengan npsn {sekolah.npsn} stelah ditambahkan")

    # sekolah mapping
    sekolahMapping = sekolah.model_dump()
    sekolahMapping.update({"id" : generate_id()})
    # alamat mapping
    alamatMapping = alamat.model_dump()
    alamatMapping.update({"id_sekolah" : sekolahMapping["id"]})

    # add sekolah
    session.add(Sekolah(**sekolahMapping,alamat = AlamatSekolah(**alamatMapping)))
    await session.commit()

    return {
        "msg" : "success",
        "data" : {
            **sekolahMapping,
            "logo" : None,
            "alamat" : alamatMapping
        }
    }
    

LOGO_SEKOLAH_STORE = os.getenv("DEV_LOGO_SEKOLAH_STORE")
LOGO_SEKOLAH_BASE_URL = os.getenv("DEV_LOGO_SEKOLAH_BASE_URL")

async def add_update_foto_profile_sekolah(id_sekolah : int,logo : UploadFile,session : AsyncSession) -> SekolahBase :
    """
    Add or update the school's profile photo.

    Args:
        id_sekolah (int): The ID of the school.
        logo (UploadFile): The logo file to be uploaded.
        session (AsyncSession): The database session.

    Returns:
        SekolahBase: The updated school data.

    Raises:
        HttpException: If the school is not found or if the file is not an image.
    """
    findSekolah = (await session.execute(select(Sekolah).where(Sekolah.id == id_sekolah))).scalar_one_or_none()
    if not findSekolah :
        raise HttpException(404,f"sekolah tidak ditemukan")

    ext_file = logo.filename.split(".")

    if ext_file[-1] not in ["jpg","png","jpeg"] :
        raise HttpException(400,f"file harus berupa gambar")

    file_name = f"{generate_id()}-{logo.filename.split(' ')[0]}.{ext_file[-1]}"
    file_name_save = f"{LOGO_SEKOLAH_STORE}{file_name}"
        
    logoSekolahBefore = findSekolah.logo

    with open(file_name_save, "wb") as f:
        f.write(logo.file.read())
        findSekolah.logo = f"{LOGO_SEKOLAH_BASE_URL}/{file_name}"
    
    if logoSekolahBefore :
        print(logoSekolahBefore)
        file_nama_db_split = logoSekolahBefore.split("/")
        file_name_db = file_nama_db_split[-1]
        os.remove(f"{LOGO_SEKOLAH_STORE}/{file_name_db}")
    
    sekolahMapping = deepcopy(findSekolah.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : sekolahMapping
    }

async def getAllsekolah(session : AsyncSession) -> SekolahWithAlamat :
    """
    Retrieve all schools from the database.

    Args:
        session (AsyncSession): The database session.

    Returns:
        SekolahWithAlamat: A list of all schools with their addresses.
    """
    sekolah = (await session.execute(select(Sekolah).options(joinedload(Sekolah.alamat)))).scalars().all()

    return {
        "msg" : "success",
        "data" : sekolah
    }

async def getSekolahById(id_sekolah : int,session : AsyncSession) -> SekolahDetail :
    """
    Retrieve a school by its ID.

    Args:
        id_sekolah (int): The ID of the school.
        session (AsyncSession): The database session.

    Returns:
        MoreSekolahBase: The school data with additional related information.

    Raises:
        HttpException: If the school is not found.
    """
    sekolah = (await session.execute(select(Sekolah).options(subqueryload(Sekolah.admin),joinedload(Sekolah.alamat),subqueryload(Sekolah.siswa)).where(Sekolah.id == id_sekolah))).scalar_one_or_none()
    if not sekolah :
        raise HttpException(404,f"sekolah tidak ditemukan")

    return {
        "msg" : "success",
        "data" : sekolah
    }


async def updateSekolah(id_sekolah : int,sekolah : UpdateSekolahRequest,alamat : UpdateAlamatBody,session : AsyncSession) -> SekolahWithAlamat :
    """
    Update a school's information.

    Args:
        id_sekolah (int): The ID of the school.
        sekolah (UpdateAlamatBody): The updated school data.
        alamat (AlamatBase): The updated address data.
        session (AsyncSession): The database session.

    Returns:
        SekolahWithAlamat: The updated school data with its address.

    Raises:
        HttpException: If the school is not found.
    """
    findSekolah = (await session.execute(select(Sekolah).options(joinedload(Sekolah.alamat)).where(Sekolah.id == id_sekolah))).scalar_one_or_none()
    if not findSekolah :
        raise HttpException(404,f"sekolah tidak ditemukan")

    if sekolah :
        updateTable(sekolah,findSekolah)
    
    if alamat :
        updateTable(alamat,findSekolah.alamat)

    sekolahDictCopy = deepcopy(findSekolah.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : sekolahDictCopy
    }

async def deleteSekolah(id_sekolah : int,session : AsyncSession) -> SekolahBase :
    """
    Delete a school from the database.

    Args:
        id_sekolah (int): The ID of the school to be deleted.
        session (AsyncSession): The database session.

    Returns:
        SekolahBase: The deleted school data.

    Raises:
        HttpException: If the school is not found.
    """
    findSekolah = (await session.execute(select(Sekolah).where(Sekolah.id == id_sekolah))).scalar_one_or_none()
    if not findSekolah :
        raise HttpException(404,f"sekolah tidak ditemukan")

    sekolahDictCopy = deepcopy(findSekolah.__dict__)
    await session.delete(findSekolah)
    await session.commit()      

    return {
        "msg" : "success",
        "data" : sekolahDictCopy
    }
    
# admin sekolah

async def add_admin_sekolah(admin : AddAdminRequest,session : AsyncSession) -> AdminWithSekolah :
    """
    Add a new school admin to the database.

    Args:
        admin (AddAdminBody): The admin data to be added.
        session (AsyncSession): The database session.

    Returns:
        AdminWithSekolah: The newly added admin with their associated school.

    Raises:
        HttpException: If the school is not found or if the username is already in use.
    """
    findSekolah = (await session.execute(select(Sekolah).where(Sekolah.id == admin.id_sekolah))).scalar_one_or_none()

    if not findSekolah :
        raise HttpException(404,"sekolah tidak ditemukan")
    
    findAdminByUsername = (await session.execute(select(Admin).where(Admin.username == admin.username))).scalar_one_or_none()

    if findAdminByUsername :
        raise HttpException(400,f"admin dengan username {admin.username} telah digunakan")
    
    findAdminByNoTelepon = (await session.execute(select(Admin).where(Admin.no_telepon == admin.no_telepon))).scalar_one_or_none()

    if findAdminByNoTelepon :
        raise HttpException(400,f"admin dengan username {admin.no_telepon} telah digunakan")
    
    findAdminByEmail = (await session.execute(select(Admin).where(Admin.email
     == admin.email))).scalar_one_or_none()

    if findAdminByEmail :
        raise HttpException(400,f"admin dengan email {admin.email} telah digunakan")
    
    adminMApping = admin.model_dump()
    adminMApping.update({"id" : generate_id(),"password" : bcrypt.create_hash_password(admin.password)})

    sekolahDictCopy = deepcopy(findSekolah.__dict__)
    session.add(Admin(**adminMApping))
    await session.commit()

    return {
        "msg" : 'success',
        "data" : {
            **adminMApping,
            "sekolah" : sekolahDictCopy
        }
    }
async def get_all_admin_sekolah(session : AsyncSession) -> AdminWithSekolah :
    """
    Retrieve all school admins from the database.

    Args:
        session (AsyncSession): The database session.

    Returns:
        AdminWithSekolah: A list of all school admins with their associated schools.
    """
    admin = (await session.execute(select(Admin).options(joinedload(Admin.sekolah)))).scalars().all()

    return {
        "msg" : "success",
        "data" : admin
    }

async def get_admin_sekolah_by_id(id_admin : int,session : AsyncSession) -> AdminWithSekolah :
    """
    Retrieve a school admin by their ID.

    Args:
        id_admin (int): The ID of the admin.
        session (AsyncSession): The database session.

    Returns:
        AdminWithSekolah: The admin data with their associated school.

    Raises:
        HttpException: If the admin is not found.
    """
    admin = (await session.execute(select(Admin).options(joinedload(Admin.sekolah)).where(Admin.id == id_admin))).scalar_one_or_none()
    if not admin :
        raise HttpException(404,f"admin tidak ditemukan")

    return {
        "msg" : "success",
        "data" : admin
    }

async def update_admin_sekolah(id_admin : int,admin : UpdateAdminRequest,session : AsyncSession) -> AdminWithSekolah :
    """
    Update a school admin's information.

    Args:
        id_admin (int): The ID of the admin to be updated.
        admin (UpdateAdminBody): The updated admin data.
        session (AsyncSession): The database session.

    Returns:
        AdminWithSekolah: The updated admin data with their associated school.

    Raises:
        HttpException: If the admin is not found.
    """
    findAdmin = (await session.execute(select(Admin).options(joinedload(Admin.sekolah)).where(Admin.id == id_admin))).scalar_one_or_none()
    if not findAdmin :
        raise HttpException(404,f"admin tidak ditemukan")

    if admin.no_telepon :
        findAdminByNoTelepon = (await session.execute(select(Admin).where(Admin.no_telepon == admin.no_telepon))).scalar_one_or_none()
        if findAdminByNoTelepon :
            raise HttpException(400,f"admin dengan no telepon {admin.no_telepon} telah digunakan")

    if admin.username :
        findAdminByUsername = (await session.execute(select(Admin).where(Admin.username == admin.username))).scalar_one_or_none()
        if findAdminByUsername :
            raise HttpException(400,f"admin dengan username {admin.username} telah digunakan")

    if admin.email :
        findAdminByEmail = (await session.execute(select(Admin).where(Admin.email == admin.email))).scalar_one_or_none()
        if findAdminByEmail :
            raise HttpException(400,f"admin dengan email {admin.email} telah digunakan")

    if admin :
        updateTable(admin,findAdmin)

    adminDictCopy = deepcopy(findAdmin.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : adminDictCopy
    }
        

async def delete_admin_sekolah(id_admin : int,session : AsyncSession) -> AdminBase :
    """
    Delete a school admin from the database.

    Args:
        id_admin (int): The ID of the admin to be deleted.
        session (AsyncSession): The database session.

    Returns:
        AdminBase: The deleted admin data.

    Raises:
        HttpException: If the admin is not found.
    """
    findAdmin = (await session.execute(select(Admin).where(Admin.id == id_admin))).scalar_one_or_none()
    if not findAdmin :
        raise HttpException(404,f"admin tidak ditemukan")

    adminDictCopy = deepcopy(findAdmin.__dict__)
    await session.delete(findAdmin)
    await session.commit()
    
    return {
        "msg" : "success",
        "data" : adminDictCopy
    }
