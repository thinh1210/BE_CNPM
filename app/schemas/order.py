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

class CheckIn(BaseModel):
    order_id: int

class CheckOut(BaseModel):
    order_id: int


class responseorder(BaseModel):
    message: str
    data: Room|OrderRoom|CancelRoom|UsedRoom|List[Room]|List[OrderRoom]|List[CancelRoom]|List[UsedRoom]|None = None