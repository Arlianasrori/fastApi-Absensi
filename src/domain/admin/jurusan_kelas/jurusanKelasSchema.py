from pydantic import BaseModel

class AddJurusanRequest(BaseModel) :
    nama : str
    id_tahun : int

class UpdateJurusanRequest(BaseModel) :
    nama : str | None = None

class AddKelasRequest(BaseModel) :
    nama : str
    id_jurusan : int

class UpdateKelasRequest(BaseModel) :
    nama : str | None = None
    id_jurusan : int | None = None