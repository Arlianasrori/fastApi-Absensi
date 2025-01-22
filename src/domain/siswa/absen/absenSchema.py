from pydantic import BaseModel
from ....models.jadwal_model import HariEnum
from enum import Enum
from fastapi import Form, File, UploadFile
from ....models.absen_model import StatusAbsenEnum
from typing import Optional

class StatusRekapAbsenMIngguanEnum(Enum) :
    HADIR = "hadir"
    IZIN = "izin"
    SAKIT = "sakit"
    ALPA = "alpa"
    LIBUR = "libur"


class ProgressAbsenMingguanRespose(BaseModel) :
    hari : HariEnum
    status : StatusRekapAbsenMIngguanEnum

class RekapAbsenMingguanResponse(BaseModel) :
    progress : list[ProgressAbsenMingguanRespose]
    total_hadir : int
    total_izin_sakit_dispensasi : int

class CekAbsenSiswaTodayResponse(BaseModel) :
    avaliableAbsen : bool

class AbsenSiswaRequest(BaseModel) :
    status : StatusAbsenEnum
    catatan : str | None = None
    dokumenFile : UploadFile
    latitude : float
    longitude : float

    @classmethod
    def as_form(
        cls,
        status: StatusAbsenEnum = Form(...),
        catatan: Optional[str] = Form(None),
        dokumenFile: UploadFile = File(...),
        latitude: float = Form(...),
        longitude: float = Form(...)
    ):
        return cls(
            status=status,
            catatan=catatan,
            dokumenFile=dokumenFile,
            latitude=latitude,
            longitude=longitude
        )
