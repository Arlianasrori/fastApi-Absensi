from fastapi import APIRouter,Depends,UploadFile

# auth-profile
from ..domain.guru_walas.auth_profile import authProfileService
from ..domain.schemas.guruWalas_schema import GuruWalasBase, GuruWalasDetailWithSekolah, GuruWalasWithAlamat
from ..domain.guru_walas.auth_profile.authProfileSchema import UpdateProfileRequest
from ..domain.schemas.alamat_schema import UpdateAlamatBody

# absen
from ..domain.guru_walas.absen import absenService
from ..domain.guru_walas.absen.absenSchema import GetAbsenBySiswaFilterQuery, GetAbsenFilterQuery, GetAbsenInKelasResponse, GetAbsenByJadwalResponse, GetStatistikAbsenResponse
from ..domain.schemas.absen_schema import AbsenWithJadwalMapel, AbsenBase, GetAbsenHarianResponse
from ..domain.schemas.jadwal_schema import JadwalWithMapelGuruMapel

# notification
from ..domain.guru_walas.notification import notificationService
from ..domain.schemas.notification_schema import NotificationModelBase, ResponseGetUnreadNotification

# depends
from ..auth.auth_depends.guru_walas.depend_auth_guru_walas import guruWalasDependAuth
from ..auth.auth_depends.guru_walas.get_guru_walas_auth import getWalasAuth

# common
from datetime import date
from ..domain.schemas.response_schema import ApiResponse
from ..db.sessionDepedency import sessionDepedency

guruWalasRouter = APIRouter(prefix="/guru-walas",dependencies=[Depends(guruWalasDependAuth)])

# auth-profile
@guruWalasRouter.get("/",response_model=ApiResponse[GuruWalasBase],tags=["GURUWALAS/AUTH-PROFILE"])
async def getguruWalas(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await authProfileService.getGuruWalas(guruWalas["id"],session)

@guruWalasRouter.get("/profile",response_model=ApiResponse[GuruWalasDetailWithSekolah],tags=["GURUWALAS/AUTH-PROFILE"])
async def getProfileguruWalas(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await authProfileService.getGuruWalasProfile(guruWalas["id"],session)

@guruWalasRouter.put("/profile",response_model=ApiResponse[GuruWalasWithAlamat],tags=["GURUWALAS/AUTH-PROFILE"])
async def updateProfileguruWalas(body : UpdateProfileRequest = UpdateProfileRequest(),alamat : UpdateAlamatBody = UpdateAlamatBody(),guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await authProfileService.updateProfile(guruWalas["id"],body,alamat,session)

@guruWalasRouter.patch("/profile/foto_profile",response_model=ApiResponse[GuruWalasBase],tags=["GURUWALAS/AUTH-PROFILE"])
async def updateFotoProfileguruWalas(foto_profile : UploadFile,guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await authProfileService.add_update_foto_profile(guruWalas["id"],foto_profile,session)

# absen
@guruWalasRouter.get("/absen/statistik",response_model=ApiResponse[GetStatistikAbsenResponse],tags=["GURUWALAS/ABSEN"])
async def getStatistikAbsen(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await absenService.getStatistikAbsen(guruWalas,session)

@guruWalasRouter.get("/absen/histori",response_model=ApiResponse[list[AbsenBase]],tags=["GURUWALAS/ABSEN"])
async def getHistoriAbsen(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
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

# notification
@guruWalasRouter.get("/notification",response_model=ApiResponse[dict[date,list[NotificationModelBase]]],tags=["GURUWALAS/NOTIFICATION"])
async def getAllNotification(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await notificationService.getAllNotification(guruWalas["id"],session)

@guruWalasRouter.get("/notification/{id_notification}",response_model=ApiResponse[NotificationModelBase],tags=["GURUWALAS/NOTIFICATION"])
async def getNotificationById(id_notification : int,guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await notificationService.getNotificationById(id_notification,guruWalas["id"],session)

@guruWalasRouter.post("/notification/read/{id_notification}",response_model=ApiResponse[NotificationModelBase],tags=["GURUWALAS/NOTIFICATION"])
async def readNotification(id_notification : int,guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await notificationService.readNotification(id_notification,guruWalas["id"],session)

@guruWalasRouter.get("/notification/unread/count",response_model=ApiResponse[ResponseGetUnreadNotification],tags=["GURUWALAS/NOTIFICATION"])
async def getUnreadNotification(guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await notificationService.getCountNotification(guruWalas["id"],session)