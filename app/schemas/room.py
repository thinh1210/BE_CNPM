from pydantic import BaseModel
from typing import Optional, List
from app.model import Room, Branch, Building, RoomType
class Branch_In(BaseModel):
    Branch_name: str

class Buiding_In(BaseModel):
    name_building: str
    id_branch: None|int
    branch_name: None|str

class TypeRoom_In(BaseModel):
    name_type_room: str

class RoomIn(BaseModel):
    id: int
    name_room: str
    id_branch: int|None
    branch_name: str|None
    id_building: int|None
    building_name: str|None
    id_type_room: int|None
    type_room_name: str|None
    max_quantity: None|int = 0
    quantity: None|int= 0
    active: bool = True


class RoomDevice(BaseModel):
    room_id: int
    led: bool = False
    projector: bool = False
    air_conditioner: bool = False
    socket: int = 0
    interactive_display: bool = False
    online_meeting_devices: bool = False
    
class Room_with_device_In(RoomIn):
    room_id: int
    led: bool = False
    projector: bool = False
    air_conditioner: bool = False
    socket: int = 0
    interactive_display: bool = False
    online_meeting_devices: bool = False

class reponse(BaseModel):
    msg: str
    data: Room|Branch|Building|RoomType|None|List[Room]|List[Branch]|List[Building]|List[RoomType]