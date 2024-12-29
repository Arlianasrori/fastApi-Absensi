from pydantic import BaseModel

class AlamatBody(BaseModel) :
    detail_tempat : str
    desa : str
    kecamatan : str
    kabupaten : str
    provinsi : str
    negara : str

class AlamatBase(BaseModel) :
    detail_tempat : str
    desa : str
    kecamatan : str
    kabupaten : str
    provinsi : str
    negara : str

class UpdateAlamatBody(BaseModel) :
    detail_tempat : str | None = None
    desa : str | None = None        
    kecamatan : str | None = None
    kabupaten : str | None = None       
    provinsi : str | None = None
    negara : str | None = None