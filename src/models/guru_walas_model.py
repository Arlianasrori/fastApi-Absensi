from sqlalchemy import Column, Integer, String, ForeignKey, Enum, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from ..db.db import Base
from ..types.user_types import GenderType

class GuruWalas(Base):
    __tablename__ = 'guru_walas'

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
    id_kelas = Column(Integer, ForeignKey('kelas.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    OTP_code = Column(Integer, nullable=True)

    # Relasi yang sudah ada
    alamat = relationship("AlamatGuruWalas", uselist=False, back_populates="guru_walas", cascade="all")
    notifications = relationship("Notification", back_populates="guru_walas")
    notification_reads = relationship("NotificationRead", back_populates="guru_walas")
    sekolah = relationship("Sekolah", back_populates="guru_walas")
    tahun = relationship("TahunSekolah", back_populates="guru_walas")
    kelas = relationship("Kelas", back_populates="guru_walas")

    __table_args__ = (UniqueConstraint('nip', 'id_sekolah', 'id_tahun', name='_nip_sekolah_tahun_guru_walas_uc'),)
    
    def __repr__(self):
        return f"<GuruWalas(id={self.id}, nip='{self.nip}', nama='{self.nama}')>"


class AlamatGuruWalas(Base):
    __tablename__ = 'alamat_guru_walas'

    id_guru_walas = Column(Integer, ForeignKey('guru_walas.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    detail_tempat = Column(String(255), nullable=False)
    desa = Column(String(255), nullable=False)
    kecamatan = Column(String(255), nullable=False)
    kabupaten = Column(String(255), nullable=False)
    provinsi = Column(String(255), nullable=False)
    negara = Column(String(255), nullable=False)

    guru_walas = relationship("GuruWalas", back_populates="alamat")

    def __repr__(self):
        return f"<AlamatGuruWalas(id={self.id_guru_walas})>"