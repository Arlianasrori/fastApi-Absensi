from copy import deepcopy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select,and_,not_
from sqlalchemy.orm import subqueryload

# models
from ....models.notification_model import Notification,NotificationRead
# schemas
from ...schemas.notification_schema import NotificationModelBase,ResponseGetUnreadNotification

# common
from ....error.errorHandling import HttpException
from collections import defaultdict
from ....utils.generateId_util import generate_id
from datetime import date

async def getAllNotification(id_guru_walas : int,session : AsyncSession) -> dict[date,list[NotificationModelBase]] :
    findNotification = (await session.execute(select(Notification).options(subqueryload(Notification.reads.and_(NotificationRead.id_guru_walas == id_guru_walas))).where(Notification.id_guru_walas == id_guru_walas).order_by(desc(Notification.created_at)))).scalars().all()

    grouped_notifications = defaultdict(list)
    for notification in findNotification:
        grouped_notifications[notification.created_at.date()].append(notification)

    return {
        "msg" : "success",
        "data" : grouped_notifications
    }

async def getNotificationById(id_notification : int,id_guru_walas : int,session : AsyncSession) -> NotificationModelBase:
    findNotification = (await session.execute(select(Notification).options(subqueryload(Notification.reads.and_(NotificationRead.id_guru_walas == id_guru_walas))).where(and_(Notification.id == id_notification,Notification.id_guru_walas == id_guru_walas)))).scalar_one_or_none()

    if not findNotification :
        raise HttpException(400,"notification tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findNotification
    }

async def readNotification(id_notification : int,id_guru_walas : int,session : AsyncSession) -> NotificationModelBase:
    findNotification = (await session.execute(select(Notification).options(subqueryload(Notification.reads.and_(NotificationRead.id_guru_walas == id_guru_walas))).where(and_(Notification.id == id_notification,Notification.id_guru_walas == id_guru_walas)))).scalar_one_or_none()

    if not findNotification :
        raise HttpException(400,"notification tidak ditemukan")
    
    if len(findNotification.reads) > 0 :
        raise HttpException(400,"notification sudah dibaca")
    
    notificationMapping = {
        "id" : generate_id(),
        "notification_id" : id_notification,
        "id_guru_walas" : id_guru_walas,
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

async def getCountNotification(id_guru_walas : int,session : AsyncSession) -> ResponseGetUnreadNotification:
    findNotification = (await session.execute(select(Notification).where(and_(Notification.id_guru_walas == id_guru_walas,not_(Notification.reads.any(NotificationRead.id_guru_walas == id_guru_walas)))))).scalars().all()

    return {
        "msg" : "success",
        "data" : {
            "count" : len(findNotification)
        }
    }