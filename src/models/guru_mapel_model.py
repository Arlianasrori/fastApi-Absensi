from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from ..db.db import Base
from ..types.user_types import GenderType

class GuruMapel(Base):
    __tablename__ = 'guru_mapel'

    id = Column(Integer, primary_key=True)
    nip = Column(String, nullable=False)
    nama = Column(String(255), nullable=False)
    no_telepon = Column(String(12), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    jenis_kelamin = Column(Enum(GenderType), nullable=False)
    tempat_lahir = Column(String(255), nullable=False)
    tanggal_lahir = Column(Date, nullable=False)
    agama = Column(String(255), nullable=False)
    foto_profile = Column(String, nullable=True)
    token_FCM = Column(String, nullable=True)
    password = Column(String(255), nullable=False)
    id_sekolah = Column(Integer, ForeignKey('sekolah.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_tahun = Column(Integer, ForeignKey('tahun_sekolah.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_mapel = Column(Integer, ForeignKey('mapel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    OTP_code = Column(Integer, nullable=True)

    # Relasi yang sudah ada
    alamat = relationship("AlamatGuruMapel", uselist=False, back_populates="guru_mapel", cascade="all")
    notifications = relationship("Notification", back_populates="guru_mapel")
    notification_reads = relationship("NotificationRead", back_populates="guru_mapel")
    sekolah = relationship("Sekolah", back_populates="guru_mapel")
    tahun = relationship("TahunSekolah", back_populates="guru_mapel")
    mapel = relationship("Mapel", back_populates="guru_mapel")
    jadwal = relationship("Jadwal", back_populates="guru_mapel")
    laporan = relationship("LaporanGuruMapel", back_populates="guru_mapel")
    laporan_BK = relationship("LaporanPetugasBK", back_populates="guru_mapel")

    __table_args__ = (UniqueConstraint('nip', 'id_sekolah', 'id_tahun', name='_nip_sekolah_tahun_guru_mapel_uc'),)
    
    def __repr__(self):
        return f"<GuruMapel(id={self.id}, nip='{self.nip}', nama='{self.nama}')>"


class AlamatGuruMapel(Base):
    __tablename__ = 'alamat_guru_mapel'

    id_guru_mapel = Column(Integer, ForeignKey('guru_mapel.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    detail_tempat = Column(String(255), nullable=False)
    desa = Column(String(255), nullable=False)
    kecamatan = Column(String(255), nullable=False)
    kabupaten = Column(String(255), nullable=False)
    provinsi = Column(String(255), nullable=False)
    negara = Column(String(255), nullable=False)

    guru_mapel = relationship("GuruMapel", back_populates="alamat")

    def __repr__(self):
        return f"<AlamatGuruMapel(id={self.id_guru_mapel})>"
