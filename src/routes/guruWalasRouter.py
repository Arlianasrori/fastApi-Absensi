from fastapi import APIRouter,Depends, UploadFile

# auth-profile
from ..domain.guru_walas.auth_profile import authProfileService
from ..domain.schemas.guruWalas_schema import GuruWalasBase, GuruWalasDetailWithSekolah

# absen
from ..domain.guru_walas.absen import absenService
from ..domain.guru_walas.absen.absenSchema import GetAbsenBySiswaFilterQuery, GetAbsenFilterQuery, GetAbsenInKelasResponse, GetAbsenByJadwalResponse
from ..domain.schemas.absen_schema import AbsenWithJadwalMapel, AbsenBase, GetAbsenHarianResponse
from ..domain.schemas.jadwal_schema import JadwalWithMapelGuruMapel

from datetime import date
# depends
from ..auth.auth_depends.guru_walas.depend_auth_guru_walas import guruWalasDependAuth
from ..auth.auth_depends.guru_walas.get_guru_walas_auth import getWalasAuth

# common
from ..domain.schemas.response_schema import ApiResponse,MessageOnlyResponse
from ..db.sessionDepedency import sessionDepedency

guruWalasRouter = APIRouter(prefix="/guru-walas",dependencies=[Depends(guruWalasDependAuth)])

# auth-profile
@guruWalasRouter.get("/",response_model=ApiResponse[GuruWalasBase],tags=["GURUWALAS/AUTH-PROFILE"])
async def getguruWalas(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await authProfileService.getGuruWalas(guruWalas["id"],session)

@guruWalasRouter.get("/profile",response_model=ApiResponse[GuruWalasDetailWithSekolah],tags=["GURUWALAS/AUTH-PROFILE"])
async def getProfileguruWalas(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await authProfileService.getGuruWalasProfile(guruWalas["id"],session)

# absen
@guruWalasRouter.get("/absen/histori",response_model=ApiResponse[list[AbsenBase]],tags=["GURUWALAS/ABSEN"])
async def getAbsenBySiswa(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await absenService.getHistoriAbsen(guruWalas,session)

@guruWalasRouter.get("/absen/kelas",response_model=ApiResponse[GetAbsenInKelasResponse],tags=["GURUWALAS/ABSEN"])
async def getAbsenByKelas(query : GetAbsenFilterQuery = Depends(),guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await absenService.getAllAbsenInKelas(guruWalas,query,session)

@guruWalasRouter.get("/absen/siswa",response_model=ApiResponse[list[AbsenWithJadwalMapel]],tags=["GURUWALAS/ABSEN"])
async def getAbsenBySiswa(query : GetAbsenBySiswaFilterQuery = Depends(),session : sessionDepedency = None) :
    return await absenService.getAllAbsenBySiswa(query,session)

@guruWalasRouter.get("/absen/detail/{id_absen}",response_model=ApiResponse[GetAbsenHarianResponse],tags=["GURUWALAS/ABSEN"])
async def getDetailAbsen(id_absen : int,session : sessionDepedency = None) :
    return await absenService.getDetailAbsenHarian(id_absen,session)

@guruWalasRouter.get("/absen/tanggalContainsAbsen",response_model=ApiResponse[list[date]],tags=["GURUWALAS/ABSEN"])
async def getTanggalContainsAbsen(month : int,guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await absenService.getAllTanggalContainsAbsen(guruWalas,month,session)

@guruWalasRouter.get("/jadwal",response_model=ApiResponse[list[JadwalWithMapelGuruMapel]],tags=["GURUWALAS/ABSEN"])
async def getJadwalByTanggal(tanggal : date,guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await absenService.getJadwalByTanggal(guruWalas,tanggal,session)

@guruWalasRouter.get("/absen/jadwal/{id_jadwal}",response_model=ApiResponse[GetAbsenByJadwalResponse],tags=["GURUWALAS/ABSEN"])
async def getAbsenInKelasByJadwal(id_jadwal : int,query : GetAbsenFilterQuery = Depends(),guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await absenService.getAbsenByJadwal(guruWalas,id_jadwal,query,session)