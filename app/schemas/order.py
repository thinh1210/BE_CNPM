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
    data: OrderRoomOut|Room|OrderRoom|CancelRoom|UsedRoom|List[Room]|List[OrderRoom]|List[CancelRoom]|List[UsedRoom]|List[OrderRoomOut]|None = None