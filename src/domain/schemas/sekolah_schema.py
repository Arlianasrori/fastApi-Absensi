from pydantic import BaseModel,EmailStr

from .alamat_schema import AlamatBase

class AlamatSekolah(AlamatBase) :
    id_sekolah : int

class SekolahBase(BaseModel) :
    id : int
    npsn : str
    nama : str
    logo : str | None

class SekolahWithAlamat(SekolahBase) :
    alamat : AlamatSekolah

class AdminBase(BaseModel) :
    id : int
    username : str
    no_telepon : str
    email : EmailStr
    id_sekolah : int

class kepalaSekolahBase(BaseModel) :
    nama : str
    nip : str

class SekolahDetail(SekolahBase) :
    admin : list[AdminBase] = []
    alamat : AlamatSekolah | None = None
    kepala_sekolah : kepalaSekolahBase | None = None

class AdminWithSekolah(AdminBase) :
    sekolah : SekolahBase

class TahunSekolahBase(BaseModel) :
    id : int
    tahun : str
    id_sekolah : int

