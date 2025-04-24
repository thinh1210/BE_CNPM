from fastapi import HTTPException
from sqlmodel import SQLModel, Session, select
from typing import List
from datetime import datetime
from app.model import Notification, Report, User, UsedRoom, Room

# ------------------- Notification CRUD -------------------
async def create_notification(
    db: Session,
    user_id: int,
    order_id: int,
    title: str,
    message: str,
    is_read: bool = False
) -> Notification:
    '''
    Create a new notification.
    need to check order_id before create notification

    Args:
    - db: Database session
    - user_id: ID of the user to whom the notification is sent
    - order_id: ID of the order related to the notification
    - title: Title of the notification
    - message: Message content of the notification
    
    returns Notification object

    '''
    # Verify user exists
    
    # Create new notification
    db_notification = Notification(
        user_id=user_id,
        order_id=order_id,
        title=title,
        message=message,
        is_read=is_read,
        date=datetime.now()
    )
    
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification

async def get_notification(db: Session, notification_id: int) -> Notification:
    notification = await db.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

async def get_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
    statement = select(Notification).where(Notification.user_id == user_id).offset(skip).limit(limit)
    results = await db.exec(statement)
    notifications = results.all()
    return notifications

async def update_notification(
    db: Session,
    notification_id: int,
    title: str | None = None,
    message: str | None = None,
    is_read: bool | None = None
) -> Notification:
    db_notification = await db.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if title is not None:
        db_notification.title = title
    if message is not None:
        db_notification.message = message
    if is_read is not None:
        db_notification.is_read = is_read
    
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification

async def delete_notification(db: Session, notification_id: int) -> dict:
    db_notification = await db.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    await db.delete(db_notification)
    await db.commit()
    return {"message": "Notification deleted successfully"}

# ------------------- Report CRUD -------------------
async def create_report(
    db: Session,
    used_room_id: int,
    user_id: int,
    room_id: int,
    led: bool = False,
    air_conditioner: bool = False,
    socket: bool = False,
    projector: bool = False,
    interactive_display: bool = False,
    online_meeting_devices: bool = False,
    description: str | None = None
) -> Report:
    # Verify foreign keys exist
    used_room = await db.get(UsedRoom, used_room_id)
    if not used_room:
        raise HTTPException(status_code=404, detail="UsedRoom not found")
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    room = await db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Create new report
    db_report = Report(
        used_room_id=used_room_id,
        user_id=user_id,
        room_id=room_id,
        led=led,
        air_conditioner=air_conditioner,
        socket=socket,
        projector=projector,
        interactive_display=interactive_display,
        online_meeting_devices=online_meeting_devices,
        description=description
    )
    
    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)
    return db_report


async def get_report(db: Session, report_id: int) -> Report:
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


async def get_reports(
    db: Session,
    user_id: int | None = None,
    room_id: int | None = None,
    skip: int = 0,
    limit: int = 100
) -> List[Report]:
    statement = select(Report)
    if user_id:
        statement = statement.where(Report.user_id == user_id)
    if room_id:
        statement = statement.where(Report.room_id == room_id)
    
    statement = statement.offset(skip).limit(limit)
    results = await db.exec(statement)
    reports = results.all()
    return reports


async def update_report(
    db: Session,
    report_id: int,
    led: bool | None = None,
    air_conditioner: bool | None = None,
    socket: bool | None = None,
    projector: bool | None = None,
    interactive_display: bool | None = None,
    online_meeting_devices: bool | None = None,
    description: str | None = None
) -> Report:
    db_report = await db.get(Report, report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if led is not None:
        db_report.led = led
    if air_conditioner is not None:
        db_report.air_conditioner = air_conditioner
    if socket is not None:
        db_report.socket = socket
    if projector is not None:
        db_report.projector = projector
    if interactive_display is not None:
        db_report.interactive_display = interactive_display
    if online_meeting_devices is not None:
        db_report.online_meeting_devices = online_meeting_devices
    if description is not None:
        db_report.description = description
    
    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)
    return db_report

async def delete_report(db: Session, report_id: int) -> dict:
    db_report = await db.get(Report, report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    await db.delete(db_report)
    await db.commit()
    return {"message": "Report deleted successfully"}