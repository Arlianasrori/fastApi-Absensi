from sqlalchemy import Column, Integer, String, ForeignKey, Date,Time, Enum, Float, Boolean
from sqlalchemy.orm import relationship
from ..db.db import Base
import enum

class StatusAbsenEnum(enum.Enum):
    izin = "izin"
    hadir = "hadir"
    izin_telat = "izin_telat"
    telat = "telat"
    sakit = "sakit"
    dispen = "dispen"

class StatusTinjauanEnum(enum.Enum) :
    diterima = "diterima"
    ditolak = "ditolak"
    belum_ditinjau = "belum_ditinjau"

class KoordinatAbsenKelas(Base) :
    __tablename__ = 'koordinat_absen_kelas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_kelas = Column(Integer, ForeignKey('kelas.id'))
    nama_tempat = Column(String(255),nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    radius_absen_meter = Column(Float)

    kelas = relationship("Kelas", back_populates="koordinat_absen")
    jadwal = relationship("Jadwal", back_populates="koordinat")

class Absen(Base):
    __tablename__ = 'absen'

    id = Column(Integer, primary_key=True)
    id_jadwal = Column(Integer, ForeignKey('jadwal.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_siswa = Column(Integer, ForeignKey('siswa.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tanggal = Column(Date, nullable=False)
    jam = Column(Time, nullable=False)
    file = Column(String, nullable=False)
    status = Column(Enum(StatusAbsenEnum), nullable=False)

    jadwal = relationship("Jadwal", back_populates="absen")
    siswa = relationship("Siswa", back_populates="absen")
    detail = relationship("AbsenDetail",uselist=False, back_populates="absen")
    
    def __repr__(self):
        return f"<Absen(id={self.id}, id_jadwal='{self.id_jadwal}', id_siswa='{self.id_siswa}', tanggal='{self.tanggal}', jam='{self.jam}', file='{self.file}')>"

class AbsenDetail(Base):
    __tablename__ = 'absen_detail'

    id = Column(Integer, primary_key=True)
    id_absen = Column(Integer, ForeignKey('absen.id'), nullable=False)
    catatan = Column(String, nullable=False)
    diterima = Column(Enum(StatusTinjauanEnum),nullable=True, default=StatusTinjauanEnum.belum_ditinjau.value)
    id_peninjau = Column(Integer, ForeignKey('petugas_BK.id'), nullable=True)
    tanggal_peninjau = Column(Date, nullable=True)

    absen = relationship("Absen", back_populates="detail")
    petugas_bk = relationship("PetugasBK", back_populates="absen_detail")

    def __repr__(self):
        return f"<AbsenDetail(id={self.id}, id_absen='{self.id_absen}', catatan='{self.catatan}')>"