from fastapi import APIRouter,Depends,UploadFile

# auth-profile
from ..domain.guru_mapel.auth_profile import authProfileService
from ..domain.schemas.guruMapel_schema import GuruMapelBase, GuruMapelDetailWithSekolah, GuruMapelWithAlamat
from ..domain.guru_mapel.auth_profile.authprofileSchema import UpdateProfileRequest
from ..domain.schemas.alamat_schema import UpdateAlamatBody

# absen
from ..domain.guru_mapel.absen import absenService
from ..domain.guru_mapel.absen.absenSchema import GetAbsenFilterQuery, GetHistoriAbsenKelasResponse, GetAbsenAbsenInKelasResponse, GetStatistikKelasAbsenResponse, GetHistoriKelasAjarResponse
from ..domain.schemas.kelasJurusan_schema import KelasBase
from ..domain.schemas.absen_schema import GetAbsenHarianResponse

# notification
from ..domain.guru_mapel.notification import notificationService
from ..domain.schemas.notification_schema import NotificationModelBase, ResponseGetUnreadNotification

# depends
from ..auth.auth_depends.guru_mapel.depend_auth_guru_mapel import guruMapelDependAuth
from ..auth.auth_depends.guru_mapel.get_guru_mapel_auth import getMapelAuth

# common
from ..domain.schemas.response_schema import ApiResponse
from ..db.sessionDepedency import sessionDepedency
from datetime import date

guruMapelRouter = APIRouter(prefix="/guru-mapel",dependencies=[Depends(guruMapelDependAuth)])

# auth-profile
@guruMapelRouter.get("/",response_model=ApiResponse[GuruMapelBase],tags=["GURUMAPEL/AUTH-PROFILE"])
async def getguruMapel(guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await authProfileService.getGuruMapel(guruMapel["id"],session)

@guruMapelRouter.get("/profile",response_model=ApiResponse[GuruMapelDetailWithSekolah],tags=["GURUMAPEL/AUTH-PROFILE"])
async def getProfileguruMapel(guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await authProfileService.getGuruMapelProfile(guruMapel["id"],session)

@guruMapelRouter.put("/profile",response_model=ApiResponse[GuruMapelWithAlamat],tags=["GURUMAPEL/AUTH-PROFILE"])
async def updateProfileGuruMapel(body : UpdateProfileRequest = UpdateProfileRequest(),alamat : UpdateAlamatBody = UpdateAlamatBody(),guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await authProfileService.updateProfile(guruMapel["id"],body,alamat,session)

@guruMapelRouter.patch("/profile/foto_profile",response_model=ApiResponse[GuruMapelBase],tags=["GURUMAPEL/AUTH_PROFILE"])
async def add_update_profile(foto_profile : UploadFile,guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await authProfileService.add_update_foto_profile(guruMapel["id"],foto_profile,session)

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


# notification
@guruMapelRouter.get("/notification",response_model=ApiResponse[dict[date,list[NotificationModelBase]]],tags=["GURUMAPEL/NOTIFICATION"])
async def getAllNotification(guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await notificationService.getAllNotification(guruMapel["id"],session)

@guruMapelRouter.get("/notification/{id_notification}",response_model=ApiResponse[NotificationModelBase],tags=["GURUMAPEL/NOTIFICATION"])
async def getNotificationById(id_notification : int,guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await notificationService.getNotificationById(id_notification,guruMapel["id"],session)

@guruMapelRouter.post("/notification/read/{id_notification}",response_model=ApiResponse[NotificationModelBase],tags=["GURUMAPEL/NOTIFICATION"])
async def readNotification(id_notification : int,guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await notificationService.readNotification(id_notification,guruMapel["id"],session)

@guruMapelRouter.get("/notification/unread/count",response_model=ApiResponse[ResponseGetUnreadNotification],tags=["GURUMAPEL/NOTIFICATION"])
async def getUnreadNotification(guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await notificationService.getCountNotification(guruMapel["id"],session)