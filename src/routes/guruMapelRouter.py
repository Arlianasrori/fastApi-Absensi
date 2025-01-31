from fastapi import APIRouter,Depends, UploadFile

# auth-profile
from ..domain.guru_mapel.auth_profile import authProfileService
from ..domain.schemas.guruMapel_schema import GuruMapelBase, GuruMapelDetailWithSekolah, GuruMapelWithAlamat
from ..domain.guru_mapel.auth_profile.authprofileSchema import UpdateProfileRequest
from ..domain.schemas.alamat_schema import UpdateAlamatBody
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

@guruMapelRouter.put("/profile",response_model=ApiResponse[GuruMapelWithAlamat],tags=["GURUMAPEL/AUTH-PROFILE"])
async def updateProfileGuruMapel(body : UpdateProfileRequest = UpdateProfileRequest(),alamat : UpdateAlamatBody = UpdateAlamatBody(),guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await authProfileService.updateProfile(guruMapel["id"],body,alamat,session)

@guruMapelRouter.patch("/profile/foto_profile/{id_guru_mapel}",response_model=ApiResponse[GuruMapelBase],tags=["GURUMAPEL/AUTH_PROFILE"])
async def add_update_profile(id_guru_mapel : int,foto_profile : UploadFile,guruMapel : dict = Depends(getMapelAuth),session : sessionDepedency = None) :
    return await authProfileService.add_update_foto_profile(id_guru_mapel,guruMapel["id_sekolah"],foto_profile,session)