from pydantic import BaseModel

class CekRadiusKoordinatRequest(BaseModel) :
    latitude : float
    longitude : float

class CekRadiusKoordinatResponse(BaseModel) :
    insideRadius : bool