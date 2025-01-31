from fastapi import APIRouter,Depends, UploadFile

# auth-profile
from ..domain.guru_walas.auth_profile import authProfileService
from ..domain.schemas.guruWalas_schema import GuruWalasBase, GuruWalasDetailWithSekolah, GuruWalasWithAlamat
from ..domain.guru_walas.auth_profile.authProfileSchema import UpdateProfileRequest
from ..domain.schemas.alamat_schema import UpdateAlamatBody

# depends
from ..auth.auth_depends.guru_walas.depend_auth_guru_walas import guruWalasDependAuth
from ..auth.auth_depends.guru_walas.get_guru_walas_auth import getWalasAuth

# common
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

@guruWalasRouter.put("/profile",response_model=ApiResponse[GuruWalasDetailWithSekolah],tags=["GURUWALAS/AUTH-PROFILE"])
async def updateProfileguruWalas(body : UpdateProfileRequest = UpdateProfileRequest(),alamat : UpdateAlamatBody = UpdateAlamatBody(),guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await authProfileService.updateProfile(guruWalas["id"],body,alamat,session)

@guruWalasRouter.put("/profile/foto_profile",response_model=ApiResponse[GuruWalasBase],tags=["GURUWALAS/AUTH-PROFILE"])
async def updateFotoProfileguruWalas(foto_profile : UploadFile,guruWalas : dict = Depends(getWalasAuth),session : sessionDepedency = None) :
    return await authProfileService.add_update_foto_profile(guruWalas["id"],foto_profile,session)