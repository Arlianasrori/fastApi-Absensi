from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_
from sqlalchemy.orm import joinedload, subqueryload

# models 
from ....models.petugas_BK_model import PetugasBK, DistribusiPetugasBK
from ....models.absen_model import Absen, AbsenDetail, StatusAbsenEnum, StatusTinjauanEnum
from ....models.siswa_model import Kelas, Siswa
from ....models.jadwal_model import Jadwal
# schemas
from .absenSchema import GetHistoriTinjauanAbsenResponse, StatistikAbsenResponse, GetAbsenByKelasFilterQuery, GetAbsenBySiswaFilterQuery, GetAbsenByKelasResponse, TinjauAbsenRequest, TinjauAbsenResponse
from ...schemas.absen_schema import  GetAbsenTinjauanResponse, GetAbsenHarianResponse,AbsenWithSiswa, AbsenWithJadwalMapel
from ...schemas.kelasJurusan_schema import KelasBase
from ...schemas.response_schema import MessageOnlyResponse
# common
from ....error.errorHandling import HttpException
from datetime import date
from collections import defaultdict
from ....utils.generateId_util import generate_id
from ....utils.updateTable_util import updateTable
from copy import deepcopy

# daftar status absen yang dapat ditinjau: diterima atau ditolak oleh petugasBK
liststatusForTinjau = [StatusAbsenEnum.dispen.value,StatusAbsenEnum.sakit.value,StatusAbsenEnum.telat.value,StatusAbsenEnum.izin_telat.value, StatusAbsenEnum.izin.value]
# for get statistix=c absen today : jumlah absen diterima, ditolak, belum ditinjau
async def getStatistikAbsen(id_petugasBK : int,session : AsyncSession) -> StatistikAbsenResponse :
    findDistribusiPetugasBK = (await session.execute(select(DistribusiPetugasBK).where(DistribusiPetugasBK.id_petugas_BK == id_petugasBK))).scalars().all()
    
    id_kelas_distribusi = [distribusi_petugas.id_kelas for distribusi_petugas in findDistribusiPetugasBK]

    getStatistikAbsen = (await session.execute(select(func.count(Absen.id).filter(Absen.detail.and_(AbsenDetail.diterima == StatusTinjauanEnum.diterima.value)).label("diterima"),func.count(Absen.id).filter(Absen.detail.and_(AbsenDetail.diterima == StatusTinjauanEnum.ditolak.value)).label("ditolak"),func.count(Absen.id).filter(Absen.detail.and_(AbsenDetail.diterima == StatusTinjauanEnum.belum_ditinjau.value)).label("belum_ditinjau")).where(Absen.siswa.and_(Siswa.id_kelas.in_(id_kelas_distribusi),Absen.tanggal == date.today())))).one()

    statistikAbsenDict = getStatistikAbsen._asdict()

    return {
        "msg" : "success",
        "data" : statistikAbsenDict
    }

# # get history absen today
# async def getHistoriAbsen(id_petugasBK : int,session : AsyncSession) -> list[AbsenDetail] :
#     findDistribusiPetugasBK = (await session.execute(select(DistribusiPetugasBK).where(DistribusiPetugasBK.id_petugas_BK == id_petugasBK))).scalars().all()

#     id_kelas_distribusi = [distribusi_petugas.id_kelas for distribusi_petugas in findDistribusiPetugasBK]

#     findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.detail)).where(and_(Absen.siswa.and_(Siswa.id_kelas.in_(id_kelas_distribusi)))).order_by(Absen.tanggal.desc()).limit(3))).scalars().all()

#     return {
#         "msg" : "success",
#         "data" : findAbsen
#     }

# get histori tinjauan absen today
async def getHistoriTinjauanAbsen(id_petugasBK : int,session : AsyncSession) -> GetHistoriTinjauanAbsenResponse :
    findDistribusiPetugasBK = (await session.execute(select(DistribusiPetugasBK).where(DistribusiPetugasBK.id_petugas_BK == id_petugasBK))).scalars().all()

    id_kelas_distribusi = [distribusi_petugas.id_kelas for distribusi_petugas in findDistribusiPetugasBK]

    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.detail),joinedload(Absen.siswa).joinedload(Siswa.kelas)).where(and_(Absen.siswa.and_(Siswa.id_kelas.in_(id_kelas_distribusi)),Absen.status.in_(liststatusForTinjau),Absen.tanggal == date.today())))).scalars().all()

    grouped_absen = defaultdict(list)
    for absenItem in findAbsen:
        status_key = absenItem.detail
        grouped_absen[status_key].append(absenItem)

    return {
        "msg" : "success",
        "data" : grouped_absen
    }

