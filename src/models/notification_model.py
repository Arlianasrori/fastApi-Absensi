from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from ..db.db import Base
from datetime import datetime


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True)
    id_siswa = Column(Integer, ForeignKey('siswa.id'), nullable=False)
    id_guru_walas = Column(Integer, ForeignKey('guru_walas.id'), nullable=False)
    id_guru_mapel = Column(Integer, ForeignKey('guru_mapel.id'), nullable=False)
    id_petugas_BK = Column(Integer, ForeignKey('petugas_BK.id'), nullable=False)
    title = Column(String(255))
    body = Column(String(1500))
    created_at = Column(DateTime, default=datetime.now())

    siswa = relationship("Siswa", back_populates="notifications")
    guru_walas = relationship("GuruWalas", back_populates="notifications")
    guru_mapel = relationship("GuruMapel", back_populates="notifications")
    petugas_BK = relationship("PetugasBK", back_populates="notifications")
    reads = relationship("NotificationRead", back_populates="notification")

class NotificationRead(Base):
    __tablename__ = 'notification_read'

    id = Column(Integer, primary_key=True)
    id_siswa = Column(Integer, ForeignKey('siswa.id'), nullable=False)
    id_guru_walas = Column(Integer, ForeignKey('guru_walas.id'), nullable=False)
    id_guru_mapel = Column(Integer, ForeignKey('guru_mapel.id'), nullable=False)
    id_petugas_BK = Column(Integer, ForeignKey('petugas_BK.id'), nullable=False)
    notification_id = Column(Integer, ForeignKey('notification.id'))
    is_read = Column(Boolean, default=True)

    notification = relationship("Notification", back_populates="reads")
    siswa = relationship("Siswa", back_populates="notification_reads")
    guru_walas = relationship("GuruWalas", back_populates="notification_reads")
    guru_mapel = relationship("GuruMapel", back_populates="notification_reads")
    petugas_BK = relationship("PetugasBK", back_populates="notification_reads")