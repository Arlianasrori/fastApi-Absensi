from fastapi import APIRouter,Depends

# auth-profile
from ..domain.siswa.auth_profile import authProfileService
from ..domain.schemas.siswa_schema import SiswaBase, SiswaDetailWithSekolah

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

# absen
from ..domain.siswa.absen import absenService
from ..domain.siswa.absen.absenSchema import RekapAbsenMingguanResponse, CekAbsenSiswaTodayResponse, AbsenSiswaRequest, GetDetailAbsenSiswaResponse, GetAllLaporanAbsenSiswaResponse
from ..domain.schemas.absen_schema import AbsenWithDetail

# common
from ..domain.schemas.response_schema import ApiResponse
from ..db.sessionDepedency import sessionDepedency
from datetime import date
siswaRouter = APIRouter(prefix="/siswa",dependencies=[Depends(siswaDependAuth)])

# auth-profile
@siswaRouter.get("/",response_model=ApiResponse[SiswaBase],tags=["SISWA/AUTH-PROFILE"])
async def getSiswa(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.getSiswa(siswa["id"],session)

@siswaRouter.get("/profile",response_model=ApiResponse[SiswaDetailWithSekolah],tags=["SISWA/AUTH-PROFILE"])
async def getProfileSiswa(siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await authProfileService.getProfile(siswa["id"],session)

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

@siswaRouter.get("/absen/laporan",response_model=ApiResponse[dict[date,list[GetAllLaporanAbsenSiswaResponse]]],tags=["SISWA/ABSEN"])
async def getAllLaporanAbsen(month : int,year : int,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await absenService.getAllLaporanAbsenSiswa(siswa,month,year,session)

@siswaRouter.get("/absen/detail/{id_absen}",response_model=ApiResponse[GetDetailAbsenSiswaResponse],tags=["SISWA/ABSEN"])
async def getDetailAbsen(id_absen : int,siswa : dict = Depends(getSiswaAuth),session : sessionDepedency = None) :
    return await absenService.getDetailAbsenSiswa(siswa,id_absen,session)