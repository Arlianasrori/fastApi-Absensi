from pydantic import BaseModel
from datetime import datetime
from typing import Union

class FilterQuery(BaseModel) :
    month : int | None = None
    year : int | None = None

class AddLaporanSiswaRequest(BaseModel) :
    catatan : str 

class UpdateLaporanSiswaRequest(BaseModel) :
    catatan : str  | None = None