from copy import deepcopy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select,and_,not_
from sqlalchemy.orm import subqueryload
from ....db.db import SessionLocal

# models
from ....models.notification_model import Notification,NotificationRead
from ....models.guru_walas_model import GuruWalas
# schemas
from ...schemas.notification_schema import NotificationModelBase,ResponseGetUnreadNotification
# services
from ...siswa.notification.notificationService import addNotification

# common
from ....error.errorHandling import HttpException
from collections import defaultdict
from ....utils.generateId_util import generate_id
from datetime import date
import asyncio

async def getAllNotification(id_petugas_BK : int,session : AsyncSession) -> dict[date,list[NotificationModelBase]] :
    findNotification = (await session.execute(select(Notification).options(subqueryload(Notification.reads.and_(NotificationRead.id_petugas_BK == id_petugas_BK))).where(Notification.id_petugas_BK == id_petugas_BK).order_by(desc(Notification.created_at)))).scalars().all()

    grouped_notifications = defaultdict(list)
    for notification in findNotification:
        grouped_notifications[notification.created_at.date()].append(notification)

    return {
        "msg" : "success",
        "data" : grouped_notifications
    }

async def getNotificationById(id_notification : int,id_petugas_BK : int,session : AsyncSession) -> NotificationModelBase:
    findNotification = (await session.execute(select(Notification).options(subqueryload(Notification.reads.and_(NotificationRead.id_petugas_BK == id_petugas_BK))).where(and_(Notification.id == id_notification,Notification.id_petugas_BK == id_petugas_BK)))).scalar_one_or_none()

    if not findNotification :
        raise HttpException(400,"notification tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findNotification
    }

async def readNotification(id_notification : int,id_petugas_BK : int,session : AsyncSession) -> NotificationModelBase:
    findNotification = (await session.execute(select(Notification).options(subqueryload(Notification.reads.and_(NotificationRead.id_petugas_BK == id_petugas_BK))).where(and_(Notification.id == id_notification,Notification.id_petugas_BK == id_petugas_BK)))).scalar_one_or_none()

    if not findNotification :
        raise HttpException(400,"notification tidak ditemukan")
    
    if len(findNotification.reads) > 0 :
        raise HttpException(400,"notification sudah dibaca")
    
    notificationMapping = {
        "id" : generate_id(),
        "notification_id" : id_notification,
        "id_petugas_BK" : id_petugas_BK,
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

async def getCountNotification(id_petugas_BK : int,session : AsyncSession) -> ResponseGetUnreadNotification:
    findNotification = (await session.execute(select(Notification).where(and_(Notification.id_petugas_BK == id_petugas_BK,not_(Notification.reads.any(NotificationRead.id_petugas_BK == id_petugas_BK)))))).scalars().all()

    return {
        "msg" : "success",
        "data" : {
            "count" : len(findNotification)
        }
    }


async def sendNotificationToSiswaWalasMapel(id_petugasBk : int,siswa : dict,id_guru_mapel : int,statusAbsen : str,statusTinjauan : str) :
    try :
        session : AsyncSession = SessionLocal()
        # send for bk
        notifMapping = {
            "id" : generate_id(),
            "id_petugas_BK" : id_petugasBk,
            "title" : f"Absen {statusAbsen} di{statusTinjauan}",
            "body" : f"Absen {statusAbsen} yang telah dilakukan oleh siswa {siswa['nama']} berhasil di{statusTinjauan}"
        }
        await addNotification(notifMapping)

        # send for siswa
        notifMapping = {
            "id" : generate_id(),
            "id_siswa" : siswa["id"],
            "title" : f"Absen {statusAbsen} di{statusTinjauan}",
            "body" : f"Absen {statusAbsen} yang telah kamu lakukan telah di{statusTinjauan} oleh petugas Bk"
        }
        await addNotification(notifMapping)

        # send for guru walas
        findGuruWalas = (await session.execute(select(GuruWalas).where(GuruWalas.id_kelas == siswa["id_kelas"]))).scalar_one_or_none()

        if findGuruWalas :
            notifMapping = {
                "id" : generate_id(),
                "id_guru_walas" : findGuruWalas.id,
                "title" : f"Absen {statusAbsen} {siswa['nama']} di{statusTinjauan}",
                "body" : f"Absen {statusAbsen} yang telah dilakukan oleh siswa {siswa['nama']} telah di{statusTinjauan} oleh petugas Bk"
            }
            await addNotification(notifMapping)

        # send for guru mapel
        notifMapping = {
            "id" : generate_id(),
            "id_guru_mapel" : id_guru_mapel,
            "title" : f"Absen {statusAbsen} {siswa['nama']} di{statusTinjauan}",
            "body" : f"Absen {statusAbsen} yang telah dilakukan oleh siswa {siswa['nama']} telah di{statusTinjauan} oleh petugas Bk"
        }
        await addNotification(notifMapping)
    finally :
        await session.close()

def sendNotificationToSiswaWalasMapelSync(id_petugasBk : int,siswa : dict,id_guru_mapel : int,statusAbsen : str,statusTinjauan : str) :
    asyncio.run(sendNotificationToSiswaWalasMapel(id_petugasBk,siswa,id_guru_mapel,statusAbsen,statusTinjauan))