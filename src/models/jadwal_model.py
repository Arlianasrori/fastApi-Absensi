from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Enum, Time
import enum
from sqlalchemy.orm import relationship
from ..db.db import Base

class HariEnum(enum.Enum):
    senin = "senin"
    selasa = "selasa"
    rabu = "rabu"
    kamis = "kamis"
    jumat = "jumat"
    sabtu = "sabtu"
    minggu = "minggu"

class Mapel(Base):
    __tablename__ = 'mapel'

    id = Column(Integer, primary_key=True)
    nama = Column(String(255), nullable=False)
    id_sekolah = Column(Integer, ForeignKey('sekolah.id'), nullable=False)
    id_tahun = Column(Integer, ForeignKey('tahun_sekolah.id'), nullable=False)

    sekolah = relationship("Sekolah", back_populates="mapel")
    tahun = relationship("TahunSekolah", back_populates="mapel")
    jadwal = relationship("Jadwal", back_populates="mapel")
    guru_mapel = relationship("GuruMapel", back_populates="mapel")

    __table_args__ = (UniqueConstraint('nama', 'id_sekolah', 'id_tahun', name='_mapel_sekolah_tahun_uc'),)
    
    def __repr__(self):
        return f"<Mapel(id={self.id} , nama='{self.nama}')>"

class Jadwal(Base):
    __tablename__ = 'jadwal'

    id = Column(Integer, primary_key=True)
    id_mapel = Column(Integer, ForeignKey('mapel.id'), nullable=False)
    id_guru_mapel = Column(Integer, ForeignKey('guru_mapel.id'), nullable=False)
    id_kelas = Column(Integer, ForeignKey('kelas.id'), nullable=False)
    id_tahun = Column(Integer, ForeignKey('tahun_sekolah.id'), nullable=False)
    id_sekolah = Column(Integer, ForeignKey('sekolah.id'), nullable=False)
    hari = Column(Enum(HariEnum), nullable=False)
    jam_mulai = Column(Time, nullable=False)
    jam_selesai = Column(Time, nullable=False)

    mapel = relationship("Mapel", back_populates="jadwal")
    guru_mapel = relationship("GuruMapel", back_populates="jadwal")
    kelas = relationship("Kelas", back_populates="jadwal")
    tahun = relationship("TahunSekolah", back_populates="jadwal")
    sekolah = relationship("Sekolah", back_populates="jadwal")
    absen = relationship("Absen", back_populates="jadwal")  

    def __repr__(self):
        return f"<Jadwal(id={self.id} , mapel='{self.mapel}', kelas='{self.kelas}', tahun='{self.tahun}')>"