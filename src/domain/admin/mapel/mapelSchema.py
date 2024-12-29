from pydantic import BaseModel

class AddMapelRequest(BaseModel) :
    nama : str
    id_tahun : int

class UpdateMapelRequest(BaseModel) :
    nama : str | None = None
    id_tahun : int | None = None