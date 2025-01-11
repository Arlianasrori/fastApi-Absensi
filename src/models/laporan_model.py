from sqlalchemy import Column, Integer, String,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from ..db.db import Base

# siswa
class LaporanSiswa(Base):
    __tablename__ = 'laporan_siswa'

    id = Column(Integer, primary_key=True)
    id_siswa = Column(Integer, ForeignKey('siswa.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    catatan = Column(String(1250), nullable=False)
    datetime = Column(DateTime, nullable=False)

    siswa = relationship("Siswa", back_populates="laporan")
    file = relationship("FileLaporanSiswa", back_populates="laporan",cascade="all")

    def __repr__(self):
        return f"<LaporanSiswa(id={self.id}, siswa='{self.siswa}')>"
    
class FileLaporanSiswa(Base):
    __tablename__ = 'file_laporan_siswa'

    id = Column(Integer, primary_key=True)
    id_laporan = Column(Integer, ForeignKey('laporan_siswa.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    file = Column(String, nullable=False)

    laporan = relationship("LaporanSiswa", back_populates="file")

    def __repr__(self):
        return f"<FileLaporanSiswa(id={self.id}')>"
    
# guru walas
class LaporanGuruWalas(Base):
    __tablename__ = 'laporan_guru_walas'

    id = Column(Integer, primary_key=True)
    id_guru_walas = Column(Integer, ForeignKey('guru_walas.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    catatan = Column(String(1250), nullable=False)
    datetime = Column(DateTime, nullable=False)

    guru_walas = relationship("GuruWalas", back_populates="laporan")
    file = relationship("FileLaporanGuruWalas", back_populates="laporan")

    def __repr__(self):
        return f"<LaporanGuruWalas(id={self.id}, guru_walas='{self.guru_walas}')>"
    
class FileLaporanGuruWalas(Base):
    __tablename__ = 'file_laporan_guru_walas'

    id = Column(Integer, primary_key=True)
    id_laporan = Column(Integer, ForeignKey('laporan_guru_walas.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    file = Column(String, nullable=False)

    laporan = relationship("LaporanGuruWalas", back_populates="file")

    def __repr__(self):
        return f"<FileLaporanGuruWalas(id={self.id}, laporan='{self.laporan}')>"
    
# guru mapel
class LaporanGuruMapel(Base):
    __tablename__ = 'laporan_guru_mapel'

    id = Column(Integer, primary_key=True)
    id_guru_mapel = Column(Integer, ForeignKey('guru_mapel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    catatan = Column(String(1250), nullable=False)
    datetime = Column(DateTime, nullable=False)

    guru_mapel = relationship("GuruMapel", back_populates="laporan")
    file = relationship("FileLaporanGuruMapel", back_populates="laporan")

    def __repr__(self):
        return f"<LaporanGuruMapel(id={self.id}, guru_mapel='{self.guru_mapel}')>"
    
class FileLaporanGuruMapel(Base):
    __tablename__ = 'file_laporan_guru_mapel'

    id = Column(Integer, primary_key=True)
    id_laporan = Column(Integer, ForeignKey('laporan_guru_mapel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    file = Column(String, nullable=False)

    laporan = relationship("LaporanGuruMapel", back_populates="file")

    def __repr__(self):
        return f"<FileLaporanGuruMapel(id={self.id}, laporan='{self.laporan}')>"
    
# petugas BK
class LaporanPetugasBK(Base):
    __tablename__ = 'laporan_petugas_BK'

    id = Column(Integer, primary_key=True)
    id_petugas_BK = Column(Integer, ForeignKey('petugas_BK.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_guru_walas = Column(Integer, ForeignKey('guru_walas.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    id_guru_mapel = Column(Integer, ForeignKey('guru_mapel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    catatan = Column(String(1250), nullable=False)
    datetime = Column(DateTime, nullable=False)

    petugas_BK = relationship("PetugasBK", back_populates="laporan")
    guru_walas = relationship("GuruWalas", back_populates="laporan_BK")
    guru_mapel = relationship("GuruMapel", back_populates="laporan_BK")
    file = relationship("FileLaporanPetugasBK", back_populates="laporan")

    def __repr__(self):
        return f"<LaporanPetugasBK(id={self.id}, petugas_BK='{self.petugas_BK}')>"
    
class FileLaporanPetugasBK(Base):
    __tablename__ = 'file_laporan_petugas_BK'

    id = Column(Integer, primary_key=True)
    id_laporan = Column(Integer, ForeignKey('laporan_petugas_BK.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    file = Column(String, nullable=False)

    laporan = relationship("LaporanPetugasBK", back_populates="file")

    def __repr__(self):
        return f"<FileLaporanPetugasBK(id={self.id}, laporan='{self.laporan}')>"
