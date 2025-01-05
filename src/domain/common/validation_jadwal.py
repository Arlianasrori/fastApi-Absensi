from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,and_

from ...models.jadwal_model import Jadwal,HariEnum
from datetime import time
from ...error.errorHandling import HttpException

async def validateJadwal(id_jadwal : int, jam_mulai : time,jam_selesai : time,id_kelas : int,hari : HariEnum, id_sekolah : int,id_tahun : int,session : AsyncSession) -> None:
    if jam_mulai >= jam_selesai :
        raise HttpException(400,f"Jam mulai tidak boleh lebih besar atau sama dengan jam selesai")
    
    findJadwal = (await session.execute(select(Jadwal).where(and_(Jadwal.id_kelas == id_kelas,Jadwal.id_sekolah == id_sekolah,Jadwal.id_tahun == id_tahun,Jadwal.hari == hari)).where(Jadwal.id != id_jadwal))).scalars().all()

    if findJadwal :
        jam_mulai = jam_mulai.replace(tzinfo=None)
        jam_selesai = jam_selesai.replace(tzinfo=None)

        for jadwalItem in findJadwal :
            print(jam_mulai,jam_selesai)
            print(jadwalItem.jam_mulai,jadwalItem.jam_selesai)
            if jam_mulai >= jadwalItem.jam_mulai and jam_mulai <= jadwalItem.jam_selesai :
                raise HttpException(400,f"Jadwal di hari {hari.value} pada jam {jam_mulai} - {jam_selesai} sudah ditambahkan")
            elif jam_selesai >= jadwalItem.jam_mulai and jam_selesai <= jadwalItem.jam_selesai :
                raise HttpException(400,f"Jadwal di hari {hari.value} pada jam {jam_mulai} - {jam_selesai} sudah ditambahkan")
