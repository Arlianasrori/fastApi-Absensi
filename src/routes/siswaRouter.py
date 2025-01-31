from fastapi import APIRouter,Depends, UploadFile

# auth-profile
from ..domain.siswa.auth_profile import authProfileService
from ..domain.schemas.siswa_schema import SiswaBase, SiswaDetailWithSekolah, SiswaWithAlamat
from ..domain.schemas.alamat_schema import UpdateAlamatBody
from ..domain.siswa.auth_profile.authProfileSchema import UpdateProfileRequest

# jadwal
from ..domain.siswa.jadwal import jadwalService
from ..domain.siswa.jadwal.jadwalSchema import GetHariContainsJadwalResponse, FilterJadwalQuery, JadwalTodayResponse
from ..domain.schemas.jadwal_schema import JadwalDetail

# depends
from ..auth.auth_depends.siswa.depend_auth_siswa import siswaDependAuth
from ..auth.auth_depends.siswa.get_siswa_auth import getSiswaAuth

# koordinat-absen
from ..domain.siswa.koordinat_absen import koordinatAbsenService
from ..domain.schemas.koordinatAbsen_schema import KoordinatAbsenKelasBase, KoordinatAbsenDetail
from ..domain.siswa.koordinat_absen.koordinatAbsenSchema import CekRadiusKoordinatRequest, CekRadiusKoordinatResponse

# laporan siswa
from ..domain.siswa.laporan import laporanService
from ..domain.siswa.laporan.laporanSchema import FilterQueryLaporan, AddLaporanSiswaRequest,UpdateLaporanSiswaRequest
from ..domain.schemas.laporanSiswa_schema import LaporanSiswaBase,LaporanSiswaDetail, LaporanSiswaWithFile

# absen
from ..domain.siswa.absen import absenService
from ..domain.siswa.absen.absenSchema import RekapAbsenMingguanResponse, CekAbsenSiswaTodayResponse, AbsenSiswaRequest
from ..domain.schemas.absen_schema import AbsenWithDetail
# common
from ..domain.schemas.response_schema import ApiResponse,MessageOnlyResponse
from ..db.sessionDepedency import sessionDepedency

siswaRouter = APIRouter(prefix="/siswa",dependencies=[Depends(siswaDependAuth)])

