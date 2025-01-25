from fastapi import APIRouter,Depends, UploadFile

# auth-profile
from ..domain.guru_walas.auth_profile import authProfileService
from ..domain.schemas.guruWalas_schema import GuruWalasBase, GuruWalasDetailWithSekolah

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

# # absen
# @petugasBKRouter.get("/absen/statistik-tinjauan",response_model=ApiResponse[StatistikAbsenResponse],tags=["PETUGASBK/ABSEN"])
# async def getStatistikAbsen(petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
#     return await absenService.getStatistikAbsen(petugasBK["id"],session)

# @petugasBKRouter.get("/absen/histori-tinjauan",response_model=ApiResponse[GetHistoriTinjauanAbsenResponse],tags=["PETUGASBK/ABSEN"])
# async def getHistoriTinjauanAbsen(petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
#     return await absenService.getHistoriTinjauanAbsen(petugasBK["id"],session)

# @petugasBKRouter.get("/absen/histori-tinjauan/{id_absen}",response_model=ApiResponse[GetHistoriTinjauanAbsenResponse],tags=["PETUGASBK/ABSEN"])
# async def getHistoriTinajuanDetil(id_absen : int,session : sessionDepedency = None) :
#     return await absenService.getDetailTinjauanAbsensiById(id_absen,session)

# @petugasBKRouter.get("/absen/kelas-tinjauan",response_model=ApiResponse[GetAllKelasTinjauanResponse],tags=["PETUGASBK/ABSEN"])
# async def getKelasTinjauan(petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
#     return await absenService.getAllKelasTinjauan(petugasBK["id"],session)

# @petugasBKRouter.get("/absen/byKelas",response_model=ApiResponse[dict[str,dict[int,AbsenBase]]],tags=["PETUGASBK/ABSEN"])
# async def getAbsenByKelas(query : GetAbsenByKelasFilterQuery = Depends(),session : sessionDepedency = None) :
#     return await absenService.getAbsenByKelas(query,session)

# @petugasBKRouter.get("/absen/bySiswa",response_model=ApiResponse[list[AbsenWithJadwalMapel]],tags=["PETUGASBK/ABSEN"])
# async def getAbsenBySiswa(query : GetAbsenBySiswaFilterQuery = Depends(),session : sessionDepedency = None) :
#     return await absenService.getAllAbsenBySiswa(query,session)

# @petugasBKRouter.get("/absen/detail/{id_absen}",response_model=ApiResponse[GetAbsenHarianResponse],tags=["PETUGASBK/ABSEN"])
# async def getDetailAbsen(id_absen : int,session : sessionDepedency = None) :
#     return await absenService.getDetailAbsenHarian(id_absen,session)

# @petugasBKRouter.patch("/absen/tinjau/{id_absen}",response_model=ApiResponse[TinjauAbsenResponse],tags=["PETUGASBK/ABSEN"])
# async def getDetailAbsen(id_absen : int,body : TinjauAbsenRequest,petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
#     return await absenService.tinjauAbsen(petugasBK,id_absen,body,session)