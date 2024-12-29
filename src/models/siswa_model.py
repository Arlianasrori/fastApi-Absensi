from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean,UniqueConstraint

from sqlalchemy.orm import relationship
from ..db.db import Base
from ..types.user_types import GenderType

class Siswa(Base):
    __tablename__ = 'siswa'

    id = Column(Integer, primary_key=True)
    nis = Column(String, nullable=False)
    nama = Column(String(255), nullable=False)
    jenis_kelamin = Column(Enum(GenderType), nullable=False)
    no_telepon = Column(String(12), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    token_FCM = Column(String, nullable=True)
    foto_profile = Column(String, nullable=True)
    id_jurusan = Column(Integer, ForeignKey('jurusan.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_kelas = Column(Integer, ForeignKey('kelas.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_sekolah = Column(Integer, ForeignKey('sekolah.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_tahun = Column(Integer, ForeignKey('tahun_sekolah.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    OTP_code = Column(Integer, nullable=True)

    # Relasi yang sudah ada
    jurusan = relationship("Jurusan", back_populates="siswa")
    kelas = relationship("Kelas", back_populates="siswa")
    alamat = relationship("AlamatSiswa", uselist=False, back_populates="siswa", cascade="all")
    notifications = relationship("Notification", back_populates="siswa")
    notification_reads = relationship("NotificationRead", back_populates="siswa")
    absen = relationship("Absen", back_populates="siswa")
    sekolah = relationship("Sekolah", back_populates="siswa")
    tahun = relationship("TahunSekolah", back_populates="siswa")
    laporan = relationship("LaporanSiswa", back_populates="siswa")

    __table_args__ = (UniqueConstraint('nis', 'id_sekolah', 'id_tahun', name='_nis_sekolah_tahun_siswa_uc'),)
    
    def __repr__(self):
        return f"<Siswa(id={self.id}, nis='{self.nis}', nama='{self.nama}')>"

# Model-model terkait lainnya (contoh singkat)
class Jurusan(Base):
    __tablename__ = 'jurusan'
    id = Column(Integer, primary_key=True)
    nama = Column(String(255), nullable=False)
    id_sekolah = Column(Integer, ForeignKey('sekolah.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_tahun = Column(Integer, ForeignKey('tahun_sekolah.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    siswa = relationship("Siswa", back_populates="jurusan")
    kelas = relationship("Kelas", back_populates="jurusan")
    sekolah = relationship("Sekolah", back_populates="jurusan")
    tahun = relationship("TahunSekolah", back_populates="jurusan")

    def __repr__(self):
        return f"<Jurusan(id={self.id}, nama='{self.nama}')>"

class Kelas(Base):
    __tablename__ = 'kelas'
    id = Column(Integer, primary_key=True)
    nama = Column(String(255), nullable=False)
    id_jurusan = Column(Integer, ForeignKey('jurusan.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    siswa = relationship("Siswa", back_populates="kelas")
    jurusan = relationship("Jurusan",uselist=False, back_populates="kelas")
    guru_walas = relationship("GuruWalas", back_populates="kelas")
    distribusi_petugas_BK = relationship("DistribusiPetugasBK", back_populates="kelas")
    jadwal = relationship("Jadwal", back_populates="kelas")
    koordinat_absen = relationship("KoordinatAbsenKelas",back_populates="kelas")

    def __repr__(self):
        return f"<Kelas(id={self.id}, nama='{self.nama}')>"

class AlamatSiswa(Base):
    __tablename__ = 'alamat_siswa'
    id_siswa = Column(Integer, ForeignKey('siswa.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    detail_tempat = Column(String(255), nullable=False)
    desa = Column(String(255), nullable=False)
    kecamatan = Column(String(255), nullable=False)
    kabupaten = Column(String(255), nullable=False)
    provinsi = Column(String(255), nullable=False)
    negara = Column(String(255), nullable=False)

    siswa = relationship("Siswa", back_populates="alamat")

    def __repr__(self):
        return f"<AlamatSiswa(id_siswa={self.id_siswa}, desa='{self.desa}', kecamatan='{self.kecamatan}')>"