# auth-profile
@siswaRouter.get("/",response_model=ApiResponse[SiswaBase],tags=["SISWA/AUTH-PROFILE"])
async def getSiswa(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.getSiswa(siswa["id"],session)

@siswaRouter.get("/profile",response_model=ApiResponse[SiswaDetailWithSekolah],tags=["SISWA/AUTH-PROFILE"])
async def getProfileSiswa(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.getProfile(siswa["id"],session)

@siswaRouter.put("/profile",response_model=ApiResponse[SiswaWithAlamat],tags=["SISWA/AUTH-PROFILE"])
async def updateProfileSiswa(body : UpdateProfileRequest = UpdateProfileRequest(),alamat : UpdateAlamatBody = UpdateAlamatBody(),siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.updateProfile(siswa["id"],body,alamat,session)

@siswaRouter.patch("/profile/foto_profile/{id_siswa}",response_model=ApiResponse[SiswaBase],tags=["ADMIN/SISWA"])
async def add_update_profile(id_siswa : int,foto_profile : UploadFile,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.add_update_foto_profile(id_siswa,siswa["id_sekolah"],foto_profile,session)


# koordinat-absen
@siswaRouter.get("/koordinat-absen",response_model=ApiResponse[list[KoordinatAbsenKelasBase]],tags=["SISWA/KOORDINAT-ABSEN"])
async def getAllKoordinat(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await koordinatAbsenService.getAllKoordinat(siswa,session)

@siswaRouter.get("/koordinat-absen/{id}",response_model=ApiResponse[KoordinatAbsenDetail],tags=["SISWA/KOORDINAT-ABSEN"])
async def getProfileSiswa(id : int,session : sessionDepedency = None) :
    return await koordinatAbsenService.getKoordinatById(id,session)

@siswaRouter.post("/koordinat-absen/cek",response_model=ApiResponse[CekRadiusKoordinatResponse],tags=["SISWA/KOORDINAT-ABSEN"])
async def cekKoordinatAbsen(koordinat : CekRadiusKoordinatRequest,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await koordinatAbsenService.cekRadiusKoordinat(siswa,koordinat,session)
  
 # jadwal
@siswaRouter.get("/jadwal/getHariContainstJadwal",response_model=ApiResponse[list[GetHariContainsJadwalResponse]],tags=["SISWA/JADWAL"])
async def getHariContainsJadwal(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await jadwalService.getHariContainsJadwal(siswa,session)

@siswaRouter.get("/jadwal",response_model=ApiResponse[list[JadwalDetail]],tags=["SISWA/JADWAL"])
async def getAllJadwal(query : FilterJadwalQuery = Depends(),siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await jadwalService.getAllJadwal(siswa,query,session)

@siswaRouter.get("/jadwal/today",response_model=ApiResponse[JadwalTodayResponse],tags=["SISWA/JADWAL"])
async def getAllJadwalToday(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await jadwalService.getAllJadwalToday(siswa,session)

# laporan siswa
@siswaRouter.post("/laporan",response_model=ApiResponse[LaporanSiswaBase],tags=["SISWA/LAPORAN"])
async def addLaporan(laporan : AddLaporanSiswaRequest,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.addLaporan(siswa["id"],laporan,session)

@siswaRouter.post("/laporan/file/{id_laporan}",response_model=ApiResponse[LaporanSiswaWithFile],tags=["SISWA/LAPORAN"])
async def addFileLaporan(id_laporan : int,file : UploadFile,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.addFileLaporan(siswa["id"],id_laporan,file,session)

@siswaRouter.delete("/laporan/file/{id_file_laporan}",response_model=MessageOnlyResponse,tags=["SISWA/LAPORAN"])
async def deleteFileLaporan(id_file_laporan : int,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.deleteFileLaporan(siswa["id"],id_file_laporan,session)

@siswaRouter.delete("/laporan/{id_laporan}",response_model=ApiResponse[LaporanSiswaDetail],tags=["SISWA/LAPORAN"])
async def deleteLaporan(id_laporan : int,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.deleteLaporan(siswa["id"],id_laporan,session)

@siswaRouter.put("/laporan/{id_laporan}",response_model=ApiResponse[LaporanSiswaBase],tags=["SISWA/LAPORAN"])
async def updateLaporan(id_laporan : int,laporan : UpdateLaporanSiswaRequest | dict = UpdateLaporanSiswaRequest(),siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.updateLaporan(siswa["id"],id_laporan,laporan,session)

@siswaRouter.get("/laporan",response_model=ApiResponse[list[LaporanSiswaBase]],tags=["SISWA/LAPORAN"])
async def getAllLaporan(query : FilterQueryLaporan = Depends(),siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await laporanService.getAllLaporan(siswa,query,session)

@siswaRouter.get("/laporan/{id_laporan}",response_model=ApiResponse[LaporanSiswaDetail],tags=["SISWA/LAPORAN"])
async def getLaporanById(id_laporan : int,session : sessionDepedency = None) :
    return await laporanService.getLaporanById(id_laporan,session)

# absen
@siswaRouter.get("/absen/rekap-mingguan",response_model=ApiResponse[RekapAbsenMingguanResponse],tags=["SISWA/ABSEN"])
async def getRekapAbsenMingguan(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await absenService.getRekapAbsenMingguan(siswa,session)

@siswaRouter.get("/absen/cekAbsen",response_model=ApiResponse[CekAbsenSiswaTodayResponse],tags=["SISWA/ABSEN"])
async def cekAbsenToday(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await absenService.cekAbsenSiswaToday(siswa,session)

@siswaRouter.post("/absen",response_model=ApiResponse[AbsenWithDetail],tags=["SISWA/ABSEN"])
async def absen(body : AbsenSiswaRequest = Depends(AbsenSiswaRequest.as_form),siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await absenService.absenSiswa(siswa,body,session)