from pydantic import BaseModel

class JurusanBase(BaseModel):
    id : int
    nama : str  
    id_sekolah : int
    id_tahun : int

class KelasBase(BaseModel) :
    id : int
    nama : str
    id_jurusan : int

class JurusanWithKelas(JurusanBase) :
    kelas : list[KelasBase] = []

class KelasWithJurusan(KelasBase) :
    jurusan : JurusanBase
