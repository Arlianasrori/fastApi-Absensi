from fastapi import APIRouter, Depends, UploadFile
# models

# auth profile
from ..domain.admin.auth_profile import authProfileService
from ..domain.schemas.sekolah_schema import AdminWithSekolah,AdminBase

# jurusan dan kelas
from ..domain.admin.jurusan_kelas.jurusanKelasSchema import AddJurusanRequest, UpdateJurusanRequest,AddKelasRequest,UpdateKelasRequest
from ..domain.schemas.kelasJurusan_schema import JurusanBase,JurusanWithKelas,KelasBase,KelasWithJurusan
from ..domain.admin.jurusan_kelas import jurusanKelasService

# tahun sekolah
from ..domain.admin.tahun_sekolah.tahunSekolahSchema import AddTahunSekolahRequest,UpdateTahunSekolahRequest
from ..domain.admin.tahun_sekolah import tahunSekolahService
from ..domain.schemas.sekolah_schema import TahunSekolahBase

# alamat
from ..domain.schemas.alamat_schema import AlamatBody,UpdateAlamatBody

# siswa
from ..domain.admin.siswa.siswaSchema import AddSiswaRequest,UpdateSiswaRequest,ResponseSiswaPag
from ..domain.admin.siswa import siswaService
from ..domain.schemas.siswa_schema import SiswaBase,SiswaWithJurusanKelasAlamat

# mapel
from ..domain.admin.mapel import mapelService
from ..domain.admin.mapel.mapelSchema import AddMapelRequest,UpdateMapelRequest
from ..domain.schemas.mapel_schema import MapelBase

# guru mapel
from ..domain.admin.guru_mapel import guruMapelService
from ..domain.schemas.guruMapel_schema import GuruMapelBase,GuruMapeldetail
from ..domain.admin.guru_mapel.guruMapelSchema import AddGuruMapelRequest,UpdateGuruMapelRequest,ResponseGuruMapelPag

# guru walas
from ..domain.admin.guru_walas import guruWalasService
from ..domain.schemas.guruWalas_schema import GuruWalasBase,GuruWalasDetail
from ..domain.admin.guru_walas.guruWalasSchema import AddGuruWalasRequest,UpdateGuruWalasRequest,ResponseGuruWalasPag

# petugas BK
from ..domain.admin.petugas_BK import petugasBKService
from ..domain.schemas.petugasBK_schema import PetugasBkBase,PetugasBKWithAlamatAndDistribusi
from ..domain.admin.petugas_BK.petugasBkSchema import AddPetugasBKRequest,UpdatePetugasBKRequest,ResponsePetugasBKPag,AddDistribusiPetugasBKRequest

# jadwal
from ..domain.admin.jadwal import jadwalService
from ..domain.schemas.jadwal_schema import JadwalBase,JadwalDetail
from ..domain.admin.jadwal.jadwalSchema import AddJadwalRequest,UpdateJadwalRequest,ResponseJadwalPag,FilterJadwalQuery

# absen
from ..domain.admin.absen import absenService
from ..domain.admin.absen.absenSchema import FilterAbsenQuery,ResponseAbsenPag
from ..domain.schemas.absen_schema import AbsenWithSiswaDetail

# koodinat absen
from ..domain.admin.koordinat_absen_kelas import koordinatAbsenKelasService
from ..domain.admin.koordinat_absen_kelas.koordinatAbsenKelasSchema import FilterKoordinatAbsenKelasQuery,ResponseKoordinatAbsenKelasPag,AddKoordinatAbsenKelasRequest,UpdateKoordinatAbsenKelasRequest
from ..domain.schemas.koordinatAbsen_schema import KoordinatAbsenKelasBase

# auth depends
from ..auth.auth_depends.admin.depend_auth_admin import adminAuth
from ..auth.auth_depends.admin.get_admin_auth import getAdminAuth

# common
from ..domain.schemas.response_schema import ApiResponse, MessageOnlyResponse
from ..db.sessionDepedency import sessionDepedency

