from pydantic import BaseModel

class AddTahunSekolahRequest(BaseModel) :
    tahun : str

class UpdateTahunSekolahRequest(BaseModel) :
    tahun : str | None = None