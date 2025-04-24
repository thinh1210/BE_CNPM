from pydantic import BaseModel
from typing import Optional, List
from app.model import Room, Branch, Building, RoomType
from app.schemas.metadata import Metadata
class Branch_In(BaseModel):
    Branch_name: str

class Buiding_In(BaseModel):
    name_building: str
    id_branch: int

class TypeRoom_In(BaseModel):
    name_type_room: str

class RoomIn(BaseModel):
    name_room: str
    id_branch: int
    id_building: int
    id_type_room: int
    max_quantity: None|int = 0
    quantity: None|int= 0
    active: bool = True


class RoomDevice(BaseModel):
    room_id: int
    led: bool = True
    projector: bool = False
    air_conditioner: bool = False
    socket: int = 0
    interactive_display: bool = False
    online_meeting_devices: bool = False
    
class Room_with_device_In(RoomIn):
    led: bool = True
    projector: bool = False
    air_conditioner: bool = False
    socket: int = 0
    interactive_display: bool = False
    online_meeting_devices: bool = False

class reponse(BaseModel):
    msg: str
    data: Room|Branch|Building|RoomType|None|List[Room]|List[Branch]|List[Building]|List[RoomType]
    metadata: Metadata|None = None
    