adminRouter = APIRouter(prefix="/admin",dependencies=[Depends(adminAuth)])

# authProfile
@adminRouter.get("",response_model=ApiResponse[AdminBase],tags=["ADMIN/AUTH PROFILE"])
async def getAdmin(admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await authProfileService.getAdmin(admin["id"],session)

@adminRouter.get("/profile",response_model=ApiResponse[AdminWithSekolah],tags=["ADMIN/AUTH PROFILE"])
async def getProfileAdmin(admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await authProfileService.getProfile(admin["id"],session)

# tahun sekolah

@adminRouter.post("/tahun-sekolah",response_model=ApiResponse[TahunSekolahBase],tags=["ADMIN/TAHUN SEKOLAH"])
async def addTahunSekolah(tahun : AddTahunSekolahRequest,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await tahunSekolahService.addTahunSekolah(admin["id_sekolah"],tahun,session)

@adminRouter.get("/tahun-sekolah",response_model=ApiResponse[list[TahunSekolahBase]],tags=["ADMIN/TAHUN SEKOLAH"])
async def getAllTahunSekolah(admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await tahunSekolahService.getAllTahunSekolah(admin["id_sekolah"],session)

@adminRouter.put("/tahun-sekolah/{id_tahun}",response_model=ApiResponse[TahunSekolahBase],tags=["ADMIN/TAHUN SEKOLAH"])
async def updateTahunSekolah(id_tahun : int,tahun : UpdateTahunSekolahRequest | None = UpdateTahunSekolahRequest(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await tahunSekolahService.updateTahunSekolah(admin["id_sekolah"],id_tahun,tahun,session)

@adminRouter.delete("/tahun-sekolah/{id_tahun}",response_model=ApiResponse[TahunSekolahBase],tags=["ADMIN/TAHUN SEKOLAH"])
async def deleteTahunSekolah(id_tahun : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await tahunSekolahService.deleteTahunSekolah(admin["id_sekolah"],id_tahun,session)


# jurusan

@adminRouter.post("/jurusan",response_model=ApiResponse[JurusanBase],tags=["ADMIN/JURUSAN"])
async def addJurusan(jurusan : AddJurusanRequest,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) -> JurusanBase :
    print("tes")
    return await jurusanKelasService.addJurusan(admin["id_sekolah"],jurusan,session)

@adminRouter.get("/jurusan",response_model=ApiResponse[list[JurusanBase]],tags=["ADMIN/JURUSAN"])
async def getAllJurusan(id_tahun : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jurusanKelasService.getAllJurusan(admin["id_sekolah"],id_tahun,session)

@adminRouter.get("/jurusan/{id}",response_model=ApiResponse[JurusanWithKelas],tags=["ADMIN/JURUSAN"])
async def getJurusanById(id : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jurusanKelasService.getJurusanById(id,admin["id_sekolah"],session)

@adminRouter.put("/jurusan/{id}",response_model=ApiResponse[JurusanBase],tags=["ADMIN/JURUSAN"])
async def updateJurusan(id : int,jurusan : UpdateJurusanRequest | None = UpdateJurusanRequest(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jurusanKelasService.updateJurusan(id,jurusan,admin["id_sekolah"],session)

@adminRouter.delete("/jurusan/{id}",response_model=ApiResponse[JurusanBase],tags=["ADMIN/JURUSAN"])
async def deleteJurusan(id : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jurusanKelasService.deleteJurusan(id,admin["id_sekolah"],session)

# kelas
@adminRouter.post("/kelas",response_model=ApiResponse[KelasBase],tags=["ADMIN/KELAS"])
async def addKelas(kelas : AddKelasRequest,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jurusanKelasService.addKelas(admin["id_sekolah"],kelas,session)

@adminRouter.get("/kelas",response_model=ApiResponse[list[KelasBase]],tags=["ADMIN/KELAS"])
async def getAllKelas(id_tahun : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jurusanKelasService.getAllKelas(admin["id_sekolah"],id_tahun,session)

@adminRouter.get("/kelas/{id}",response_model=ApiResponse[KelasWithJurusan],tags=["ADMIN/KELAS"])
async def getKelasById(id : int,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await jurusanKelasService.getKelasById(id,admin["id_sekolah"],session)

@adminRouter.put("/kelas/{id}",response_model=ApiResponse[KelasBase],tags=["ADMIN/KELAS"])
async def updateKelas(id : int,kelas : UpdateKelasRequest | None = UpdateKelasRequest(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jurusanKelasService.updateKelas(id,admin["id_sekolah"],kelas,session)

@adminRouter.delete("/kelas/{id}",response_model=ApiResponse[KelasBase],tags=["ADMIN/KELAS"])
async def deleteKelas(id : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jurusanKelasService.deleteKelas(id,admin["id_sekolah"],session)


# siswa
@adminRouter.post("/siswa",response_model=ApiResponse[SiswaWithJurusanKelasAlamat],tags=["ADMIN/SISWA"])
async def addSiswa(siswa : AddSiswaRequest,alamat : AlamatBody,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await siswaService.addSiswa(admin["id_sekolah"],siswa,alamat,session)

@adminRouter.patch("/siswa/foto_profile/{id_siswa}",response_model=ApiResponse[SiswaBase],tags=["ADMIN/SISWA"])
async def add_update_profile(id_siswa : int,foto_profile : UploadFile,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await siswaService.add_update_foto_profile(id_siswa,admin["id_sekolah"],foto_profile,session)

@adminRouter.get("/siswa",response_model=ApiResponse[list[SiswaWithJurusanKelasAlamat] | ResponseSiswaPag],tags=["ADMIN/SISWA"])
async def getAllSiswa(id_tahun : int,page : int | None = None,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await siswaService.getAllSiswa(page,admin["id_sekolah"],id_tahun,session)

@adminRouter.get("/siswa/{id_siswa}",response_model=ApiResponse[SiswaWithJurusanKelasAlamat],tags=["ADMIN/SISWA"])
async def getSiswaById(id_siswa : int,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await siswaService.getSiswaById(id_siswa,admin["id_sekolah"],session)

@adminRouter.put("/siswa/{id_siswa}",response_model=ApiResponse[SiswaWithJurusanKelasAlamat],tags=["ADMIN/SISWA"])
async def updateSiswa(id_siswa : int,siswa : UpdateSiswaRequest | None = UpdateSiswaRequest(),alamat : UpdateAlamatBody | None = UpdateAlamatBody(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await siswaService.updateSiswa(id_siswa,admin["id_sekolah"],siswa,alamat,session)

@adminRouter.delete("/siswa/{id_siswa}",response_model=ApiResponse[SiswaBase],tags=["ADMIN/SISWA"])
async def deleteSiswa(id_siswa : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await siswaService.deleteSiswa(id_siswa,admin["id_sekolah"],session)


# mapel

@adminRouter.post("/mapel",response_model=ApiResponse[MapelBase],tags=["ADMIN/MAPEL"])
async def addMapel(mapel : AddMapelRequest,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await mapelService.addMapel(admin["id_sekolah"],mapel,session)

@adminRouter.get("/mapel",response_model=ApiResponse[list[MapelBase]],tags=["ADMIN/MAPEL"])
async def getAllMapel(id_tahun : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await mapelService.getAllMapel(admin["id_sekolah"],id_tahun,session)

@adminRouter.put("/mapel/{id_mapel}",response_model=ApiResponse[MapelBase],tags=["ADMIN/MAPEL"])
async def updateMapel(id_mapel : int,mapel : UpdateMapelRequest | None = UpdateMapelRequest(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await mapelService.updateMapel(admin["id_sekolah"],id_mapel,mapel,session)

@adminRouter.delete("/mapel/{id_mapel}",response_model=ApiResponse[MapelBase],tags=["ADMIN/MAPEL"])
async def deleteMapel(id_mapel : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await mapelService.deleteMapel(admin["id_sekolah"],id_mapel,session)


# guru mapel

@adminRouter.post("/guru-mapel",response_model=ApiResponse[GuruMapeldetail],tags=["ADMIN/GURU MAPEL"])
async def addGuruMapel(guruMapel : AddGuruMapelRequest,alamat : AlamatBody,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await guruMapelService.addGuruMapel(admin["id_sekolah"],guruMapel,alamat,session)

@adminRouter.patch("/guru-mapel/foto_profile/{id_guru}",response_model=ApiResponse[GuruMapelBase],tags=["ADMIN/GURU MAPEL"])
async def add_update_profile(id_guru : int,foto_profile : UploadFile,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await guruMapelService.add_update_foto_profile(id_guru,admin["id_sekolah"],foto_profile,session)

@adminRouter.get("/guru-mapel",response_model=ApiResponse[list[GuruMapeldetail] | ResponseGuruMapelPag],tags=["ADMIN/GURU MAPEL"])
async def getAllGurumapel(id_tahun : int,page : int | None = None,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await guruMapelService.getAllGuruMapel(page,admin["id_sekolah"],id_tahun,session)

@adminRouter.get("/guru-mapel/{id}",response_model=ApiResponse[GuruMapeldetail],tags=["ADMIN/GURU MAPEL"])
async def getGurumapelById(id : int,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await guruMapelService.getGuruMapelId(id,admin["id_sekolah"],session)

@adminRouter.put("/guru-mapel/{id}",response_model=ApiResponse[GuruMapeldetail],tags=["ADMIN/GURU MAPEL"])
async def updateGurumapel(id : int,guruMapel : UpdateGuruMapelRequest | None = UpdateGuruMapelRequest(),alamat : UpdateAlamatBody | None = UpdateAlamatBody(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await guruMapelService.updateGuruMapel(id,admin["id_sekolah"],guruMapel,alamat,session)

@adminRouter.delete("/guru-mapel/{id}",response_model=ApiResponse[GuruMapelBase],tags=["ADMIN/GURU MAPEL"])
async def deleteGuruMapel(id : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await guruMapelService.deleteGuruMapel(id,admin["id_sekolah"],session)


# guru walas

@adminRouter.post("/guru-walas",response_model=ApiResponse[GuruWalasBase],tags=["ADMIN/GURU WALAS"])
async def addGuruWalas(guruWalas : AddGuruWalasRequest,alamat : AlamatBody,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await guruWalasService.AddGuruWalas(admin["id_sekolah"],guruWalas,alamat,session)

@adminRouter.patch("/guru-walas/foto_profile/{id_guru}",response_model=ApiResponse[GuruWalasBase],tags=["ADMIN/GURU WALAS"])
async def add_update_profile(id_guru : int,foto_profile : UploadFile,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await guruWalasService.add_update_foto_profile(id_guru,admin["id_sekolah"],foto_profile,session)

@adminRouter.get("/guru-walas",response_model=ApiResponse[list[GuruWalasDetail] | ResponseGuruWalasPag],tags=["ADMIN/GURU WALAS"])
async def getAllGuruWalas(id_tahun : int,page : int | None = None,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await guruWalasService.getAllGuruWalas(page,admin["id_sekolah"],id_tahun,session)

@adminRouter.get("/guru-walas/{id}",response_model=ApiResponse[GuruWalasDetail],tags=["ADMIN/GURU WALAS"])
async def getGuruWalasById(id : int,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await guruWalasService.getGuruWalasId(id,admin["id_sekolah"],session)

@adminRouter.put("/guru-walas/{id}",response_model=ApiResponse[GuruWalasDetail],tags=["ADMIN/GURU WALAS"])
async def updateGuruWalas(id : int,guruWalas : UpdateGuruWalasRequest | None = UpdateGuruWalasRequest(),alamat : UpdateAlamatBody | None = UpdateAlamatBody(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await guruWalasService.updateGuruWalas(id,admin["id_sekolah"],guruWalas,alamat,session)

@adminRouter.delete("/guru-walas/{id}",response_model=ApiResponse[GuruWalasBase],tags=["ADMIN/GURU WALAS"])
async def deleteGuruWalas(id : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await guruWalasService.deleteGuruWalas(id,admin["id_sekolah"],session)


# petugas BK

@adminRouter.post("/petugasBK",response_model=ApiResponse[PetugasBKWithAlamatAndDistribusi],tags=["ADMIN/PETUGAS BK"])
async def addPetugasBK(petugasBK : AddPetugasBKRequest,alamat : AlamatBody,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await petugasBKService.AddPetugasBK(admin["id_sekolah"],petugasBK,alamat,session)

@adminRouter.patch("/petugasBK/foto_profile/{id_petugasBK}",response_model=ApiResponse[PetugasBkBase],tags=["ADMIN/PETUGAS BK"])
async def add_update_profile(id_petugasBK : int,foto_profile : UploadFile,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await petugasBKService.add_update_foto_profile(id_petugasBK,admin["id_sekolah"],foto_profile,session)

@adminRouter.get("/petugasBK",response_model=ApiResponse[list[PetugasBKWithAlamatAndDistribusi] | ResponsePetugasBKPag],tags=["ADMIN/PETUGAS BK"])
async def getAllPetugasBK(id_tahun : int,page : int | None = None,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await petugasBKService.getAllPetugasBK(page,admin["id_sekolah"],id_tahun,session)

@adminRouter.get("/petugasBK/{id_petugasBK}",response_model=ApiResponse[PetugasBKWithAlamatAndDistribusi],tags=["ADMIN/PETUGAS BK"])
async def getPetugasBKById(id_petugasBK : int,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await petugasBKService.getPetugasBKId(id_petugasBK,admin["id_sekolah"],session)

@adminRouter.put("/petugasBK/{id_petugasBK}",response_model=ApiResponse[PetugasBKWithAlamatAndDistribusi],tags=["ADMIN/PETUGAS BK"])
async def updatePetugasBK(id_petugasBK : int,petugasBK : UpdatePetugasBKRequest | None = UpdatePetugasBKRequest(),alamat : UpdateAlamatBody | None = UpdateAlamatBody(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await petugasBKService.updatePetugasBK(id_petugasBK,admin["id_sekolah"],petugasBK,alamat,session)

@adminRouter.delete("/petugasBK/{id_petugasBK}",response_model=ApiResponse[PetugasBkBase],tags=["ADMIN/PETUGAS BK"])
async def deletePetugasBK(id_petugasBK : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await petugasBKService.deletePetugasBK(id_petugasBK,admin["id_sekolah"],session)

@adminRouter.post("/petugasBk/distribusi/{id_petugasBK}",response_model=MessageOnlyResponse,tags=["ADMIN/PETUGAS BK"])
async def addPetugasBKDistribusi(id_petugasBK : int,id_tahun : int,distribusi : AddDistribusiPetugasBKRequest,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await petugasBKService.addDistribusiPetugasBK(id_petugasBK,admin["id_sekolah"],id_tahun,distribusi,session)

@adminRouter.delete("/petugasBK/distribusi/{id_distribusi}",response_model=MessageOnlyResponse,tags=["ADMIN/PETUGAS BK"])
async def deletePetugasBKDistribusi(id_distribusi : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await petugasBKService.deleteDistribusiPetugasBK(id_distribusi,admin["id_sekolah"],session)

# jadwal

@adminRouter.post("/jadwal",response_model=ApiResponse[JadwalDetail],tags=["ADMIN/JADWAL"])
async def addJadwal(id_tahun : int, jadwal : AddJadwalRequest,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jadwalService.addJadwal(admin["id_sekolah"],id_tahun,jadwal,session)

@adminRouter.get("/jadwal",response_model=ApiResponse[list[JadwalDetail] | ResponseJadwalPag],tags=["ADMIN/JADWAL"])
async def getAllJadwal(id_tahun : int,page : int | None = None,query : FilterJadwalQuery = Depends(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jadwalService.getAllJadwal(page,admin["id_sekolah"],id_tahun,query,session)

@adminRouter.get("/jadwal/{id}",response_model=ApiResponse[JadwalDetail],tags=["ADMIN/JADWAL"])
async def getJadwalById(id : int,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await jadwalService.getJadwalId(id,admin["id_sekolah"],session)

@adminRouter.put("/jadwal/{id}",response_model=ApiResponse[JadwalDetail],tags=["ADMIN/JADWAL"])
async def updateJadwal(id : int,id_tahun : int,jadwal : UpdateJadwalRequest | None = UpdateJadwalRequest(),admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jadwalService.updateJadwal(id,admin["id_sekolah"],id_tahun,jadwal,session)

@adminRouter.delete("/jadwal/{id}",response_model=ApiResponse[JadwalBase],tags=["ADMIN/JADWAL"])
async def deleteJadwal(id : int,admin : dict = Depends(getAdminAuth), session : sessionDepedency = None) :
    return await jadwalService.deleteJadwal(id,admin["id_sekolah"],session)

# absen
@adminRouter.get("/absen",response_model=ApiResponse[list[AbsenWithSiswaDetail] | ResponseAbsenPag],tags=["ADMIN/ABSEN"])
async def getAllAbsen(id_tahun : int,page : int | None = None,admin : dict = Depends(getAdminAuth),query : FilterAbsenQuery = Depends(), session : sessionDepedency = None) :
    return await absenService.getAllAbsen(page,admin["id_sekolah"],id_tahun,query,session)

@adminRouter.get("/absen/{id}",response_model=ApiResponse[AbsenWithSiswaDetail],tags=["ADMIN/ABSEN"])
async def getAbsenById(id : int,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await absenService.getAbsenById(id,admin["id_sekolah"],session)


# koordinat absen kelas
@adminRouter.get("/koordinatAbsenKelas",response_model=ApiResponse[list[KoordinatAbsenKelasBase] | ResponseKoordinatAbsenKelasPag],tags=["ADMIN/KOORDINAt ABSEN KELAS"])
async def getAllKoordinatAbsen(id_tahun : int,page : int | None = None,admin : dict = Depends(getAdminAuth),query : FilterKoordinatAbsenKelasQuery = Depends(), session : sessionDepedency = None) :
    return await koordinatAbsenKelasService.getAllKoordinatAbsen(page,admin["id_sekolah"],id_tahun,query,session)

@adminRouter.get("/koordinatAbsenKelas/{id}",response_model=ApiResponse[KoordinatAbsenKelasBase],tags=["ADMIN/KOORDINAt ABSEN KELAS"])
async def getKoordinatById(id : int,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await koordinatAbsenKelasService.getKoordinatById(id,admin["id_sekolah"],session)

@adminRouter.post("/koordinatAbsenKelas",response_model=ApiResponse[KoordinatAbsenKelasBase],tags=["ADMIN/KOORDINAt ABSEN KELAS"])
async def addKoordinatAbsenKelas(koordinat : AddKoordinatAbsenKelasRequest,admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await koordinatAbsenKelasService.addKoordinatAbsenKelas(admin["id_sekolah"],koordinat,session)

@adminRouter.put("/koordinatAbsenKelas/{id_koordinat}",response_model=ApiResponse[KoordinatAbsenKelasBase],tags=["ADMIN/KOORDINAt ABSEN KELAS"])
async def updateKoordinatAbsenKelas(id_koordinat : int,koordinat : UpdateKoordinatAbsenKelasRequest = UpdateKoordinatAbsenKelasRequest(),admin : dict = Depends(getAdminAuth),session : sessionDepedency = None) :
    return await koordinatAbsenKelasService.updateKoordinatAbsenKelas(id_koordinat,admin["id_sekolah"],koordinat,session)