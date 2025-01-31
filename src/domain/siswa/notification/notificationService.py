from copy import deepcopy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select,and_,not_
from sqlalchemy.orm import subqueryload
from ....db.db import SessionLocal

# models
from ....models.notification_model import Notification,NotificationRead
from ....models.petugas_BK_model import PetugasBK, DistribusiPetugasBK
from ....models.guru_walas_model import GuruWalas
from ....models.guru_mapel_model import GuruMapel
# schemas
from ...schemas.notification_schema import NotificationModelBase,ResponseGetUnreadNotification
# service
from ...notification_method.notificationService import addNotification
# common
from ....error.errorHandling import HttpException
from collections import defaultdict
from ....utils.generateId_util import generate_id
from datetime import date
import asyncio

async def getAllNotification(id_siswa : int,session : AsyncSession) -> dict[date,list[NotificationModelBase]] :
    findNotification = (await session.execute(select(Notification).options(subqueryload(Notification.reads.and_(NotificationRead.id_siswa == id_siswa))).where(Notification.id_siswa == id_siswa).order_by(desc(Notification.created_at)))).scalars().all()

    grouped_notifications = defaultdict(list)
    for notification in findNotification:
        grouped_notifications[notification.created_at.date()].append(notification)

    return {
        "msg" : "success",
        "data" : grouped_notifications
    }

async def getNotificationById(id_notification : int,id_siswa : int,session : AsyncSession) -> NotificationModelBase:
    findNotification = (await session.execute(select(Notification).options(subqueryload(Notification.reads.and_(NotificationRead.id_siswa == id_siswa))).where(and_(Notification.id == id_notification,Notification.id_siswa == id_siswa)))).scalar_one_or_none()

    if not findNotification :
        raise HttpException(400,"notification tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findNotification
    }

async def readNotification(id_notification : int,id_siswa : int,session : AsyncSession) -> NotificationModelBase:
    findNotification = (await session.execute(select(Notification).options(subqueryload(Notification.reads.and_(NotificationRead.id_siswa == id_siswa))).where(and_(Notification.id == id_notification,Notification.id_siswa == id_siswa)))).scalar_one_or_none()

    if not findNotification :
        raise HttpException(400,"notification tidak ditemukan")
    
    if len(findNotification.reads) > 0 :
        raise HttpException(400,"notification sudah dibaca")
    
    notificationMapping = {
        "id" : generate_id(),
        "notification_id" : id_notification,
        "id_siswa" : id_siswa,
        "is_read" : True
    }

    notifDictCopy = deepcopy(findNotification.__dict__)
    session.add(NotificationRead(**notificationMapping))
    await session.commit()

    return {
        "msg" : "success",
        "data" : {
            **notifDictCopy,
            "reads" : [notificationMapping]
        }
    }

async def getCountNotification(id_siswa : int,session : AsyncSession) -> ResponseGetUnreadNotification:
    findNotification = (await session.execute(select(Notification).where(and_(Notification.id_siswa == id_siswa,not_(Notification.reads.any(NotificationRead.id_siswa == id_siswa)))))).scalars().all()

    return {
        "msg" : "success",
        "data" : {
            "count" : len(findNotification)
        }
    }

async def sendNotificationToBkWalasMapel(siswa : dict,id_guru_mapel : int,statusAbsen : str) :
    try :
        session : AsyncSession = SessionLocal()
        findPetugasBk = (await session.execute(select(DistribusiPetugasBK).where(DistribusiPetugasBK.id_kelas == siswa["id_kelas"]))).scalars().all()

        if len(findPetugasBk) > 0 :
            for petugasBk in findPetugasBk :
                notifMapping = {
                    "id" : generate_id(),
                    "id_petugas_BK" : petugasBk.id_petugas_BK,
                    "title" : f"Siswa {siswa['nama']} melakukan absen {statusAbsen}",
                    "body" : f"Siswa {siswa['nama']} telah melakukan absen {statusAbsen} hari ini, Silahkan melakukan tinjaun absen"
                }
                await addNotification(notifMapping)

        findGuruWalas = (await session.execute(select(GuruWalas).where(GuruWalas.id_kelas == siswa["id_kelas"]))).scalar_one_or_none()

        if findGuruWalas :
            notifMapping = {
                "id" : generate_id(),
                "id_guru_walas" : findGuruWalas.id,
                "title" : f"Siswa {siswa['nama']} melakukan absen {statusAbsen}",
                "body" : f"Siswa {siswa['nama']} telah melakukan absen {statusAbsen} hari ini"
            }
            await addNotification(notifMapping)

        notifMapping = {
            "id" : generate_id(),
            "id_guru_mapel" : id_guru_mapel,
            "title" : f"Siswa {siswa['nama']} melakukan absen {statusAbsen}",
            "body" : f"Siswa {siswa['nama']} telah melakukan absen {statusAbsen} hari ini"
        }
        await addNotification(notifMapping)
    finally :
        await session.close()

def sendNotificationToBkWalasMapelSync(siswa : dict,id_guru_mapel : int,statusAbsen : str) :
    asyncio.run(sendNotificationToBkWalasMapel(siswa,id_guru_mapel,statusAbsen))