# get detail tinjauan absen by id
async def getDetailTinjauanAbsensiById(id_absen : int,session : AsyncSession) -> GetAbsenTinjauanResponse :
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.detail).joinedload(AbsenDetail.petugas_bk),joinedload(Absen.siswa).options(joinedload(Siswa.kelas).joinedload(Kelas.guru_walas)),joinedload(Absen.jadwal).options(joinedload(Jadwal.koordinat),joinedload(Jadwal.guru_mapel)),joinedload(Absen.jadwal).joinedload(Jadwal.guru_mapel),joinedload(Absen.jadwal).joinedload(Jadwal.koordinat)).where(Absen.id == id_absen))).scalar_one_or_none()

    if findAbsen is None :
        raise HttpException(404,"Absen tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findAbsen
    }

# get all kelas yang ditinjau atau didistribusi untuk guru bk
async def getAllKelasTinjauan(id_petugasBK : int,session : AsyncSession) -> list[KelasBase] :
    findDistribusiPetugasBK = (await session.execute(select(DistribusiPetugasBK).options(joinedload(DistribusiPetugasBK.kelas)).where(DistribusiPetugasBK.id_petugas_BK == id_petugasBK))).scalars().all()

    kelasResponse = [distribusi_petugas.kelas for distribusi_petugas in findDistribusiPetugasBK]

    return {
        "msg" : "success",
        "data" : kelasResponse
    }

# get all absen by kelas
async def getAbsenByKelas(query : GetAbsenByKelasFilterQuery,session : AsyncSession) -> GetAbsenByKelasResponse :
    findKelas = (await session.execute(select(Kelas).options(joinedload(Kelas.siswa),joinedload(Kelas.guru_walas)).where(Kelas.id == query.id_kelas))).scalar_one_or_none()

    if not findAbsen :
        raise HttpException(404,"kelas tidak ditemukan")
    
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.siswa)).where(and_(Absen.siswa.and_(Siswa.id_kelas == query.id_kelas),Absen.tanggal == query.tanggal)))).scalars().all()

    grouped_absen = defaultdict(list)
    for absenItem in findAbsen:
        namaSiswa_key = absenItem.siswa.nama
        grouped_absen[namaSiswa_key].append(absenItem)

    return {
        "msg" : "success",
        "data" : {
            "jumlah_siswa" : len(findKelas.siswa),
            "guru_walas" : findKelas.guru_walas,
            "absen" : grouped_absen
        }
    }

# get all absen by siswa
async def getAllAbsenBySiswa(query : GetAbsenBySiswaFilterQuery,session : AsyncSession) -> list[AbsenWithJadwalMapel] :
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.jadwal).joinedload(Jadwal.mapel)).where(and_(Absen.siswa.and_(Siswa.id == query.id_siswa),Absen.tanggal == query.tanggal)))).scalars().all()

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

async def tinjauAbsen(petugasBk : dict,id_absen : int,body : TinjauAbsenRequest, session : AsyncSession) -> TinjauAbsenResponse :
    findAbsen = (await session.execute(select(Absen).options(joinedload(Absen.detail)).where(Absen.id == id_absen))).scalar_one_or_none()

    if findAbsen is None :
        raise HttpException(404,"absen tidak ditemukan")
    
    if findAbsen.status not in liststatusForTinjau :
        raise HttpException(400,f"Jenis absen {findAbsen.status} tidak perlu ditinjau")
    
    if not findAbsen.detail :
        detailAbsenMapping = {"id" : generate_id(),"id_absen" : findAbsen.id,"catatan" : None,"diterima" : StatusTinjauanEnum.belum_ditinjau.value}

        session.add(AbsenDetail(**detailAbsenMapping))
        await session.commit()
        await session.refresh(findAbsen)

    updateDetailAbsenMapping = {"id_peninjau" : petugasBk["id"],"status_tinjauan" : body.status_tinjauan.value,"tanggal_tinjauan" : date.today()}
    updateTable(updateDetailAbsenMapping,findAbsen.detail)
    absenDictCopy = deepcopy(findAbsen.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : {
            "status" : body.status_tinjauan,
            "petugasBK" : petugasBk,
            "absen" : absenDictCopy
        }
    }

    