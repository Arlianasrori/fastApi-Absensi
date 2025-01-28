from fastapi import APIRouter,Depends, UploadFile

# auth-profile
from ..domain.guru_mapel.auth_profile import authProfileService
from ..domain.schemas.guruMapel_schema import GuruMapelBase, GuruMapelDetailWithSekolah
# depends
from ..auth.auth_depends.guru_mapel.depend_auth_guru_mapel import guruMapelDependAuth
from ..auth.auth_depends.guru_mapel.get_guru_mapel_auth import getMapelAuth

# common
from ..domain.schemas.response_schema import ApiResponse,MessageOnlyResponse
from ..db.sessionDepedency import sessionDepedency

guruMapelRouter = APIRouter(prefix="/guru-mapel",dependencies=[Depends(guruMapelDependAuth)])

# auth-profile
@guruMapelRouter.get("/",response_model=ApiResponse[GuruMapelBase],tags=["GURUMAPEL/AUTH-PROFILE"])
async def getguruMapel(guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await authProfileService.getGuruMapel(guruMapel["id"],session)

@guruMapelRouter.get("/profile",response_model=ApiResponse[GuruMapelDetailWithSekolah],tags=["GURUMAPEL/AUTH-PROFILE"])
async def getProfileguruMapel(guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await authProfileService.getGuruMapelProfile(guruMapel["id"],session)

# # absen
# @guruWalasRouter.get("/absen/statistik",response_model=ApiResponse[GetStatistikAbsenResponse],tags=["GURUWALAS/ABSEN"])
# async def getStatistikAbsen(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
#     return await absenService.getStatistikAbsen(guruWalas,session)

# @guruWalasRouter.get("/absen/histori",response_model=ApiResponse[list[AbsenBase]],tags=["GURUWALAS/ABSEN"])
# async def getAbsenBySiswa(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
#     return await absenService.getHistoriAbsen(guruWalas,session)

# @guruWalasRouter.get("/absen/kelas",response_model=ApiResponse[GetAbsenInKelasResponse],tags=["GURUWALAS/ABSEN"])
# async def getAbsenByKelas(query : GetAbsenFilterQuery = Depends(),guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
#     return await absenService.getAllAbsenInKelas(guruWalas,query,session)

# @guruWalasRouter.get("/absen/siswa",response_model=ApiResponse[list[AbsenWithJadwalMapel]],tags=["GURUWALAS/ABSEN"])
# async def getAbsenBySiswa(query : GetAbsenBySiswaFilterQuery = Depends(),session : sessionDepedency = None) :
#     return await absenService.getAllAbsenBySiswa(query,session)

# @guruWalasRouter.get("/absen/detail/{id_absen}",response_model=ApiResponse[GetAbsenHarianResponse],tags=["GURUWALAS/ABSEN"])
# async def getDetailAbsen(id_absen : int,session : sessionDepedency = None) :
#     return await absenService.getDetailAbsenHarian(id_absen,session)

# @guruWalasRouter.get("/absen/tanggalContainsAbsen",response_model=ApiResponse[list[date]],tags=["GURUWALAS/ABSEN"])
# async def getTanggalContainsAbsen(month : int,guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
#     return await absenService.getAllTanggalContainsAbsen(guruWalas,month,session)

# @guruWalasRouter.get("/jadwal",response_model=ApiResponse[list[JadwalWithMapelGuruMapel]],tags=["GURUWALAS/ABSEN"])
# async def getJadwalByTanggal(tanggal : date,guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
#     return await absenService.getJadwalByTanggal(guruWalas,tanggal,session)

# @guruWalasRouter.get("/absen/jadwal/{id_jadwal}",response_model=ApiResponse[GetAbsenByJadwalResponse],tags=["GURUWALAS/ABSEN"])
# async def getAbsenInKelasByJadwal(id_jadwal : int,query : GetAbsenFilterQuery = Depends(),guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
#     return await absenService.getAbsenByJadwal(guruWalas,id_jadwal,query,session)