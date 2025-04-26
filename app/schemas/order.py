from pydantic import BaseModel
from typing import Optional, List
from app.model import Room,OrderRoom, CancelRoom, User, Room, Branch, Building, RoomType, UsedRoom, Report
from datetime import datetime, date, time



class OrderIn(BaseModel):
    room_id: int
    date: int
    month: int
    year: int
    start_time: int
    end_time: int

class CancelIn(BaseModel):
    order_id: int

class CheckIn1(BaseModel):
    room_id: int

class CheckOut1(BaseModel):
    room_id: int

class CheckIn2(BaseModel):
    order_id: int
class CheckOut2(BaseModel):
    order_id: int

class Report(BaseModel):
    room_id: int
    led: bool = True,
    air_conditioner: bool = True,
    socket: bool =True,
    projector: bool = True,
    interactive_display: bool = True,
    online_meeting_devices: bool = True,
    description: str | None = "Short description of the problem"


class changetime(BaseModel):
    order_id: int
    date: int
    month: int
    year: int
    start_time: int
    end_time: int

class OrderRoomOut(BaseModel):
    order: OrderRoom
    cancel: CancelRoom|None
    used: UsedRoom|None


class responseorder(BaseModel):
    msg: str
    data: User|Report|OrderRoomOut|Room|OrderRoom|CancelRoom|UsedRoom|List[Report]|List[Room]|List[OrderRoom]|List[CancelRoom]|List[UsedRoom]|List[OrderRoomOut]|None = None