from pydantic import BaseModel

class FileLaporanBase(BaseModel):
    id : int
    file : str