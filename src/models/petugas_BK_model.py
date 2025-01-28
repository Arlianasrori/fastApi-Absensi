from sqlalchemy import Column, Integer, String, ForeignKey, Enum, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from ..db.db import Base
from ..types.user_types import GenderType

class PetugasBK(Base):
    __tablename__ = 'petugas_BK'

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
    OTP_code = Column(Integer, nullable=True)

    # Relasi yang sudah ada
    alamat = relationship("AlamatPetugasBK", uselist=False, back_populates="petugas_BK", cascade="all")
    notifications = relationship("Notification", back_populates="petugas_BK")
    notification_reads = relationship("NotificationRead", back_populates="petugas_BK")
    sekolah = relationship("Sekolah", back_populates="petugas_BK")
    tahun = relationship("TahunSekolah", back_populates="petugas_BK")
    distribusi_petugas_BK = relationship("DistribusiPetugasBK", back_populates="petugas_BK",cascade="all")
    laporan = relationship("LaporanPetugasBK", back_populates="petugas_BK")
    absen_detail = relationship("AbsenDetail", back_populates="petugas_bk")

    __table_args__ = (UniqueConstraint('nip', 'id_sekolah', 'id_tahun', name='_nip_sekolah_tahun_petugas_BK_uc'),)
    
    def __repr__(self):
        return f"<PetugasBK(id={self.id}, nip='{self.nip}', nama='{self.nama}')>"

class DistribusiPetugasBK(Base):
    __tablename__ = 'distribusi_petugas_BK'

    id = Column(Integer, primary_key=True)
    id_petugas_BK = Column(Integer, ForeignKey('petugas_BK.id', ondelete='CASCADE', onupdate='CASCADE'),nullable=False)
    id_kelas = Column(Integer, ForeignKey('kelas.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    petugas_BK = relationship("PetugasBK",uselist=False, back_populates="distribusi_petugas_BK",cascade="all")
    kelas = relationship("Kelas",uselist=False, back_populates="distribusi_petugas_BK")

    __table_args__ = (UniqueConstraint('id_petugas_BK', 'id_kelas', name='_petugas_BK_kelas_tahun_sekolah_uc'),)  

    def __repr__(self):
        return f"<DistribusiPetugasBK(id={self.id_petugas_BK})>"

class AlamatPetugasBK(Base):
    __tablename__ = 'alamat_petugas_BK'

    id_petugas_BK = Column(Integer, ForeignKey('petugas_BK.id'), primary_key=True)
    detail_tempat = Column(String(255), nullable=False)
    desa = Column(String(255), nullable=False)
    kecamatan = Column(String(255), nullable=False)
    kabupaten = Column(String(255), nullable=False)
    provinsi = Column(String(255), nullable=False)
    negara = Column(String(255), nullable=False)

    petugas_BK = relationship("PetugasBK", back_populates="alamat")

    def __repr__(self):
        return f"<AlamatPetugasBK(id={self.id_petugas_BK})>"
