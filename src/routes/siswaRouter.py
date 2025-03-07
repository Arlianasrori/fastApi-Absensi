from fastapi import APIRouter,Depends

# auth-profile
from ..domain.siswa.auth_profile import authProfileService
from ..domain.schemas.siswa_schema import SiswaBase, SiswaWithJurusanKelasAlamat

# depends
from ..auth.auth_depends.siswa.depend_auth_siswa import siswaDependAuth
from ..auth.auth_depends.siswa.get_siswa_auth import getSiswaAuth

# common
from ..domain.schemas.response_schema import ApiResponse,MessageOnlyResponse
from ..db.sessionDepedency import sessionDepedency

siswaRouter = APIRouter(prefix="/siswa",dependencies=[Depends(siswaDependAuth)])

# admin developer auth
@siswaRouter.get("/",response_model=ApiResponse[SiswaBase],tags=["AUTH/SISWA"])
async def getSiswa(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.getSiswa(siswa["id"],session)

@siswaRouter.get("/profile",response_model=ApiResponse[SiswaWithJurusanKelasAlamat],tags=["AUTH/SISWA"])
async def getProfileSiswa(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.getProfile(siswa["id"],session)