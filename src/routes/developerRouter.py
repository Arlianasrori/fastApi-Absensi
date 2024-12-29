from fastapi import APIRouter,Depends, Request, UploadFile

# model and service
from ..domain.developer.developerSchema import Developer,AddSekolahRequest,UpdateSekolahRequest,AddAdminRequest,UpdateAdminRequest
from ..domain.developer import developerService

from ..domain.schemas.sekolah_schema import SekolahBase,SekolahWithAlamat,SekolahDetail,AdminWithSekolah,AdminBase
from ..domain.schemas.alamat_schema import AlamatBase,UpdateAlamatBody
from ..domain.schemas.response_schema import ApiResponse

# depends
from ..auth.auth_depends.developer.depend_auth_developer import developerAuth
from ..db.sessionDepedency import sessionDepedency

developerRouter = APIRouter(prefix="/developer",dependencies=[Depends(developerAuth)])


# admin developer auth
@developerRouter.get("/",response_model=ApiResponse[Developer],tags=["DEVELOPER"])
async def getDeveloper(Req : Request) :
    return {
        "msg" : "success",
        "data" : Req.developer
    }

# sekolah
@developerRouter.post("/sekolah",response_model=ApiResponse[SekolahWithAlamat],tags=["DEVELOPER/SEKOLAH"])
async def add_sekolah(sekolah : AddSekolahRequest,alamat : AlamatBase,session : sessionDepedency) :
    return await developerService.add_sekolah(sekolah,alamat,session)

@developerRouter.patch("/sekolah/logo/{id_sekolah}",response_model=ApiResponse[SekolahBase],tags=["DEVELOPER/SEKOLAH"])
async def update_logo_sekolah(id_sekolah : int,logo : UploadFile,session : sessionDepedency) :
    return await developerService.add_update_foto_profile_sekolah(id_sekolah,logo,session)

@developerRouter.get("/sekolah",response_model=ApiResponse[list[SekolahWithAlamat]],tags=["DEVELOPER/SEKOLAH"])
async def get_all_sekolah(session : sessionDepedency) :
    return await developerService.getAllsekolah(session)

@developerRouter.get("/sekolah/{id_sekolah}",response_model=ApiResponse[SekolahDetail],tags=["DEVELOPER/SEKOLAH"])
async def get_sekolah_by_id(id_sekolah : int,session : sessionDepedency) :
    return await developerService.getSekolahById(id_sekolah,session)

@developerRouter.put("/sekolah/{id_sekolah}",response_model=ApiResponse[SekolahWithAlamat],tags=["DEVELOPER/SEKOLAH"])
async def update_sekolah(id_sekolah : int,sekolah : UpdateSekolahRequest | None = None,alamat : UpdateAlamatBody | None = None,session : sessionDepedency = None) :
    return await developerService.updateSekolah(id_sekolah,sekolah,alamat,session)

@developerRouter.delete("/sekolah/{id_sekolah}",response_model=ApiResponse[SekolahBase],tags=["DEVELOPER/SEKOLAH"])
async def delete_sekolah(id_sekolah : int,session : sessionDepedency) :
    return await developerService.deleteSekolah(id_sekolah,session)

# admin
@developerRouter.post("/admin",response_model=ApiResponse[AdminWithSekolah],tags=["DEVELOPER/ADMIN"])
async def add_admin(admin : AddAdminRequest,session : sessionDepedency) :
    return await developerService.add_admin_sekolah(admin,session)

@developerRouter.get("/admin",response_model=ApiResponse[list[AdminWithSekolah]],tags=["DEVELOPER/ADMIN"])
async def get_all_admin(session : sessionDepedency) :
    return await developerService.get_all_admin_sekolah(session)

@developerRouter.get("/admin/{id_admin}",response_model=ApiResponse[AdminWithSekolah],tags=["DEVELOPER/ADMIN"])
async def get_admin_by_id(id_admin : int,session : sessionDepedency) :
    return await developerService.get_admin_sekolah_by_id(id_admin,session)
    
@developerRouter.put("/admin/{id_admin}",response_model=ApiResponse[AdminWithSekolah],tags=["DEVELOPER/ADMIN"])
async def update_admin(id_admin : int,admin : UpdateAdminRequest | None = None,session : sessionDepedency = None) :
    return await developerService.update_admin_sekolah(id_admin,admin,session)

@developerRouter.delete("/admin/{id_admin}",response_model=ApiResponse[AdminBase],tags=["DEVELOPER/ADMIN"])
async def delete_admin(id_admin : int,session : sessionDepedency) :
    return await developerService.delete_admin_sekolah(id_admin,session)

