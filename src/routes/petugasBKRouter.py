from fastapi import APIRouter,Depends, UploadFile

# auth-profile
from ..domain.petugasBK.auth_profile import authProfileService
from ..domain.schemas.petugasBK_schema import PetugasBkBase,PetugasBKDetailWithSekolah

# absen
from ..domain.petugasBK.absen import absenService
from ..domain.petugasBK.absen.absenSchema import GetHistoriTinjauanAbsenResponse, StatistikAbsenResponse, GetAbsenByKelasFilterQuery, GetAbsenBySiswaFilterQuery, TinjauAbsenRequest, TinjauAbsenResponse,GetAllKelasTinjauanResponse
from ..domain.schemas.absen_schema import AbsenBase, GetAbsenTinjauanResponse, GetAbsenHarianResponse,AbsenWithSiswa,AbsenWithJadwalMapel
from ..domain.schemas.kelasJurusan_schema import KelasBase

# depends
from ..auth.auth_depends.petugas_BK.depend_auth_petugasBK import petugasBKDependAuth 
from ..auth.auth_depends.petugas_BK.get_guru_petugasBK_auth import getPetugasBKAuth

# common
from ..domain.schemas.response_schema import ApiResponse,MessageOnlyResponse
from ..db.sessionDepedency import sessionDepedency

petugasBKRouter = APIRouter(prefix="/petugasBK",dependencies=[Depends(petugasBKDependAuth)])

# auth-profile
@petugasBKRouter.get("/",response_model=ApiResponse[PetugasBkBase],tags=["PETUGASBK/AUTH-PROFILE"])
async def getPetugasBK(petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
    return await authProfileService.getPetugasBK(petugasBK["id"],session)

@petugasBKRouter.get("/profile",response_model=ApiResponse[PetugasBKDetailWithSekolah],tags=["PETUGASBK/AUTH-PROFILE"])
async def getProfilePetugasBK(petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
    return await authProfileService.getProfile(petugasBK["id"],session)

# absen
@petugasBKRouter.get("/absen/statistik-tinjauan",response_model=ApiResponse[StatistikAbsenResponse],tags=["PETUGASBK/ABSEN"])
async def getStatistikAbsen(petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
    return await absenService.getStatistikAbsen(petugasBK["id"],session)

@petugasBKRouter.get("/absen/histori-tinjauan",response_model=ApiResponse[GetHistoriTinjauanAbsenResponse],tags=["PETUGASBK/ABSEN"])
async def getHistoriTinjauanAbsen(petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
    return await absenService.getHistoriTinjauanAbsen(petugasBK["id"],session)

@petugasBKRouter.get("/absen/histori-tinjauan/{id_absen}",response_model=ApiResponse[GetHistoriTinjauanAbsenResponse],tags=["PETUGASBK/ABSEN"])
async def getHistoriTinajuanDetil(id_absen : int,session : sessionDepedency = None) :
    return await absenService.getDetailTinjauanAbsensiById(id_absen,session)

@petugasBKRouter.get("/absen/kelas-tinjauan",response_model=ApiResponse[GetAllKelasTinjauanResponse],tags=["PETUGASBK/ABSEN"])
async def getKelasTinjauan(petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
    return await absenService.getAllKelasTinjauan(petugasBK["id"],session)

@petugasBKRouter.get("/absen/byKelas",response_model=ApiResponse[dict[str,dict[int,AbsenBase]]],tags=["PETUGASBK/ABSEN"])
async def getAbsenByKelas(query : GetAbsenByKelasFilterQuery = Depends(),session : sessionDepedency = None) :
    return await absenService.getAbsenByKelas(query,session)

@petugasBKRouter.get("/absen/bySiswa",response_model=ApiResponse[list[AbsenWithJadwalMapel]],tags=["PETUGASBK/ABSEN"])
async def getAbsenBySiswa(query : GetAbsenBySiswaFilterQuery = Depends(),session : sessionDepedency = None) :
    return await absenService.getAllAbsenBySiswa(query,session)

@petugasBKRouter.get("/absen/detail/{id_absen}",response_model=ApiResponse[GetAbsenHarianResponse],tags=["PETUGASBK/ABSEN"])
async def getDetailAbsen(id_absen : int,session : sessionDepedency = None) :
    return await absenService.getDetailAbsenHarian(id_absen,session)

@petugasBKRouter.patch("/absen/tinjau/{id_absen}",response_model=ApiResponse[TinjauAbsenResponse],tags=["PETUGASBK/ABSEN"])
async def getDetailAbsen(id_absen : int,body : TinjauAbsenRequest,petugasBK : dict = Depends(getPetugasBKAuth),session : sessionDepedency = None) :
    return await absenService.tinjauAbsen(petugasBK,id_absen,body,session)