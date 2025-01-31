from fastapi import APIRouter,Depends

# auth-profile
from ..domain.guru_mapel.auth_profile import authProfileService
from ..domain.schemas.guruMapel_schema import GuruMapelBase, GuruMapelDetailWithSekolah

# absen
from ..domain.guru_mapel.absen import absenService
from ..domain.guru_mapel.absen.absenSchema import GetAbsenFilterQuery, GetHistoriAbsenKelasResponse, GetAbsenAbsenInKelasResponse, GetStatistikKelasAbsenResponse, GetHistoriKelasAjarResponse
from ..domain.schemas.kelasJurusan_schema import KelasBase
from ..domain.schemas.absen_schema import GetAbsenHarianResponse

# depends
from ..auth.auth_depends.guru_mapel.depend_auth_guru_mapel import guruMapelDependAuth
from ..auth.auth_depends.guru_mapel.get_guru_mapel_auth import getMapelAuth

# common
from ..domain.schemas.response_schema import ApiResponse
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
@guruMapelRouter.get("/absen/histori-kelas-ajar",response_model=ApiResponse[list[GetHistoriKelasAjarResponse]],tags=["GURUMAPEL/AUTH-PROFILE"])
async def getHistoriKelasAjar(guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await absenService.getHistoriKelasAjar(guruMapel,session)

@guruMapelRouter.get("/absen/histori-absen-kelas",response_model=ApiResponse[GetHistoriAbsenKelasResponse],tags=["GURUMAPEL/ABSEN"])
async def getAllAbsenByHistori(query : GetAbsenFilterQuery = Depends(),guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await absenService.getAllAbsenByHistori(guruMapel,query,session)

@guruMapelRouter.get("/absen/statistik-kelas-ajar",response_model=ApiResponse[GetStatistikKelasAbsenResponse],tags=["GURUMAPEL/ABSEN"])
async def getStatistikKelasAjar(guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await absenService.getStatistikKelasAbsen(guruMapel,session)

@guruMapelRouter.get("/absen/detail/{id_absen}",response_model=ApiResponse[GetAbsenHarianResponse],tags=["GURUMAPEL/ABSEN"])
async def getDetailAbsenHarian(id_absen : int,session : sessionDepedency = None) :
    return await absenService.getDetailAbsenHarian(id_absen,session)

@guruMapelRouter.get("/absen/kelas",response_model=ApiResponse[GetAbsenAbsenInKelasResponse],tags=["GURUMAPEL/ABSEN"])
async def getAbsenInKelas(query : GetAbsenFilterQuery = Depends(),guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await absenService.getAllAbsenInKelas(guruMapel,query,session)

@guruMapelRouter.get("/kelas-ajar",response_model=ApiResponse[list[KelasBase]],tags=["GURUMAPEL/ABSEN"])
async def getKelasAjar(guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await absenService.getKelasAjar(guruMapel,session)