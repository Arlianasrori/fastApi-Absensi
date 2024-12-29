from pydantic import BaseModel

class MapelBase(BaseModel) :
    id : int
    nama : str
    id_sekolah : int
    id_tahun : int