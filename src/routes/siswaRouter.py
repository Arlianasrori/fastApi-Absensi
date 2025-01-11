from fastapi import APIRouter,Depends, UploadFile

# auth-profile
from ..domain.siswa.auth_profile import authProfileService
from ..domain.schemas.siswa_schema import SiswaBase, SiswaWithJurusanKelasAlamat

# jadwal
from ..domain.siswa.jadwal import jadwalService
from ..domain.siswa.jadwal.jadwalSchema import GetHariContainsJadwalResponse, FilterJadwalQuery
from ..domain.schemas.jadwal_schema import JadwalWithMapelGuruMapel

# depends
from ..auth.auth_depends.siswa.depend_auth_siswa import siswaDependAuth
from ..auth.auth_depends.siswa.get_siswa_auth import getSiswaAuth

# koordinat-absen
from ..domain.siswa.koordinat_absen import koordinatAbsenService
from ..domain.schemas.koordinatAbsen_schema import KoordinatAbsenKelasBase, KoordinatAbsenDetail


# laporan siswa
from ..domain.siswa.laporan import laporanService
from ..domain.siswa.laporan.laporanSchema import FilterQueryLaporan, AddLaporanSiswaRequest,UpdateLaporanSiswaRequest
from ..domain.schemas.laporanSiswa_schema import LaporanSiswaBase,LaporanSiswaDetail, LaporanSiswaWithFile

# common
from ..domain.schemas.response_schema import ApiResponse,MessageOnlyResponse
from ..db.sessionDepedency import sessionDepedency

siswaRouter = APIRouter(prefix="/siswa",dependencies=[Depends(siswaDependAuth)])

# auth-profile
@siswaRouter.get("/",response_model=ApiResponse[SiswaBase],tags=["AUTH/SISWA/AUTH-PROFILE"])
async def getSiswa(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.getSiswa(siswa["id"],session)

@siswaRouter.get("/profile",response_model=ApiResponse[SiswaWithJurusanKelasAlamat],tags=["AUTH/SISWA/AUTH-PROFILE"])
async def getProfileSiswa(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.getProfile(siswa["id"],session)

# koordinat-absen
@siswaRouter.get("/koordinat-absen",response_model=ApiResponse[list[KoordinatAbsenKelasBase]],tags=["AUTH/SISWA/KOORDINAT-ABSEN"])
async def getAllKoordinat(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await koordinatAbsenService.getAllKoordinat(siswa,session)

@siswaRouter.get("/koordinat-absen/{id}",response_model=ApiResponse[KoordinatAbsenDetail],tags=["AUTH/SISWA/KOORDINAT-ABSEN"])
async def getProfileSiswa(id : int,session : sessionDepedency = None) :
    return await koordinatAbsenService.getKoordinatById(id,session)
  
 # jadwal
@siswaRouter.get("/jadwal/getHariContainstJadwal",response_model=ApiResponse[list[GetHariContainsJadwalResponse]],tags=["AUTH/SISWA/JADWAL"])
async def getHariContainsJadwal(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await jadwalService.getHariContainsJadwal(siswa,session)

@siswaRouter.get("/jadwal",response_model=ApiResponse[list[JadwalWithMapelGuruMapel]],tags=["AUTH/SISWA/JADWAL"])
async def getProfileSiswa(query : FilterJadwalQuery = Depends(),siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await jadwalService.getAllJadwal(siswa,query,session)

# laporan siswa
@siswaRouter.post("/laporan",response_model=ApiResponse[LaporanSiswaBase],tags=["AUTH/SISWA/LAPORAN"])
async def addLaporan(laporan : AddLaporanSiswaRequest,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.addLaporan(siswa["id"],laporan,session)

@siswaRouter.post("/laporan/file/{id_laporan}",response_model=ApiResponse[LaporanSiswaWithFile],tags=["AUTH/SISWA/LAPORAN"])
async def addFileLaporan(id_laporan : int,file : UploadFile,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.addFileLaporan(siswa["id"],id_laporan,file,session)

@siswaRouter.delete("/laporan/file/{id_file_laporan}",response_model=MessageOnlyResponse,tags=["AUTH/SISWA/LAPORAN"])
async def deleteFileLaporan(id_file_laporan : int,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.deleteFileLaporan(siswa["id"],id_file_laporan,session)

@siswaRouter.delete("/laporan/{id_laporan}",response_model=ApiResponse[LaporanSiswaDetail],tags=["AUTH/SISWA/LAPORAN"])
async def deleteLaporan(id_laporan : int,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.deleteLaporan(siswa["id"],id_laporan,session)

@siswaRouter.put("/laporan/{id_laporan}",response_model=ApiResponse[LaporanSiswaBase],tags=["AUTH/SISWA/LAPORAN"])
async def updateLaporan(id_laporan : int,laporan : UpdateLaporanSiswaRequest | dict = UpdateLaporanSiswaRequest(),siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.updateLaporan(siswa["id"],id_laporan,laporan,session)

@siswaRouter.get("/laporan",response_model=ApiResponse[list[LaporanSiswaBase]],tags=["AUTH/SISWA/LAPORAN"])
async def getAllLaporan(query : FilterQueryLaporan = Depends(),siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.getAllLaporan(siswa,query,session)

@siswaRouter.get("/laporan/{id_laporan}",response_model=ApiResponse[LaporanSiswaDetail],tags=["AUTH/SISWA/LAPORAN"])
async def getLaporanById(id_laporan : int,session : sessionDepedency = None) :
    return await laporanService.getLaporanById(id_laporan,session)
